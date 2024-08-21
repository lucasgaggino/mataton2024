import json
import os
import requests

from openai import OpenAI
from dotenv import load_dotenv
import random

from tools.tools_functions import *

# Load the API key from the .env file

KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Load the tools from the JSON file
TOOLS_PATH = "./chatgpt/tools/cisco.json"
with open(TOOLS_PATH) as f:
    tools = json.load(f)

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
            "send_command": send_command,
            "end_chat": end_chat,
        }
        for tool_call in tool_calls:
            print(f"Function: {tool_call.function.name}")
            print(f"Params:{tool_call.function.arguments}")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name in available_functions:
                function_response = function_to_call(
                        command=function_args.get("command"),
                    )
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
    else:
        second_response = response
    return second_response

#DATOS PROVISIORIOS

if __name__ == "__main__":

    question = f"""Does this Cisco router have any issues? used the tools function to run the commands you think are necessary to diagnose the issue. 
    Add to the diagnosis the description of the interfaces with problems"""
    response = run_conversation(question,tools=tools)
    print(question)
    for chunk in response:
        print(chunk.choices[0].delta.content or "", end='', flush=True)


