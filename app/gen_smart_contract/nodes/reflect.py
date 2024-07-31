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
    existing_contract = state["existing_contract"]
    prompt = state["prompt"]
    error = state["error"]
    error_message = state["error_message"]

    if error == "yes":
        print("---REGENERATING CODE SOLUTION---")
        prompt += error_message

    updated_code = code_update_chain.invoke(
        {"context": concatenated_content, "prompt": prompt, "existing_contract": existing_contract}
    )

    return {
        "contract": updated_code.contract,
        "compiler_version": updated_code.solVersion,
    }
