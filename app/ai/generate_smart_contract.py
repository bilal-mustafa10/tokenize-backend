import logging

from app.smart_contract_generator.langgraph_workflow import app
from app.smart_contract_generator.schema import SmartContractDetails

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_smart_contract_logic(description: str):
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
                print(f"Output from node '{key}':")
                print("---")
                print(value)
            print("\n---\n")

        return results
    except Exception as e:
        logger.error(f"Error generating smart contract: {e}")
        raise
