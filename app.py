import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Configure the Google Gemini API client
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except AttributeError:
    print("⚠️ Gemini API Key not found. Please set it in your .env file.")
    exit()

# Initialize the Generative Model
# Using gemini-1.5-flash for speed and cost-effectiveness
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # The system prompt provides context for the model
        system_prompt = (
            "You are an expert AI Career Advisor integrated into a website. Your goal is to provide helpful, "
            "clear, and encouraging advice on careers in technology and AI. Keep responses concise and friendly."
        )
        
        # Combine the system prompt and user message for the API call
        full_prompt = f"{system_prompt}\n\nUser's Question: {user_message}"

        # Generate content using the Gemini model
        response = model.generate_content(full_prompt)

        # Extract the AI's response text and send it back
        return jsonify({"response": response.text})

    except Exception as e:
        # Log the detailed error to the console for debugging
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to get a response from the AI model."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
