from langchain_core.prompts import ChatPromptTemplate

code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in Solidity smart contracts. \n Based on the following requirements, generate a detailed and fully functional smart contract. \n

Here is a full set of Solidity documentation:  
    \n ------- \n
    {context}  
    \n ------- \n

    Requirements: {requirements}

    \n ------- \n

    User prompt: {prompt}
    
    \n ------- \n

    Now, generate a smart contract based on the provided requirements. The code should include:
    - SPDX-License-Identifier and pragma statements.
    - Necessary imports.
    - Contract definition and state variables.
    - Constructor function.
    - Functions to implement the required functionality.
    - Appropriate access control mechanisms.
    - Detailed comments explaining each part of the code.
    - Optimized for gas usage.
    - No imports from other Solidity files; this will be the only code.
    - Avoid current security vulnerabilities as stated in the documentation.

    Please provide your response in the following JSON format:

    {{
        "contract": "<Generated Solidity code>",
        "solVersion": "<Solidity version used>"
    }} 

    """,
        )
    ]
)
