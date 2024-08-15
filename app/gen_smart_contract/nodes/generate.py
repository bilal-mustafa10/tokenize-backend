from app.gen_smart_contract.common import code_gen_chain
from app.gen_smart_contract.load_data import concatenated_content
from app.gen_smart_contract.state import GraphState


def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    requirements = state["contract_requirements"]
    contract_type = state["contract_type"]
    prompt = state["prompt"]
    error = state["error"]
    error_message = state["error_message"]
    iterations = state["iterations"]

    if error == "yes":
        print("---REGENERATING CODE SOLUTION---")
        prompt += error_message

    # Solution
    code_solution = code_gen_chain.invoke(
        {"context": concatenated_content, "prompt": prompt, "requirements": requirements}
    )

    iterations += 1

    return {
        "contract": code_solution.contract,
        "compiler_version": code_solution.solVersion,
        "contract_type": contract_type,
        "contract_requirements": requirements,
        "iterations": iterations,
    }
