import logging

from app.smart_contract_generator.langgraph_workflow import app
from app.smart_contract_generator.schema import SmartContractDetails, SmartContractClassifier, SmartContractCode, FunctionDescription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_smart_contract_logic(description: str) -> SmartContractDetails:
    """
    Generate the smart contract based on the description.

    Parameters
    ----------
    description : str
        The description of the smart contract.

    Returns
    -------
    SmartContractDetails
        The generated smart contract details.
    """
    logger.info(f"Generating smart contract for description: {description}")

    try:
        results = {}
        for output in app.stream(description):
            for key, value in output.items():
                results[key] = value
            print("\n---\n")

        # Ensure the values are converted to dictionaries if they are not already
        classifiers_data = results['classify_contract']
        solidity_code_data = results['generate_smart_contract_code']
        function_descriptions_data = results['describe_smart_contract_function']

        if isinstance(classifiers_data, SmartContractClassifier):
            classifiers_data = classifiers_data.dict()
        if isinstance(solidity_code_data, SmartContractCode):
            solidity_code_data = solidity_code_data.dict()
        if isinstance(function_descriptions_data, list):
            function_descriptions_data = [fd.dict() if isinstance(fd, FunctionDescription) else fd for fd in function_descriptions_data]

        # Convert the results to their respective schema objects
        classifiers = SmartContractClassifier(**classifiers_data)
        solidity_code = SmartContractCode(**solidity_code_data)
        function_descriptions = [FunctionDescription(**func) for func in function_descriptions_data]

        return SmartContractDetails(
            classifiers=classifiers,
            solidity_code=solidity_code,
            function_descriptions=function_descriptions
        )
    except Exception as e:
        logger.error(f"Error generating smart contract: {e}")
        raise
