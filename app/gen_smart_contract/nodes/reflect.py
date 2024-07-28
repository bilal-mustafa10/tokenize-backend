from app.gen_smart_contract.common import code_update_chain
from app.gen_smart_contract.load_data import concatenated_content
from app.gen_smart_contract.state import GraphState


def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---UPDATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    existing_contract = state["existing_contract"]
    error = state["error"]

    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again to classify a smart contract."
            )
        ]

    updated_code = code_update_chain.invoke(
        {"context": concatenated_content, "messages": messages, "existing_contract": existing_contract}
    )

    messages += [
        (
            "assistant",
            f"{updated_code.contract}",
        )
    ]
    iterations = iterations + 1
    return {
        "contract": updated_code.contract,
        "messages": messages,
        "iterations": iterations,
    }
