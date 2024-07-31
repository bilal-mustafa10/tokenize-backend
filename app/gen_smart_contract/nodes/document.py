from typing import Dict, Any

from app.gen_smart_contract.common import documentation_gen_chain
from app.gen_smart_contract.state import GraphState


def document(state: GraphState) -> Dict[str, Any]:
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE DOCUMENTATION---")

    # State
    contract = state["contract"]
    compiler_version = state["compiler_version"]
    contract_type = state["contract_type"]
    requirements = state["contract_requirements"]

    documentation = documentation_gen_chain.invoke({
        "contract": contract
    })

    return {
        "contract": contract,
        "contract_type": contract_type,
        "contract_requirements": requirements,
        "documentation": documentation.documentation,
        "compiler_version": compiler_version
    }
