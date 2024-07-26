import logging
import json

from app.smart_contract_generator.common import model
from app.smart_contract_generator.schema import SmartContractClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def smart_contract_classifier(description: str) -> SmartContractClassifier:
    logger.info('Creating smart contract classifier...')

    prompt = f"""
    You are an expert in Solidity smart contracts. Based on the following description, classify the smart contract type and list all the necessary requirements in a well-formatted way:

    Description: {description}

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
    response = model.invoke(prompt)
    content = response.content
    logger.info('Successfully created smart contract classifier.')
    try:
        # Parse the JSON response
        parsed_content = json.loads(content)
        contract_type = parsed_content["contract_type"]
        requirements = parsed_content["requirements"]
        logger.info('Successfully created smart contract classifier.')

        return SmartContractClassifier(contract_type=contract_type, requirements=requirements)
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError("Invalid response format") from e

