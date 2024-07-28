from langchain_core.prompts import ChatPromptTemplate

classify_contract_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",

            """You are an expert in Solidity smart contracts. Based on the following description, classify the smart contract type and list all the necessary requirements in a well-formatted way:

    Description: {messages}

    Please provide your response in the following JSON format:
    {{
        "contract_type": "<Type>",
        "requirements": [
            "<Requirement 1>",
            "<Requirement 2>",
            ...
        ]
    }}
    """
        ),
        ("placeholder", "{messages}"),
    ]
)