import solcx
from solcx import compile_source, install_solc
from app.gen_smart_contract.state import GraphState


def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error, and error details if any
    """

    print("---CHECKING CODE---")

    # State
    compiler_version = state["compiler_version"]
    contract = state["contract"]
    error_message = state["error_message"]

    # Compile Solidity code
    try:
        install_solc(compiler_version)

        compile_source(contract, solc_version=compiler_version)

        print("---COMPILED SOLIDITY OUTPUT---")
        print("---NO CODE TEST FAILURES---")
        error = "no"
        errors = ""

    except solcx.exceptions.SolcError as e:
        print("---CODE TEST FAILURES---")
        error = "yes"
        errors = f"SolcError: {e}"
    except Exception as e:
        print("---GENERAL ERROR DURING COMPILATION---")
        error = "yes"
        errors = f"Exception: {e}"

    if error == "yes":
        error_message = (
            "\n ----- \n"
            "\n The following compilation errors were detected in your Solidity code: \n"
            "\n ----- \n"
            f"{contract}\n"
            "\n ----- \n"
            f"{errors}\n"
            "\n ----- \n"
            "To resolve these issues, consider the following steps:\n"
            "1. GO THROUGH THE DOCUMENTATION OF SOLIDITY THAT HAS BEEN PROVIDED"
            "2. **Review the Solidity syntax and structure:** Ensure that your contract adheres to the correct Solidity syntax and structure. Common issues include missing semicolons, unmatched braces, and incorrect function definitions.\n"
            "3. **Check the compiler version:** Ensure that you are using the correct version of the Solidity compiler as specified in your code. Different versions may have different syntax and features.\n"
            "4. **Consult the Solidity documentation:** Look up the specific error codes and messages in the Solidity documentation. This can provide more context and examples of how to fix the issues.\n"
            "5. **Test incrementally:** Make small, incremental changes to your contract and recompile often. This can help you identify the exact changes that introduce errors.\n"
            "6. **Seek help from the community:** If you're stuck, consider reaching out to the Solidity community for help. Forums like Stack Exchange, GitHub, and the Solidity Gitter can be valuable resources.\n\n"
            "Once the errors are fixed, re-generate your code and try again."
        )

    return {
        "error": error,
        "error_message": error_message,
    }
