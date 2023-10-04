from daconx.traverse_data_collection import data_collection_1

my_input_data=[
        ["HoloToken.sol","HoloToken","0.4.18",[],""],
        ["Crowdsale.sol", "Crowdsale", "0.4.25",[],""],
        ["DoubleEther.sol","DoubleEther","0.5.1",[],"https://github.com/EtherAuthority/Smart-Contracts-Library/blob/main/Game/Double%20Ether%20(with%20its%20own%20token).sol"],

]

solidity_file_path = "./test_data/"
contract_index = 2
solidity_file_name = my_input_data[contract_index][0]
contract_name = my_input_data[contract_index][1]
solc_version = my_input_data[contract_index][2]


def test_data_collection():

    contract_level_info,contract_detailed_data=data_collection_1(solidity_file_path, solidity_file_name, solc_version)


    assert len(contract_level_info)>0 and len(contract_detailed_data)>0

