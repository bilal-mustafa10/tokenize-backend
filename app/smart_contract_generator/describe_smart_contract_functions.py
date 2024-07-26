import logging
import json
from typing import List

from app.smart_contract_generator.common import model
from app.smart_contract_generator.schema import SmartContractCode, FunctionDescription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def describe_smart_contract_functions(solidity_code: SmartContractCode) -> List[FunctionDescription]:
    logger.info('Describing smart contract functions')


    prompt = f""" You are an expert Solidity developer. Based on the following Solidity smart contract code, for each function, provide the function name, the full code, and a general description of what the function does:

    Code:
    {solidity_code.code}

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
    response = model.invoke(prompt)
    content = response.content
    logger.info('Describing smart contract functions')

    try:
        # Parse the JSON response
        function_descriptions = [FunctionDescription(**func) for func in json.loads(content)]
        logger.info('Successfully describing smart contract functions')
        return function_descriptions
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError("Invalid response format") from e


