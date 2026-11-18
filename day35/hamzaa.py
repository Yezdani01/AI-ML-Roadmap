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
    result = response.embeddings[0]
    return result


def llm_response(request):
    response = chat(
        model='llama3:8b',
        messages=[  {
                'role': 'system',
                'content': 'You are a professional Python trainer. Answer only questions related to Python, programming languages and computer science.'
            },{
                'role': 'user', 'content': f'{request}'
                }
                ],
        format='json'
    )
    return response.message.content

while True:
    user_input = input("\nHi I am your Python Trainer,Enter the Input (or type 'q' to quit): ")

    if user_input.lower() in ["exit", "quit","q"]:
        break

    prompt = f"""Hey you are a professional python trainer for the freshers and this is the question asked by the student {user_input} the student is a fresher graduate and has basic knowledge, answer in a professional manner and return the answer in the json format strictly like this 
    {{"chat title": "A short 2-3 words of summary of the user's query",
    "answer":"if the question is about the pytohn then your detailed, begineer friendly explanation here",
    "an example":"if the question is about python then a small example to help the understanding"
    }}
    Follow these important instructions:
    1.donot answer anything unrelated to python, anything the user asks should be strictly related to the python, programming languages, and computer science only AND if the user asks something which is not related to one of these reply this "Ask related to python and computer science"
    2. if user greets , greet back and ask for the questions regarding python
    """

    a = llm_response(prompt)
    # embedding = embeddings(user_input)
    embedding = 'None for now'

    if a is not None:
        # start_index = a.find("{")
        # end_index = a.rfind("}") + 1
        # response = json.loads(a[start_index:end_index])
        response = json.loads(a)
        chunk_data = {
            "User_input":f"{user_input}",
            "LLM-Response":f"{response}",
            "Vector-embeddings":f"{embedding}"
        }
        # with open("/Users/hamzahamza/Desktop/Roadmap/day35/data.json","w") as json_file:
        #     json.dump(chunk_data,json_file,indent = 4)
        with open("/Users/hamzahamza/Desktop/Roadmap/day35/data.json", "a") as json_file:
            json_file.write(json.dumps(chunk_data) + "\n")
        with open("/Users/hamzahamza/Desktop/Roadmap/day35/response.txt","w",encoding='utf-8') as f:
            f.write(a)
        # print("The output is\n")
        print(response["answer"])
    else:
        print("No response was generated")

