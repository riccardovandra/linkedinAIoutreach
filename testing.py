#Caching Data

import json
import requests
import pandas as pd

def fetch_data(*, update: bool = False, json_cache: str, url: str):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache,'r') as f:
                json_data = json.load(f)
                print('Fetched data from Local Cache')
        except(FileExistsError,json.JSONDecodeError) as e:
            print(f'No local cache found...({e})')
            json_data = None

    if not json_data:
        print('Fetching new json data... (creating local cache)')
        json_data = requests.get(url).json()
        with open(json_data,'w') as f:
            json.dump(json_data,f)


    return json_data



# Get LinkedIn Data Function

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
        response_data = get_linkedIn_data(linkedin_url)

        headline = response_data['response']['headline']
        summary = response_data['response']['summary']
        experiences = response_data['response']['experiences']

        # Append this data to the DataFrame at the specific row
        df.loc[index, 'linkedin_headline'] = headline
        df.loc[index, 'linkedin_summary'] = summary
        df.loc[index, 'linkedin_experiences'] = str(experiences)  # Convert list to string for storage in a DataFrame cell

        


def get_linkedIn_data(url):
    json_cache = 'json_cache.json'
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api_key = 'XQ3SZMfXxGntNYO2hlsxRw'
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