from daconx.models.id_name import id_name
from daconx.models.parameter import ParameterInfo


class EventInfo():
    def __init__(self, id:int=-1, name:str="",code:str="",parameter_info:{ParameterInfo}={}):
        self.id=id
        self.name=name
        self.code=code
        self.parameter_info=parameter_info

    def reset(self):
        self.id = -1
        self.name = ""
        self.code = ""
        self.parameter_info = {}

    def to_json(self):
        return {
            "name": self.name,
            "parameter_info": {name: param.to_json()
                               for name, param in self.parameter_info.items()},
            "code": self.code

        }

    def initialize(self,components:list,event_code_dict:dict):
        items = components[0].split('\n')
        if len(items) == 0: return

        if items[0].startswith('event_name:'):
            self.name = items[0].split('event_name:')[-1]
            # collect basic data
            for item in items[1:]:
                if item.startswith("id:"):
                    self.id = int(item.split("id:")[-1])
                    id_name.add_id_name(self.id,self.name)
                elif item.startswith('parameter_type'):
                    param = ParameterInfo()
                    param.reset()
                    param.initialize(item)
                    self.parameter_info[param.name] = param

            self.code=event_code_dict[self.name]

