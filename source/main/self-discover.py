import os
from operator import itemgetter
from langchain_openai import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import uuid
from constants import SELF_DISCOVER_REASONING_MODULE



os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-09-01-preview"

def query_selfdiscover(task_example: str):
    """
    Queries the self-discovery prompt using the given task example.

    Args:
        task_example (str): The example of the task.

    Returns:
        str: The final answer obtained from the self-discovery prompt.
    """
    model = AzureChatOpenAI(
        deployment_name="gpt-4-turbo",
        model_name="gpt-4",
    )
    # SELECT relevant reasoning modules for the task.
    select_reasoning_modules = ChatPromptTemplate.from_template(
        "Given the task: {task_description}, which of the following reasoning modules are relevant? Do not elaborate on why.\n\n" + "\n".join(SELF_DISCOVER_REASONING_MODULE)
    )

    # ADAPT the selected reasoning modules to be more specific to the task.
    adapt_reasoning_modules = ChatPromptTemplate.from_template(
        "Without working out the full solution, adapt the following reasoning modules to be specific to our task:\n{selected_modules}\n\nOur task:\n{task_example}"
    )

    #  IMPLEMENT the adapted reasoning modules into an actionable reasoning structure.
    implement_reasoning_structure = ChatPromptTemplate.from_template(
        "Without working out the full solution, create an actionable reasoning structure for the task using these adapted reasoning modules:\n{adapted_modules}\n\nTask Description:\n{task_description}"
    )

    execute_reasoning_structure = ChatPromptTemplate.from_template(
        "Using the following reasoning structure: {reasoning_structure}\n\nSolve this task, providing your final answer: {task_example}"
    )

    select_chain = select_reasoning_modules | model | StrOutputParser()
    adapt_chain = adapt_reasoning_modules | model | StrOutputParser()
    implement_chain = implement_reasoning_structure | model | StrOutputParser()
    reasoning_chain = execute_reasoning_structure | model | StrOutputParser()

    overall_chain = (
        RunnablePassthrough.assign(selected_modules=select_chain)
        .assign(adapted_modules=adapt_chain)
        .assign(reasoning_structure=implement_chain)
        .assign(answer=reasoning_chain)
    )

    reasoning_modules_str = "\n".join(SELF_DISCOVER_REASONING_MODULE)
    return overall_chain.invoke(
        {"task_description": task_example, "task_example": task_example, "reasoning_modules": reasoning_modules_str}
    )
