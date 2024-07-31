from langchain_core.prompts import ChatPromptTemplate

update_contract_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in Solidity smart contracts. \n Based on the following context, existing code, and user feedback, update the smart contract accordingly.  \n

Here is a full set of Solidity documentation:  
    \n ------- \n
    {context}  
    \n ------- \n

    Existing Contract
    \n ------- \n
    {existing_contract}
    \n ------- \n
    
    \n ------- \n
    User Feedback: {prompt}
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

    """,
        )
    ]
)
