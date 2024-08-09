import json
import os
import requests

from openai import OpenAI
from dotenv import load_dotenv
import random

from tools.tools_functions import get_pc_data

# Load the API key from the .env file

KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Load the tools from the JSON file
TOOLS_PATH = "./chatgpt/tools/random.json"
with open(TOOLS_PATH) as f:
    tools = json.load(f)

def get_current_weather(latitude, longitude):
    """Get the current weather in a given latitude and longitude"""
    response_sim = {
        "latitude": latitude,
        "longitude": longitude,
        "temperature":random.randint(0, 40), 
        "humidity":random.randint(0, 100),
        "pressure":random.randint(0, 1020),
        "rain_chance":random.randint(0, 60)}

    return json.dumps(response_sim)

def run_conversation(content,tools=None):
    messages = [{"role": "user", "content": content}]
    tools = tools
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)

        available_functions = {
            "get_current_weather": get_current_weather,
            "get_pc_data": get_pc_data,
        }
        for tool_call in tool_calls:
            print(f"Function: {tool_call.function.name}")
            print(f"Params:{tool_call.function.arguments}")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name == "get_current_weather":
                function_response = function_to_call(
                    latitude=function_args.get("latitude"),
                    longitude=function_args.get("longitude"),
                    )
            elif function_name == "get_pc_data":
                function_response = function_to_call()
            print(f"API: {function_response}")
            messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
            )

        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
    return second_response

if __name__ == "__main__":
    question = "Should i wear a winter jacket in Buenos Aires today?"
    #question= "What's my pc total memory ?"
    response = run_conversation(question,tools=tools)
    print(question)
    for chunk in response:
        print(chunk.choices[0].delta.content or "", end='', flush=True)


