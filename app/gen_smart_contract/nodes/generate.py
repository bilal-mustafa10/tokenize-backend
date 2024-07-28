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
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]
    contract_type = state["contract_type"]

    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again to generate a code solution",
            )
        ]

    # Solution
    code_solution = code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages, "requirements": requirements}
    )
    messages += [
        (
            "assistant",
            f"{code_solution.contract}",
        )
    ]

    # Increment
    iterations = iterations + 1
    return {
        "contract": code_solution.contract,
        "contract_type": contract_type,
        "contract_requirements": requirements,
        "messages": messages,
        "iterations": iterations,
    }
