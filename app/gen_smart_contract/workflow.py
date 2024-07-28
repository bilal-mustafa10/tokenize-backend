from langgraph.graph import END, StateGraph, START

from app.gen_smart_contract.edges.decide_to_finish import decide_to_finish
from app.gen_smart_contract.nodes.classify import classify
from app.gen_smart_contract.nodes.code_check import code_check
from app.gen_smart_contract.nodes.functions import functions
from app.gen_smart_contract.nodes.generate import generate
from app.gen_smart_contract.nodes.reflect import reflect
from app.gen_smart_contract.state import GraphState

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("classify", classify)  # classify smart contract
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("functions", functions)  # functions
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "classify")
workflow.add_edge("classify", "generate")
workflow.add_edge("generate", "functions")
workflow.add_edge("functions", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
#app = workflow.compile(checkpointer=memory, interrupt_before=["end"])
smart_contract_generator = workflow.compile()