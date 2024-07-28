from langchain_openai import ChatOpenAI

from app.gen_smart_contract.prompts.classify_contract_prompt import classify_contract_prompt
from app.gen_smart_contract.prompts.code_functions import code_functions
from app.gen_smart_contract.prompts.code_gen_prompt import code_gen_prompt
from app.gen_smart_contract.schema import classifyContractModel, generateContractModel, codeFunctionsModel

expt_llm = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0, model=expt_llm)

classify_contract_chain = classify_contract_prompt | llm.with_structured_output(classifyContractModel)
code_gen_chain = code_gen_prompt | llm.with_structured_output(generateContractModel)
code_functions_chain = code_functions | llm.with_structured_output(codeFunctionsModel)