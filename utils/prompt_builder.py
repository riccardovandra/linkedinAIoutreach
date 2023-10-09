from langchain import PromptTemplate

def get_prompt_template(template):
    prompt = PromptTemplate.from_template(template)
    return prompt