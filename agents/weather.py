from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import os
load_dotenv()

client = OpenAI()

def get_weather(city: str):
    # TODO!: Do an actual API call
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The Weather in {city} is {response.text}"
    return "Something Went Wrong : )"

def run_command(command):
    print(f"commad:- {command}")
    breakpoint()
    result = os.system(command = command)
    return result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an inputs and returns the current weather for the city"
    },
    "run_command":{
        "fn": run_command,
        "description": "Takes a command as an input and returns the result of the command"
    }
}


system_prompts = """
    You are an helpfull AI Assistant who is secialized in resolving user query.
    Your work is start, plan, action, observe mode.
    For the given user query and avaliable tools,  plan the step by step execution,  based on the planning,
    select the relevent tool form the avalible tool. and based on the tool selection you perfrom an action to call the tool.
    wait for the observation and based on the observation form the tool call resollve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Alwase perform one steo at a time and wait for the next input.
    - Carefully analyse the user query.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of the function if the step is the action",
        "input": "The input parameter for the function"
    }}

    Avaliable Tools:
    - get_weather: Takes a city name as an input and returns the current weather fot the city.
    - run_command: Takes a command as an input and excute on system and returns the output.

    Eample:
    User Query: What is the weather of new york ?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

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
            tool_input = parse_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                message.append({'role': 'assistant', 'content': json.dumps({ "step": "observe", "output": output })})
                continue

        if parse_output.get("step") == "output":
            print(f"🤖: {parse_output.get("content")}")
            break

    # Ask for next input after the inner loop breaks
    user_input = input('> ')
    message.append({'role': 'user', 'content': user_input})

# response = client.chat.completions.create(
   
#     response_format={'type': 'json_object'},
#     messages=[
#         {'role': 'system', 'content': system_prompts},
#         {'role': 'user', 'content': 'What is the weather today in Odisha ?'},
#         {'role': 'assistant', 'content': json.dumps({ "step": "plan", "content": "The user is asking for the current weather data in Odisha." })},
#         {'role': 'assistant', 'content': json.dumps({"step": "plan", "content": "From the available tools, I should call get_weather to obtain the weather data for Odisha."})},
#         {'role': 'assistant', 'content': json.dumps({"step": "action", "function": "get_weather", "input": "Odisha"})},
#         {'role': 'assistant', 'content': json.dumps({"step": "observe", "output": "30 Degree Cel"})}

#     ]
# )

