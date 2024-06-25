from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3"
    
)  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

res = llm.invoke("Tell me a joke")

print(res)