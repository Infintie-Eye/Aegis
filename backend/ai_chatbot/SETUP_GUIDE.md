# Quick Setup Guide

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

## Step 2: Set Up Environment

Create a `.env` file in the `backend` directory:

```bash
cd backend
touch .env
```

Add your API key to the `.env` file:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

## Step 3: Install Dependencies

```bash
# Make sure you're in the backend directory
cd backend

# Install all requirements
pip install -r requirements.txt
```

**Note:** If you encounter issues with specific packages, install them individually:

```bash
pip install crewai==0.51.0
pip install crewai-tools==0.8.3
pip install langchain-google-genai==1.0.10
pip install google-generativeai==0.7.2
```

## Step 4: Create Memory Directory

```bash
mkdir -p ai_chatbot/memory
```

## Step 5: Test the Installation

Run the example script:

```bash
cd ai_chatbot
python example_usage.py
```

## Step 6: Verify Everything Works

You should see output like:

```
================================================================================
EXAMPLE 1: Basic Emotional Support
================================================================================

USER: I've been feeling really down lately...

CHATBOT: [Response from the AI chatbot]
```

## Troubleshooting

### Issue: ImportError for crewai

**Solution:** Make sure you have the correct versions:

```bash
pip install --upgrade crewai crewai-tools
```

### Issue: Google API Key Error

**Solution:**

1. Check that your `.env` file is in the `backend` directory
2. Verify your API key is correct
3. Make sure there are no extra spaces in the `.env` file

### Issue: Memory/Context Window Errors

**Solution:** The system is optimized for Gemini 1.5 Pro. If you need to use a different model, update the model name in
`main_orchestrator.py`:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # or "gemini-pro"
    ...
)
```

### Issue: Rate Limit Errors

**Solution:** The system is set to 60 RPM. If you're on a free tier, reduce the `max_rpm` in `main_orchestrator.py`:

```python
crew = Crew(
    ...
    max_rpm=10,  # Reduce for free tier
    ...
)
```

## Next Steps

1. **Customize Agents**: Edit `config/agent_config.py` to customize agent behaviors
2. **Adjust Crews**: Modify `config/crew_config.py` to change crew compositions
3. **Tune Tasks**: Update `config/task_config.py` for different therapeutic approaches
4. **Add Tools**: Create new tools in the `tools/` directory
5. **Integrate with Frontend**: Connect the orchestrator to your web application

## Integration Example

```python
# In your FastAPI/Flask app
from ai_chatbot.main_orchestrator import MainOrchestrator

@app.post("/api/chat")
async def chat(user_id: str, message: str):
    orchestrator = MainOrchestrator(user_id=user_id)
    response = await orchestrator.process_message(message)
    return response
```

## Performance Tips

1. **Enable Caching**: Caching is enabled by default. Agents and crews are reused across requests.
2. **Batch Requests**: Process multiple messages for the same user in the same session when possible.
3. **Monitor Usage**: Track `cache_efficiency` in responses to monitor performance.
4. **Optimize for Production**: Set `verbose=False` in crew/agent configs for production.

## Security Considerations

1. **API Key Security**: Never commit `.env` files to version control
2. **User Data**: Implement proper encryption for user conversations
3. **HIPAA Compliance**: If handling PHI, ensure proper security measures
4. **Rate Limiting**: Implement rate limiting in your API layer
5. **Input Validation**: Sanitize all user inputs before processing

## Support

If you encounter issues:

1. Check the logs in `memory/` directory
2. Review the error messages
3. Consult the main README.md
4. Test with the example script first

## Quick Reference

### Start a Conversation

```python
orchestrator = MainOrchestrator(user_id="user_123")
response = await orchestrator.process_message("I need help...")
```

### Get User Progress

```python
progress = await orchestrator.get_user_progress_report()
```

### Clear Caches (if needed)

```python
orchestrator.clear_caches()
```

---

**You're all set!** 🎉 Start building your AI-powered mental health support system.
