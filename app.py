from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Initialize conversation history
conversation = [
    {"role": "model", "parts": ["You are NutriGuide, a friendly and knowledgeable diet coach. Help users with meal planning, nutrition advice, and healthy eating tips."]},
    {"role": "model", "parts": ["Welcome to NutriGuide! 🌿 I'm here to help with your diet goals. What would you like to explore today?"]}
]

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        
        # Add user message to conversation
        conversation.append({"role": "user", "parts": [user_message]})
        
        # Get response from Gemini
        response = model.generate_content(conversation)
        
        # Extract the response text
        bot_response = response.text
        
        # Add bot response to conversation
        conversation.append({"role": "model", "parts": [bot_response]})
        
        return jsonify({
            "success": True,
            "response": bot_response
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)