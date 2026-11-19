from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1"
)


# prompt = ChatPromptTemplate.from_template(
#     "You are a Python trainer. Explain {topic} "
#     "to a beginner with a simple example and strictly under 20 words."
# )

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional Python trainer. 
        Answer Python and computer science questions 
        in a beginner-friendly manner and strictly under 20 words"""
    ),
    (
        "user",
        "Explain {topic} with an example."
    )
])

chain = prompt | model #chain operator to build the connecetion between the prompt and the model
# The | operator connects the two components.
# chain.invoke()
# chain.batch()
# chain.stream
def give_topic(python_topic):
    for chunk in chain.stream({"topic": f"{python_topic}"}):
        a = print(chunk.content, end="")
    return a

# for chunk in chain.stream({"topic": "Python loops"}):
#     print(chunk.content, end="")

print("Enter the python topic\n")
a = input("")
response = give_topic(a)
print(response)