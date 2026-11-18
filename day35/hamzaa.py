# print('hamza') #using the terminal cat <<< "print('hamza')" > hamzaa.py
# ollama pull bge-m3 
# pip install ollama 
# https://ollama.com/library/bge-m3
import ollama

response = ollama.embed(
    model='bge-m3',
    input='Told the stars',
)
# print(response)
# print(response.embeddings)
# print(response.embeddings[:4])
print(response.embeddings[0][:4])
