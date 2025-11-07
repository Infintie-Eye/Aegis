# Aegis Mental Wellness Platform - Quick Start Guide

## ⚡ Super Quick Start (Windows)

### Option 1: Using Batch Scripts

1. **Setup (First Time Only)**:
   ```cmd
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Backend**:
    - Double-click `start_backend.bat`
    - Wait for message: "Starting Aegis Mental Wellness API on 0.0.0.0:5000"

3. **Start Frontend** (in new terminal):
    - Double-click `start_frontend.bat`
    - Wait for message about server running on port 8000

4. **Open Browser**:
    - Navigate to: http://localhost:8000

### Option 2: Manual Start

**Terminal 1 (Backend):**

```cmd
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 (Frontend):**

```cmd
cd frontend
python -m http.server 8000
```

## ⚡ Super Quick Start (Mac/Linux)

**Terminal 1 (Backend):**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 (Frontend):**

```bash
cd frontend
python3 -m http.server 8000
```

## 🎯 What You Get

Once running, you'll have access to:

- **Landing Page**: http://localhost:8000/
- **AI Chatbot**: http://localhost:8000/pages/aichatbot.html
- **Community Chatrooms**: http://localhost:8000/pages/community_list.html
- **User Dashboard**: http://localhost:8000/pages/userdashboard.html
- **Analysis Tools**: http://localhost:8000/pages/analysis.html
- **Backend API**: http://localhost:5000

## 🔑 Important Files

- `backend/.env` - Contains API keys and configuration
- `backend/ai_chatbot/.env` - Gemini API key for AI chatbot
- `frontend/js/firebase.js` - Firebase configuration
- `frontend/js/ai-chatbot.js` - AI chatbot frontend integration

## 📋 Quick Feature Test

### 1. Test AI Chatbot

1. Go to http://localhost:8000/pages/aichatbot.html
2. Type: "I've been feeling stressed lately"
3. You should get an AI-powered response with wellness suggestions

### 2. Test Chatrooms

1. Go to http://localhost:8000/pages/community_list.html
2. Click on any chatroom (e.g., "Anxiety Support")
3. Send a message
4. Your message should appear in real-time

### 3. Test Analysis

1. Go to http://localhost:8000/pages/analysis.html
2. Complete the personality analysis
3. View your results with detailed insights

## ⚠️ Common Issues

### "Module not found" error

```bash
cd backend
pip install -r requirements.txt
```

### "Port already in use"

- Backend (5000): Kill other Python processes or change port in `.env`
- Frontend (8000): Use different port: `python -m http.server 8001`

### "API key not valid"

- Check `backend/.env` has `GOOGLE_API_KEY`
- Verify key is valid in Google AI Studio

### CORS errors

- Ensure backend is running on port 5000
- Check `flask-cors` is installed

## 📖 Full Documentation

For detailed setup, configuration, and deployment:

- See `INTEGRATION_GUIDE.md` for complete integration details
- See `README.md` for project overview
- See `backend/ai_chatbot/README.md` for AI chatbot details

## 🎉 You're Ready!

Start building mental wellness with Aegis! 🌟

For support: team@aegis.com
