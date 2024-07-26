from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List


class FunctionDescription(BaseModel):
    function_name: str = Field(..., description="The name of the function.")
    code: str = Field(..., description="The full Solidity code of the function.")
    description: str = Field(..., description="A general description of what the function does.")


class SmartContractClassifier(BaseModel):
    contract_type: str = Field(..., description="The type of the smart contract.")
    requirements: List[str] = Field(..., description="The list of requirements for the smart contract.")


class SmartContractCode(BaseModel):
    code: str = Field(..., description="The generated Solidity code for the smart contract.")


class SmartContractDetails(BaseModel):
    classifiers: SmartContractClassifier
    solidity_code: SmartContractCode
    function_descriptions: List[FunctionDescription]

    def dict(self, **kwargs):
        return {
            "classifiers": self.classifiers.dict(**kwargs),
            "solidity_code": self.solidity_code.dict(**kwargs),
            "function_descriptions": [fd.dict(**kwargs) for fd in self.function_descriptions]
        }
