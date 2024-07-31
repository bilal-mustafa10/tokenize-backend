from langchain_openai import ChatOpenAI

from app.gen_smart_contract.prompts.classify_contract_prompt import classify_contract_prompt
from app.gen_smart_contract.prompts.code_gen_prompt import code_gen_prompt
from app.gen_smart_contract.prompts.documentation_gen_prompt import documentation_gen_prompt
from app.gen_smart_contract.prompts.update_contract_prompt import update_contract_prompt
from app.gen_smart_contract.schema import classifyContractModel, generateContractModel, documentationGenerateModel

expt_llm = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0, model=expt_llm)

classify_contract_chain = classify_contract_prompt | llm.with_structured_output(classifyContractModel)
code_gen_chain = code_gen_prompt | llm.with_structured_output(generateContractModel)
code_update_chain = update_contract_prompt | llm.with_structured_output(generateContractModel)
documentation_gen_chain = documentation_gen_prompt | llm.with_structured_output(documentationGenerateModel)