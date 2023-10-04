from daconx.extract_extraction_utils import collect_assignment_general, collect_condition_general, \
    collect_an_independent_function_call_general, collect_local_variable_general
from daconx.models.id_name import id_name


class ModifierInfo():
    def __init__(self,name:str="",id:int=-1,state_variables_read:list=[],conditions:list=[],assignments:list=[],state_variables_written:list=[],code:str="",function_calls:list=[]):
        self.name=name
        self.id=id

        self.conditions=conditions
        self.state_variables_read = state_variables_read

        self.assignments=assignments
        self.state_variables_written = state_variables_written

        self.code=code
        self.function_calls=function_calls
        self.independent_function_calls=[]
        self.local_variables={}
        self.inlineAssembly=[]
        self.emitStatements=[]

    def reset(self):
        self.name = ""
        self.id = -1

        self.conditions = []
        self.state_variables_read = []

        self.assignments = []
        self.state_variables_written = []

        self.code = ""
        self.function_calls = []
        self.independent_function_calls=[]
        self.local_variables = {}
        self.inlineAssembly=[]
        self.emitStatements=[]

    def to_json(self):
        return {
            "name": self.name,
            "conditions":self.conditions,
            "state_variables_read":self.state_variables_read,
            "assignments":self.assignments,
            "state_variables_written":self.state_variables_written,

            "function_calls":self.function_calls,
            "code":self.code

        }


    def initialize(self,components:list,state_variables:list,modifier_code_dict:dict):
        """

        :param text:
        :return:
        """

        items = components[0].split('\n')
        if len(items)==0: return
        if items[0].startswith('modifier_name'):
            """ format:                    
                modifier_name:onlyMinter
                ----
                function_call:
                require
            """

            self.name = items[0].split('modifier_name:')[-1]
            for item in items[1:]:
                if item.startswith("id:"):
                    self.id=int(item.split("id:")[-1])
                    id_name.add_id_name(self.id, self.name)

            # collect more data about modifier
            for component in components[1:]:
                items = component.split('\n')
                if len(items) == 0: continue

                if items[0].startswith('function_call'):
                    if items[1].startswith('require@@Identifier') or items[1].startswith('assert@@Identifier') :
                        # collect conditions
                        self.collect_condition(items, state_variables)
                    else:
                        self.collect_an_independent_function_call(items,state_variables)

                elif items[0].startswith('if_statement'):
                    self.collect_condition(items, state_variables)
                elif items[0].startswith('while_statement'):
                    self.collect_condition(items, state_variables)
                elif items[0].startswith('for_statement'):
                    self.collect_condition(items, state_variables)
                elif items[0].startswith('assignment'):
                    self.collect_assignment(items, state_variables)
                elif items[0].startswith('state_variable_name:'):
                    self.collect_local_variable(items)
                elif items[0].startswith('inlineAssembly:'):
                    assembly = "assembly"
                    for item in items:
                        if item.startswith("inlineAssembly:"):
                            assembly += item.split("inlineAssembly:")[-1]
                        else:
                            assembly += item
                    self.inlineAssembly.append(assembly)
                elif items[0].startswith('emitStatement:'):
                    emit_str=items[0].split('emitStatement:')[-1]
                    if emit_str.startswith('emit'):
                        emit_str=emit_str.lstrip('emit')
                    self.emitStatements.append(emit_str)

                else:
                    if len(component) == 0: continue
                    if str(component) == '----': continue
                    if '@@' in items[0]:
                        name = str(items[0]).split("@@")[0]
                        if name in ['delete']:
                            # means an independent function calls
                            self.collect_an_independent_function_call(items, state_variables)
                            continue

                    print(f'info: check what this case is in modifier.py\n')




            self.code=modifier_code_dict[self.name]

    def collect_local_variable(self, items):
        v_names, v_value, function_calls, condi = collect_local_variable_general(items)
        if len(v_names) > 0:
            for v_name in v_names:
                self.local_variables[v_name] = v_value
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)
        if condi not in self.conditions:
            self.conditions.append(condi)

    def collect_assignment(self, items: list, state_variables: list):
        """
            collect the assignments that write state variables
            need to update the state variable written as well
        :param items:
        :param state_variables:
        :return:
        """
        code_statement, sv_written, function_calls = collect_assignment_general(items, state_variables)

        if len(sv_written) > 0:  # a statement that write state variables
            self.assignments.append(code_statement)
        for sv in sv_written:
            if sv not in self.state_variables_written:
                self.state_variables_written.append(sv)
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)

    def collect_condition(self, items:list,state_variables:list):
        condition,sv_read,function_calls=collect_condition_general(items,state_variables)
        self.conditions.append(condition)
        for sv in sv_read:
            if sv not in self.state_variables_read:
                self.state_variables_read.append(sv)
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)

    def collect_an_independent_function_call(self,items:list,state_variables:list):
        call_code,sv_read,function_calls=collect_an_independent_function_call_general(items,state_variables)
        if call_code not in self.function_calls:
            self.function_calls.append(call_code)
        self.independent_function_calls.append([call_code,sv_read])
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)
