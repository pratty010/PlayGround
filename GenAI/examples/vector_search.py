from langchain_community.llms import Ollama
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import os

# Set the LangChain tracing global paramater
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

# create a global instance of the LLM model of choice and set parameters
llm = Ollama(
    model = "mistral",
    num_gpu = 8,
    # format = "json",
    )

ollmaebd = OllamaEmbeddings(
    model="mistral",
)

# Test documents with page contents and metadata.
# The metadata attribute can capture information about the source of the document, its relationship to other documents, and other information. Note that an individual Document object often represents a chunk of a larger document.
test_documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]


def create_vectors():
    """
    This function creates a vector store from a list of documents using Ollama embeddings for the known model.
    Refer : https://python.langchain.com/v0.2/docs/tutorials/retrievers/#documents

    Parameters:
    None

    Returns:
    vectorstore : Chroma
        A vector store created from the test documents using Ollama embeddings.

    Raises:
    None

    Note:
    The function uses the Chroma vector store from the langchain_chroma library.
    The test_documents and ollmaebd are assumed to be defined in the global scope.
    """
    
    # Create a vector store from the test documents using Ollama embeddings
    vectorstore = Chroma.from_documents(
        test_documents,
        embedding=ollmaebd,
    )
    
    return vectorstore

def vector_search(vectorstore):
    """
    This function performs a vector search on a given vector store using the similarity_search method.
    LangChain VectorStore objects contain methods for adding text and Document objects to the store, and querying them using various similarity metrics. They are often initialized with embedding models, which determine how text data is translated to numeric vectors.
    Refer : https://python.langchain.com/v0.2/docs/tutorials/retrievers/#vector-stores

    Parameters:
    vectorstore (Chroma): A vector store created from a list of documents using Ollama embeddings.

    Returns:
    List[Document]: A list of documents that are most similar to the input query based on the vector store's similarity_search method.

    Note:
    This function demonstrates three different ways to perform a vector search using the Chroma vector store.
    - The first method uses the vector store's similarity_search method for the word "cat".
    - The second method uses the vector store's similarity_search_with_score method for the word "cat".
    - The third method returns documents based on similarity to a embedded query for the word "dogs".
    """

    # Create a retriever that uses the vector store's similarity_search method for the word "cat"
    retriever = vectorstore.similarity_search("cat")

    # Chroma here returns a distance metric that should vary inversely with similarity.
    # retriever = vectorstore.similarity_search_with_score("cat")

    # Return documents based on similarity to a embedded query
    emb = ollmaebd.embed_query("dogs")
    retriever = vectorstore.similarity_search_by_vector_with_relevance_scores(emb)

    # print(retriever)

    return retriever

 
def retriever_search(vectorstore):
    """
    This function demonstrates batch processing of queries using the RunnableLambda and vector store's similarity_search_with_score method.

    Parameters:
    vectorstore (Chroma): A vector store created from a list of documents using Ollama embeddings.

    Returns:
    None

    Note:
    This function creates a RunnableLambda object that wraps the vector store's similarity_search_with_score method.
    The RunnableLambda object is then bound to a single query ("cat") and a top result (k=1) is selected.
    The RunnableLambda object is then batched with another query ("shark").
    The results of the batch processing are printed to the console.
    """

    # RunnableLambda converts a python callable into a Runnable.
    # The wrapper is created around the vector store's similarity_search_with_score method.
    # retriever = RunnableLambda(vectorstore.similarity_search_with_score).bind(k=1)  # select top result

    # Vectorstores implement an as_retriever method that will generate a Retriever, specifically a VectorStoreRetriever. 
    # These retrievers include specific search_type and search_kwargs attributes that identify what methods of the underlying vector store to call, and how to parameterize them. 
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )

    # LangChain Retrievers are Runnables, so they implement a standard set of methods (e.g., synchronous and asynchronous invoke and batch operations) and are designed to be incorporated in LCEL chains.
    res = retriever.invoke(["cat", "shark"])

    # Print the results
    # print(res)

    return res


def prompt_ret_search(vectorstore):
    """
    This function demonstrates a Retrieval Augmented Generation (RAG) chain using a vector store and a language model.
    The function uses a retriever to find the most relevant document in the vector store based on a given question.
    The retrieved document is then used as context for a prompt that is passed to the language model.
    The language model generates an answer to the question based on the provided context.
    Refer : https://python.langchain.com/v0.2/docs/tutorials/retrievers/#retrievers

    Parameters:
    vectorstore (Chroma): A vector store created from a list of documents using Ollama embeddings.

    Returns:
    str: The generated answer to the question.

    Note:
    This function uses the LangChain library for building the RAG chain.
    The retriever is set to retrieve the top 1 most relevant document based on similarity.
    The ChatPromptTemplate is used to format the question and context for the language model.
    The RunnablePassthrough is used to pass the question directly to the language model.
    The rag_chain is then invoked with the question "tell me about cats".
    The generated answer is printed to the console.
    """

    # Create a template for the question and context.
    message = """
    Answer this question using the provided context only.

    {question}

    Context:
    {context}
    """
    message = """
    Answer this question using the provided context only.

    {question}

    Context:
    {context}
    """
    
     # Create a retriever that uses the vector store's similarity_search method with k=1
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )

    # Create a prompt template that includes a question and a context placeholder
    prompt = ChatPromptTemplate.from_messages([("human", message)])

    # Create a RAG chain by combining the retriever, prompt, and LLM
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

    # Invoke the RAG chain with the question "tell me about cats"
    response = rag_chain.invoke("tell me about cats")
    
    # Print the generated answer
    print(response)

    return response

def main():
    vectorstore = create_vectors()
    # res = vector_search(vectorstore)
    res = retriever_search(vectorstore)
    # res = prompt_ret_search(vectorstore)

    print(res)

if __name__ == "__main__":
    main()