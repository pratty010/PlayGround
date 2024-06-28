from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder, StringPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage, FunctionMessage, ChatMessage
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser

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

def zero_shot_prompt() -> str:
    """
    This function generates a zero-shot prompt using a ChatPromptTemplate.
    It uses the Ollama LLM model to generate a response based on the input topic.

    Parameters:
    None

    Returns:
    str: The generated response from the LLM model.

    Raises:
    None
    """

    # # String PromptTemplates
    # These prompt templates are used to format a single string, and generally are used for simpler inputs. 
    prompt = PromptTemplate.from_template(
        template="Tell me about this {topic}."
    )

    ## ChatPromptTemplates
    # These prompt templates are used to format a list of messages. These "templates" consist of a list of templates themselves.
    prompt = ChatPromptTemplate.from_messages(
        messages= ([
            ("human", "Tell me bout this {topic}."),
        ])
    )

    # print(prompt.input_variables)
    # print(prompt.messages)
    # print(prompt.pretty_print())

    # Create a chain of LLM model, PromptTemplate, and OutputParser
    chain = prompt | llm | StrOutputParser()

    # Invoke the chain with the input topic
    res = chain.invoke({
        "topic" : "AI",
        })

    return res

def one_shot_prompt() -> str:
    """
    This function generates one-shot prompts using ChatPromptTemplate.
    It uses the Ollama LLM model to generate a response based on the input parameters.

    Parameters:
    None

    Returns:
    str: The generated response from the LLM model.

    Raises:
    None
    """

    # Basic one-shot prompt as a System Message is set
    # This prompt sets a system message that specifies the output format.
    prompt_0 = ChatPromptTemplate.from_messages(
        messages= [
            SystemMessage(content="Please provide the answer in 2 paragraphs."),
            HumanMessage(content="Tell me about this AI."),
        ],
        template_format="mustache",
    )

    # Printing the input variables, messages, and a pretty-printed version of the prompt
    print(prompt_0.input_variables)
    print(prompt_0.messages)
    print(prompt_0.pretty_print())

    ## ChatPromptTemplates
    # These prompt templates are used to format a list of messages. These "templates" consist of a list of templates themselves.
    # This prompt template uses placeholders for the number of paragraphs and the topic.
    prompt_1 = ChatPromptTemplate.from_messages(
        messages= [
            ("system", "Please provide the answer in {para_num} paragraphs."),
            ("human", "Tell me bout this {topic}."),
        ],
    )

    # Formatting the prompt with specific values for the placeholders
    print(prompt_1.format_prompt(para_num = "2", topic = "AI"))

    # Invoking the prompt with specific values for the placeholders and getting the response from the LLM model
    print(prompt_1.invoke({
        "para_num" : 2,
        "topic" : "AI",
        }))

    # Printing the input variables, messages, and a pretty-printed version of the prompt
    print(prompt_1.input_variables)
    print(prompt_1.messages)
    print(prompt_1.pretty_print())


    # One-shot prompt for multiple messages placeholder.
    # This prompt template uses a placeholder for multiple messages.
    prompt_2 = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant"),
        # MessagesPlaceholder("msgs"),
        ("placeholder", "{msgs}"),
    ])

    # Invoking the prompt with specific messages and getting the response from the LLM model
    print(prompt_2.invoke({
        "msgs" : [("user", "Tell me about AI."), ("user", "Also, tell me about are you it?") ],
        }))

    # Printing the input variables, messages, and a pretty-printed version of the prompt
    print(prompt_2.input_variables)
    print(prompt_2.messages)
    print(prompt_2.pretty_print())


    # Create a chain of LLM model, PromptTemplate, and OutputParser
    # This chain takes the formatted prompt, passes it to the LLM model, and parses the output.
    chain = prompt_1 | llm | StrOutputParser()

    # Invoking the chain with specific values for the placeholders and getting the response from the LLM model
    res = chain.invoke({
        "para_num" : "2",
        "topic" : "AI",
    })

    # Printing the final response
    print(res)

    return res

def few_shot_prompt() -> str:
    """
    This function demonstrates the use of few-shot prompting with LangChain.
    It creates a few-shot prompt using a list of examples and a template.
    The prompt is then invoked with a new question, and the response is parsed.

    Returns:
    str: The final response from the LLM model.

    Raises:
    None
    """

    # Create a prompt for a Q/A using a PromptTemplate
    example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")

    # Examples to feed to the few shot prompt
    examples = [
        {
        "question": "Who lived longer, Muhammad Ali or Alan Turing?",
        "answer": """
        Are follow up questions needed here: Yes.
        Follow up: How old was Muhammad Ali when he died?
        Intermediate answer: Muhammad Ali was 74 years old when he died.
        Follow up: How old was Alan Turing when he died?
        Intermediate answer: Alan Turing was 41 years old when he died.
        So the final answer is: Muhammad Ali
        """,
        },
        {
        "question": "When was the founder of craigslist born?",
        "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who was the founder of craigslist?
        Intermediate answer: Craigslist was founded by Craig Newmark.
        Follow up: When was Craig Newmark born?
        Intermediate answer: Craig Newmark was born on December 6, 1952.
        So the final answer is: December 6, 1952
        """,
        },
        {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who was the mother of George Washington?
        Intermediate answer: The mother of George Washington was Mary Ball Washington.
        Follow up: Who was the father of Mary Ball Washington?
        Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
        So the final answer is: Joseph Ball
        """,
        },
        {
        "question": "Are both the directors of Jaws and Casino Royale from the same country?",
        "answer": """
        Are follow up questions needed here: Yes.
        Follow up: Who is the director of Jaws?
        Intermediate Answer: The director of Jaws is Steven Spielberg.
        Follow up: Where is Steven Spielberg from?
        Intermediate Answer: The United States.
        Follow up: Who is the director of Casino Royale?
        Intermediate Answer: The director of Casino Royale is Martin Campbell.
        Follow up: Where is Martin Campbell from?
        Intermediate Answer: New Zealand.
        So the final answer is: No
        """,
        }
    ]

    # Create a few shot prompt using the examples and the example prompt template.
    prompt  = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        input_variables=["input"],
        suffix="Question: {input}",
    )

    # Invoke the prompt with a new question
    print(
        prompt.invoke({"input": " When was the founder of craigslist born?"}).to_string()
    )

    # This chain takes the formatted prompt, passes it to the LLM model, and parses the output.
    chain = prompt | llm | StrOutputParser()

    # Invoking the chain with specific values for the placeholders and getting the response from the LLM model
    res = chain.invoke({
        "input": " When was the founder of craigslist born? Print where you found it?"
    })

    # Printing the final response
    # print(res)

    return res

def main():
    # res =  zero_shot_prompt()
    # res = one_shot_prompt()
    res = few_shot_prompt()

    print(res)


if __name__ == "__main__":
    main()
