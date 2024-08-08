import requests
from dotenv import load_dotenv
import os


KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)


api_key = os.getenv("SLF_OPENSTACK_DEMO01_API_KEY")
url = "https://demo01.iquall.net/demo01/api/v2/serverlessfunctions/namespace/7wk-g7p-t2i/function/create_instance/env/sandbox"
headers = {
    "accept": "application/json",
    "apikey": api_key,
    "Content-Type": "application/json"
}
payload = {"asas": "asas"}

cookie_name= os.getenv("DEMO01_COOKIE_NAME")
cookie_value= os.getenv("DEMO01_COOKIE_VALUE")
cookies = {
    cookie_name: cookie_value
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload, cookies=cookies)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())