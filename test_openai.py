import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('OPENAI')

messages = [{'role': 'user', 'content': 'hi'}]

timestamp = time.time()

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(time.time() - timestamp)

completion_text = completion.choices[0].message.content

print(completion_text)