# print('hamza') #using the terminal cat <<< "print('hamza')" > hamzaa.py
# ollama pull bge-m3 
# pip install ollama 
# https://ollama.com/library/bge-m3
from ollama import chat
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
def llm(text):
    model = ChatOllama(
        model="llama3:8b",
        temperature=0
    )

    response = model.invoke(text)

    print(response.content)

def do_embeddings(text):
    embeddings = OllamaEmbeddings(
        model="bge-m3"
    )

    vector = embeddings.embed_query(
        f"{text}"
    )

    print(vector)
# embed_query() converts a user query into a vector.
# embed_documents() converts a list of documents into vectors.

documents = [
    "Python is a programming language.",
    "FastAPI is a Python web framework."
]
embeddings = OllamaEmbeddings(
        model="bge-m3"
    )

vectors = embeddings.embed_documents(documents)

# print(len(vectors))