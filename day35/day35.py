from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from pydantic import BaseModel, Field

load_dotenv()


class PythonExplanation(BaseModel):
    title: str = Field(description="The topic title")
    explanation: str = Field(description="A beginner-friendly explanation")
    example: str = Field(description="A Python code example")

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
        in a, beginner-friendly manner and strictly under 20 words"""
    ),
    (
        "user",
        "Explain {topic} with an example. use this format {format_instructions}"
    )
])

# parser = StrOutputParser()
parser = PydanticOutputParser(pydantic_object=PythonExplanation)
# JsonOutputParser
# prompt = ChatPromptTemplate.from_template("""
# Explain {topic}.

# Return your answer as JSON with these keys:
# - title
# - explanation
# - example
# """)
chain = prompt | model | parser #chain operator to build the connecetion between the prompt and the model
# The | operator connects the two components.
# chain.invoke()
# chain.batch()
# chain.stream
def give_topic(python_topic):
    response = chain.invoke({"topic": f"{python_topic}",
                             "format_instructions": parser.get_format_instructions()
                            })
    return response

# for chunk in chain.stream({"topic": "Python loops"}):
#     print(chunk.content, end="")

print("Enter the python topic\n")
a = input("")
response = give_topic(a)
# print(response)
print(response.title)
print(response.explanation)
print(response.example)