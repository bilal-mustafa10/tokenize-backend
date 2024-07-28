from app.gen_smart_contract.state import GraphState

max_iterations = 3
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
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        return "reflect"
