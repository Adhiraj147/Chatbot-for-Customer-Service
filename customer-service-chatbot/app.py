from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot import chatbot_engine
from utils import logger
import uuid

app = FastAPI(
    title="AI Customer Service Chatbot API",
    description="REST API for the NLP-powered Customer Service Chatbot",
    version="1.0.0"
)

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# In-memory dictionary to store basic chat history per session (optional usage)
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main chatbot interface."""
    logger.info("Accessing root endpoint.")
    # Generate a unique session ID for a new user if not handled fully client-side
    session_id = str(uuid.uuid4())
    return templates.TemplateResponse("index.html", {"request": request, "session_id": session_id})

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    """
    Receives user message, passes it to the Gemini engine, and returns the response.
    """
    user_message = chat_request.message
    session_id = chat_request.session_id or "default"
    
    logger.info(f"Session {session_id} - Received message: {user_message}")
    
    if not user_message:
        return JSONResponse(status_code=400, content={"error": "Message cannot be empty."})
        
    try:
        # Get response from chatbot engine, passing session_id for context memory
        bot_response = chatbot_engine.get_response(user_message, session_id=session_id)
        
        # Save to history
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append({"user": user_message, "bot": bot_response})
        
        return {"response": bot_response, "session_id": session_id}
        
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error."})

@app.get("/health")
async def health_check():
    """Returns the health status of the API."""
    return {"status": "healthy", "llm_ready": chatbot_engine.api_key is not None and chatbot_engine.api_key != "your_api_key_here"}

@app.post("/clear_history")
async def clear_history(session_id: str = Form(...)):
    """Clears the chat history for a given session."""
    logger.info(f"Clearing history for session {session_id}")
    
    # Clear from LLM engine memory
    chatbot_engine.clear_session(session_id)
    
    # Clear from local memory
    if session_id in sessions:
        sessions.pop(session_id)
        return {"message": "Chat history cleared successfully.", "status": "success"}
    return {"message": "Session not found.", "status": "not_found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
