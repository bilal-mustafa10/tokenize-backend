from langgraph.graph import Graph

from app.smart_contract_generator.describe_smart_contract_functions import describe_smart_contract_functions
from app.smart_contract_generator.smart_contract_classifier import smart_contract_classifier
from app.smart_contract_generator.smart_contract_code_generator import smart_contract_code_generator

workflow = Graph()

workflow.add_node("classify_contract", smart_contract_classifier)
workflow.add_node("generate_smart_contract_code", smart_contract_code_generator)
workflow.add_node("describe_smart_contract_function", describe_smart_contract_functions)

workflow.add_edge('classify_contract', 'generate_smart_contract_code')
workflow.add_edge('generate_smart_contract_code', 'describe_smart_contract_function')

workflow.set_entry_point("classify_contract")
workflow.set_finish_point("describe_smart_contract_function")

app = workflow.compile()
