import os
import json
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.environ['OPENAI_API_KEY']


def read_json_file(file):
    try:
        with open(file, 'r') as file_in:
            output_json_file = json.load(file_in)
        return output_json_file
    except FileNotFoundError:
        print(f"File {file} not found.  Aborting")
        sys.exit(1)
    except OSError:
        print(f"OS error occurred trying to open {file}")
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error opening {file} is", repr(err))


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def parse_string_to_json(input_string):
    if input_string is None:
        return None
    try:
        input_string = input_string.replace("'", "\"")
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None