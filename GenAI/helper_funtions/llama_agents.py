from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent, AgentRunner
from llama_index.core import Settings
import tiktoken

llm = Ollama(
    model="llama3",
    # request_timeout=120,
    # context_window=10,
    # json_mode=True,
)

# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def addition(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a + b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
addition_tool = FunctionTool.from_defaults(fn=addition)

# initialize ReAct agent
agent = AgentRunner.from_llm([multiply_tool, addition_tool], llm=llm, verbose=True)

agent.chat("What is 2123 +  215123")

