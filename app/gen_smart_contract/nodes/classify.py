from app.gen_smart_contract.common import classify_contract_chain
from app.gen_smart_contract.state import GraphState


def classify(state: GraphState):
    """
    Classify smart contract

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---CLASSIFYING SMART CONTRACT---")

    # State
    prompt = state["prompt"]

    classify_contract = classify_contract_chain.invoke(
        {"prompt": prompt}
    )

    return {
        "contract_type": classify_contract.contract_type,
        "contract_requirements": classify_contract.requirements,
    }
