from langchain_community.document_loaders import CSVLoader, DirectoryLoader, TextLoader, BSHTMLLoader,  UnstructuredMarkdownLoader, PyMuPDFLoader, PyPDFLoader, PythonLoader
from langchain_core.documents import Document

import requests
import tempfile
import os

def text_loader(file_path: str) -> list:
    """
    This function loads text data from a specified file path into a list of Document objects.

    Parameters:
    file_path (str): The path to the text file to be loaded.

    Returns:
    list: A list of Document objects, where each Document represents a line in the text file.

    Raises:
    AssertionError: If the loaded data does not contain at least one Document object.

    Note:
    This function uses the TextLoader class from the langchain_community.document_loaders module.
    It automatically detects the encoding of the text file.
    """

    # Create an instance of TextLoader with the specified file path and autodetect encoding
    loader = TextLoader(
        file_path = file_path,
        autodetect_encoding=True,
    )

    # Load data from the text file
    data = loader.load()

    # Assert that the loaded data contains at least one Document object
    assert isinstance(data[0], Document)

    return data

def csv_loader(file_path: str, csv_args: dict = {
            "delimiter": ",",
            "quotechar": '"',
        }) -> list:
    """
    This function loads data from a CSV file into a list of dictionaries.

    Parameters:
    file_path (str): The path to the CSV file.
    csv_args (dict, optional): Additional arguments for the CSV reader. Defaults to {
        "delimiter": ",",
        "quotechar": '"'
    }.

    Returns:
    list: A list of dictionaries, where each dictionary represents a row in the CSV file.

    Raises:
    FileNotFoundError: If the file at the specified path does not exist.
    """
    
    # create instance of a CSV loader
    loader = CSVLoader(
        file_path = file_path,
        csv_args= csv_args,
        # source_column = "Total Revenue",
    )

    # load data from CSV
    data = loader.load()

    # Assert that the loaded data contains Document object
    # assert len(data) == <check condition>
    assert isinstance(data[0], Document)

    return data

def htmlbs4_loader(url_paths: list) -> list:
    """
    This function loads data from HTML pages using BeautifulSoup4 and saves them as temporary HTML files.
    Then, it loads these temporary HTML files into a list of Document objects using the BSHTMLLoader.

    Parameters:
    url_paths (list): A list of URLs from which to load HTML data.

    Returns:
    list: A list of Document objects, each representing an HTML page.

    Raises:
    None
    """

    # Create a temporary directory to store the downloaded HTML files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f'Temporary directory created: {temp_dir}')

        counter = 0
        # Download HTML data from each URL and save it as a temporary HTML file
        for url in url_paths:   
            res = requests.get(url)
            print(res.text)
            file_path = os.path.join(temp_dir, str(counter) + ".html")
            print(file_path)
            with open(file_path, "w") as f:
                f.write(res.text)
                counter += 1

        # Get a list of the temporary HTML files
        files = os.listdir(temp_dir)

        data = []
        # Load each temporary HTML file into a Document object using the BSHTMLLoader
        for file in files:
            loader = BSHTMLLoader(
                file_path=temp_dir + "/" + file,
            )

            url_data = loader.load()

            # Assert that the loaded data contains Document object
            # assert len(data) == <check condition>
            assert isinstance(url_data[0], Document)

            data.append(url_data)

    return data

def md_loader(file_path: str) -> list:
    """
    This function loads data from a Markdown file using UnstructuredMarkdownLoader.
    It then asserts that the loaded data contains exactly one Document object.

    Parameters:
    file_path (str): The path to the Markdown file.

    Returns:
    list: A list containing the loaded Document object.

    Raises:
    AssertionError: If the loaded data does not contain exactly one Document object.
    """

    # Create an instance of UnstructuredMarkdownLoader with the specified file path
    loader = UnstructuredMarkdownLoader(
        file_path=file_path,
    )

    # Load data from the Markdown file
    data = loader.load()

    # Assert that the loaded data contains exactly one Document object
    assert len(data) == 1
    assert isinstance(data[0], Document)

    # Return the loaded data
    return data

def pdf_loader(file_path: str) -> list:
    """
    This function loads data from a PDF file using PyMuPDFLoader.
    It then returns a list of Document objects, each representing a page in the PDF.

    Parameters:
    file_path (str): The path to the PDF file.

    Returns:
    list: A list of Document objects, each representing a page in the PDF.

    Raises:
    None

    Note:
    PyMuPDFLoader is used instead of PyPDFLoader because PyMuPDFLoader is more efficient and supports more features.
    """

    # loader = PyPDFLoader(
    #     file_path=file_path,
    # )

    loader = PyMuPDFLoader(
        file_path=file_path,
    )

    # Load data from the PDF file
    pages = loader.load()

    # Assert that the loaded data contains Document object
    # assert len(pages) == 1
    assert isinstance(pages[0], Document)

    # Return the loaded data
    return pages

def python_loader(file_path: str) -> list:
    """
    This function loads data from a Python (.py) file using PythonLoader.
    It then returns a list of Document objects, each representing a line in the Python file.

    Parameters:
    file_path (str): The path to the Python (.py) file.

    Returns:
    list: A list of Document objects, each representing a line in the Python file.

    Raises:
    None

    Note:
    The PythonLoader reads the file line by line and creates a Document object for each line.
    The page_content of each Document object is the content of the corresponding line in the Python file.
    """

    # Create an instance of PythonLoader with the specified file path
    loader = PythonLoader(file_path)

    # Load data from the Python file
    data = loader.load()

    # Assert that the loaded data contains exactly one Document object per line
    assert len(data) == 1
    assert isinstance(data[0], Document)

    # Return the loaded data
    return data

def dir_loader(dir_path: str, glob: str="**/*.md", loader_cls=TextLoader) -> list:
    """
    This function loads data from a directory using the specified loader class.

    Parameters:
    dir_path (str): The path to the directory to load data from.
    glob (str, optional): A glob pattern to filter files. Defaults to "**/*.md".
    loader_cls (class, optional): The class to use for loading data. Defaults to TextLoader.

    Returns:
    list: A list of Document objects, each representing a file in the directory.

    Note:
    The loader_cls should be a subclass of langchain_community.document_loaders.DocumentLoader.
    """

    # Initialize the DirectoryLoader with the specified parameters
    loader = DirectoryLoader(
        dir_path,
        glob=glob,
        show_progress=True,
        use_multithreading=True,
        loader_cls=loader_cls, 
        silent_errors=True,
    )

    # Load data from the directory
    docs = loader.load()

    # Print the content of the first loaded document for debugging purposes
    # print(docs[0].page_content)

    # Return the loaded documents
    return docs

def main():
    csv_file_path = "/home/ace/PlayGround/GenAI/fin_bot/data/financials/income_statements/income_stmt_annually_AAPL.csv"
    md_file_path = "/home/ace/PlayGround/GenAI/opt/test/Write_Up.md"
    pdf_file_path = "/home/ace/PlayGround/GenAI/opt/Alumni_Employment_Verification_Letter.pdf"
    py_file_path = "/home/ace/PlayGround/GenAI/fin_bot/yahoo_finance.py"
    dir_path = "/home/ace/PlayGround/GenAI/fin_bot/data/financials/income_statements"
    url_paths = ["https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/", "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/"]
    
    data = text_loader(md_file_path)
    # data = csv_loader(csv_file_path, {})
    # data = dir_loader(dir_path, "**/*.csv", CSVLoader)
    # data = htmlbs4_loader(url_paths)
    # data = md_loader(md_file_path)
    # data = pdf_loader(pdf_file_path)
    # data = python_loader(py_file_path)

    print(data)

if __name__ == "__main__":
    main()