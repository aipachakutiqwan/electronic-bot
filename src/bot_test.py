import os
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


print(os.environ['OPENAI_API_KEY'])


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content
    #return response.choices[0].message["content"]


def get_completion_and_token_count(messages,
                                   model="gpt-3.5-turbo",
                                   temperature=0,
                                   max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content
    token_dict = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens,
    }
    return content, token_dict


messages = [
{'role':'system',
 'content':"""You are an assistant who responds\
 in the style of shop assistant"""},
{'role':'user',
 'content':"""write me a very short poem \ 
 about selling electronic products"""},
]
response, token_dict = get_completion_and_token_count(messages)
print(response)



