from app.gen_smart_contract.state import GraphState

flag = "do not reflect"


def decide_to_finish_update(state: GraphState):
    """
    Determines whether to finish the update

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]

    if error == "no":
        print("---DECISION: FINISH---")
        return "document"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        return "reflect"
