# print('hamza') #using the terminal cat <<< "print('hamza')" > hamzaa.py
# ollama pull bge-m3 
# pip install ollama 
# https://ollama.com/library/bge-m3
import ollama

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

user_input = input("Enter the Input")
a = embeddings(user_input)
print("The output is\n")
print(a)

