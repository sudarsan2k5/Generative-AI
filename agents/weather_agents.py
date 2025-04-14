from dotenv import load_dotenv
from openai import OpenAI
import json
import os
load_dotenv()

client = OpenAI()

def run_command(command):
    print(f"commad:- {command}")
    result = os.system(command = command)
    return result

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    return f"Directory {path} created successfully."

def create_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Content written to {file_path} successfully."

def read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def list_directory(path):
    return os.listdir(path)

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a shell command as input, executes it, and returns the output (stdout/stderr) and return code."
    },
    "create_directory": {
        "fn": create_directory,
        "description": "Creates a new directory at the specified path. Handles nested directories."
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a new file at the specified path. Can optionally include initial content."
    },
     "write_to_file": {
        "fn": write_to_file,
        "description": "Writes (or overwrites) content to the specified file. Creates the file if it doesn't exist."
    },
    "read_file_content": {
        "fn": read_file_content,
        "description": "Reads and returns the entire content of the specified file."
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists the files and directories within the specified path. Defaults to the current directory if no path is provided."
    }
}


system_prompts = """
    You are an AI assistant specialized in coding and full-stack project development, operating entirely within a terminal.
    Your goal is to help the user build and modify software projects step-by-step.
    You operate in a cycle: Plan -> Action -> Observe -> Output.

    1.  **Plan:** Based on the user's request and the current project state (if applicable), break down the task into logical steps. Announce each step clearly. For follow-up requests, you might need to read existing files first to understand the context.
    2.  **Action:** Select the most appropriate tool from the available list to execute the current step. Specify the function name and necessary input parameters.
    3.  **Observe:** You will receive the output/result from the executed tool.
    4.  **Output:** Based on the observation, either report the result to the user, confirm completion, or explain the next step/plan if the task isn't finished. If the task is multi-step, loop back to Plan/Action for the next step after observing the result of the previous one.

    Rules:
    - Follow the Output JSON Format precisely for each step.
    - Perform ONE step (Plan or Action or Output) at a time and wait for the next input (which might be tool output).
    - Carefully analyze the user query and the context from previous steps and file contents (if read).
    - When writing code, provide the complete code content needed for the 'write_to_file' or 'create_file' action.
    - Refer to files using relative paths from the current working directory where the script is run, unless the user specifies otherwise.

    Output JSON Format:
    {{
        "step": "plan | action | output",
        "content": "Description of the plan, the observation, or the final response to the user.",
        "function": "[Optional] The name of the function if the step is 'action'.",
        "input": "[Optional] The input parameter(s) for the function if the step is 'action'. This should be a single string or a dictionary if the function expects multiple arguments (though current tools take single strings)."
    }}

    Available Tools:
    - run_command: Takes a shell command as input, executes it, and returns the output (stdout/stderr) and return code. Use for installations (pip, npm), builds, etc.
    - create_directory: Creates a new directory at the specified path. Handles nested directories. Input: {{"path": "directory_path"}}
    - create_file: Creates a new file at the specified path with optional initial content. Input: {{"file_path": "path/to/file", "content": "initial file content"}}
    - write_to_file: Writes (or overwrites) content to the specified file. Creates the file if it doesn't exist. Input: {{"file_path": "path/to/file", "content": "content to write"}}
    - read_file_content: Reads and returns the entire content of the specified file. Needed for understanding context before modifying files. Input: {{"file_path": "path/to/file"}}
    - list_directory: Lists the files and directories within the specified path. Defaults to the current directory if no path is provided. Input: {{"path": "directory_path"}}

    Example Interaction (Creating a simple Python project):
    User Query: Create a new python project folder named 'my_app'.
    Output: {{ "step": "plan", "content": "The user wants to create a project folder named 'my_app'." }}
    Output: {{ "step": "action", "function": "create_directory", "input": {{"path": "my_app"}} }}
    Output: {{ "step": "observe", "output": "Directory 'my_app' created successfully." }}
    Output: {{ "step": "output", "content": "Created the project folder 'my_app'." }}

    User Query: Now create an empty file named `main.py` inside `my_app`.
    Output: {{ "step": "plan", "content": "The user wants to create an empty file `main.py` inside the `my_app` directory." }}
    Output: {{ "step": "action", "function": "create_file", "input": {{"file_path": "my_app/main.py", "content": ""}} }}
    Output: {{ "step": "observe", "output": "File 'my_app/main.py' created successfully." }}
    Output: {{ "step": "output", "content": "Created empty file `my_app/main.py`." }}
    User Query: Add `print('Hello, World!')` to `main.py`.
    Output: {{ "step": "plan", "content": "The user wants to add a print statement to `my_app/main.py`. I should write the content to the file." }}
    Output: {{ "step": "action", "function": "write_to_file", "input": {{"file_path": "my_app/main.py", "content": "print('Hello, World!')"}} }}
    Output: {{ "step": "observe", "output": "Content written to 'my_app/main.py' successfully." }}
    Output: {{ "step": "output", "content": "Added `print('Hello, World!')` to `my_app/main.py`." }}

    User Query: list the files in my_app
    Output: {{ "step": "plan", "content": "The user wants to see the contents of the `my_app` directory." }}
    Output: {{ "step": "action", "function": "list_directory", "input": {{"path": "my_app"}} }}
    Output: {{ "step": "observe", "output": "Contents of 'my_app': main.py" }}
    Output: {{ "step": "output", "content": "Files in `my_app`: main.py" }}

"""

message = [
    {'role': 'system', 'content': system_prompts}
]
user_input = input('> ')
message.append({'role': 'user', 'content': user_input})

while True:

    while True:
        response = client.chat.completions.create(
            model='gpt-4o',
            response_format={'type': 'json_object'},
            messages=message
        )

        parse_output = json.loads(response.choices[0].message.content)
        message.append({'role': 'assistant', 'content': json.dumps(parse_output)})


        if parse_output.get("step") == "plan":
            print(f"🧠: {parse_output.get("content")}")
            continue
        
        if parse_output.get("step") == "action":
            tool_name = parse_output.get("function")
            tool_input_raw = parse_output.get("input") # Get raw input
            tool_input = tool_input_raw # Initialize tool_input

            # Attempt to parse if the raw input is a string that looks like JSON
            if isinstance(tool_input_raw, str):
                try:
                    # Check if it looks like a JSON object or array before parsing
                    if tool_input_raw.strip().startswith(('{', '[')):
                         tool_input = json.loads(tool_input_raw)
                except json.JSONDecodeError:
                    # If parsing fails, keep tool_input as the original string
                    pass 

            if available_tools.get(tool_name, False) != False:
                tool_function = available_tools[tool_name].get("fn")
                
                # Now, check if tool_input (potentially parsed) is a dictionary
                if isinstance(tool_input, dict):
                    try:
                        output = tool_function(**tool_input)
                    except TypeError as e:
                        print(f"⚠️ Warning: Tool {tool_name} called with dict {tool_input} but failed with TypeError: {e}. Trying with first value...")
                        try:
                             first_value = next(iter(tool_input.values()))
                             output = tool_function(first_value)
                        except Exception as inner_e:
                             print(f"🚨 Error: Fallback attempt failed for {tool_name}: {inner_e}")
                             output = f"Error executing tool {tool_name}: {inner_e}"
                else:
                    # Handle tools expecting a single positional argument (or correctly non-JSON string input)
                    output = tool_function(tool_input) 
                message.append({'role': 'assistant', 'content': json.dumps({ "step": "observe", "output": output })})
                continue

        if parse_output.get("step") == "output":
            print(f"🤖: {parse_output.get("content")}")
            break

    # Ask for next input after the inner loop breaks
    user_input = input('> ')
    message.append({'role': 'user', 'content': user_input})

