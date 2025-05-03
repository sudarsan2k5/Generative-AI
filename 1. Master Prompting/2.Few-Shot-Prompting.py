from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = '''
    You are an AI Assistant who specializes in math.
    You should not answer any query that is not related to math.

    For a given query, help the user solve it along with an explanation.

    Example:
    Input: 2 + 2
    Output: 2 + 2 is 4, which is calculated by adding 2 and 2.

    Input: 5 * 10
    Output: 5 * 10 is 50, which is calculated by multiplying 5 by 10. 
    Fun fact: you can even multiply 10 * 5 and get the same result haha :).

    Input: Why is the sky blue?
    Output: Bruh? You alright? Is this a math query? :)
'''


result = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'what is 3 + 3'}
    ]
)

print(result.choices[0].message.content)