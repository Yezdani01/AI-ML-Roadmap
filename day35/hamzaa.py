# print('hamza') #using the terminal cat <<< "print('hamza')" > hamzaa.py
# ollama pull bge-m3 
# pip install ollama 
# https://ollama.com/library/bge-m3
import ollama
from ollama import chat
import os
import json

def embeddings(text):
    response = ollama.embed(
        model='bge-m3',
        input=f"{text}",
    )
    # print(response)
    # print(response.embeddings)
    # print(response.embeddings[:4])
    # print(response.embeddings[0][:4])
    result = response.embeddings[0][:4]
    return result


def llm_response(request):
    response = chat(
        model='llama3:8b',
        messages=[{'role': 'user', 'content': f'{request}'}],
    )
    return response.message.content

while True:
    user_input = input("\nEnter the Input (or type 'q' to quit): ")

    if user_input.lower() in ["exit", "quit","q"]:
        break


    a = llm_response(user_input)
    embedding = embeddings(a)

    chunk_data = {
        "User_input":f"{user_input}",
        "LLM-Response":f"{a}",
        "Vector-embeddings":f"{embedding}"
    }


    if a is not None:
        with open("/Users/hamzahamza/Desktop/Roadmap/day35/data.json","w") as json_file:
            json.dump(chunk_data,json_file,indent = 4)
        with open("/Users/hamzahamza/Desktop/Roadmap/day35/response.txt","w",encoding='utf-8') as f:
            f.write(a)
        print("The output is\n")
        print(a)
    else:
        print("No response was generated")

