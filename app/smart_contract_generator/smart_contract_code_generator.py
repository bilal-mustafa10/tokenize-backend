import json
import logging

from app.smart_contract_generator.common import model
from app.smart_contract_generator.schema import SmartContractClassifier, SmartContractCode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def smart_contract_code_generator(requirements: SmartContractClassifier) -> SmartContractCode:
    logger.info('Generating smart contract code')
    logger.info(f'Requirements: {requirements.requirements}')

    # Detailed prompt with best practices
    prompt = f"""
    You are an expert Solidity developer. Based on the following requirements, generate the corresponding Solidity smart contract code.
    Ensure the code is well-formatted, includes necessary comments for clarity, and adheres to the latest Solidity documentation standards.

    Follow these best practices while writing the smart contract:
    1. **Use the Latest Compiler Version**: Always specify the latest stable version of the Solidity compiler to avoid deprecated features and ensure the latest security updates.
    2. **License Identifier**: Include an SPDX license identifier at the top of the contract.
    3. **Visibility Specifiers**: Explicitly define the visibility of functions and state variables.
    4. **State Mutability**: Use the appropriate state mutability specifiers (`pure`, `view`, `payable`) for functions.
    5. **Error Handling**: Use `require`, `assert`, and `revert` for error handling.
    6. **Check Effects Interactions Pattern**: Ensure external calls are the last step in functions to prevent reentrancy attacks.
    7. **Avoid Magic Numbers**: Use constants or enums instead of magic numbers to improve readability.
    8. **Events for State Changes**: Emit events for critical state changes to facilitate tracking and auditing.
    9. **SafeMath for Arithmetic Operations**: Use the SafeMath library for arithmetic operations to prevent overflow and underflow.
    10. **Modifiers for Access Control**: Use function modifiers to enforce access control.

    Here is a template to follow:

    \\```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    import "@openzeppelin/contracts/utils/math/SafeMath.sol";

    contract <ContractName> {{
        using SafeMath for uint256;

        // State Variables
        <StateVariables>

        // Events
        <Events>

        // Modifiers
        <Modifiers>

        // Constructor
        constructor(<ConstructorParameters>) {{
            <ConstructorCode>
        }}

        // Public and External Functions
        <PublicExternalFunctions>

        // Internal Functions
        <InternalFunctions>

        // Private Functions
        <PrivateFunctions>

        // Fallback Function
        fallback() external payable {{
            <FallbackCode>
        }}

        // Receive Function
        receive() external payable {{
            <ReceiveCode>
        }}
    }}
    \\```

    Requirements: {requirements.requirements}

    Please provide your response in the following JSON format:
    {{
        "code": "solidity\\n// SPDX-License-Identifier: MIT\\npragma solidity ^0.8.0;\\n\\ncontract <ContractName> {{\\n    <GeneratedCode>\\n}}\\n"
    }}
"""

    response = model.invoke(prompt)
    content = response.content.strip()

    logger.info('Generated smart contract code')
    logger.debug(f'Content: {content}')

    try:
        # Log the raw response content for debugging
        logger.debug(f'Raw response content: {content}')

        # Attempt to parse the JSON response
        parsed_content = json.loads(content)

        logger.debug(f'Parsed content: {parsed_content}')

        code = parsed_content["code"]

        logger.info('Successfully parsed smart contract code')
        return SmartContractCode(code=code)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Raw response content: {content}")
        raise ValueError("Invalid JSON format in response") from e
    except KeyError as e:
        logger.error(f"Key error: {e}")
        logger.error(f"Parsed content: {parsed_content}")
        raise ValueError("Missing expected key in response JSON") from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
