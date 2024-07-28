from langgraph.graph import END, StateGraph, START

from app.gen_smart_contract.edges.decide_to_finish_update import decide_to_finish_update
from app.gen_smart_contract.nodes.code_check import code_check
from app.gen_smart_contract.nodes.functions import functions
from app.gen_smart_contract.nodes.reflect import reflect
from app.gen_smart_contract.state import GraphState

update_workflow = StateGraph(GraphState)

# Define the nodes
update_workflow.add_node("functions", functions)  # functions
update_workflow.add_node("check_code", code_check)  # check code
update_workflow.add_node("reflect", reflect)  # reflect

# Build graph
update_workflow.add_edge(START, "reflect")
update_workflow.add_edge("reflect", "functions")
update_workflow.add_edge("functions", "check_code")
update_workflow.add_conditional_edges(
    "check_code",
    decide_to_finish_update,
    {
        "end": END,
        "reflect": "reflect",
    },
)

update_smart_contract_workflow = update_workflow.compile()