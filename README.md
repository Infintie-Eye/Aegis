# Aegis - Intelligent Mental Wellness Platform

<div align="center">

![Aegis Logo](https://img.shields.io/badge/Aegis-Mental%20Wellness-4F46E5?style=for-the-badge&logo=shield&logoColor=white)

**Bridging AI Empathy with Human Connection**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Cloud-orange?style=flat-square&logo=firebase)](https://firebase.google.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-purple?style=flat-square&logo=google)](https://ai.google.dev/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-red?style=flat-square)](https://github.com/joaomdmoura/crewAI)

</div>

---

## 🌟 Overview

**Aegis** is an AI-powered mental wellness platform designed to provide personalized, scalable, and secure emotional
support. It combines cutting-edge AI technology with peer support communities to create a comprehensive mental health
solution.

### Core Features

🤖 **AI Companion**

- Powered by Google Gemini API and CrewAI multi-agent system
- 15+ specialized therapeutic AI agents (CBT, mindfulness, crisis intervention, etc.)
- Personalized responses based on emotional state and history
- Real-time crisis detection and intervention
- Wellness recommendations (yoga, nutrition, mindfulness, spiritual practices)

👥 **Peer Support Communities**

- Anonymous, secure chatrooms for specific challenges
- Real-time messaging via Firebase Firestore
- Themed spaces: Depression, Anxiety, Academic Stress, Work Stress, Relationships, Loneliness
- AI-powered moderation and safety protocols

📊 **Mental Health Analysis**

- Mood tracking and progress monitoring
- Emotional sentiment analysis
- Voice analysis (placeholder for future implementation)
- Personality insights and recommendations

🛡️ **Safety & Privacy**

- End-to-end encryption ready
- Crisis detection with immediate resource provision
- Anonymous user support
- Firebase Authentication integration
- GDPR/HIPAA compliance ready architecture

---

## 📋 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one free](https://ai.google.dev/))
- Firebase project ([Create one](https://console.firebase.google.com/))

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/aegis.git
cd aegis
```

**2. Set up backend:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**3. Configure environment variables:**

Create `backend/.env`:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
PORT=5000
```

Create `backend/ai_chatbot/.env`:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
```

**4. Start the application:**

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**

```bash
cd frontend
python -m http.server 8000
```

**5. Open browser:**

- Frontend: http://localhost:8000
- Backend API: http://localhost:5000
- AI Chatbot: http://localhost:8000/pages/aichatbot.html

---

## 📁 Project Structure

```
Aegis/
├── backend/
│   ├── ai_chatbot/              # AI chatbot with CrewAI
│   │   ├── agents/              # 15+ specialized AI agents
│   │   ├── config/              # Agent and crew configurations
│   │   ├── memory/              # Conversation & emotional memory
│   │   ├── utils/               # Safety, wellness, community matching
│   │   ├── main_orchestrator.py # Core AI orchestration
│   │   └── .env                 # Gemini API key
│   ├── routes/
│   │   ├── chat_routes.py       # AI chatbot API endpoints
│   │   ├── analysis_routes.py   # Analysis & mood tracking
│   │   ├── room_routes.py       # Chatroom management
│   │   └── auth_routes.py       # Authentication endpoints
│   ├── app.py                   # Main Flask application
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Backend configuration
├── frontend/
│   ├── pages/
│   │   ├── index.html           # Landing page
│   │   ├── aichatbot.html       # AI chatbot interface ⭐
│   │   ├── community_list.html  # Chatroom directory
│   │   ├── depression.html      # Depression support chatroom
│   │   ├── anxiety.html         # Anxiety support chatroom
│   │   ├── academic.html        # Academic stress chatroom
│   │   ├── work.html            # Work stress chatroom
│   │   ├── relationship.html    # Relationship issues chatroom
│   │   ├── lonliness.html       # Loneliness support chatroom
│   │   ├── analysis.html        # Mental health analysis
│   │   ├── userdashboard.html   # User dashboard
│   │   ├── profile.html         # User profile
│   │   ├── login.html           # Login page
│   │   └── sign_up.html         # Sign up page
│   ├── js/
│   │   ├── firebase.js          # Firebase configuration
│   │   ├── ai-chatbot.js        # AI chatbot frontend ⭐
│   │   ├── chat.js              # Firebase real-time chat
│   │   ├── authguard.js         # Route protection
│   │   ├── sidebar.js           # Navigation sidebar
│   │   └── navbar.js            # Navigation bar
│   └── css/                     # Stylesheets
├── documentation/
│   └── API_DOCUMENTATION.md
├── INTEGRATION_GUIDE.md         # Complete integration guide
├── QUICKSTART.md                # Quick start instructions
├── start_backend.bat            # Windows backend launcher
└── start_frontend.bat           # Windows frontend launcher
```

---

## 🎯 Key Features Explained

### 1. AI Companion (Chatbot)

**Technology Stack:**

- Google Gemini Pro API for natural language processing
- CrewAI for multi-agent orchestration
- 15 specialized therapeutic agents

**Capabilities:**

- **Emotional Support**: Empathetic listening and validation
- **CBT Therapy**: Cognitive behavioral therapy techniques
- **Crisis Intervention**: Suicide risk assessment and safety planning
- **Mindfulness Coaching**: Meditation and stress reduction
- **Progress Tracking**: Monitor emotional trends over time
- **Wellness Recommendations**: Personalized activities
- **Community Matching**: Connect with relevant support groups

**How to Use:**

1. Navigate to `/pages/aichatbot.html`
2. Type your message (e.g., "I've been feeling really anxious lately")
3. Receive personalized AI response with:
    - Therapeutic advice
    - Emotional validation
    - Wellness suggestions (breathing exercises, mindfulness, etc.)
    - Community recommendations
    - Crisis resources (if needed)

**API Endpoint:**

```javascript
POST /api/chat/message
{
  "message": "Your message here",
  "user_id": "user123",
  "session_context": {}
}
```

### 2. Peer Support Chatrooms

**Available Rooms:**

- Depression Support
- Anxiety Support
- Academic Stress
- Work Stress
- Relationship Issues
- Loneliness & Isolation

**Features:**

- Real-time messaging via Firebase Firestore
- Anonymous user support with auto-generated names
- Message persistence and history
- User presence indicators
- Safe, moderated environment

**How to Use:**

1. Go to `/pages/community_list.html`
2. Choose a chatroom matching your needs
3. Start chatting with peers in similar situations
4. Your identity is protected with anonymous usernames

### 3. Mental Health Analysis

**Features:**

- **Mood Tracking**: Log daily mood and intensity
- **Progress Analysis**: View trends and patterns
- **Sentiment Analysis**: Analyze text for emotional state
- **Voice Analysis**: (Placeholder for future implementation)
- **Personality Insights**: Comprehensive analysis tools

**API Endpoints:**

```javascript
// Track mood
POST /api/analysis/mood
{
  "user_id": "user123",
  "mood": "happy",
  "intensity": 7,
  "notes": "Had a great day"
}

// Get progress
GET /api/analysis/progress/user123
```

---

## 🔗 Integration Details

### Backend ↔ Frontend Connection

#### AI Chatbot Flow

```
User message (aichatbot.html)
    ↓
frontend/js/ai-chatbot.js
    ↓
POST /api/chat/message
    ↓
backend/routes/chat_routes.py
    ↓
ai_chatbot/main_orchestrator.py
    ↓
CrewAI agents + Gemini API
    ↓
Response with therapy + wellness + community
    ↓
Display in frontend with rich formatting
```

#### Chatroom Flow

```
User opens chatroom page
    ↓
frontend/js/chat.js initializes
    ↓
Firebase Firestore listener
    ↓
Real-time message sync
    ↓
/chatrooms/{roomId}/messages collection
```

#### Analysis Flow

```
User tracks mood
    ↓
POST /api/analysis/mood
    ↓
backend/routes/analysis_routes.py
    ↓
Store mood data
    ↓
GET /api/analysis/progress/{user_id}
    ↓
Return insights and trends
```

### Adding AI Chatbot to Frontend

To integrate the AI chatbot into `aichatbot.html`, add this before the closing `</body>` tag:

```html
<!-- Add this line -->
<script src="../js/ai-chatbot.js"></script>
<script src="../js/sidebar.js"></script>
</body>
</html>
```

The `ai-chatbot.js` script handles:

- User input capture
- API communication
- Response rendering
- Wellness suggestions display
- Community recommendations
- Crisis resource display

---

## 🚀 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### Chat Endpoints

| Method | Endpoint                   | Description                |
|--------|----------------------------|----------------------------|
| POST   | `/chat/message`            | Send message to AI chatbot |
| GET    | `/chat/history/<user_id>`  | Get chat history           |
| GET    | `/chat/insights/<user_id>` | Get user insights          |
| GET    | `/chat/wellness/<user_id>` | Get wellness suggestions   |
| DELETE | `/chat/clear/<user_id>`    | Clear user data            |

#### Room Endpoints

| Method | Endpoint                 | Description         |
|--------|--------------------------|---------------------|
| GET    | `/rooms/list`            | List all chatrooms  |
| GET    | `/rooms/<room_id>`       | Get room details    |
| POST   | `/rooms/<room_id>/join`  | Join a room         |
| POST   | `/rooms/<room_id>/leave` | Leave a room        |
| GET    | `/rooms/categories`      | Get room categories |

#### Analysis Endpoints

| Method | Endpoint                       | Description            |
|--------|--------------------------------|------------------------|
| POST   | `/analysis/mood`               | Track mood             |
| GET    | `/analysis/mood/<user_id>`     | Get mood history       |
| GET    | `/analysis/progress/<user_id>` | Get progress analysis  |
| POST   | `/analysis/voice-analysis`     | Analyze voice          |
| POST   | `/analysis/sentiment`          | Analyze text sentiment |

#### Auth Endpoints

| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| POST   | `/auth/register`  | Register new user        |
| POST   | `/auth/login`     | Login user               |
| POST   | `/auth/anonymous` | Create anonymous session |
| POST   | `/auth/verify`    | Verify session token     |
| POST   | `/auth/logout`    | Logout user              |

---

## 🧪 Testing

### Test Backend Health

```bash
curl http://localhost:5000/health
```

### Test AI Chatbot

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need someone to talk to", "user_id": "test_user"}'
```

### Test Chatrooms

```bash
curl http://localhost:5000/api/rooms/list
```

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Complete integration documentation
- **[backend/ai_chatbot/README.md](backend/ai_chatbot/README.md)** - AI chatbot technical details
- **[API_DOCUMENTATION.md](documentation/API_DOCUMENTATION.md)** - Complete API reference

---

## 🛠️ Technology Stack

### Backend

- **Flask** - Web framework
- **CrewAI** - Multi-agent AI orchestration
- **Google Gemini Pro** - Large language model
- **LangChain** - LLM framework
- **Python-dotenv** - Environment management

### Frontend

- **Vanilla JavaScript** - No framework dependencies
- **Firebase** - Authentication & real-time database
- **HTML5 & CSS3** - Modern web standards

### AI/ML

- **Transformers** - NLP models
- **Scikit-learn** - Machine learning utilities
- **NLTK** - Natural language toolkit
- **spaCy** - Advanced NLP
- **VaderSentiment** - Sentiment analysis

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

Built with ❤️ by Team Aegis at Guru Nanak Dev University, Amritsar, Punjab, India

---

## 🙏 Acknowledgments

- Google for Gemini API
- Firebase for backend infrastructure
- CrewAI community for multi-agent framework
- All contributors and mental health advocates

---

## 📞 Support

- **Email**: team@aegis.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/aegis/issues)
- **Documentation**: [Full Docs](documentation/)

---

## ⚠️ Disclaimer

**Aegis is NOT a substitute for professional mental health care.**

If you're experiencing a mental health crisis:

- **Call 988** - National Suicide Prevention Lifeline
- **Text HOME to 741741** - Crisis Text Line
- **Call 911** - For immediate emergency

Always consult with qualified mental health professionals for diagnosis and treatment.

---

<div align="center">

**Building Mental Wellness Through Technology** 🌟

[Website](https://aegis.com) • [Documentation](https://docs.aegis.com) • [Community](https://community.aegis.com)

</div>