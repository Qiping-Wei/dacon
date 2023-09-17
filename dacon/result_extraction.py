
from dacon.models.event import EventInfo
from dacon.models.function import FunctionInfo
from dacon.models.modifier import ModifierInfo
from dacon.models.state_variable import StateVariableInfo
from dacon.utils import dump_to_json


def collect_state_variable_data(contract_record:str,sv_code_dict:dict):
    # collect state variables
    state_variable_info={}
    for segment in contract_record.split("====\n"):
        segment = segment.strip()
        if len(segment) == 0: continue

        components = segment.split('----\n')
        if len(components)==0:continue

        svInfo=StateVariableInfo()
        svInfo.reset()
        svInfo.initialize(components,sv_code_dict)
        if svInfo.id>0:
            state_variable_info[svInfo.name]=svInfo

    return state_variable_info

def collect_event_data(contract_record:str,event_code_dict:dict={}):
    event_info = {}
    for segment in contract_record.split("====\n"):
        segment = segment.strip()
        if len(segment) == 0: continue

        components = segment.split('----\n')
        if len(components) == 0: continue

        eInfo = EventInfo()
        eInfo.reset()
        eInfo.initialize(components, event_code_dict)
        if eInfo.id>0:
            event_info[eInfo.name] = eInfo

    return event_info



def collect_modifier_data(contract_record:str,state_variables:list,modifier_code_dict:dict):
    # collect state variables
    modifier_info={}
    segments=contract_record.split("====\n")
    for segment in contract_record.split("====\n"):
        segment = segment.strip()
        if len(segment) == 0: continue

        components = segment.split('----\n')
        if len(components) ==0: continue

        mInfo=ModifierInfo()
        mInfo.reset()
        mInfo.initialize(components,state_variables,modifier_code_dict)
        if mInfo.id>0:
            modifier_info[mInfo.name]=mInfo

    return modifier_info


def collect_function_data(contract_record:str,state_variables:list=[],events:list=[],function_code_dict:dict={}):
    function_info={}
    for segment in contract_record.split("====\n"):
        segment = segment.strip()
        if len(segment) == 0: continue

        components = segment.split('----\n')
        if len(components)==0:continue

        fInfo=FunctionInfo()
        fInfo.reset()
        fInfo.initialize(components,state_variables,events,function_code_dict)
        if fInfo.id>0:
            function_info[fInfo.name]=fInfo


    return function_info


