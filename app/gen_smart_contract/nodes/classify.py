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
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]

    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again to classify a smart contract."
            )
        ]

    # Solution

    classify_contract = classify_contract_chain.invoke(
        {"messages": messages}
    )

    messages += [
        (
            "assistant",
            f"{classify_contract.contract_type} \n Requirements: {classify_contract.requirements}",
        )
    ]

    # Increment
    iterations = iterations + 1
    return {
        "contract_type": classify_contract.contract_type,
        "contract_requirements": classify_contract.requirements,
        "messages": messages,
        "iterations": iterations,
    }
