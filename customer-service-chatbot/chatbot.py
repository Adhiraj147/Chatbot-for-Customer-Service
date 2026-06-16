import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils import logger

load_dotenv()

class ChatbotEngine:
    def __init__(self, intents_file="intents.json"):
        self.intents_file = intents_file
        self.tfidf_matrix = True  
        self.client = None

    def get_response(self, user_message: str, session_id: str = None) -> str:
        if self.client is None:
            try:
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key:
                    self.client = genai.Client(api_key=api_key)
                else:
                    self.client = genai.Client()
                logger.info("Gemini Engine explicitly initialized inside response call.")
            except Exception as init_err:
                logger.error(f"Failed to build Gemini client: {str(init_err)}")
                return f"Configuration Error: {str(init_err)}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a helpful customer service assistant.",
                        temperature=0.7
                    )
                )
                return response.text
                
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    logger.warning("Hit a 503 server spike. Retrying...")
                    time.sleep(1.5)
                    continue
                
                logger.error(f"Gemini API Failure: {str(e)}")
                return f"Backend API Error Details: {str(e)}"

chatbot_engine = ChatbotEngine()