from langchain_core.pydantic_v1 import BaseModel, Field


class classifyContractModel(BaseModel):
    contract_type: str = Field(description="Type of smart contract")
    requirements: list[str] = Field(description="List of requirements")


class generateContractModel(BaseModel):
    contract: str = Field(description="Generated smart contract")
    solVersion: str = Field(description="Solidity Compiler Version")


class documentationGenerateModel(BaseModel):
    documentation: str = Field(description="Formatted documentation of the smart contract")


class functionModel(BaseModel):
    function_name: str = Field(description="Name of the function")
    code: str = Field(description="Full code of the function")
    description: str = Field(description="Description of the function")
