from daconx.extract_extraction_utils import collect_assignment_general, collect_condition_general, \
    collect_local_variable_general, collect_an_independent_function_call_general, collect_conditional_expression_general
from daconx.models.id_name import id_name
from daconx.models.parameter import ParameterInfo
from daconx.utils import get_bool_value


class FunctionInfo():
    def __init__(self, name:str='', id:int=-1, selector:str="", is_constructor:str=False,implemented:bool=False, visibility:str='',stateMutability:str='nonpayable', virtual:bool=False, parameter_info:{ParameterInfo}={}, return_values:list=[], modifiers:list=[], branch_conditions:list=[], state_variables_read_in_BC:list=[], code_statement_write_state_variables:list=[], state_variables_written:list=[],function_calls:list=[], function_code:str=''):

        self.name=name if "(" not in name else name.split("(")[0].strip()
        self.id=id
        self.selector=selector
        self.is_constructor=is_constructor
        self.implemented=implemented
        self.visibility = visibility
        self.stateMutability=stateMutability
        self.virtual=virtual

        self.parameter_info=parameter_info
        self.return_values=return_values

        self.modifiers=modifiers

        self.branch_conditions=branch_conditions
        self.state_variables_read_in_BC=state_variables_read_in_BC

        self.code_statement_write_state_variables=code_statement_write_state_variables
        self.state_variables_written=state_variables_written

        self.function_calls=[]
        self.function_code=function_code
        self.local_variables={}
        self.inlineAssembly = []
        self.emitStatements = []
        self.returnStatements = []
        self.independent_function_calls=[]

    def reset(self):
        self.name = ""
        self.id = -1
        self.selector = ""
        self.is_constructor = False
        self.implemented = False
        self.visibility = ""
        self.stateMutability = ""
        self.virtual = False

        self.parameter_info = {}
        self.return_values = []

        self.modifiers = []

        self.branch_conditions = []
        self.state_variables_read_in_BC = []

        self.code_statement_write_state_variables =[]
        self.state_variables_written = []

        self.function_calls = []
        self.function_code = ""
        self.local_variables = {}
        self.events=[]
        self.inlineAssembly=[]
        self.emitStatements=[]
        self.returnStatements=[]
        self.independent_function_calls = []

    def to_json(self):
        return {
            "name": self.name,
            "selector":self.selector,
            "is_constructor":self.is_constructor,
            "implemented":self.implemented,
            "virtual":self.virtual,
            "visibility":self.visibility,
            "stateMutability":self.stateMutability,
            "parameter_info":{name:param.to_json()
                              for name,param in self.parameter_info.items()},
            "return_values":[param.to_json() for param in self.return_values],

            "modifiers":self.modifiers,
            "branch_conditions":self.branch_conditions,
            "state_variables_read_in_BC":self.state_variables_read_in_BC,
            "code_statement_write_state_variables":self.code_statement_write_state_variables,
            "state_variables_written":self.state_variables_written,
            "function_calls":self.function_calls,
            "function_code":self.function_code,
            "local_variables":self.local_variables,
            "events":self.events,
        }



    def initialize(self,components:list,state_variables:list,events:list,function_code_dict:{}):
        """ format
               function_name:mint
               visibility:external
               is_constructor:False
               modifier_name:onlyMinter
               modifier_name:canMint
               parameter_type:address;parameter_name:_to
               parameter_type:uint256;parameter_name:_amount
               return_values:
               parameter_type:bool;parameter_name:NULL

               ----------------------
               function_call:
               ...
           """

        items = components[0].split('\n')
        if len(items)==0:return

        if items[0].startswith('function_name:'):
            self.name = items[0].split('function_name:')[-1]
            # collect basic data
            for item in items[1:]:
                if item.startswith("id:"):
                    self.id=int(item.split("id:")[-1])
                    id_name.add_id_name(self.id, self.name)
                elif item.startswith("is_constructor:"):
                    self.id=get_bool_value(item.split('is_constructor:')[-1])
                elif item.startswith('functionSelector:'):
                    self.selector=item.split('functionSelector:')[-1]
                elif item.startswith('implemented:'):
                    self.implemented=get_bool_value(item.split('implemented:')[-1])
                elif item.startswith('stateMutability:'):
                    self.stateMutability=item.split('stateMutability:')[-1]
                elif item.startswith('virtual:'):
                    self.virtual=get_bool_value(item.split('virtual')[-1])
                elif item.startswith('visibility:'):
                    self.visibility=item.split('visibility:')[-1]
                elif item.startswith('modifier_name'):
                    self.modifiers.append(item.split('modifier_name:')[-1])
                elif item.startswith('parameter_type'):
                    param=ParameterInfo()
                    param.reset()
                    param.initialize(item)
                    self.parameter_info[param.name]=param
                elif item.startswith('return_value_type'):
                    param = ParameterInfo()
                    param.reset()
                    param.initialize(item,False)
                    self.return_values.append(param)
                else: pass

            # collect more data about function
            for component in components[1:]:
                items = component.split('\n')
                if len(items)==0:continue

                if items[0].startswith('function_call'):
                    if items[1].startswith('require@@Identifier') or items[1].startswith('assert@@Identifier'):
                        # collect conditions
                        self.collect_condition(items, state_variables)
                    else:
                        if '@@' in items[1]:
                            name=str(items[1]).split("@@")[0]
                            if name in events:
                                self.events.append(name)
                                continue
                        # means an independent function calls
                        self.collect_an_independent_function_call(items,state_variables)

                elif items[0].startswith('assignment'):
                    """
                        assignment:
                        balances[_from]
                        =
                        function_call:
                        balances[_from].sub
                        (
                        _value
                        )
                    """
                    self.collect_assignment(items,state_variables)

                elif items[0].startswith('if_statement'):
                    self.collect_condition(items,state_variables)

                elif items[0].startswith('for_statement'):
                    """
                    ----------------------
                    for_statement
                    i
                    <
                    tos.length
                    ----------------------
                    """
                    self.collect_condition(items,state_variables)

                elif items[0].startswith('state_variable_name'):
                    # get local state variable (it will be replaced by its value at where it is used.
                    self.collect_local_variable(items)

                elif items[0].startswith('emitStatement:'):
                    emit_str=items[0].split('emitStatement:')[-1]
                    if emit_str.startswith('emit'):
                        emit_str=emit_str.lstrip('emit')
                    self.emitStatements.append(emit_str)

                elif items[0].startswith('inlineAssembly:'):
                    assembly="assembly"
                    for item in items:
                        if item.startswith("inlineAssembly:"):
                            assembly+=item.split("inlineAssembly:")[-1]
                        else:
                            assembly+=item
                    self.inlineAssembly.append(assembly)
                elif items[0].startswith('return:'):
                    re_value = ""
                    for item in items:
                        if item.startswith("return:"):
                            re_value += item.split("return:")[-1]
                        else:
                            re_value += item
                    self.returnStatements.append(re_value)
                elif items[0].startswith('conditional_expression:'):
                    self.collect_conditional_expression(items,state_variables)
                    # print(f'need to handle conditional expression')
                elif items[0].startswith('while_statement:'):
                    self.collect_condition(items,state_variables)
                elif items[0].startswith('do_while_statement:'):
                    self.collect_condition(items,state_variables)
                else:
                    if '@@' in items[0]:
                        node_type = str(items[0]).split("@@")[-1]
                        name = str(items[0]).split("@@")[0]
                        if node_type=='operator':
                            """
                                a case: unary operation
                                delete@@operator
                                set.index[value]@@IndexAccess                            
                            """
                            code=""
                            for item in items:
                                if '@@' in item:
                                    item_ele = item.split("@@")
                                    code += item_ele[0]+" "
                                else:
                                    code += item
                            if name not in ['delete','++','--']:
                                print(f'info: captured but not saved: {code} in funcion {self.name} in function.py\n')
                    else:
                        if len(component)==0:continue
                        if str(component)=='----':continue
                        print(f'info: check which is not handled in function.py\n')

            self.function_code=function_code_dict[self.name]


    def collect_local_variable(self,items):
        v_names,v_value,function_calls,condi=collect_local_variable_general(items)
        if len(v_names)>0:
            for v_name in v_names:
                self.local_variables[v_name]=v_value
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)
        if condi not in self.branch_conditions:
            self.branch_conditions.append(condi)

    def collect_condition(self, items:list,state_variables:list):
        condition,sv_read,function_calls=collect_condition_general(items,state_variables)
        self.branch_conditions.append(condition)
        for sv in sv_read:
            if sv not in self.state_variables_read_in_BC:
                self.state_variables_read_in_BC.append(sv)
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)

    def collect_assignment(self,items:list,state_variables:list):
        """
            collect the assignments that write state variables
            need to update the state variable written as well
        :param items:
        :param state_variables:
        :return:
        """
        code_statement,sv_written,function_calls=collect_assignment_general(items,state_variables)

        if len(sv_written) > 0:  # a statement that write state variables
            self.code_statement_write_state_variables.append(code_statement)
        for sv in sv_written:
            if sv not in self.state_variables_written:
                self.state_variables_written.append(sv)
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

    def collect_conditional_expression(self,items:list,state_variables:list):
        condition,epxre,sv_read,function_calls=collect_conditional_expression_general(items,state_variables)
        if condition not in self.branch_conditions:
            self.branch_conditions.append(condition)
        for sv in sv_read:
            if sv not in self.state_variables_read_in_BC:
                self.state_variables_read_in_BC.append(sv)
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)
        return epxre