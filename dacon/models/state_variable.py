from dacon.config import result_extraction_symbols
from dacon.models.id_name import id_name


class StateVariableInfo():
    def __init__(self, name: str='', id:int=-1, type:str='', visibility: str = '', initial_value: str = '',code:str="",function_calls:list=[]):
        self.name = name,
        self.id=id
        self.type = type,
        self.visibility = visibility
        self.initial_value = initial_value
        self.code=code,
        self.function_calls=function_calls
    def reset(self):
        self.name = "",
        self.id = -1
        self.type = "",
        self.visibility = "private"
        self.initial_value ="NULL"
        self.code = "",
        self.function_calls = []


    def to_json(self):
        return {
            "name": self.name,
            "type":self.type,
            "visibility":self.visibility,
            "initial_value":self.initial_value,
            "function_calls":self.function_calls,
            "code":self.code

        }


    def initialize(self,components:list,sv_code_dict:dict):
        """
        format:
                state_variable_name:name
                visibility:public
                type:string memory
                "HoloToken"
                ...

        :param text:
        :return:
        """
        items = components[0].split('\n')
        if len(items)==0:return

        if not items[0].startswith('state_variable_name:'):return

        self.name = items[0].split('state_variable_name:')[-1]
        self.visibility = 'internal'
        self.type = 'NULL'
        self.initial_value = ''
        self.function_calls = []
        for item in items[1:]: # start from the second item
            if item.startswith('visibility'):
               self.visibility = item.split('visibility:')[-1]
            elif item.startswith('type'):
                self.type = item.split('type:')[-1]
            elif item.startswith("id:"):
                self.id=int(item.split("id:")[-1])
                id_name.add_id_name(self.id, self.name)
            else:
                if item in ['function_call:']: continue
                # collect function call names
                if item.startswith(result_extraction_symbols["function_call"]):
                    function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
                    if function_call_name not in self.function_calls:
                        self.function_calls.append(function_call_name)
                    continue
                # collect expression of the value
                if '@@' in item:
                    item_ele = item.split('@@')
                    self.initial_value += item_ele[0]
                else:
                    self.initial_value += item

        if len(self.initial_value) == 0:
            self.initial_value = 'NULL'
        self.code=sv_code_dict[self.name]