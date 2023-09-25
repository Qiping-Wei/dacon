from daconx.config import result_extraction_symbols
from daconx.utils import is_assignment_operator, is_in_given_list


"""
reconstruct code from items instead of getting the code from the parent nodes so that each item can be considered separately.
"""
def collect_local_variable_general(items:list):
    """
    a case of two local variables are defined in one statement.
     (bool ok, bytes memory returnData) = _UPGRADE_BEACON.staticcall("");
     ['state_variable_name:ok', 'id:10', 'visibility:internal', 'type:bool', 'NULL', 'state_variable_name:returnData', 'id:12', 'visibility:internal', 'type:bytes', 'NULL', 'initial_value:', 'function_call:', '_UPGRADE_BEACON.staticcall@@MemberAccess', 'xxxxfunction_call:_UPGRADE_BEACON:staticcall', '(', '""@@Literal', ')', '']
    :param items:
    :return:
    """
    function_calls=[]
    sv_names=[]
    v_name = items[0].split('state_variable_name:')[-1]
    sv_names.append(v_name)
    v_value = ""
    flag_read = False
    for item in items[1:]:
        if item in ['function_call:']: continue
        if item.startswith(result_extraction_symbols["function_call"]):
            function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
            if function_call_name not in function_calls:
                function_calls.append(function_call_name)
            continue
        elif item.startswith('id:'): continue
        elif item.startswith("visibility:"):continue
        elif item.startswith("type:"):continue
        elif item.startswith('state_variable_name:'):
            v_name = item.split('state_variable_name:')[-1]
            sv_names.append(v_name)

        if item.startswith('initial_value'):
            flag_read=True
        else:
            if flag_read:
                if item in ['function_call:']: continue
                if item.startswith(result_extraction_symbols["function_call"]):
                    function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
                    if function_call_name not in function_calls:
                        function_calls.append(function_call_name)
                    continue
                if '@@' in item:
                    item_ele = item.split("@@")
                    v_value += item_ele[0]
                else:
                    v_value += item
    return sv_names,v_value,function_calls


def collect_assignment_general(items:list,state_variables:list):
    """
        collect the assignment that write a state variable and function calls if there are
    :param items:
    :param state_variables:
    :return:
    """
    function_calls=[]
    code_statement = ''
    sv_left_hand_side = []  # save variables on the left hand side
    flag_stop = False
    for item in items[1:]:
        if item in ['function_call:']: continue
        if item.startswith(result_extraction_symbols["function_call"]):
            function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
            if function_call_name not in function_calls:
                function_calls.append(function_call_name)
            continue

        if '@@' in item:
            item_ele = item.split('@@')
            code_statement += item_ele[0]
            if not flag_stop:
                sv_left_hand_side.append(item)
            if is_assignment_operator(item):
                flag_stop = True
        else:
            code_statement += item

    sv_written = []
    # check if a state variable is written
    for item in sv_left_hand_side:
        is_sv, sv = is_in_given_list(item, state_variables)
        if is_sv:
            sv_written.append(sv)

    return code_statement,sv_written,function_calls

def collect_condition_general( items:list,state_variables:list):
    """
    collect the condition, the state varibles read in it and function calls invoked it
    :param items:
    :param state_variables:
    :return:
    """
    condition = ""
    function_calls=[]
    sv_read=[]
    for item in items[1:]:
        if item in ['function_call:']: continue
        if item.startswith(result_extraction_symbols["function_call"]):
            function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
            if function_call_name not in function_calls:
                function_calls.append(function_call_name)
            continue
        if '@@' in item:
            item_ele = item.split("@@")
            condition += item_ele[0]
            is_sv, sv = is_in_given_list(item, state_variables)
            if is_sv:
                if sv not in sv_read:
                    sv_read.append(sv)
        else:
            condition += item
    return condition,sv_read,function_calls

def collect_an_independent_function_call_general(items:list,state_variables:list):
    test=['function_call:', '(', 'function_call:', 'address@@ElementaryTypeNameExpression', '(', 'this@@Identifier', ')', ',', '_amount@@Identifier', ',', '0@@Literal', ',', '0@@Literal', ',', 'function_call:', 'address@@ElementaryTypeNameExpression', '(', 'this@@Identifier', ')', ',', 'block.timestamp@@MemberAccess', ')']
    call_code = ""
    function_calls = []
    sv_read = []
    for item in items[1:]:
        if item in ['function_call:']: continue
        if item.startswith(result_extraction_symbols["function_call"]):
            function_call_name = item.split(result_extraction_symbols["function_call"])[-1]
            if function_call_name not in function_calls:
                function_calls.append(function_call_name)
            continue
        if '@@' in item:
            item_ele = item.split("@@")
            call_code += item_ele[0]
            is_sv, sv = is_in_given_list(item, state_variables)
            if is_sv:
                if sv not in sv_read:
                    sv_read.append(sv)
        else:
            call_code += item
    return call_code, sv_read, function_calls
