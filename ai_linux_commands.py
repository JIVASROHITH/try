import subprocess
import shlex

# Define a simple mapping of commands
command_map = {
    "list files": "ls",
    "show files": "ls",
    "current directory": "pwd",
    "show directory": "pwd",
    "disk usage": "df -h",
    "show disk": "df -h",
    "check disk": "df -h",
    "disk space": "df -h",
}

def execute_command(command):
    try:
        result = subprocess.run(shlex.split(command), capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def get_command_from_prompt(prompt):
    # Normalize the prompt to lower case
    prompt = prompt.lower()
    # Check for each key in the command_map to see if it's in the prompt
    for key in command_map.keys():
        if key in prompt:
            return command_map[key]
    return None

while True:
    user_prompt = input("Enter your command prompt: ")
    if user_prompt.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    linux_command = get_command_from_prompt(user_prompt)
    if linux_command:
        output = execute_command(linux_command)
        print(output)
    else:
        print("Command not recognized. Please try again.")
