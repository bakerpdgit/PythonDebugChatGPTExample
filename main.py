from flask import Flask, request, jsonify, render_template
import openai
import os
import datetime
import random

app = Flask(__name__)

MAX_HISTORY_LENGTH = 4  # Maximum number of messages (2 exchanges)
MAX_MESSAGE_LENGTH = 500  # Maximum length of each message


def generate_daily_key():
    # have some function to return a key based on date
    # to retain teacher control who can generate key locally and issue to class
    # for now...
    return 1010


def validate_usage_key(usage_key):
    correct_key = generate_daily_key()
    return usage_key == correct_key


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    usage_key = data.get('usage_key')
    user_message = data.get('user_message')
    mode = data.get('mode')
    chat_history = data.get('chat_history', [])

    if not validate_usage_key(usage_key) or not user_message or not mode:
        assistant_message = "Sorry, a correct usage key, user message and mode are all required."
        return jsonify({'assistant_message': assistant_message.strip(), 'chat_history': chat_history})

    user_message = user_message[:MAX_MESSAGE_LENGTH]

    if len(chat_history) >= MAX_HISTORY_LENGTH:
        chat_history.append({'role': 'user', 'content': user_message})
        assistant_message = "Sorry, I am unable to help further because I am limited to 2 exchanges per conversation."
        chat_history.append(
            {'role': 'assistant', 'content': assistant_message.strip()})
        return jsonify({'assistant_message': assistant_message.strip(), 'chat_history': chat_history})

    try:
        openai.api_key = os.getenv('API_KEY')

        if mode == 'socratic':
            system_message = "Your role is to ask guiding questions to help a student find and fix bugs in their python code snippet. Avoid giving direct answers; instead give one fairly clear nudge in the form of a hint or question for every mistake or likely issue identified. You are writing for a 14 year old, so keep your questions simple and clear and NEVER answer anything off of the topic of python debugging; just politely decline if asked to do so."
        else:
            system_message = "Your role is a teacher to concisely advise a student on bugs in their python code snippet WITHOUT giving the full corrected code although you can give individual line improvements and be quite specific. You must NEVER answer anything off of the topic of python debug suggestions; just politely decline if asked to do so. You are writing for a 14 year old so keep it simple and short. Ensure you NEVER include the full corrected code in your response however, only individual suggestions."

        messages = [
            {
                "role": "system",
                "content": system_message
            }
        ]

        messages.extend([{'role': msg['role'], 'content': msg['content']}
                        for msg in chat_history])

        # minimal protection against injecting system messages
        messages.append(
            {"role": "user", "content": user_message.replace("system", "systum")})

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        assistant_message = response.choices[0].message.content

        chat_history.append({'role': 'user', 'content': user_message})
        chat_history.append(
            {'role': 'assistant', 'content': assistant_message})

        return jsonify({'assistant_message': assistant_message, 'chat_history': chat_history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
