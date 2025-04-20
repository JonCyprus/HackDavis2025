from flask import Flask, send_from_directory, request, jsonify
import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv, find_dotenv

# Load environment variables and initialize Cerebras client
load_dotenv(find_dotenv())
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

app = Flask(__name__, static_folder='../public')

# Store chat history in memory (in production, you'd want to use a database)
chat_history = [
    {"role": "system", "content": "You are a helpful AI assistant, conversing with an end user."}
]

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_message})
    
    # Get AI response
    chat = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=chat_history
    )
    
    # Get AI response and add to chat history
    ai_response = chat.choices[0].message.content
    chat_history.append({"role": "assistant", "content": ai_response})
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
