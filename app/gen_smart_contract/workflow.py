from langgraph.graph import END, StateGraph, START

from app.gen_smart_contract.edges.decide_to_finish import decide_to_finish
from app.gen_smart_contract.nodes.classify import classify
from app.gen_smart_contract.nodes.code_check import code_check
from app.gen_smart_contract.nodes.document import document
from app.gen_smart_contract.nodes.generate import generate
from app.gen_smart_contract.state import GraphState

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("classify", classify)
workflow.add_node("generate", generate)
workflow.add_node("check_code", code_check)
workflow.add_node("document", document)

# Build graph
workflow.add_edge(START, "classify")
workflow.add_edge("classify", "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "document": "document",
        "generate": "generate",
    },
)
workflow.add_edge("document", END)

smart_contract_generator = workflow.compile()
