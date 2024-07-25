import logging

from app.smart_contract_generator.common import model

logger = logging.getLogger(__name__)


def smart_contract_classifier(description):
    prompt = f"""
    You are an expert in Solidity smart contracts. Based on the following description, classify the smart contract type and list all the necessary requirements in a well-formatted way:

    Description: {description}

    Please provide your response in the following format:

    Contract Type: <Type>
    Requirements:
    1. <Requirement 1>
    2. <Requirement 2>
    3. ...
    """
    response = model.invoke(prompt)

    return response.content
