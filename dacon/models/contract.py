
from dacon.models.event import EventInfo
from dacon.models.function import FunctionInfo
from dacon.models.modifier import ModifierInfo
from dacon.models.state_variable import StateVariableInfo


class ContractInfo():
    def __init__(self, solidity_file_name:str="", contract_name:str="", solc_version:str="0.5.0",state_variable_info:{StateVariableInfo}={}, modifier_info:{ModifierInfo}={}, function_info:{FunctionInfo}={},event_info:{EventInfo}={}):

        self.solidity_file_name=solidity_file_name
        self.contract_name=contract_name
        self.solc_version=solc_version

        self.state_variables = list(state_variable_info.keys())
        self.state_variable_info = state_variable_info

        self.modifiers = list(modifier_info.keys())
        self.modifier_info = modifier_info

        self.functions = list(function_info.keys())
        self.function_info = function_info

        self.events=list(event_info.keys())
        self.event_info=event_info

    def to_json(self):
        return {
            "solidity_file_name": self.solidity_file_name,
            "contract_name":self.contract_name,
            "solc_version":self.solc_version,
            "state_variables":self.state_variables,
            "modifiers":self.modifiers,
            "events":self.events,
            "functions":self.functions,
            "state_variable_info":{name:svInfo.to_json()
                for name,svInfo in self.state_variable_info.items()
            },

            "modifier_info":{name:mInfo.to_json()
                for name,mInfo in self.modifier_info.items()
            },

            "function_info":{name:fInfo.to_json() for name,fInfo in self.function_info.items()},

             "event_info":{name:eInfo.to_json() for name,eInfo in self.event_info.items()}
        }




class ContractLevelInfo():
    def __init__(self):
        self.name=""
        self.id=-1
        self.abstract=False
        self.fullyImplemented=True
        self.baseContracts=[]
        self.dependencies=[]
        self.libraries= {}
        self.linearizedBaseContracts=[]
        self.node=None
        self.code=""

    def reset(self):
        self.name = ""
        self.id = -1
        self.abstract = False
        self.fullyImplemented = True
        self.baseContracts = []
        self.dependencies = []
        self.libraries = {}
        self.linearizedBaseContracts = []
        self.node = None
        self.code = ""

    def to_json(self):
        return {
            "name": self.name,
            "abstract": self.abstract,
            "fullyImplemented": self.fullyImplemented,
            "baseContracts": self.baseContracts,
            "dependencies": self.dependencies,
            "libraries": self.libraries,
            "linearizedBaseContracts": self.linearizedBaseContracts,
            "code": self.code,

        }
