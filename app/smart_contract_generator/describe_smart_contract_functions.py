import logging

from app.smart_contract_generator.common import model

logger = logging.getLogger(__name__)


def describe_smart_contract_functions(solidity_code):
    prompt = f""" You are an expert Solidity developer. Based on the following function from a Solidity smart 
    contract, for each of the function, provide the function name, the full code, and a general description of what 
    the function does:

    Code:
    ```
    {solidity_code}
    ```

    Please provide your response in the following format:

    Function Name: <Name>
    Code: <Full Code>
    Description: <What the function does>
    """
    response = model.invoke(prompt)
    return response.content



