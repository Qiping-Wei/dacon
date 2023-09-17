import json
import logging
import os
import re
logger = logging.getLogger(__name__)

def read_a_file(file_path):
    if os.path.exists(file_path):
        return open(file_path, 'r', encoding="utf8").read()
    else:
        logger.error("Error message: does not exits: {}".format(file_path))
        return []



def remove_comments(input_str):
    # Remove single-line comments (// ...)
    input_str = re.sub(r'\/\/.*', '', input_str)

    # Remove multi-line comments (/* ... */)
    input_str = re.sub(r'\/\*.*?\*\/', '', input_str, flags=re.DOTALL)

    # Remove unnecessary space lines
    input_str = re.sub(r'\n\s*\n', '\n', input_str, flags=re.MULTILINE)

    return input_str


def remove_import_statements(file_content:str)->str:
    # Define the regular expression pattern to match import statements
    import_pattern = r'^\s*import\s+[^\n\r;]+[;\n\r]'
    # Remove import statements from the Solidity code
    cleaned_code = re.sub(import_pattern, '', file_content, flags=re.MULTILINE)

    return cleaned_code

def is_in_given_list(data,item_list:list):
    def is_sv(value:str,type:str):
        if value in item_list:
            if type in ['Literal', 'IndexAccess', 'Identifier', 'MemberAccess']:
                return True,value
        return False,None

    if isinstance(data,str):
        if '@@' in data:
            items=data.split('@@')
            type=items[-1]
            if '[' in items[0]:
                v=items[0].split('[')[0].strip()
            else:
                v=items[0]
            return is_sv(v,type)

    logger.info('wrong data format.Expected: value@@type')
    return False,None


def is_assignment_operator(data:str)->bool:
    if '@@' in data:
        items=data.split('@@')
        if items[1]=='operator':
            if items[0] in ['=','+=','-=','*=','/=','&=']:
                return True
    return False

def dump_to_json(data,file_path:str,indent=4):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data.to_json(), f, indent=indent)

def dump_json_object_to_json(data,file_path:str,indent=4):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)
