from enum import Enum

class InputType(Enum):
    TextFieldInp = "textfield"
    TextAreaInp = "textarea"
    BoolInp = "boolean"
    VaultInp = "vault"

class Job:
    def __init__(self, title="", desc="", handler=None):
        self.title = title
        self.description = desc
        self.handler = handler
    handler = None
    title = ""
    description = ""
    dependsOn = []
    args = []
    interaction = None

class Argument:
    def __init__(self, desc="", inputType=InputType.TextFieldInp, key="", value=""):
        self.description = desc
        self.inputType = inputType
        self.key = key
        self.value = value
    description = ""
    inputType = InputType.TextFieldInp
    key = ""
    value = ""

class ManualInteraction:
    def __init__(self, desc="", inputType=InputType.TextFieldInp, value=""):
        self.description = desc
        self.inputType = inputType
        self.value = value
    description = ""
    inputType = InputType.TextFieldInp
    value = ""

def GetJob(hash, cachedJobs):
    for job in cachedJobs:
            if job.job.unique_id == hash:
                return job
    return None

class JobWrapper:
    handler = None
    job = None
