from langchain_community.llms import Ollama
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache

import os

# Set global langsmith env variables
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY'] = "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"
os.environ['LANGCHAIN_PROJECT'] = "TestLLM"


def in_memory_cache():
    cache = InMemoryCache()

    # create a global instance of the LLM model of choice and set parameters
    llm = Ollama(
        model = "llama3",
        # num_gpu = 32,
        # format = "json",
        )

    set_llm_cache(InMemoryCache())

    # invoke a one shot prompt
    res1 = llm.invoke("Tell me a joke")
    print(res1)
    res2 = llm.invoke("Tell me another joke")
    print(res2)


def main():
    in_memory_cache()

if __name__ == "__main__":
    main()