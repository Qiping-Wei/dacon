
import logging
import os.path

from daconx.models.id_name import id_name
from daconx.models.contract import ContractLevelInfo, ContractInfo

from daconx.node_traverse import AST_NodeTraverse
from daconx.result_extraction import collect_state_variable_data, collect_modifier_data, collect_function_data, \
    collect_event_data
from daconx.solc_compile import get_ast_nodes
from daconx.utils import dump_to_json

logger = logging.getLogger(__name__)

def get_code_from_src(src: str, content:str):
    items = src.split(":")
    assert len(items) >= 2
    start = int(items[0])
    length = int(items[1])
    return content[start:start + length]

def contract_level_data_collection(nodes:list, solidity_file_content):
    assert len(nodes)==1
    contract_level_info={}

    if hasattr(nodes[0],'nodes'):
        for node in nodes[0].nodes:
            if hasattr(node, 'nodeType'):
                if node.nodeType == 'ContractDefinition':
                    con_level_info = ContractLevelInfo()
                    con_level_info.reset()
                    con_level_info.name = node.name
                    con_level_info.code = get_code_from_src(node.src, solidity_file_content)
                    con_level_info.node = node

                    if hasattr(node, 'id'):
                        con_level_info.id = node.id
                    if hasattr(node,'abstract'):
                        con_level_info.abstract=node.abstract
                    if hasattr(node, 'fullyImplemented'):
                        con_level_info.fullyImplemented = node.fullyImplemented

                    if hasattr(node,'baseContracts'):
                        for base in node.baseContracts:
                            base_name=""
                            base_id=-1
                            if hasattr(base,'baseName'):
                                if hasattr(base.baseName,'name'):
                                    base_name=base.baseName.name
                                if hasattr(base.baseName,'id'):
                                    base_id=base.baseName.id
                            con_level_info.baseContracts.append(base_name)
                            id_name.add_id_name(base_id,base_name)

                    if hasattr(node,'dependencies'):
                        for dp in node.dependencies:
                            dp_name=""
                            dp_id=-1
                            if hasattr(dp,'name'):
                                dp_name=dp.name
                            if hasattr(dp,'id'):
                                dp_id=dp.id
                            con_level_info.dependencies.append(dp_name)
                            id_name.add_id_name(dp_id,dp_name)

                    if hasattr(node,'linearizedBaseContracts'):
                        con_level_info.linearizedBaseContracts=node.linearizedBaseContracts
                    if hasattr(node,'libraries'):
                        if isinstance(node.libraries,dict):
                            for key,library in node.libraries.items():
                                if hasattr(library, 'name'):
                                    if hasattr(library, 'id'):
                                        id_name.add_id_name(library.id, library.name)
                                        con_level_info.libraries[key]=library.name
                        else:
                            print('need to check the type of libraries properties of a contract in traverse_data_collection.py')



                    contract_level_info[con_level_info.name]=con_level_info

    # replace id with name for linearizedBaseContracts
    for con_level_info in contract_level_info.values():
        con_level_info.linearizedBaseContracts=[id_name.get_name_from_id(id_) for id_ in con_level_info.linearizedBaseContracts]
    return contract_level_info


def contract_detailed_data_collection(solidity_file_name,solc_version,contract_level_data:ContractLevelInfo,solidity_file_content:str):
    contract_detailed_data={}
    for con_name,con_level_info in contract_level_data.items():
        logger.info(f'**** {con_name} ****')
        node_traverse=AST_NodeTraverse(solidity_file_content)
        # traverse the contract ast nodes
        node_traverse.traverse_ast(con_level_info.node)

        # collect state variable data
        state_variable_info=collect_state_variable_data(node_traverse.accumulated_print_results,node_traverse.state_variable_code_dict)
        state_variables=list(state_variable_info.keys())

        # collect event data
        event_info = collect_event_data(node_traverse.accumulated_print_results, node_traverse.event_code_dict)
        events = list(set(event_info.keys()))

        # collect modifier data
        modifier_info=collect_modifier_data(node_traverse.accumulated_print_results,state_variables,node_traverse.modifier_code_dict)


        # collect function data
        function_info=collect_function_data(node_traverse.accumulated_print_results,state_variables,events,node_traverse.function_code_dict)


        # collect contract detailed result
        contractInfo=ContractInfo(solidity_file_name,con_name,solc_version,state_variable_info,modifier_info,function_info,event_info)

        # save the contract detailed data
        contract_detailed_data[con_name]=contractInfo
    return contract_detailed_data


def output_contract_level_data(contract_level_data:ContractLevelInfo, result_path_name:str):
    # Define a dictionary-like object
    class MyDict(dict):
        # Custom method
        def to_json(self):
            return{key:value.to_json()
                for key,value in self.items()
            }

    my_data=MyDict(contract_level_data)

    dump_to_json(my_data,result_path_name,indent=4)




def data_collection(args):
    # compile to get ast nodes and the file content that solc compiles from it
    nodes, solidity_file_content = get_ast_nodes(args.solidity_file_path, args.solidity_file_name, args.solv,
                                                 args.imports)

    # collect contract level data
    contract_level_info=contract_level_data_collection(nodes, solidity_file_content)


    # for each contract, collect more data
    contract_detailed_data=contract_detailed_data_collection(args.solidity_file_name,args.solv,contract_level_info,solidity_file_content)

    if os.path.exists(args.result_path):
        path = "{}{}_{}.json".format(args.result_path, args.solidity_file_name, "contract_level_data")
        output_contract_level_data(contract_level_info, path)

        for con_name, contractInfo in contract_detailed_data.items():
            path="{}{}_{}_{}.json".format(args.result_path,args.solidity_file_name,"contract_detailed_data",con_name)
            dump_to_json(contractInfo,path)
    else:
        logger.info(f'Path {args.result_path} does not exist.')



