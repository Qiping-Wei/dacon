import solcast
import solcx
from solcx import compile_standard

from dacon.utils import read_a_file

"""
Assume that all related libraries or contracts are in a single file.
This is critical to using source mapping to get back the source code.

When in a single file, I can preprocess this single file and git it to the solc. The result is that I can correctly get back the source code for each entity.

When libraries or contracts are scattered in different files, I can not preprocess them without some effort ( the effort to find the related files and give the preprocessed files to solc.)

If the files are not processed, the code I get based on the source mapping misses some characters at the beginning. I guess solc compiles based on a slightly different version (of course, the code of contracts is not changed). I do not have time to explore this at this moment. So, right now, I just assume that all the required code is in a single file.

-----------------
multiple files -> multiple SourceUnit nodes
one file -> one SourceUnit node

"""

def get_ast_nodes(solidity_file_path:str,solidity_file_name: str, solc_version: str, import_paths: list = []):
    # solcx_binary_path = "/home/wei/.solcx/"
    # os.environ["SOLCX_BINARY"] = solcx_binary_path

    # set the version of solc. Install it if the version required is not installed.
    if solc_version not in solcx.get_installed_solc_versions():
        solcx.install_solc(solc_version)
    solcx.set_solc_version(solc_version)

    allowed_paths = import_paths + ["."]


    solidity_file_path_name = solidity_file_path + solidity_file_name

    file_content = read_a_file(solidity_file_path_name)


    # Compile the contract using py-solc-x
    compiled_contract = compile_standard(
        {
            "language": "Solidity",
            "sources": {solidity_file_path_name: {"content": file_content}}, # ok
            # "sources": {solidity_file_path_name: {"urls": [solidity_file_path_name]}}, # ok
            "settings": {
                "outputSelection": {
                    "*": {
                        "": ["ast"]
                    }
                }
            }
        },
        allow_paths=allowed_paths
    )

    SourceUnit_all_nodes = solcast.from_standard_output(compiled_contract)

    return SourceUnit_all_nodes,file_content