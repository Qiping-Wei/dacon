from dacon.config import result_extraction_symbols
from dacon.utils import is_assignment_operator, is_in_given_list

def collect_local_variable_general(items:list):
    function_calls=[]
    v_name = items[0].split('state_variable_name:')[-1]
    v_value = ""
    flag_read = False
    for item in items[1:]:
        if item in ['function_call:']: continue
        if item.startswith('result_extraction_symbols["function_call"]'):
            function_call_name = item.split('result_extraction_symbols["function_call"]')[-1]
            if function_call_name not in function_calls:
                function_calls.append(function_call_name)
            continue
        elif item.startswith('id:'): continue
        elif item.startswith("visibility:"):continue
        elif item.startswith("type:"):continue

        if item.startswith('initial_value'):
            flag_read=True
        else:
            if flag_read:
                if '@@' in item:
                    item_ele = item.split("@@")
                    v_value += item_ele[0]
                else:
                    v_value += item
    return v_name,v_value,function_calls


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
