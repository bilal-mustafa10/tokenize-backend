from langchain_core.prompts import ChatPromptTemplate

classify_contract_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in Solidity smart contracts. Based on the following description, classify the smart contract type and provide a comprehensive list of all the necessary requirements. Ensure that the requirements are detailed enough to allow for the generation of a well-crafted smart contract code.


    User prompt: {prompt}
    
    \n ------- \n


    Please provide your response in the following JSON format:
    {{
        "contract_type": "<Type>",
        "requirements": [
            "<Requirement 1>",
            "<Requirement 2>",
            ...
        ]
    }}
    
    \n ------- \n

    Each requirement should include:
    - A clear description of the functionality.
    - Any specific data structures or variables needed.
    - Details on access control and permissions.
    - Events that should be emitted.
    - Any relevant conditions or constraints.
    - Example of expected behavior or usage.
    """
        )
    ]
)
