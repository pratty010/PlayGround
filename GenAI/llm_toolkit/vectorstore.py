from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor, LLMChainFilter, EmbeddingsFilter, DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter, EmbeddingsClusteringFilter
from langchain_text_splitters import CharacterTextSplitter

import sys
sys.path.append("/home/ace/PlayGround/GenAI/")

from llm_toolkit import langchain_loaders, langchain_splitters

# create a global instance of the LLM model of choice and set parameters
llm = Ollama(
    model = "llama3",
    # num_gpu = 30,
    # format = "json",
    )

# This is used to create embeddings using the Ollama model.
ollama_embed = OllamaEmbeddings(
    model="llama3",
    # num_gpu= 30,
)

def pretty_print_docs(docs):
    # Helper function for printing docs

    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

def create_chroma_vectors(documents: Document, vectordb_path:str = None) -> Chroma:
    """
    This function creates a Chroma vector store from a list of documents using Ollama embeddings.
    If a vectordb_path is provided, the vector store will be saved to the specified directory.

    Parameters:
    documents (List[Document]): A list of Document objects containing the text data and metadata.
    vectordb_path (str, optional): The path to save the vector store. If not provided, the vector store will not be saved.

    Returns:
    Chroma: A Chroma vector store created from the input documents.

    Note:
    If a vectordb_path is provided, the vector store will be saved to the specified directory.
    The function uses the Chroma.from_documents method to create the vector store.
    """

    # If no path is provided, create a Chroma vector store without saving it
    if vectordb_path is None:
        vectorstore = Chroma.from_documents(
            documents = documents,
            embedding = ollama_embed,
        )

        return vectorstore

    # If a path is provided, create a Chroma vector store and save it to the specified directory
    else:
        vectorstore = Chroma.from_documents(
            documents = documents,
            embedding = ollama_embed,
            persist_directory=vectordb_path
        )

        print(f"vectorstore saved to {vectordb_path}")
        return None

def create_FAISS_vectors(documents: Document, vectordb_path:str = None) -> FAISS:
    """
    This function creates a FAISS vector store from a list of documents using Ollama embeddings.
    If a vectordb_path is provided, the vector store will be saved to the specified directory.

    Parameters:
    documents (List[Document]): A list of Document objects containing the text data and metadata.
    vectordb_path (str, optional): The path to save the vector store. If not provided, the vector store will not be saved.

    Returns:
    FAISS: A FAISS vector store created from the input documents.

    Note:
    If a vectordb_path is provided, the vector store will be saved to the specified directory.
    The function uses the FAISS.from_documents method to create the vector store.
    """

    # Create a FAISS vector store from the documents using Ollama embeddings
    vectorstore = FAISS.from_documents(
        documents = documents,
        embedding = ollama_embed,
    )
      
    # If no path is provided, return the vector store
    if vectordb_path is None:
        return vectorstore
    # If a path is provided, save the vector store to the specified directory and print a success message
    else:
        vectorstore.save_local(vectordb_path)
        print(f"vectorstore saved to {vectordb_path}")
        return None
    
def ret_vectorstore(vectordb_path: str, store: str) -> Chroma | FAISS:
    """
    This function returns a vector store based on the specified store type.

    Parameters:
    vectordb_path (str): The path to the directory where the vector store will be saved or loaded.
    store (str): The type of vector store to return. It can be either "Chroma" or "FAISS".

    Returns:
    Chroma | FAISS: The vector store based on the specified store type.

    Note:
    If the store type is "Chroma", the function creates a Chroma vector store and returns it.
    If the store type is "FAISS", the function loads a FAISS vector store from the specified directory and returns it.
    If the store type is neither "Chroma" nor "FAISS", the function prints an error message and returns None.
    """
    # if vector store is Chroma
    if store in ["Chroma", "chroma"]:
        vectordb = Chroma(
            persist_directory=vectordb_path,
            embedding_function = ollama_embed,
        )
    # if vector store is FAISS
    elif store in ["FAISS", "faiss"]:
        vectordb = FAISS.load_local(
            folder_path = vectordb_path,
            embeddings = ollama_embed,
            allow_dangerous_deserialization=True
        )
    # if store type is neither Chroma nor FAISS
    else:
        print(f"{store} is not a valid store type")
        return None

    return vectordb

def get_retriever(vectordb: Chroma | FAISS):
    """
    This function creates a retriever object from a vector store.
    The retriever is used to perform search operations on the vector store.

    Parameters:
    vectordb (Chroma | FAISS): The vector store from which to create the retriever.
        This parameter can be either a Chroma or FAISS vector store.

    Returns:
    Retriever: A retriever object that can be used to perform search operations on the vector store.
        The retriever is configured with a search type of "mmr" (Maximum Marginal Relevance) and specific search_kwargs.

    Note:
    This function uses the as_retriever method of the vector store to create the retriever.
    The retriever is configured with a search type of "mmr" (Maximum Marginal Relevance) and specific search_kwargs.
    The search_kwargs include "k" (number of results to return) and "score_threshold" (minimum score for a result to be included).
    More Info: https://python.langchain.com/v0.2/docs/how_to/vectorstore_retriever/
    """

    # Create a retriever object from the vector store
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 2,
            "score_threshold": 0.5
        },
    )

    return retriever

def get_multiquery_retriever(vectordb: Chroma | FAISS):
    """
    This function creates a MultiQueryRetriever object from a vector store and an LLM.
    The MultiQueryRetriever is used to perform multi-query search operations on the vector store. This allows us to get better context given our keywords in query.

    Parameters:
    vectordb (Chroma | FAISS): The vector store from which to create the MultiQueryRetriever.
        This parameter can be either a Chroma or FAISS vector store.
    llm (LLM): The language model to use for query processing.

    Returns:
    MultiQueryRetriever: A MultiQueryRetriever object that can be used to perform multi-query search operations on the vector store.
        The MultiQueryRetriever is configured with the provided retriever and LLM.

    Note:
    This function uses the MultiQueryRetriever.from_llm method to create the MultiQueryRetriever.
    The MultiQueryRetriever is configured with the provided retriever and LLM.
    More Info: https://python.langchain.com/v0.2/docs/how_to/MultiQueryRetriever/
    """

    # create multi query retiever object for better semantic search.
    multi_retriever = MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(),
        llm = llm,
        )

    return multi_retriever

def context_compressed_retriever(retriever):
    """
    This function creates a ContextualCompressionRetriever object from a given retriever and an LLM.
    The ContextualCompressionRetriever is used to perform contextual compression on the retrieved results.
    Applies context constraints on the final answer to get more fruitful results by extracting only the context from results.

    Parameters:
    retriever (Retriever): The retriever object from which to create the ContextualCompressionRetriever.
        This parameter can be either a Chroma or FAISS retriever.

    Returns:
    ContextualCompressionRetriever: A ContextualCompressionRetriever object that can be used to perform contextual compression on the retrieved results.
        The ContextualCompressionRetriever is configured with the provided retriever and LLM.

    Note:
    This function uses the LLMChainExtractor.from_llm method to create an LLMChainExtractor. It will iterate over the initially returned documents and extract from each only the content that is relevant to the query.
    The LLMChainExtractor is used as the base compressor for the ContextualCompressionRetriever.
    The ContextualCompressionRetriever is configured with the provided retriever and LLMChainExtractor.
    More Info: https://python.langchain.com/v0.2/docs/how_to/ContextualCompressionRetriever/
    """
    
    # Create an LLMChainExtractor/LLMChainFilter/EmbeddingsFilter object from the LLM
    # compressor = LLMChainExtractor.from_llm(llm) 
    # compressor = LLMChainFilter.from_llm(llm) 
    # compressor = EmbeddingsFilter(embeddings=ollama_embed)

    # Create DocumentCompressorPipeline to easily combine multiple compressors in sequence
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separator=". ")
    # redundant_filter = EmbeddingsClusteringFilter(
    #     embeddings=ollama_embed,
    #     num_clusters=1,
    #     remove_duplicates=True
    #     ) 
    redundant_filter = EmbeddingsRedundantFilter(
        embeddings=ollama_embed,
        ) # used to filter out redundant documents based on embedding similarity between documents.
    relevant_filter = EmbeddingsFilter(embeddings=ollama_embed, similarity_threshold=0.5)
    compressor = DocumentCompressorPipeline(
        transformers=[splitter, redundant_filter, relevant_filter]
        )   

    # Create a ContextualCompressionRetriever object from the compressor and retriever
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=retriever,
    )

    return compression_retriever

def main():

    md_file_path = "/home/ace/PlayGround/GenAI/opt/test/Write_Up.md"
    pdf_file_path = "/home/ace/PlayGround/GenAI/opt/2021 FTE Onboarding Packet.pdf"
    vectordb_path = "/home/ace/PlayGround/GenAI/llm_toolkit/data/.vectordb"

    query = "When are H1-B lottery results released?"

    fdata = langchain_loaders.pdf_loader(pdf_file_path)
    # print(fdata[0].page_content)
    pages = langchain_splitters.char_splitter(fdata)
    # print(len(pages))

    # vectordb = create_chroma_vectors(pages)
    # create_chroma_vectors(pages, vectordb_path)
    # vectordb = create_FAISS_vectors(pages)
    create_FAISS_vectors(pages, vectordb_path)
    # print(type(vectordb))

    vectordb = ret_vectorstore(vectordb_path, "FAISS")

    # to do a similarity check to retrieve our query
    # docs = vectordb.similarity_search(query)
    # docs = vectordb.similarity_search_with_score(query)
    # docs = vectordb.similarity_search_with_relevance_scores(query)

    # print(docs)

    # retriever = get_retriever(vectordb)
    retriever = get_multiquery_retriever(vectordb)
    # # retriever = context_compressed_retriever( retriever)

    docs = retriever.invoke(query)
    pretty_print_docs(docs)

if __name__ == "__main__":
    main()


