
#!/usr/bin/env python3
import json
import subprocess
import re
import os
from llamaapi import LlamaAPI

# Initialize the Llama API with your token
llama = LlamaAPI("LL-Qig6k4VbqcY1vfjf14pJ4FkhsK5G13C8vhsWKsiekTBw10GA3aFW4YsQmzvrPN7d")

def prompt_to_command(prompt):
    """Converts a natural language prompt to a command using Llama API."""
    api_request_json = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Give only the command."}
        ],
        "stream": False
    }

    try:
        response = llama.run(api_request_json)
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            command = response_data["choices"][0]["message"]["content"]
            return command.strip()
        else:
            print("No command generated.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def rag_agent(command):
    """Enhances command execution with rule-based modifications and automation."""
    if not command:
        return None

    # Safety checks and common command modifications
    if re.search(r"rm\s+-rf\s+/", command):
        print("Unsafe command detected. Aborting execution.")
        return None

    if "ping" in command and not re.search(r"\d+\.\d+\.\d+\.\d+", command):
        print("No IP address found in the command, defaulting to 8.8.8.8.")
        return "ping 8.8.8.8"

    if "ls" in command and "-l" not in command:
        print("Adding detailed listing option to 'ls' command.")
        command += " -l"

    if command.startswith("mkdir"):
        folder_name = command.split()[-1]
        if os.path.exists(folder_name):
            print(f"Directory {folder_name} already exists.")
            return None
        else:
            print(f"Creating directory: {folder_name}")
            command = f"mkdir -p {folder_name}"

    if command.startswith("rm"):
        print("Adding -i option to 'rm' command to confirm each removal.")
        command = command.replace("rm", "rm -i", 1)

    # Automation tasks
    if "update system" in command:
        print("Automating system update.")
        return "sudo apt-get update && sudo apt-get upgrade -y"

    if "backup" in command:
        parts = command.split()
        if len(parts) == 3:
            source, destination = parts[1], parts[2]
            print(f"Automating backup from {source} to {destination}.")
            return f"rsync -avh --progress {source} {destination}"
        else:
            print("Incorrect backup command format. Use 'backup source destination'.")
            return None

    # Additional rules for specific commands and automations can be added here

    return command

def execute_command(command):
    """Executes the given command and provides detailed feedback."""
    if command:
        try:
            print(f"Executing Command: {command}")
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as exec_error:
            print(f"Execution Error: {exec_error}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
    else:
        print("No command to execute.")
        return False

def retry_command(prompt):
    """Retries command execution with alternative suggestions based on common issues."""
    alternatives = {
        "command not found": "Ensure the command is installed or use a similar available command.",
        "permission denied": "Try running the command with 'sudo' or check file permissions.",
        "No such file or directory": "Verify the file or directory path and try again.",
    }

    for error_message, suggestion in alternatives.items():
        if error_message in prompt:
            print(f"Error identified: {error_message}. Suggestion: {suggestion}")
            # Implement additional logic to generate alternative commands if needed
            return suggestion
    return "No alternative command suggestion found."

def main():
    while True:
        user_prompt = input("Enter your prompt (or type 'exit' to quit): ")
        if user_prompt.lower() == 'exit':
            print("Exiting...")
            break

        command = prompt_to_command(user_prompt)
        if command:
            print(f"Generated Command: {command}")
            command = rag_agent(command)
            if command:
                success = execute_command(command)
                if not success:
                    alternative_suggestion = retry_command(command)
                    print(f"Alternative suggestion: {alternative_suggestion}")
            else:
                print("No command to execute after RAG agent processing.")
        else:
            print("No command to execute.")

if __name__ == "__main__":
    main()
