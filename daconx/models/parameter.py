from daconx.models.id_name import id_name


class ParameterInfo():
    def __init__(self, id:int=-1,name: str="", type: str=""):
        self.id=id
        self.name = name
        self.type = type
    def reset(self):
        self.id = -1
        self.name = ""
        self.type = ""

    def initialize(self, text: str, is_parameter:bool=True):
        items=text.split(';')
        if is_parameter:
            self.id = int(items[2].split('id:')[-1])
            self.name = items[1].split('parameter_name:')[-1]
            self.type = items[0].split('parameter_type:')[-1]
        else:
            self.id=int(items[2].split('id:')[-1])
            self.name=items[1].split('return_value_name:')[-1]
            self.type=items[0].split('return_value_type:')[-1]
        id_name.add_id_name(self.id,self.name)

    def to_json(self):
        return {
            "name": self.name,
            "type": self.type,
        }
