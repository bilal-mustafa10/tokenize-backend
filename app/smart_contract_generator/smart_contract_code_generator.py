import json
import logging

from app.smart_contract_generator.common import model
from app.smart_contract_generator.schema import SmartContractClassifier, SmartContractCode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def smart_contract_code_generator(requirements: SmartContractClassifier) -> SmartContractCode:
    logger.info('Generating smart contract code')
    logger.info(f'Requirements: {requirements.requirements}')

    prompt = f"""
    You are an expert Solidity developer. Based on the following requirements, generate the corresponding Solidity smart contract code. Make sure the code is well-formatted and includes necessary comments for clarity:

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
