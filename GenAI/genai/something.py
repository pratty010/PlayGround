from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.document_loaders import DirectoryLoader,TextLoader, CSVLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter,  RecursiveCharacterTextSplitter
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma

from time import time
import sys
sys.path.append("/home/ace/PlayGround/GenAI/")

from llm_toolkit import vectorstore
from 


# create a global instance of the LLM model of choice and set parameters
llm = Ollama(
    model = "llama3",
    num_gpu = 30,
    # format = "json",
    )

ollama_embd = OllamaEmbeddings(
    model="llama3",
)

store = LocalFileStore("/home/ace/PlayGround/GenAI/genai/data/.cache")

def main():
    dir_path = "/home/ace/PlayGround/GenAI/fin_bot/data/financials"
    data = vectorstore.dir_loader(dir_path, "**/*.csv", CSVLoader)
    # print(data[0])




if __name__ == "__main__":
    main()