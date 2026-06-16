# AI Customer Service Chatbot

A complete, production-ready AI Customer Service Chatbot built with Python, FastAPI, and simple Natural Language Processing (NLP) techniques.

## 🚀 Project Overview

This project implements an intelligent chatbot capable of understanding and answering frequently asked customer questions (FAQs). It uses a rule-based engine combined with NLP (TF-IDF and Cosine Similarity) to match user queries with the most appropriate predefined intent and response. 

The chatbot handles queries regarding:
- Order Status & Shipping
- Return & Refund Policies
- Payment Methods
- Product Availability
- Business Hours & Contact Info

## ✨ Features

- **NLP-Powered Engine**: Uses NLTK for text preprocessing (tokenization, lemmatization, stopword removal) and Scikit-Learn for intent matching (TF-IDF Vectorization, Cosine Similarity).
- **REST API Backend**: Fast and robust backend built with FastAPI.
- **Modern UI**: A responsive, aesthetically pleasing frontend using Vanilla CSS with dark mode support, glassmorphism, and smooth animations.
- **Session Management**: Maintains chat history during the user's session.
- **Comprehensive Logging & Error Handling**: Production-ready logging built-in.
- **Extensive Intent Dataset**: Preconfigured with 20 distinct intents and over 200 training patterns.

## 🛠 Technologies Used

### Backend
- **Python 3.8+**
- **FastAPI** & **Uvicorn**
- **NLTK** (Natural Language Toolkit)
- **Scikit-Learn**
- **Pytest** (for unit testing)

### Frontend
- **HTML5**
- **CSS3** (Custom Properties, Flexbox, Animations)
- **Vanilla JavaScript** (ES6+)

## 📁 Folder Structure

```
customer-service-chatbot/
│
├── app.py                # FastAPI application & endpoints
├── chatbot.py            # NLP logic, TF-IDF training, response generation
├── intents.json          # Dataset containing intents, patterns, responses
├── preprocess.py         # Text preprocessing utilities (NLTK)
├── utils.py              # Logging and helper functions
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── static/               # Frontend assets
│   ├── style.css         # UI Styling & Dark Mode
│   └── script.js         # Frontend logic & API integration
│
├── templates/            # HTML templates
│   └── index.html        # Main Chatbot UI
│
├── tests/                # Unit tests
│   └── test_chatbot.py
│
└── logs/                 # Auto-generated application logs
```

## 📸 Screenshots

*(Placeholder for Screenshots)*
- **Light Mode UI**
- **Dark Mode UI**
- **Mobile Responsive View**

## 💻 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd customer-service-chatbot
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *The server will start on `http://localhost:8000`.*

5. **Access the Chatbot:**
   Open your browser and navigate to `http://localhost:8000`.

## 🧪 Testing

Run unit tests using Pytest:
```bash
pytest tests/
```

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.
- **Swagger UI**: Navigate to `http://localhost:8000/docs`
- **ReDoc**: Navigate to `http://localhost:8000/redoc`

### Endpoints
- `GET /` : Returns the chatbot HTML UI.
- `POST /chat` : Accepts `{"message": "string", "session_id": "string"}` and returns the bot's response.
- `GET /health` : Returns API health status.
- `POST /clear_history` : Clears the session history.

## 🚀 Deployment

### Deploying on Render / Railway
1. Push your code to a GitHub repository.
2. Connect your repo to Render/Railway.
3. Set the start command to: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Deploy!

### Deploying on Vercel (Frontend only if decoupled)
If you wish to host the frontend separately on Vercel, you will need to update the API base URL in `script.js` to point to your deployed backend.

## 🔮 Future Improvements

- **LLM Integration**: Upgrade from rule-based to generative AI using OpenAI/Gemini API.
- **Voice Capabilities**: Add speech-to-text and text-to-speech support.
- **Multi-language Support**: Implement automatic translation.
- **Database Integration**: Store chat history persistently using PostgreSQL or MongoDB.
- **Admin Dashboard**: Build a React/Vue dashboard to monitor chat logs and update intents dynamically.
- **WhatsApp Integration**: Connect the chatbot to WhatsApp Business API.
