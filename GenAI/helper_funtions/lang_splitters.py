from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings

import sys

sys.path.append("/home/ace/PlayGround/GenAI")

from helper_funtions import lang_loaders

embd = OllamaEmbeddings(
    model="llama3"
)

def char_splitter(data: list) -> list:
    """
    This function splits a given document into smaller chunks based on character separators.

    Parameters:
    data (Document): The document to be split. It should have a 'page_content' attribute.

    Returns:
    list: A list of smaller documents, each containing a chunk of the original document.
    """

    # Initialize the CharacterTextSplitter with specific parameters
    char_splitter = CharacterTextSplitter(
        separator="\n\n",  # The separator to split the document
        chunk_size=1000,  # The maximum size of each chunk
        chunk_overlap=400,  # The overlap between chunks
        length_function=len,  # The function to calculate the length of a chunk
        is_separator_regex=False,  # Whether the separator is a regular expression
    )

    # Use the create_documents method of the text_splitter to split the document
    # texts = char_splitter.create_documents(data[0].page_content)
    texts = char_splitter.split_documents(data)

    # Return the list of smaller documents
    return texts

def rec_char_splitter(data: list, language: str=None) -> list:
    """
    This function splits a given document into smaller chunks based on recursive character separators.

    Parameters:
    data (Document): The document to be split. It should have a 'page_content' attribute.
    language (str, optional): The language of the document. If not provided, a default set of separators will be used. Defaults to None.

    Returns:
    list: A list of smaller documents, each containing a chunk of the original document.

    Note:
    The supported languages are defined in the 'Language' enum from the 'langchain_text_splitters' module.
    """

    # Get the list of supported languages
    supported_langs = [e.value for e in Language]

    # Get the separators for the 'python' language
    supported_sep =  RecursiveCharacterTextSplitter.get_separators_for_language("python")

    # If no language is specified, use a default set of separators
    if language is None:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
            ],
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
    else:
        # If a language is specified, use the corresponding text splitter
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=500,
            chunk_overlap=100,
        )

    # Split the document into smaller chunks and return the list of smaller documents
    # texts = text_splitter.create_documents(data[0].page_content)
    texts = text_splitter.split_documents(data) 
    return texts

def md_splitter(data: list) -> list:
    """
    This function splits a Markdown document into smaller chunks based on specified headers.

    Parameters:
    data (list): A list containing a single Document object. The Document object should have a 'page_content' attribute.

    Returns:
    list: A list of smaller Document objects, each containing a chunk of the original document.

    Note:
    The function uses the MarkdownHeaderTextSplitter from the langchain_text_splitters module.
    It splits the document based on the specified headers ("#" and "##" by default).
    The 'strip_headers' parameter is set to False, so the headers are included in the chunks.
    The 'return_each_line' parameter is set to True, so each line of the document is considered for splitting.
    """
    
    # Define the headers to split the Markdown document on
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
    
    # Create an instance of MarkdownHeaderTextSplitter
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on,
        strip_headers=False,
        return_each_line=True,
    )
    
    # Split the Markdown document into smaller chunks
    docs = markdown_splitter.split_text(data[0].page_content)

    # Commented out code for chunking the split documents
    # chunk_size = 10
    # chunk_overlap = 1
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=chunk_size, chunk_overlap=chunk_overlap
    # )
    # chucked_docs = text_splitter.split_documents(docs)
    # return chucked_docs 

    # Return the list of smaller Document objects
    return docs 

def semantic_text_splitter(data: list) -> list:
    """
    This function splits a given document into smaller chunks based on semantic similarity.

    Parameters:
    data (list): A list containing a single Document object. The Document object should have a 'page_content' attribute.

    Returns:
    list: A list of smaller Document objects, each containing a chunk of the original document.

    Note:
    The function uses the SemanticChunker from the langchain_experimental.text_splitter module.
    It splits the document based on semantic similarity using the provided embeddings.
    The 'breakpoint_threshold_type' parameter is set to "standard_deviation". Can change it to other values as explained here - https://python.langchain.com/v0.2/docs/how_to/semantic-chunker/
    """

    # Create an instance of SemanticChunker
    text_splitter = SemanticChunker(
        embd,  # The embeddings to be used for semantic similarity calculation
        breakpoint_threshold_type="standard_deviation",  # The type of threshold to determine chunk breakpoints
    )

    # Split the document into smaller chunks based on semantic similarity
    docs = text_splitter.split_text(data[0].page_content)

    # Return the list of smaller Document objects
    return docs

def main():
    md_file_path = "/home/ace/PlayGround/GenAI/opt/test/Write_Up.md"
    pdf_file_path = "/home/ace/PlayGround/GenAI/opt/Alumni_Employment_Verification_Letter.pdf"
    py_file_path = "/home/ace/PlayGround/GenAI/fin_bot/yahoo_finance.py"
    url_paths = ["https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/", "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/"]
    
    fdata = lang_loaders.md_loader(md_file_path)
    print(fdata)

    data = char_splitter(fdata)
    # data = rec_char_splitter(fdata)
    # data = rec_char_splitter(fdata, "python")
    # data = rec_char_splitter(fdata, "markdown")
    # data = md_splitter(fdata)
    # data = semantic_text_splitter(fdata)

    print(len(data))


if __name__ == "__main__":
    main()