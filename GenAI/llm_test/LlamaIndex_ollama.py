from llama_index.llms.ollama import Ollama

def create_ollama_llm():
    """
    This function creates an instance of the Ollama LLM with specific configurations.

    Parameters:
    - model (str): The name of the LLM model to be used. Default is "llama3".
    - request_timeout (int): The maximum time in seconds to wait for a response from the LLM. Default is 360.
    - context_window (int): The number of previous tokens to include in the context. Default is not set.
    - json_mode (bool): Whether to use JSON mode for the LLM. Default is False.

    Returns:
    - llm (Ollama): An instance of the Ollama LLM with the specified configurations.
    """
    llm = Ollama(
        model="llama3",
        request_timeout=360,
        # context_window=10,
        # json_mode=True,
    )
    return llm


def ask_question():
    """
    This function asks a question using the Ollama LLM and returns the response.

    Parameters:
    - None

    Returns:
    - str: The response from the Ollama LLM to the question "What is AGI?".
    """
    # Create an instance of the Ollama LLM with specific configurations
    llm = create_ollama_llm()

    # Use the Ollama LLM to complete the question
    response = llm.complete("What is AGI?")

    # Return the response
    return response


# Example usage
forecast = ask_question()
print(forecast)