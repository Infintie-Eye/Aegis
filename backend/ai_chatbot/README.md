# AI Mental Health Chatbot - CrewAI Implementation

## Overview

This is a **highly optimized AI-powered mental health chatbot** built using the **CrewAI framework** with **Google's
Gemini Pro API**. The system provides personalized therapeutic support through an intelligent multi-agent architecture
designed specifically for mental health care.

## Key Features

### 🎯 Core Capabilities

- **Crisis Detection & Intervention**: Real-time assessment of suicidal ideation and self-harm risk
- **Multi-Agent Therapeutic Support**: Specialized AI agents for different therapeutic modalities
- **Personalized Treatment Plans**: Adaptive responses based on user history and preferences
- **Continuous Learning**: System learns from interactions to improve support quality
- **Comprehensive Safety System**: Multi-layered safety checks and crisis protocols
- **Wellness Integration**: Holistic recommendations including yoga, nutrition, mindfulness, and spiritual practices
- **Community Matching**: Connects users with appropriate support groups and peer mentors

### 🤖 Specialized AI Agents

1. **CBT Therapist Agent**: Cognitive Behavioral Therapy techniques
2. **Crisis Detection Agent**: Suicide risk assessment and safety planning
3. **Emotional Support Agent**: Validation and empathetic listening
4. **Mindfulness Coach Agent**: Meditation and grounding techniques
5. **Progress Tracker Agent**: Treatment outcome monitoring
6. **Wellness Advisor Agent**: Holistic health recommendations
7. **Community Connector Agent**: Peer support and social connection
8. **Trauma-Informed Agent**: PTSD and trauma support
9. **Motivational Coach Agent**: Goal-setting and behavior change
10. **Cultural Competency Agent**: Culturally responsive care
11. **Family Systems Agent**: Relationship and family dynamics
12. **Grief Counselor Agent**: Bereavement and loss support
13. **Eating Disorder Specialist**: ED treatment and recovery
14. **Substance Abuse Counselor**: Addiction and recovery support
15. **Adolescent Specialist**: Youth-specific mental health support

### 🛠️ Therapeutic Tools

#### Assessment Tools

- **Crisis Assessment Tool**: Evaluates immediate danger and risk level
- **Mental Health Screening Tool**: DSM-5 aligned symptom screening
- **Emotional State Assessment Tool**: Current emotional analysis

#### Therapeutic Tools

- **CBT Cognitive Restructuring Tool**: Identifies and challenges cognitive distortions
- **Mindfulness Exercise Tool**: Guided meditation and grounding techniques
- **Behavioral Activation Tool**: Activity planning for depression

#### Emotional Support Tools

- **Emotional Validation Tool**: Empathetic validation and normalization
- **Emotional Processing Guide Tool**: Healthy emotion processing frameworks
- **Self-Compassion Tool**: Self-kindness and self-compassion practices

## Architecture

### System Components

```
MainOrchestrator
├── Memory Systems
│   ├── SessionManager
│   ├── ConversationMemory
│   ├── EmotionalMemory
│   └── UserPreferences
├── Utility Systems
│   ├── SafetyChecker
│   ├── EmotionalDetector
│   ├── WellnessRecommender
│   ├── MentalStateMonitor
│   ├── CommunityMatcher
│   └── PersonalizationEngine
├── Crews (Multi-Agent Teams)
│   ├── Crisis Intervention Crew
│   ├── Depression Support Crew
│   ├── Anxiety Intervention Crew
│   ├── Stress Management Crew
│   ├── Trauma Processing Crew
│   └── [12+ more specialized crews]
└── Tools Registry
    ├── Assessment Tools (3)
    ├── Therapeutic Tools (3)
    └── Emotional Tools (3)
```

### Processing Pipeline

1. **Safety Assessment**: Immediate crisis detection
2. **Emotional Analysis**: Comprehensive emotion and sentiment analysis
3. **Mental State Assessment**: Multi-dimensional mental health screening
4. **Memory Update**: Update all memory systems
5. **Strategy Determination**: Select optimal therapeutic approach
6. **Crew Selection**: Choose appropriate multi-agent team
7. **Task Creation**: Generate personalized therapeutic tasks
8. **Response Generation**: Execute crew with full context
9. **Wellness Recommendations**: Provide holistic wellness suggestions
10. **Community Suggestions**: Match with support resources
11. **Insights Generation**: Compile session insights
12. **Interaction Logging**: Log for continuous learning

## Installation

### Prerequisites

```bash
Python 3.10+
pip or conda
Google Gemini API Key
```

### Setup

1. **Clone the repository**

```bash
cd backend/ai_chatbot
```

2. **Install dependencies**

```bash
pip install -r ../requirements.txt
```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. **Initialize memory directories**

```bash
mkdir -p memory
```

## Usage

### Basic Usage

```python
from main_orchestrator import MainOrchestrator
import asyncio

async def main():
    # Initialize orchestrator for a user
    orchestrator = MainOrchestrator(user_id="user_123")
    
    # Process a message
    response = await orchestrator.process_message(
        message="I've been feeling really down lately and don't know what to do.",
        session_context={"session_id": "session_456"}
    )
    
    print(response['response'])
    print(response['wellness_suggestions'])
    print(response['therapeutic_guidance'])

asyncio.run(main())
```

### Response Structure

```python
{
    "response": "Therapeutic response text...",
    "response_type": "depression_support",
    "emotional_analysis": {
        "dominant_emotion": "sadness",
        "intensity": "moderate",
        "support_urgency": "high"
    },
    "mental_state": {
        "overall_score": 4.2,
        "primary_concerns": ["depression", "low_motivation"],
        "progress_indicators": []
    },
    "therapeutic_guidance": ["cognitive_approach", "behavioral_activation"],
    "wellness_suggestions": {
        "mindfulness": [...],
        "physical_activities": [...],
        "nutrition": [...]
    },
    "community_suggestions": {
        "support_groups": [...],
        "connection_priority": "high"
    },
    "safety_status": {
        "safe": true,
        "risk_level": "low",
        "monitoring_needed": false
    },
    "session_insights": {...},
    "follow_up_recommendations": [...]
}
```

### Crisis Handling

The system automatically detects crisis situations and triggers appropriate protocols:

```python
# When crisis is detected (risk_level >= 8)
crisis_response = {
    "response": "Crisis intervention response...",
    "crisis_level": 9,
    "urgency": "CRITICAL",
    "immediate_resources": [
        {"name": "National Suicide Prevention Lifeline", "contact": "988"},
        {"name": "Crisis Text Line", "contact": "Text HOME to 741741"}
    ],
    "safety_plan": {...},
    "professional_intervention_recommended": true
}
```

## Configuration

### Agent Configuration (`config/agent_config.py`)

Customize agent roles, goals, backstories, and specializations:

```python
agent_configs = {
    'cbt_therapist_agent': {
        'role': 'CBT Therapist',
        'goal': 'Help identify and challenge negative thought patterns...',
        'backstory': 'You are a licensed therapist...',
        'tools': ['therapeutic_tools', 'assessment_tools'],
        'allow_delegation': False
    },
    # ... more agents
}
```

### Crew Configuration (`config/crew_config.py`)

Define multi-agent teams for different situations:

```python
crew_configs = {
    'depression_support': {
        'agents': ['cbt_therapist_agent', 'emotional_support_agent', 
                   'motivational_coach_agent', 'wellness_advisor_agent'],
        'process': 'sequential',
        'priority': 'high'
    },
    # ... more crews
}
```

### Task Configuration (`config/task_config.py`)

Customize task descriptions and expected outputs for each therapeutic approach.

## Optimization Features

### 🚀 Performance Optimizations

1. **Intelligent Caching**: Agents and crews are cached for reuse
2. **Async Operations**: Full async/await support for concurrent processing
3. **Tool Registry**: Pre-initialized tools for instant access
4. **Batch Processing**: Efficient memory updates
5. **Rate Limit Management**: Optimized for Gemini API limits (60 RPM)

### 📊 Performance Metrics

- **Cache Efficiency**: Tracks agent/crew reuse rate
- **Response Quality**: Predicts effectiveness using learned patterns
- **Interaction Count**: Monitors engagement levels
- **Memory Optimization**: Efficient memory system updates

### 🔒 Safety Features

1. **Multi-Layer Crisis Detection**: Keyword + pattern + severity scoring
2. **Real-Time Risk Assessment**: Continuous monitoring during conversation
3. **Automatic Escalation**: Triggers appropriate protocols based on risk level
4. **Safety Plan Generation**: Personalized safety planning
5. **Resource Connection**: Immediate access to crisis resources

## Personalization

### Learning System

The system continuously learns from interactions:

- **Communication Style**: Adapts to user's preferred communication style
- **Therapeutic Approaches**: Tracks what works best for each user
- **Cultural Sensitivity**: Adapts to cultural background and values
- **Topic Preferences**: Identifies most helpful discussion areas
- **Intervention Effectiveness**: Monitors and learns from outcomes

### Memory Systems

1. **Conversation Memory**: Maintains conversation context
2. **Emotional Memory**: Tracks emotional patterns over time
3. **User Preferences**: Stores and learns user preferences
4. **Session Manager**: Manages session state and continuity

## Wellness Integration

### Holistic Recommendations

- **Mindfulness**: Meditation, breathing, grounding techniques
- **Physical Activity**: Yoga, exercise, movement therapy
- **Nutrition**: Mood-boosting meals and stress-reducing foods
- **Spiritual Practices**: Prayer, meditation, worship activities
- **Travel Therapy**: Nature therapy, retreats, cultural immersion

### Community Matching

- **Support Groups**: Matches users with relevant support groups
- **Peer Mentors**: Connects with recovered individuals
- **Community Events**: Recommends local/online mental health events

## API Integration

### Gemini Pro Optimization

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Latest model
    temperature=0.7,  # Balanced creativity
    max_tokens=4096,  # Comprehensive responses
    top_p=0.9,  # High diversity
    top_k=40,  # Optimal for nuanced responses
    convert_system_message_to_human=True
)
```

### Rate Limiting

- **Max RPM**: 60 requests per minute
- **Request Queuing**: Automatic queue management
- **Retry Logic**: Built-in retry with exponential backoff

## Testing

### Unit Tests

```bash
pytest tests/test_orchestrator.py
pytest tests/test_agents.py
pytest tests/test_tools.py
```

### Integration Tests

```bash
pytest tests/test_integration.py
```

### Load Testing

```bash
python tests/load_test.py --users 100 --duration 300
```

## Monitoring & Analytics

### Key Metrics

- **Response Time**: Average crew execution time
- **Cache Hit Rate**: Efficiency of caching system
- **Safety Incidents**: Crisis detection and intervention stats
- **User Engagement**: Interaction frequency and patterns
- **Therapeutic Outcomes**: Progress tracking metrics

### Logging

```python
# Interaction logging
{
    'user_id': 'user_123',
    'timestamp': '2024-01-01T12:00:00',
    'response_type': 'depression_support',
    'safety_level': 'low',
    'cache_efficiency': 85.5
}
```

## Best Practices

### For Developers

1. **Always handle crisis situations first**: Check safety before other processing
2. **Use async/await**: Leverage async capabilities for better performance
3. **Cache intelligently**: Reuse agents and crews when appropriate
4. **Log comprehensively**: Track all interactions for learning
5. **Test safety systems**: Regular testing of crisis detection
6. **Monitor performance**: Track cache efficiency and response times
7. **Update configurations**: Keep agent/crew configs current with best practices

### For Deployment

1. **Set appropriate rate limits**: Match your Gemini API tier
2. **Configure memory systems**: Set up persistent storage (database)
3. **Enable monitoring**: Use application monitoring tools
4. **Implement backups**: Regular backup of user data and configurations
5. **Security**: Encrypt sensitive user data, secure API keys
6. **Scaling**: Use load balancers for high traffic
7. **Compliance**: Ensure HIPAA/GDPR compliance for health data

## Limitations & Disclaimers

### Important Disclaimers

⚠️ **NOT A SUBSTITUTE FOR PROFESSIONAL CARE**: This system is a supportive tool and not a replacement for professional
mental health treatment.

⚠️ **EMERGENCY SITUATIONS**: In case of immediate danger, always call 988 (Suicide Prevention Lifeline) or 911.

⚠️ **AI LIMITATIONS**: AI can make mistakes. Always verify critical information with qualified professionals.

### Known Limitations

- **Context Window**: Limited by model's context window
- **Cultural Nuances**: May not fully capture all cultural contexts
- **Crisis Detection**: Not 100% accurate; human oversight recommended
- **Personalization**: Requires multiple interactions to optimize
- **Language**: Currently optimized for English

## Roadmap

### Planned Features

- [ ] Voice interface integration
- [ ] Multi-language support
- [ ] Video therapy session support
- [ ] Integration with wearable devices
- [ ] Expanded cultural competency
- [ ] Professional therapist collaboration features
- [ ] Mobile app integration
- [ ] Advanced progress visualization
- [ ] Family/support network features
- [ ] Insurance integration for professional referrals

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

[Your License Here]

## Support

For issues, questions, or contributions:

- GitHub Issues: [Your Repo]
- Email: [Your Email]
- Documentation: [Your Docs]

## Acknowledgments

- CrewAI Framework
- Google Gemini API
- Evidence-based therapeutic modalities (CBT, DBT, ACT, etc.)
- Mental health research community

---

**Built with ❤️ for mental health support**
