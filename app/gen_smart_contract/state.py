from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error: Binary flag for control flow to indicate whether a test error was tripped.
        error_message: A detailed message describing the nature of the error if one occurred.
        prompt: The input or query that led to the current state of the graph.
        contract_type: Specifies the type of contract being referenced or generated.
        contract_requirements: A list of requirements or conditions that the contract must fulfill.
        documentation: The documentation or descriptive information related to the contract.
        contract: The actual contract content or code.
        compiler_version: The version of the compiler used to compile the contract.
        existing_contract: The content or code of an existing contract, if applicable.
    """

    error: str
    error_message: str

    prompt: str
    iterations: int
    contract_type: str
    contract_requirements: List[str]
    documentation: str
    contract: str
    compiler_version: str

    existing_contract: str
