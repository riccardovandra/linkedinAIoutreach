from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from . import prompt_builder
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

openai_key = os.getenv("OPENAI_API_KEY")

def initialize_llm_chain(prompt_template):
    chain = LLMChain(llm=ChatOpenAI(openai_api_key=openai_key,model='gpt-3.5-turbo-16k'),prompt=prompt_template)
    return chain

def run_llm_chain(chain,input_variable):
    result = chain.run(input_variable)
    return result