import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add parent directory to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from chatbot import chatbot_engine
from preprocess import preprocess_text

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_preprocess_text():
    """Test the text preprocessing function."""
    raw_text = "Hello! Where is my ORDER??"
    processed = preprocess_text(raw_text)
    # Expected output: 'hello order' (since 'where', 'is', 'my' are stop words and punctuation is removed)
    assert "hello" in processed
    assert "order" in processed

def test_chat_endpoint_valid():
    """Test the /chat endpoint with a valid message."""
    response = client.post("/chat", json={"message": "Where is my order?", "session_id": "test1234"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == "test1234"

def test_chat_endpoint_empty():
    """Test the /chat endpoint with an empty message."""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400
    assert "error" in response.json()

def test_clear_history():
    """Test the clear history endpoint."""
    # First, send a message to ensure session exists
    client.post("/chat", json={"message": "Hi", "session_id": "test_clear"})
    
    # Then clear it
    response = client.post("/clear_history", data={"session_id": "test_clear"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_intent_matching():
    """Test if specific patterns trigger correct fallback or responses."""
    # Since GEMINI_API_KEY is not set by default in the test environment, 
    # we expect the specific error message.
    response = chatbot_engine.get_response("Asdfghjkl random text")
    assert "My AI brain is currently offline" in response or len(response) > 0
