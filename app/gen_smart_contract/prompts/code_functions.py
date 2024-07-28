from langchain_core.prompts import ChatPromptTemplate

code_functions = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert Solidity developer. Based on the following Solidity smart contract code, for each function, provide the function name, the full code, and a general description of what the function does:

    Smart Contract:
    {contract}

    Please provide your response in the following JSON format:
    [
        {{
            "function_name": "<Name>",
            "code": "<Full Code>",
            "description": "<What the function does>"
        }},
        ...
    ]
            """
        ),
        ("placeholder", "{messages}"),
    ]
)