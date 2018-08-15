from enum import Enum

class InputType(Enum):
    TextFieldInp = "textfield"
    TextAreaInp = "textarea"
    BoolInp = "boolean"
    VaultInp = "vault"

class Job:
    handler = None
    title = ""
    description = ""
    dependsOn = []
    args = []
    interaction = None

class Argument:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    description = ""
    inputType = InputType.TextFieldInp
    key = ""
    value = ""

class ManualInteraction:
    description = ""
    inputType = InputType.TextFieldInp
    value = ""

