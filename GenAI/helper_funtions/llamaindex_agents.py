from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent, AgentRunner


# define the llm model with appropriate parameters
llm = Ollama(
    model="gemma2",
    temperature=0.5,
    # num_workers=8,
    # request_timeout=120,
    json_mode=True,
)

# define sample Tool for the Agent to be utilized.
def addition(a: float, b: float) -> float:
    """Add two numbers and return the result"""
    return a + b

def subtraction(a: float, b: float) -> float:
    """Subtract second number from first number and return the result"""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result"""
    return a * b

def division(a: float, b: float) -> float:
    """Divide first number from second number and return the result"""
    return a / b


# Create the funtion to be called for each tool.
addition_tool = FunctionTool.from_defaults(fn=addition)
subtract_tool = FunctionTool.from_defaults(fn=subtraction)
multiply_tool = FunctionTool.from_defaults(fn=multiply)
division_tool = FunctionTool.from_defaults(fn=division)

# initialize ReAct agent
agent = ReActAgent.from_tools(
    tools = [addition_tool, subtract_tool, multiply_tool, division_tool],
    llm=llm,
    max_iterations=20,
    verbose=True
    )

# to get a view of the prompt that the agent uses for reasoning and reactions
prompt_dict = agent.get_prompts()
for k, v in prompt_dict.items():
    print(f"Prompt: {k}\n\nValue: {v.template}")

# Initiate the agent with a math problem to see BODMAS in action
res = agent.chat("What is (36/6)*3+4-3+5? Calculate step by step")
print(res)
