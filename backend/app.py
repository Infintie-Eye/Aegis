from ai_chatbot.main_orchestrator import MainOrchestrator

# Initialize for a user
orchestrator = MainOrchestrator(user_id="user123")

# Process a message
response = orchestrator.process_message("I've been feeling really anxious lately")
print(response)