import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from .config.agent_config import agent_configs
from .config.crew_config import crew_configs
from .config.task_config import task_configs
from .memory.session_manager import SessionManager
from .memory.conversation_memory import ConversationMemory
from .memory.emotional_memory import EmotionalMemory
from .memory.user_preferences import UserPreferences
from .models.user_context import UserContext
from .utils.safety_checker import SafetyChecker

load_dotenv()

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

class MainOrchestrator:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_manager = SessionManager(user_id)
        self.conversation_memory = ConversationMemory(user_id)
        self.emotional_memory = EmotionalMemory(user_id)
        self.user_preferences = UserPreferences(user_id)
        self.safety_checker = SafetyChecker()
        self.user_context = UserContext(user_id)

    def process_message(self, message):
        # Check for safety (crisis, harmful content, etc.)
        safety_check = self.safety_checker.check(message)
        if safety_check['crisis_detected']:
            # Handle crisis: trigger crisis crew
            return self.handle_crisis(message)
        
        # Update conversation memory
        self.conversation_memory.add_message(message)
        
        # Update emotional state (using emotional detector)
        emotional_state = self.update_emotional_state(message)
        
        # Determine which crew to use based on context
        crew_type = self.determine_crew_type(emotional_state, message)
        
        # Create the crew
        crew = self.create_crew(crew_type)
        
        # Define the task
        task = Task(
            description=task_configs[crew_type]['description'],
            agent=crew_configs[crew_type]['agent'],
            expected_output=task_configs[crew_type]['expected_output']
        )
        
        # Run the crew
        result = crew.kickoff(inputs={'message': message, 'user_context': self.user_context})
        
        # Update memory and preferences
        self.update_memory_and_preferences(result, emotional_state)
        
        return result

    def handle_crisis(self, message):
        # Create crisis assessment crew
        crew = self.create_crew('crisis_assessment')
        task = Task(
            description=task_configs['crisis_assessment']['description'],
            agent=crew_configs['crisis_assessment']['agent'],
            expected_output=task_configs['crisis_assessment']['expected_output']
        )
        result = crew.kickoff(inputs={'message': message, 'user_context': self.user_context})
        # In a real crisis, we might also trigger emergency protocols
        return result

    def update_emotional_state(self, message):
        # Use emotional detector to get emotional state
        from .utils.emotional_detector import EmotionalDetector
        detector = EmotionalDetector()
        emotional_state = detector.detect(message)
        self.emotional_memory.update(emotional_state)
        return emotional_state

    def determine_crew_type(self, emotional_state, message):
        # Logic to determine which crew to use based on emotional state and message content
        # This is a simplified version; in practice, it would be more complex
        if emotional_state.get('crisis', False):
            return 'crisis_assessment'
        elif emotional_state.get('negative_emotion') in ['anxiety', 'stress']:
            return 'intervention'
        else:
            return 'mental_support'

    def create_crew(self, crew_type):
        # Create agents for the crew
        agents = []
        for agent_name in crew_configs[crew_type]['agents']:
            agent_config = agent_configs[agent_name]
            agent = Agent(
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config['backstory'],
                llm=llm,
                verbose=True,
                allow_delegation=False,
                tools=agent_config.get('tools', [])
            )
            agents.append(agent)
        
        # Create the crew
        crew = Crew(
            agents=agents,
            tasks=[],  # We will add the task separately
            verbose=2,
            process=Process.sequential  # or Process.hierarchical, depending on the crew
        )
        return crew

    def update_memory_and_preferences(self, result, emotional_state):
        # Update conversation memory with the response
        self.conversation_memory.add_message(result, is_response=True)
        # Update user preferences based on the interaction
        self.user_preferences.update_from_interaction(result, emotional_state)
        # Update user context
        self.user_context.update(result, emotional_state)