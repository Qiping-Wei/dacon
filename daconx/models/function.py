from daconx.extract_extraction_utils import collect_assignment_general, collect_condition_general, \
    collect_local_variable_general
from daconx.models.id_name import id_name
from daconx.models.parameter import ParameterInfo



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
                    self.id=bool(item.split('is_constructor:')[-1])
                elif item.startswith('functionSelector:'):
                    self.selector=item.split('functionSelector:')[-1]
                elif item.startswith('implemented:'):
                    self.implemented=bool(item.split('implemented:')[-1])
                elif item.startswith('stateMutability:'):
                    self.stateMutability=item.split('stateMutability:')[-1]
                elif item.startswith('virtual:'):
                    self.virtual=bool(item.split('virtual')[-1])
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
                        else:
                            print(f'check what this case is in function.py')

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

            self.function_code=function_code_dict[self.name]


    def collect_local_variable(self,items):
        v_name,v_value,function_calls=collect_local_variable_general(items)
        if len(v_name)>0:
            self.local_variables[v_name]=v_value
        for call_name in function_calls:
            if call_name not in self.function_calls:
                self.function_calls.append(call_name)


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