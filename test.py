#!/usr/bin/env python3
import json
import subprocess
import re
import os
import shlex
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

    # Split the command and arguments for better handling
    parts = shlex.split(command)
    base_command = parts[0]

    # Safety checks for potentially dangerous commands
    dangerous_commands = [
        "rm", "dd", "mkfs", "mv", "cp", "chmod", "chown", "shutdown", "reboot",
        "useradd", "usermod", "groupadd", "groupdel", "passwd", "userdel",
        "kill", "killall", "pkill", "systemctl", "service", "crontab", "apt-get", "yum", "rpm", "mkfs", "fdisk"
    ]
    
    if base_command in dangerous_commands:
        confirmation = input(f"Are you sure you want to execute this command: '{command}'? (yes/no): ").strip().lower()
        if confirmation != 'yes':
            print("Command aborted.")
            return None

    # Handle specific commands with custom logic
    if base_command == "ping" and not re.search(r"\d+\.\d+\.\d+\.\d+", command):
        print("No IP address found in the command, defaulting to 8.8.8.8.")
        command = "ping 8.8.8.8"

    if base_command == "ls" and "-l" not in parts:
        print("Adding detailed listing option to 'ls' command.")
        command += " -l"

    if base_command == "mkdir":
        folder_name = parts[-1]
        if os.path.exists(folder_name):
            print(f"Directory {folder_name} already exists.")
            return None
        else:
            print(f"Creating directory: {folder_name}")
            command = f"mkdir -p {folder_name}"

    if base_command == "update":
        print("Automating system update.")
        return "sudo apt-get update && sudo apt-get upgrade -y"

    if base_command == "backup":
        if len(parts) == 3:
            source, destination = parts[1], parts[2]
            print(f"Automating backup from {source} to {destination}.")
            return f"rsync -avh --progress {source} {destination}"
        else:
            print("Incorrect backup command format. Use 'backup source destination'.")
            return None

    # General handling for a broader range of commands
    general_command_handlers = {
        # File and Directory Management
        "cp": "Handling cp command.",
        "mv": "Handling mv command.",
        "rm": "Handling rm command.",
        "touch": "Handling touch command.",
        "find": "Handling find command.",
        "locate": "Handling locate command.",
        "updatedb": "Handling updatedb command.",
        "df": "Handling df command.",
        "du": "Handling du command.",
        "tree": "Handling tree command.",
        "file": "Handling file command.",
        "chmod": "Handling chmod command.",
        "chown": "Handling chown command.",
        "ln": "Handling ln command.",
        
        # Networking
        "ping": "Handling ping command.",
        "ifconfig": "Handling ifconfig command.",
        "ip": "Handling ip command.",
        "netstat": "Handling netstat command.",
        "ss": "Handling ss command.",
        "traceroute": "Handling traceroute command.",
        "curl": "Handling curl command.",
        "wget": "Handling wget command.",
        "scp": "Handling scp command.",
        "ftp": "Handling ftp command.",
        "nc": "Handling nc (netcat) command.",
        
        # System Monitoring and Management
        "top": "Handling top command.",
        "htop": "Handling htop command.",
        "ps": "Handling ps command.",
        "free": "Handling free command.",
        "uptime": "Handling uptime command.",
        "dmesg": "Handling dmesg command.",
        "journalctl": "Handling journalctl command.",
        "lsblk": "Handling lsblk command.",
        "mount": "Handling mount command.",
        "umount": "Handling umount command.",
        "iostat": "Handling iostat command.",
        
        # Package Management
        "apt-get": "Handling apt-get command.",
        "apt-cache": "Handling apt-cache command.",
        "dpkg": "Handling dpkg command.",
        "yum": "Handling yum command.",
        "dnf": "Handling dnf command.",
        "rpm": "Handling rpm command.",
        "zypper": "Handling zypper command.",
        "pacman": "Handling pacman command.",
        
        # Text Processing
        "cat": "Handling cat command.",
        "more": "Handling more command.",
        "less": "Handling less command.",
        "head": "Handling head command.",
        "tail": "Handling tail command.",
        "grep": "Handling grep command.",
        "sed": "Handling sed command.",
        "awk": "Handling awk command.",
        "cut": "Handling cut command.",
        "paste": "Handling paste command.",
        "sort": "Handling sort command.",
        "uniq": "Handling uniq command.",
        
        # System Administration
        "useradd": "Handling useradd command.",
        "usermod": "Handling usermod command.",
        "userdel": "Handling userdel command.",
        "groupadd": "Handling groupadd command.",
        "groupdel": "Handling groupdel command.",
        "passwd": "Handling passwd command.",
        "crontab": "Handling crontab command.",
        "systemctl": "Handling systemctl command.",
        "service": "Handling service command.",
        "shutdown": "Handling shutdown command.",
        "reboot": "Handling reboot command.",
        "halt": "Handling halt command.",
        "pkill": "Handling pkill command.",
        
        # Disk Management
        "fdisk": "Handling fdisk command.",
        "mkfs": "Handling mkfs command.",
        "mount": "Handling mount command.",
        "umount": "Handling umount command.",
        "parted": "Handling parted command.",
        "lsblk": "Handling lsblk command.",
        "df": "Handling df command.",
        "du": "Handling du command.",
        
        # Miscellaneous
        "alias": "Handling alias command.",
        "unalias": "Handling unalias command.",
        "history": "Handling history command.",
        "man": "Handling man command.",
        "info": "Handling info command.",
        "which": "Handling which command.",
        "whereis": "Handling whereis command.",
        "type": "Handling type command.",
        
        # Security
        "sudo": "Handling sudo command.",
        "ssh": "Handling ssh command.",
        "gpg": "Handling gpg command.",
        "openssl": "Handling openssl command.",
        "passwd": "Handling passwd command.",
        
        # Development
        "gcc": "Handling gcc command.",
        "make": "Handling make command.",
        "cmake": "Handling cmake command.",
        "gdb": "Handling gdb command.",
        "valgrind": "Handling valgrind command.",
        
        # Virtualization
        "docker": "Handling docker command.",
        "vagrant": "Handling vagrant command.",
        "kvm": "Handling kvm command.",
        "qemu": "Handling qemu command.",
        
        # Other
        "tar": "Handling tar command.",
        "gzip": "Handling gzip command.",
        "bzip2": "Handling bzip2 command.",
        "xz": "Handling xz command.",
        "zip": "Handling zip command.",
        "unzip": "Handling unzip command.",
    }

    # Check for known commands
    if base_command in general_command_handlers:
        print(general_command_handlers[base_command])
        # Add specific handling if necessary
    else:
        # For unknown commands, provide basic execution
        print(f"Handling {base_command} command.")
    
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
