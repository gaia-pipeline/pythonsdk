import sys
import time
import os
import grpc
import plugin_pb2
import plugin_pb2_grpc

from grpc_health.v1.health import HealthServicer
from grpc_health.v1 import health_pb2, health_pb2_grpc
from concurrent import futures

from fnvhash import fnv1a_32
from job import Job, Argument, ManualInteraction, GetJob, JobWrapper, InputType

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

cachedJobs = []

class ExitPipeline(Exception):
    pass

class GRPCServer(plugin_pb2_grpc.PluginServicer):
    """Implementation of Plugin service."""

    def GetJobs(self, request, context):
        for job in cachedJobs:
            yield job.job

    def ExecuteJob(self, request, context):
        job = GetJob(request.unique_id, cachedJobs)
        if job == None:
            return "job not found"
        
        # transform args
        args = []
        if hasattr(request, "args"):
            for arg in request.args:
                a = Argument("", InputType.TextFieldInp, arg.key, arg.value)
                args.append(a)

        # Execute job
        result = plugin_pb2.JobResult()
        try:
            job.handler(args)
        except ExitPipeline, e:
            result.exit_pipeline = True
            result.unique_id = job.job.unique_id
            result.message = str(e)
        except Exception, e:
            result.exit_pipeline = True
            result.failed = True
            result.unique_id = job.job.unique_id
            result.message = str(e)

        return result

def serve(jobs):
    # Cache the jobs list for later processing.
	# We first have to translate given jobs to different structure.
    for job in jobs:
        # Create proto object
        p = plugin_pb2.Job()

        # Manual interaction
        if job.interaction != None:
            p.interaction.description = job.interaction.description
            p.interaction.type = job.interaction.inputType
            p.interaction.value = job.interaction.value
        
        # Arguments
        args = []
        if job.args:
            for arg in job.args:
                a = plugin_pb2.Argument()
                a.description = arg.description
                a.type = arg.inputType.value
                a.key = arg.key
                a.value = arg.value

                args.append(a)

        # Set the rest of the fields
        p.unique_id = fnv1a_32(bytes(job.title))
        p.title = job.title
        p.description = job.description
        p.args.extend(args)

        # Resolve dependencies
        if job.dependsOn:
            for depJob in job.dependsOn:
                for currJob in jobs:
                    if depJob.lower() == currJob.title.lower():
                        p.dependson.append(fnv1a_32(bytes(currJob.title)))
                        foundDep = True
                        break
                    
                if not foundDep:
                    raise Exception("job '" + job.title + "' has dependency '" + depJob + "' which is not declared")
        
        # job wrapper object for this job
        w = JobWrapper(job.handler, p)
        cachedJobs.append(w)

    # Check if two jobs have the same title which is restricted
    for x, job in enumerate(cachedJobs):
        for y, innerJob in enumerate(cachedJobs):
            if x != y and job.job.unique_id == innerJob.job.unique_id:
                raise Exception("duplicate job found (two jobs with same title)")

    # get certificate path from environment variables
    certPath = os.environ['GAIA_PLUGIN_CERT']
    keyPath = os.environ['GAIA_PLUGIN_KEY']
    caCertPath = os.environ['GAIA_PLUGIN_CA_CERT']

    # check if all certs are available
    if not os.path.isfile(certPath):
        raise Exception("cannot find path to certificate")
    if not os.path.isfile(keyPath):
        raise Exception("cannot find path to key")
    if not os.path.isfile(caCertPath):
        raise Exception("cannot find path to root certificate")

    # Open files
    private_key = open(keyPath).read()
    certificate_chain = open(certPath).read()
    root_cert = open(caCertPath).read()

    # We need to build a health service to work with go-plugin
    health = HealthServicer()
    health.set("plugin", health_pb2.HealthCheckResponse.ServingStatus.Value('SERVING'))

    # Start the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    private_key_certificate_chain_pairs = ( (private_key, certificate_chain), )
    server_credentials = grpc.ssl_server_credentials(private_key_certificate_chain_pairs, root_cert, True)
    plugin_pb2_grpc.add_PluginServicer_to_server(GRPCServer(), server)
    health_pb2_grpc.add_HealthServicer_to_server(health, server)
    port = server.add_secure_port('localhost:0', server_credentials)
    server.start()

    # Output information
    print("1|2|tcp|localhost:" + str(port) + "|grpc")
    sys.stdout.flush()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
