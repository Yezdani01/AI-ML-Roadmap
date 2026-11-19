from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3:8b",
    temperature=2
)

prompt = ChatPromptTemplate.from_template(
    "You are a Python trainer. Explain {topic} "
    "to a beginner with a simple example and strictly under 20 words."
)

chain = prompt | model #chain operator to build the connecetion between the prompt and the model
# The | operator connects the two components.

def give_topic(python_topic):
    response = chain.invoke({
        "topic": "{python_top}"
    })
    return response

print("Enter the python topic\n")
a = input("")
response = give_topic(a)
print(response.content)