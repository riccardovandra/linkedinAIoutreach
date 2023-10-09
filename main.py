import streamlit as st
import pandas as pd
from utils import workflow
import requests
import json
import os


st.set_page_config(
    page_title= "Show my leads"
)

#Read Leads - Section #1
def read_leads():
    st.title("AI for Outbound")
    uploaded_file = st.file_uploader(
        label="Upload your lead list here in csv format",
        type=["csv"]
    )

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        data = st.dataframe(dataframe)
        if st.button(label="Get LinkedIn Data"):
            data.empty()
            get_linkedIn(dataframe)
        if st.button(label="Generate LinkedIn First Lines"):
            return


#Get LinkedIn Data

def get_linkedIn(df):
    # 1. Search for the column containing LinkedIn URLs
    linkedin_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains("http://www.linkedin.com/in/").any():
            linkedin_col = col
            break

    # 2. If column not found, return an error message
    if linkedin_col is None:
        return "Error: No column with LinkedIn URLs found."
    

    #Iterate through the value and get the LinkedIn Information
    for index, row in df.iterrows():
        linkedin_url = row[linkedin_col]
        response_data = get_linkedIn_data(linkedin_url) # API Call
        open_minded = workflow.get_open_minded(linkedInData=str(response_data))
        open_minded_fl = workflow.get_op_first_line(open_minded)

        headline = response_data['headline']
        summary = response_data['summary']
        experiences = response_data['experiences']

        # Append this data to the DataFrame at the specific row
        df.loc[index, 'linkedin_headline'] = headline
        df.loc[index, 'linkedin_summary'] = summary
        df.loc[index, 'linkedin_experiences'] = str(experiences)  # Convert list to string for storage in a DataFrame cell
        df.loc[index, 'Why Open Minded'] = open_minded
        df.loc[index, 'Open Minded First Line'] = open_minded_fl

    finalized_csv = st.dataframe(df)

    # @st.cache
    # def convert_csv(_df):
    #     return df.to_csv(index=False).encode('utf-8')
    
    # st.write("Open Minded First Line Personalization Was Added to 5 Leads")

    # st.download_button(
    #     label="Press to download leads",
    #     data=convert_csv(finalized_csv),
    #     file_name='leads_modifed.csv',
    #     mime='text/csv',
    #     )

def get_linkedIn_data(url):
    json_cache = 'json_cache.json'
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api_key = os.getenv('PROXYCURL_API')
    header_dic = {'Authorization': 'Bearer ' + api_key}
    params = {
        'linkedin_profile_url': url,
        'use_cache': 'if-present',
    }

    ## Try to fetch data from local cache
    try:
        with open(json_cache, 'r') as f:
            cached_data = json.load(f)
            for entry in cached_data:
                if entry['linkedin_url'] == url:
                    print('Fetched data from Local Cache')
                    return entry['response']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'No local cache found...({e})')
        cached_data = []
    
    # If data not found in cache, make an API call
    print('Fetching new json data... (updating local cache)')
    response = requests.get(api_endpoint,
                        params=params,
                        headers=header_dic)
    
    new_data = {
        'linkedin_url': url,
        'response': response.json()
    }
    cached_data.append(new_data)
    
    # Update the local cache with new data
    with open(json_cache, 'w') as f:
        json.dump(cached_data, f,  indent=4)
    
    return new_data['response']

read_leads()



