# Aegis Mental Wellness Platform - Complete Integration Guide

## 🚀 Overview

This guide provides step-by-step instructions to set up and run the complete Aegis Mental Wellness Platform with all
components properly integrated.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [AI Chatbot Integration](#ai-chatbot-integration)
6. [Running the Application](#running-the-application)
7. [Testing the Integration](#testing-the-integration)
8. [Troubleshooting](#troubleshooting)

## 💻 System Requirements

- **Python**: 3.10 or higher
- **Node.js**: 16.x or higher (for development tools)
- **Firebase Account**: For authentication and real-time database
- **Google Gemini API Key**: For AI chatbot functionality
- **Operating System**: Windows 10/11, macOS, or Linux

## 📁 Project Structure

```
Aegis/
├── backend/
│   ├── ai_chatbot/          # AI chatbot with CrewAI
│   │   ├── agents/          # Specialized AI agents
│   │   ├── config/          # Agent/crew configurations
│   │   ├── memory/          # Memory management systems
│   │   ├── utils/           # Utility functions
│   │   ├── .env             # Gemini API key
│   │   └── main_orchestrator.py
│   ├── routes/              # Flask API routes
│   │   ├── chat_routes.py   # AI chatbot endpoints
│   │   ├── analysis_routes.py # Analysis endpoints
│   │   ├── room_routes.py   # Chatroom endpoints
│   │   └── auth_routes.py   # Authentication endpoints
│   ├── analysis/            # Analysis modules
│   ├── chatrooms/           # Chatroom management
│   ├── .env                 # Backend environment variables
│   ├── app.py               # Main Flask application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── pages/               # All HTML pages
│   │   ├── index.html       # Landing page
│   │   ├── aichatbot.html   # AI chatbot interface
│   │   ├── community_list.html
│   │   ├── depression.html  # Chatrooms
│   │   ├── anxiety.html
│   │   ├── academic.html
│   │   ├── work.html
│   │   ├── relationship.html
│   │   ├── lonliness.html
│   │   ├── analysis.html    # Mental health analysis
│   │   ├── profile.html
│   │   ├── login.html
│   │   └── sign_up.html
│   ├── js/                  # JavaScript modules
│   │   ├── firebase.js      # Firebase configuration
│   │   ├── ai-chatbot.js    # AI chatbot integration
│   │   ├── chat.js          # Firebase chat handler
│   │   ├── authguard.js     # Authentication guard
│   │   ├── sidebar.js       # Sidebar navigation
│   │   └── navbar.js        # Navbar handler
│   ├── css/                 # Stylesheets
│   └── assets/              # Images and icons
└── documentation/           # Project documentation
```

## 🔧 Backend Setup

### Step 1: Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installation may take 10-15 minutes due to large packages (torch, transformers, etc.)

### Step 3: Configure Environment Variables

Create or verify `backend/.env` file:

```env
# Google Gemini API Key (REQUIRED)
GOOGLE_API_KEY=AIzaSyDq8ch3npPUVVIUWm0FgU8Sjx7uKs2CbjA
GEMINI_API_KEY=AIzaSyDq8ch3npPUVVIUWm0FgU8Sjx7uKs2CbjA

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=aegis-mental-wellness-secret-key-change-in-production

# Firebase Configuration
FIREBASE_API_KEY=AIzaSyBFb1BxuqBt-N9u5YWgroqMVuSIQjRbtEc
FIREBASE_AUTH_DOMAIN=aegis-d1a50.firebaseapp.com
FIREBASE_PROJECT_ID=aegis-d1a50

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### Step 4: Verify AI Chatbot Configuration

Ensure `backend/ai_chatbot/.env` exists:

```env
GEMINI_API_KEY="AIzaSyDq8ch3npPUVVIUWm0FgU8Sjx7uKs2CbjA"
```

## 🎨 Frontend Setup

### Step 1: Verify Firebase Configuration

Check `frontend/js/firebase.js`:

```javascript
const firebaseConfig = {
    apiKey: "AIzaSyBFb1BxuqBt-N9u5YWgroqMVuSIQjRbtEc",
    authDomain: "aegis-d1a50.firebaseapp.com",
    projectId: "aegis-d1a50",
    storageBucket: "aegis-d1a50.firebasestorage.app",
    messagingSenderId: "405698913839",
    appId: "1:405698913839:web:bf420b565e7259fb8208da",
    measurementId: "G-KZTDL9HLPR"
};
```

### Step 2: Update AI Chatbot Integration

Add the AI chatbot script to `frontend/pages/aichatbot.html` before `</body>`:

```html
<!-- Add this line before sidebar.js -->
<script src="../js/ai-chatbot.js"></script>
<script src="../js/sidebar.js"></script>
```

### Step 3: Update API Base URL (if needed)

In `frontend/js/ai-chatbot.js`, update the API URL if your backend is not on localhost:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';  // Change if needed
```

## 🤖 AI Chatbot Integration

### How It Works

1. **User sends message** via `aichatbot.html`
2. **Frontend** (`ai-chatbot.js`) sends request to Flask backend
3. **Backend** (`chat_routes.py`) forwards to `MainOrchestrator`
4. **MainOrchestrator** uses CrewAI with multiple specialized agents
5. **Gemini API** powers the AI responses
6. **Response** includes therapeutic advice, wellness suggestions, community recommendations
7. **Frontend** displays response with additional resources

### Key Endpoints

- `POST /api/chat/message` - Send message and get AI response
- `GET /api/chat/history/<user_id>` - Get chat history
- `GET /api/chat/insights/<user_id>` - Get user insights
- `GET /api/chat/wellness/<user_id>` - Get wellness suggestions
- `DELETE /api/chat/clear/<user_id>` - Clear chat history

### Example Request

```javascript
fetch('http://localhost:5000/api/chat/message', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: "I've been feeling really anxious lately",
        user_id: "user123",
        session_context: {}
    })
});
```

### Example Response

```json
{
    "status": "success",
    "response": "I understand that anxiety can be overwhelming...",
    "emotional_state": {
        "dominant_emotion": "anxiety",
        "intensity": 0.7
    },
    "mental_state_score": 6.5,
    "wellness_suggestions": [
        "Try deep breathing exercises",
        "Practice mindfulness meditation",
        "Consider journaling your thoughts"
    ],
    "community_suggestions": {
        "support_groups": ["Anxiety Support Group", "Mindfulness Community"]
    },
    "safety_status": {
        "safe": true,
        "crisis_level": 3
    }
}
```

## 🏃 Running the Application

### Method 1: Development Mode (Recommended)

**Terminal 1 - Backend Server:**

```bash
cd backend
# Activate virtual environment first
python app.py
```

You should see:

```
🚀 Starting Aegis Mental Wellness API on 0.0.0.0:5000
📝 Debug mode: True
🔑 API Key configured: True
```

**Terminal 2 - Frontend Server:**

```bash
# Using Python's built-in HTTP server
cd frontend
python -m http.server 8000
```

Or use any static file server:

```bash
# Using Node.js http-server (install with: npm install -g http-server)
cd frontend
http-server -p 8000
```

**Access the application:**

- Frontend: http://localhost:8000
- Backend API: http://localhost:5000
- API Health Check: http://localhost:5000/health

### Method 2: Production Mode

For production deployment, use proper WSGI server:

```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Testing the Integration

### 1. Test Backend Health

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
    "status": "healthy",
    "service": "Aegis Mental Wellness API",
    "timestamp": "2024-01-01T12:00:00",
    "version": "1.0.0"
}
```

### 2. Test AI Chatbot Endpoint

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need someone to talk to",
    "user_id": "test_user_123"
  }'
```

### 3. Test Chatroom Endpoints

```bash
# List all chatrooms
curl http://localhost:5000/api/rooms/list

# Get specific room details
curl http://localhost:5000/api/rooms/anxiety
```

### 4. Test Analysis Endpoints

```bash
# Track mood
curl -X POST http://localhost:5000/api/analysis/mood \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "mood": "happy",
    "intensity": 7
  }'
```

### 5. Test Frontend Integration

1. **Open Browser**: Navigate to `http://localhost:8000`
2. **Sign Up/Login**: Create account or log in
3. **Navigate to AI Chatbot**: Click "AI Companion" in sidebar
4. **Send Message**: Type a message and click send
5. **Verify Response**: Should receive AI-powered response within 3-5 seconds

## 🔗 Page-to-Backend Connections

### AI Chatbot Page (`aichatbot.html`)

- **Backend Route**: `/api/chat/*`
- **Script**: `frontend/js/ai-chatbot.js`
- **Features**:
    - Real-time AI responses via Gemini API
    - Emotional state detection
    - Wellness suggestions
    - Crisis detection and intervention
    - Community recommendations

### Chatroom Pages

- **Pages**: `depression.html`, `anxiety.html`, `academic.html`, etc.
- **Backend Route**: `/api/rooms/*`
- **Script**: `frontend/js/chat.js` (Firebase)
- **Features**:
    - Real-time peer-to-peer chat
    - Anonymous user support
    - Firebase Firestore integration
    - Message persistence

### Analysis Page (`analysis.html`)

- **Backend Route**: `/api/analysis/*`
- **Features**:
    - Mood tracking
    - Progress analysis
    - Voice analysis (placeholder)
    - Sentiment analysis

### User Dashboard (`userdashboard.html`)

- **Scripts**: `authguard.js`, `firebase.js`
- **Features**:
    - Firebase authentication
    - User profile management
    - Activity tracking

### Profile Page (`profile.html`)

- **Backend**: Firebase Firestore
- **Features**:
    - Profile editing
    - Preferences management
    - Avatar management

## 🎯 Feature Connections

### 1. Authentication Flow

```
login.html / sign_up.html
    ↓
frontend/js/firebase.js (Firebase Auth)
    ↓
authguard.js (Route protection)
    ↓
Protected pages (dashboard, profile, chatbot)
```

### 2. AI Chatbot Flow

```
User types message in aichatbot.html
    ↓
frontend/js/ai-chatbot.js captures input
    ↓
POST /api/chat/message (Flask)
    ↓
backend/routes/chat_routes.py
    ↓
ai_chatbot/main_orchestrator.py
    ↓
CrewAI agents + Gemini API
    ↓
Response with therapy, wellness, community suggestions
    ↓
Display in frontend with rich formatting
```

### 3. Peer Chatroom Flow

```
User opens chatroom (e.g., depression.html)
    ↓
frontend/js/chat.js initializes
    ↓
Firebase Firestore real-time listener
    ↓
Messages stored in /chatrooms/{roomId}/messages
    ↓
Real-time updates to all participants
```

### 4. Analysis Flow

```
User tracks mood in analysis.html
    ↓
POST /api/analysis/mood
    ↓
backend/routes/analysis_routes.py
    ↓
Store mood data
    ↓
GET /api/analysis/progress/{user_id}
    ↓
Return progress insights and trends
```

## 🐛 Troubleshooting

### Issue: Backend won't start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:

```bash
cd backend
pip install -r requirements.txt
```

### Issue: AI Chatbot not responding

**Error**: `Error: 400 API key not valid`

**Solution**:

1. Check `backend/.env` has `GOOGLE_API_KEY`
2. Verify API key is valid in Google AI Studio
3. Ensure `.env` is in the `backend` directory

### Issue: CORS error in browser

**Error**: `Access to fetch at 'http://localhost:5000' from origin 'http://localhost:8000' has been blocked`

**Solution**:

- Verify `flask-cors` is installed
- Check `app.py` has `CORS(app)` configured
- Restart backend server

### Issue: Firebase not working

**Error**: `Firebase: Error (auth/configuration-not-found)`

**Solution**:

1. Check `frontend/js/firebase.js` has correct config
2. Verify Firebase project is active
3. Enable Authentication in Firebase Console

### Issue: Long response times

**Cause**: Gemini API rate limiting or cold start

**Solution**:

- First request after restart takes longer (agent initialization)
- Subsequent requests are faster due to caching
- Check Gemini API rate limits (60 RPM for free tier)

### Issue: Memory/Session data not persisting

**Cause**: In-memory storage is cleared on server restart

**Solution**:

- For production, implement database storage (PostgreSQL, MongoDB)
- Current implementation uses in-memory dictionaries
- Consider Redis for session storage

## 📚 API Documentation

### Complete API Endpoints

#### Chat Endpoints

- `POST /api/chat/message` - Send message to AI chatbot
- `GET /api/chat/history/<user_id>` - Get chat history
- `GET /api/chat/insights/<user_id>` - Get user insights
- `GET /api/chat/wellness/<user_id>` - Get wellness suggestions
- `DELETE /api/chat/clear/<user_id>` - Clear user data

#### Room Endpoints

- `GET /api/rooms/list` - List all chatrooms
- `GET /api/rooms/<room_id>` - Get room details
- `POST /api/rooms/<room_id>/join` - Join a room
- `POST /api/rooms/<room_id>/leave` - Leave a room
- `GET /api/rooms/categories` - Get room categories

#### Analysis Endpoints

- `POST /api/analysis/mood` - Track mood
- `GET /api/analysis/mood/<user_id>` - Get mood history
- `GET /api/analysis/progress/<user_id>` - Get progress analysis
- `POST /api/analysis/voice-analysis` - Analyze voice (placeholder)
- `POST /api/analysis/sentiment` - Analyze text sentiment

#### Auth Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/anonymous` - Create anonymous session
- `POST /api/auth/verify` - Verify session token
- `POST /api/auth/logout` - Logout user

## 🚀 Deployment Checklist

### Before Production

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use proper database (PostgreSQL/MongoDB) instead of in-memory storage
- [ ] Set up proper session management (Redis)
- [ ] Enable HTTPS
- [ ] Set `FLASK_ENV=production`
- [ ] Configure proper CORS origins
- [ ] Set up logging and monitoring
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization
- [ ] Set up backup systems
- [ ] Configure Firebase security rules
- [ ] Review Gemini API rate limits and upgrade if needed

### Production Servers

- Backend: Gunicorn + Nginx
- Frontend: Nginx or CDN (Vercel, Netlify)
- Database: PostgreSQL/MongoDB
- Cache: Redis
- Monitoring: Sentry, New Relic, or similar

## 💡 Additional Features to Implement

### Priority Enhancements

1. **Database Integration**: Replace in-memory storage with PostgreSQL
2. **Redis Sessions**: Implement proper session management
3. **WebSocket Support**: Real-time AI chatbot responses
4. **Voice Analysis**: Implement actual voice emotion detection
5. **Better NLP**: Enhance sentiment analysis with spaCy/NLTK
6. **Progress Dashboard**: Visual analytics for user progress
7. **Notification System**: Email/SMS for crisis situations
8. **Mobile App**: React Native or Flutter mobile app
9. **Admin Panel**: Monitor users, moderate chatrooms
10. **Multi-language**: Support for multiple languages

## 📞 Support

For issues or questions:

- **GitHub Issues**: [Repository URL]
- **Email**: team@aegis.com
- **Documentation**: Check README.md files in each directory

## 🎉 Success!

If you've followed all steps, you should now have:

- ✅ Backend API running on http://localhost:5000
- ✅ Frontend running on http://localhost:8000
- ✅ AI Chatbot fully functional with Gemini API
- ✅ Firebase authentication working
- ✅ Real-time peer chatrooms active
- ✅ Analysis and tracking features operational

**Start exploring the platform and enjoy building mental wellness! 🌟**
