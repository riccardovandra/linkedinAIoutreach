from . import chains
from . import prompts
from . import prompt_builder

def process_chain(prompt_template,data=''):
    """
    Helper function to process a language learning model (LLM) chain with the given data.

    Args:
        prompt_template (str): The prompt template.
        data (str or dict): The data to input to the chain.

    Returns:
        str: The result of running the chain.
    """
    template = prompt_builder.get_prompt_template(prompt_template)
    chain = chains.initialize_llm_chain(template)
    return chains.run_llm_chain(chain, data)

def get_open_minded(linkedInData):
    open_minded = process_chain(prompts.why_open_minded,data=linkedInData)
    return open_minded

def get_op_first_line(open_minded):
    op_first_line = process_chain(prompts.open_minded_first_line,open_minded)
    return op_first_line