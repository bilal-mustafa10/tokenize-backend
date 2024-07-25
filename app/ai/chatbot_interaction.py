from langchain import (
OpenAIFunctionsAgent,)


def chatbot_interaction(user_query):
    chatbot = OpenAIFunctionsAgent()
    return chatbot.chat(user_query)
