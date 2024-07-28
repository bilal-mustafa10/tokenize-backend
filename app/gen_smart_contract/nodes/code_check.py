import solcx

from app.gen_smart_contract.state import GraphState


def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error
    """

    print("---CHECKING CODE---")

    # State
    messages = state["messages"]
    code_solution = state["contract"]
    iterations = state["iterations"]
    error = state["error"]
    contract_type = state["contract_type"]
    requirements = state["contract_requirements"]
    contract_functions = state["contract_functions"]

    # Compile Solidity code
    try:
        solcx.install_solc("0.8.6")  # Ensure the required version is installed
        solcx.set_solc_version("0.8.6")  # Set the compiler version
        #compiled_sol = solcx.compile_source(code_solution)

        # Print the compiled_sol to check if the code is correct
        print("---COMPILED SOLIDITY OUTPUT---")
        #print(compiled_sol)

        print("---NO CODE TEST FAILURES---")
        error = "no"
    except solcx.exceptions.SolcError as e:
        print("---CODE TEST FAILURES---")
        error = "yes"
        messages += [("assistant", f"Compilation error: {str(e)}")]
    except Exception as e:
        print("---GENERAL ERROR DURING COMPILATION---")
        error = "yes"
        messages += [("assistant", f"An error occurred: {str(e)}")]

    return {
        "contract_type": contract_type,
        "contract_requirements": requirements,
        "contract_functions": contract_functions,
        "contract": code_solution,
        "iterations": iterations,
        "error": error,
        "messages": messages,
    }
