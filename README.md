## Dacon ##
The name of Dacon comes from **Da**ta of smart **con**tract. It is designed to collect the data of Solidity smart contract for static analysis. Essentially, it can get data by traversing the AST nodes of a smart contract. 

### Contract Level Data ###
```json
{
    "name":"contract name",        
    "abstract":"is abstract?",
    "fullyImplemented":"is fully implemented?",
    "baseContracts":["base contract name",...],
    "dependencies":["base contract name",...],
    "libraries":["base contract name",...],
    "linearizedBaseContracts":["base contract name",...],
    "node":"the root ast node of the contract",
    "code":"Solidity code of the contract"
}
```

### Contract Detailed Data ###
```json
{
  "state variables": {
      "name":"state variable name",
      "type":"type",
      "visibility":"visibility",
      "initial_value":"initial value",
      "code":"the code of declaring the variable",
      "function_calls":["function called",...]
  },
  
  "modifiers": {
      "name":"name",  
      "conditions":["condition",...],
      "state_variables_read":["state variable read in condition",...],      
      "assignments":["assignment that write a state variable",...],
      "state_variables_written": ["state variable written",...],
      "code": "the code of the modifier",
      "function_calls":["function called",...]
  },
  
  "functions": {
      "name":"function name",
      "selector":"function selector (4-byte signature)",
      "is_constructor":"is a constructor?",
      "implemented":"is implemented ?",
      "visibility":"visibility",
      "stateMutability":"stateMutability",
      "virtual":"is virtual?",
      "parameter_info":["parameter",...],
      "return_value_info":["return value",...],
      "modifiers":["modifier name",...],
      "branch_conditions":["condition",...],
      "state_variables_read_in_BC":["state variable read in a branch condition",...],
      "code_statement_write_state_variables":["assignment that write a state variable",...],
      "state_variables_written":["state vairable written",...],
      "function_calls":["function called",...],
      "function_code":"the code of the function",
      "local_variables":["local variable",...],
      "events": ["event name",...]
  },
  
  "events": {
      "name": "event name",
      "parameters": ["parameter",...],
      "code": "the code of the event"
  },
      
}
```
Note that since the root AST node of a contract is given, you can get other detailed data based on your need.

### Installation ###
```python
pip install dacon
```

### Useage ###
#### Use as a command: ####
```commandline
extract -p "path to the Solidity file name" -n "file name" --solv "solc version" --result_path "path to save the result" 
```


#### In the development case: ####

The arguments provided to extract.py in the root directory:
```commandline
-p "path to the Solidity file name"
-n "Solidity file name"
--solv "the version of solc"
--result_path "path to save the result"
```
Here is an example to get data for the Solidity file YodaiToken.sol.
```commandline
-p ./contracts/
-n YodaiToken.sol
--solv 0.8.17
--result_path ./results/
```


### Limitations ###
- Requires the related libraries or contracts in a single Solidity file. Here is a [tool](https://github.com/Qiping-Wei/funion) to help merge the scattered libraries or contracts together.

- The detailed contract data collected may be limited. However, you can get your own data as the AST nodes are provided at the contract level.
