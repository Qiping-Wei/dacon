dataset_contract_info_path= "C:\\Users\\18178\\PycharmProjects\\dependency\\dataset\\contract_info\\"
dataset_path='./dataset/'
temp_path="C:\\Users\\18178\\PycharmProjects\\dependency\\temp\\"
result_path='./example_results/'
prompt_path="C:\\Users\\18178\\PycharmProjects\\dependency\\prompts\\"
dataset_solidity_path="C:\\Users\\18178\\PycharmProjects\\dependency\\dataset\\solidity_files\\"



parameters=[
        ["HoloToken.sol","HoloToken","0.4.18",[],""],
        ["Crowdsale.sol", "Crowdsale", "0.4.25",[],""],
        ["data_dependency.sol","Simple","",[],"from slither"],
        ["GenericMetaTxProcessor.sol","GenericMetaTxProcessor","0.6.1",[],"https://github.com/wighawag/singleton-1776-meta-transaction"],
        # ["MetaCoin.sol","MetaCoin","0.5.2",[zeppelin_solidity_path+"token\\ERC20\\"],"https://github.com/austintgriffith/native-meta-transactions"],
        ["DoubleEther.sol","DoubleEther","0.5.1",[],"https://github.com/EtherAuthority/Smart-Contracts-Library/blob/main/Game/Double%20Ether%20(with%20its%20own%20token).sol"],
        ["HXXD.sol","HXXD","0.4.25",[],""], # 5  can not be compiled
        ["PlaceIt.sol","PlaceIt","0.4.25",[],""], #6 can not be compiled
        ["CrowdSale.sol","Crowdsale","0.4.25",[],""], # 7
        ["DydxToken.sol","DydxToken","0.7.5",[],"https://etherscan.io/address/0x92d6c1e31e14520e676a687f0a93788b716beff5#code"],
        ["PupperCoinCrowdsale.sol","PupperCoinCrowdsale","0.5.0",[],""],
        ["YodaiToken.sol","Yodatoshi","0.8.17",[],"https://github.com/EtherAuthority/Smart-Contracts-Library/blob/main/Yodai%20Token/YodaiToken.sol"]
    ]
# dataset_solidity_path="C:\\Users\\18178\\PycharmProjects\\dependency\\dataset\\temp\\governance_contracts\\"
contract_index=10 # specify which contract will be evaluated.


color_prefix={
"Black": "\033[30m",
"Red": "\033[31m",
"Green": "\033[32m",
"Yellow": "\033[33m",
"Blue": "\033[34m",
"Magenta": "\033[35m",
"Cyan": "\033[36m",
"White": "\033[37m",
"Gray": "\033[0m",
}

account_address_mapping = {
    "contract": "0x03C6FcED478cBbC9a4FAB34eF9f40767739D1Ff7",
    "user": "0x1aE0EA34a72D944a8C7603FfB3eC30a6669E454C",
    "owner": "0x14723A09ACff6D2A60DcdF7aA4AFf308FDDC160C"
}

state_format = '[{"contract":{"balance":"value","storage":{"goal":"value", "phase":"value", "raised":"value", "end":"value", "owner"="value", "investments": "value" },"constraints":["the constraints to reach this state",...]},"user":{"balance":"value"},"owner":{"balance":"value"}},...]'

solidity_built_in_variables=["now",'msg.value','msg.sender','msg.data','block.number','block.timestamp','tx.origin','block.coinbase']



result_extraction_symbols={
    "function_call":"xxxxfunction_call:"
}