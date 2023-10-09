import streamlit as st
import os
from dotenv import set_key, find_dotenv


st.set_page_config(
    page_title= "AI Outreach Settings"
)

st.header("Add your API Keys here")

openai_key = st.text_input('OpenAI API Key')
proxycurl_key = st.text_input('LinkedIn Enricher API Key')

btn = st.button('Store Keys')

if btn:
    # Store API Keys for later retrieval
    set_key(find_dotenv(),'OPENAI_API_TOKEN',openai_key)
    set_key(find_dotenv(),'PROXYCURL_API',proxycurl_key)



