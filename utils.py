import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
import json



KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)


def run_slf(ns_id:str, slf_name:str,params:dict,env:str="sandbox"):

    api_key = os.getenv("SLF_OPENSTACK_DEMO01_API_KEY")
    url = f"https://demo01.iquall.net/demo01/api/v2/serverlessfunctions/namespace/{ns_id}/function/{slf_name}/env/{env}"
    print(url)
    headers = {
        "accept": "application/json",
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    payload = params

    cookie_name= os.getenv("DEMO01_COOKIE_NAME")
    cookie_value= os.getenv("DEMO01_COOKIE_VALUE")
    cookies = {
        cookie_name: cookie_value
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload, cookies=cookies)
    return response


def promt_chatgpt_single(client,prompt, model="gpt-4o-mini", max_tokens=1000,role_description:str="user"):
    messages=[
        {
            "role": role_description,
            "content": prompt,
        },
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        return response
    except Exception as e:
        return f"An error occurred: {e}"
    

def extract_json_to_dict(delimited_string):
    DELIM_CHAR = '**'
    # Find the start and end positions of the JSON string
    start_pos = delimited_string.find(DELIM_CHAR) + len(DELIM_CHAR)
    end_pos = delimited_string.rfind(DELIM_CHAR)
    
    # Extract the JSON string using the positions
    json_string = delimited_string[start_pos:end_pos]
    
    # Parse the JSON string into a dictionary
    return json.loads(json_string)
