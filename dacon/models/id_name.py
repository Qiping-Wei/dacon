class Id_Name():
    def __init__(self):
        self.id_to_name = {}
        self.name_to_id = {}

    def add_id_name(self, id: int, name: str):
        if id > 0 and len(name) > 0:
            if id not in self.id_to_name.keys():
                self.id_to_name[id] = name
            if name not in self.name_to_id.keys():
                self.name_to_id[name] = id

    def get_id_from_name(self, name: str):
        if name in self.name_to_id.keys():
            return self.name_to_id[name]
        else:
            return -1

    def get_name_from_id(self, id: int):
        if id in self.id_to_name.keys():
            return self.id_to_name[id]
        else:
            return ""


id_name=Id_Name()