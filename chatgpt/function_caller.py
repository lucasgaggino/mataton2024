import json
import os
import requests

from openai import OpenAI
from dotenv import load_dotenv
import random

from tools.tools_functions import get_pc_data
from tools.tools_functions import *

# Load the API key from the .env file

KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Load the tools from the JSON file
TOOLS_PATH = "./chatgpt/tools/remediacion-inteligente.json"
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
            "remediation_action_do_nothing": remediation_action_do_nothing,
            "remediation_action_restart_interface": remediation_action_restart_interface,
            "remediation_action_restart_device": remediation_action_restart_device,
            "remediation_action_change_bsp_configuration": remediation_action_change_bsp_configuration,
            "get_ip_interface_brief": get_ip_interface_brief,
            "show_running_config_interface": show_running_config_interface,
            "show_interfaces": show_interfaces,
            "show_ip_route": show_ip_route,
            "ping": ping,
            "traceroute": traceroute,
            "show_logging": show_logging
        }
        for tool_call in tool_calls:
            print(f"Function: {tool_call.function.name}")
            print(f"Params:{tool_call.function.arguments}")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name in available_functions:
                function_response = function_to_call(
                        device_name=function_args.get("device_name"),
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
    return second_response

#DATOS PROVISIORIOS
ESTADO = ["DEGRADATION","AFFECTATION","FATAL EVENT","NO ISSUES"][1]
SERVICIO = ["INTERNET","TELEFONIA_MOVIL","TELEFONIA_FIJA"][0]
TARGET = "NE-PALERMO-01"
HISTORIAL = [
 
    ]

if __name__ == "__main__":

    question = f"""Your are a smart troubleshooting agent for a CSP. Given troublehsooting information about Cisco routers you will determine which actions to take to remediate the isssue.
    There has been {ESTADO} in the service {SERVICIO} in the device {TARGET}
    The device is a {DEFAULT_DEVICE_NAME}, these are the last actions taken in the past: {HISTORIAL}.
    Given your knowledge and experience, you will determine which REMEDATION ACTION to take and return the command sequence
    to execute in the target device. You can call as many functions as you need. You can call the troubleshooting functions to get more device info if needed.
    You must return only the command sequence with no enclosing characters or the literal string NO_ACTION_NEEDED if there is no action to take. You must not return any troubleshooting commands."""
    response = run_conversation(question,tools=tools)
    print(question)
    for chunk in response:
        print(chunk.choices[0].delta.content or "", end='', flush=True)


