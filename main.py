from waitress import serve
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.environ.get('OPENAI')

history = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        message = request.form['Body']

        print(message)
        
        if message == 'clear':
            history['WaId'] = []
            twiml = MessagingResponse()
            twiml.message('State Cleared Successfully')
            return str(twiml)
        
        messages = []
        if history.get('WaId'):
            for input_text, completion_text in history['WaId']:
                messages.append({'role': 'user', 'content': input_text})
                messages.append({'role': 'assistant', 'content': completion_text})
        messages.append({'role': 'user', 'content': message})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        completion_text = completion.choices[0].message.content

        print(completion_text)
        
        if 'WaId' in history:
            history['WaId'].append((message, completion_text))
        else:
            history['WaId'] = [(message, completion_text)]
        
        twiml = MessagingResponse()
        twiml.message(completion_text)
        return str(twiml)
    
    except Exception as e:
        print(e)
        return str(e)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'production':
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(debug=True, port=5000)
