from app.gen_smart_contract.state import GraphState

flag = "do not reflect"


def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == 4:
        print("---DECISION: FINISH---")
        return "document"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        return "generate"
