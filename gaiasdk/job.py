from enum import Enum

class InputType(Enum):
    TextFieldInp = "textfield"
    TextAreaInp = "textarea"
    BoolInp = "boolean"
    VaultInp = "vault"

class Job:
    def __init__(self, title="", desc="", handler=None, dependsOn=[], args=[], interaction=None):
        self.title = title
        self.description = desc
        self.handler = handler
        self.dependsOn = dependsOn
        self.args = args
        self.interaction = interaction

class Argument:
    def __init__(self, desc="", inputType=InputType.TextFieldInp, key="", value=""):
        self.description = desc
        self.inputType = inputType
        self.key = key
        self.value = value

class ManualInteraction:
    def __init__(self, desc="", inputType=InputType.TextFieldInp, value=""):
        self.description = desc
        self.inputType = inputType
        self.value = value

def GetJob(hash, cachedJobs):
    for job in cachedJobs:
            if job.job.unique_id == hash:
                return job
    return None

class JobWrapper:
    def __init__(self, handler=None, job=None):
        self.handler = handler
        self.job = job
