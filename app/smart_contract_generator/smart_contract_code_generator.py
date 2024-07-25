from app.smart_contract_generator.common import model


def smart_contract_code_generator(requirements):
    prompt = f"""
    You are an expert Solidity developer. Based on the following requirements, generate the corresponding Solidity smart contract code. Make sure the code is well-formatted and includes necessary comments for clarity:

    Requirements: {requirements}

    Please provide your response in the following format:

    ```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract <ContractName> {{
        <GeneratedCode>
    }}
    ```
    """
    response = model.invoke(prompt)

    return response.content
