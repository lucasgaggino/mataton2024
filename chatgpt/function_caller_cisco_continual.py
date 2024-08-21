import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

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

# Define the log file path
file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE_PATH = f"./chats/{file_name}.txt"

def log_to_file(content):
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(content + "\n")

def run_conversation(tools=None):
    messages = []
    log_to_file("=== Conversation Started ===")
    
    while True:
        content = input("Enter your question: ")
        if content.lower() == "exit":
            log_to_file("User ended the chat.")
            print("Ending chat...")
            break

        messages.append({"role": "user", "content": content})
        log_to_file(f"User: {content}")
        
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
            log_to_file(f"ChatGPT: {response_message}")

            available_functions = {
                "send_command": send_command,
                "end_chat": lambda: (log_to_file("ChatGPT called end_chat. Ending chat..."), exit()),
            }
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                log_to_file(f"Function Call: {function_name} with arguments {function_args}")

                function_to_call = available_functions.get(function_name)
                if function_to_call:
                    if function_name == "end_chat":
                        function_to_call()
                        return
                    else:
                        function_response = function_to_call(command=function_args.get("command"))
                        log_to_file(f"Function Response: {function_response}")
                        #print(f"API: {function_response}")
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
                messages=messages
            )
        else:
            messages.append(response_message)
            second_response = response
        
        response_message = second_response.choices[0].message.content
        log_to_file(f"ChatGPT: {response_message}")
        

    
    log_to_file("=== Conversation Ended ===")

if __name__ == "__main__":
    run_conversation(tools=tools)
