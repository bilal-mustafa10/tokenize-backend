from app.gen_smart_contract.common import code_gen_chain
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

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["contract"]
    error = state["error"]
    contract_type = state["contract_type"]
    requirements = state["contract_requirements"]
    contract_functions = state["contract_functions"]

    # Add reflection
    reflections = code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages, "requirements": requirements}
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"contract": code_solution, "messages": messages, "iterations": iterations}
