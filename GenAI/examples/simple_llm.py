from langchain_community.llms import Ollama
# import ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from time import time


# Set the LangChain tracing global paramater
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

# create a global instance of the LLM model of choice and set parameters
llm = Ollama(
    model = "llama2",
    stream = True,
    num_gpu = 16,
    # format = "json",
    )

# client = ollama.Client(host='http://localhost:11434')

# Define the global parser for the data recieved from LLM to be parsed in human format.
parser = StrOutputParser()

# Create a list of messages for LLM
# It creates a list of messages, including a SystemMessage and two HumanMessage objects.
# The SystemMessage sets the context for the LLM, while the HumanMessage objects contain the input data.
messages = [
    SystemMessage(content="Tell me in detail about"),
    HumanMessage(content="Earth"),
    # SystemMessage(content="Now tell me about"),
    # HumanMessage(content="Earth"),
]

def simple():
    """
    This function demonstrates the usage of the LangChain library to interact with a language model (LLM).
    The function invokes the LLM with the messages and prints the result normally or in a desired parser.

    Parameters:
    messages : list
        A list of messages to be sent to the LLM. Each message is an instance of the `SystemMessage` or `HumanMessage` class.
        The `SystemMessage` sets the context for the LLM, while the `HumanMessage` objects contain the input data.

    Returns:
    res : str
        The result of the LLM invocation. The result is a string that contains the LLM's response to the input messages.
    parres : str
        The parsed result of the LLM invocation. The parsed result is a string that contains the LLM's response to the input messages in a desired format.
    """

    # Invoke the LLM with the list of messages
    res = llm.invoke(messages)
    # print(res)

    # Passing the result in a desired parser
    parres = parser.invoke(res)
    # print(parres)
    
    # return results
    return res
    # return parres


def chain():
    """
    This function demonstrates the chaining of operations using the LangChain library.
    It creates a chain where the output of the LLM instance is passed as input to the parser instance.

    Parameters:
    chain : str
        This parameter represents the chain of operations where the output of the LLM instance is passed as input to. The '|' operator represents the chaining of operations.

    Returns:
    chainres : str
        The parsed result of the LLM invocation. The parsed result is a string that contains the LLM's response to the input messages in a desired format.
    """

    chain = llm | parser

    # Invoke the chain with the list of messages
    chainres = chain.invoke(messages)
    print(chainres)

    return chainres


def prompt():
    """
    This function demonstrates the use of a ChatPromptTemplate to create a custom prompt, chaining it with an LLM and a parser.

    Parameters:
    system_template : str
        A string template that sets the system message for the prompt.
        It includes a placeholder for the target language.
    prompt_template : ChatPromptTemplate
        An instance of ChatPromptTemplate that combines the system message and user input.
    result : Message
        The result of invoking the prompt_template with specific parameters.
        It contains the translated text.
    chain : Chain
        A chain of operations that includes the prompt_template, LLM, and parser.

    Returns:
    promptres : str
        The parsed result of the LLM invocation.
        It contains the translated text in a desired format.
    """

    system_template = "Translate the following into {language}:"
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{text}")
            ]
        )

    # To check results for the prompt template generation
    result = prompt_template.invoke({"language": "italian", "text": "hi"})
    # print(result)
    # print(result.to_messages())

    # Create a chain of operations with the prompt_template, LLM, and parser
    chain = prompt_template | llm | parser
    promptres = chain.invoke({"language": "italian", "text": "hi"})
    # print(promptres)

    return promptres

def main():
    """
    The main function orchestrates the execution of different functions.
    """

    start_time = time()
    # Commented out calls to other functions for demonstration purposes
    res = simple()
    # res = chain()

    # Call to the prompt function
    # res = prompt()
    
    end_time = time()

    # Calculate the time taken to execute the simple function
    execution_time = end_time - start_time

    # Print the result and the execution time
    print(f"Result: {res}")
    print(f"Execution Time: {execution_time} seconds")


if __name__ == "__main__":
    main()