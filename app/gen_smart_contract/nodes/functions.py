from typing import Dict, Any

from app.gen_smart_contract.common import code_functions_chain
from app.gen_smart_contract.state import GraphState


def functions(state: GraphState) -> Dict[str, Any]:
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE FUNCTIONS---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]
    contract = state["contract"]
    contract_type = state["contract_type"]
    requirements = state["contract_requirements"]

    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]
        # Solution
    code_functions = code_functions_chain.invoke(
        {"contract": contract, "messages": messages}
    )

    messages += [
        (
            "assistant",
            f"{code_functions}",
        )
    ]

    # Increment
    iterations = iterations + 1

    return {
        "contract": contract,
        "contract_type": contract_type,
        "contract_requirements": requirements,
        "messages": messages,
        "iterations": iterations,
        "contract_functions": code_functions.dict(),  # Ensure it's a dict
    }
