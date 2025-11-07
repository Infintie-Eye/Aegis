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
from .utils.emotion_detector import EmotionalDetector
from .utils.wellness_recommender import WellnessRecommender
from .utils.mental_state_monitor import MentalStateMonitor
from .utils.community_matcher import CommunityMatcher
from .utils.personalization_engine import PersonalizationEngine

load_dotenv()

# Initialize the LLM with optimized settings
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_tokens=2048,
    top_p=0.8
)

class MainOrchestrator:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_manager = SessionManager(user_id)
        self.conversation_memory = ConversationMemory(user_id)
        self.emotional_memory = EmotionalMemory(user_id)
        self.user_preferences = UserPreferences(user_id)
        self.safety_checker = SafetyChecker()
        self.emotion_detector = EmotionalDetector()
        self.wellness_recommender = WellnessRecommender()
        self.mental_state_monitor = MentalStateMonitor(user_id)
        self.community_matcher = CommunityMatcher()
        self.personalization_engine = PersonalizationEngine(user_id)
        self.user_context = UserContext(user_id)

        # Initialize agents cache for efficiency
        self._agents_cache = {}
        self._crews_cache = {}

    async def process_message(self, message, session_context=None):
        """Main message processing with enhanced mental health support"""
        try:
            # Update session context
            if session_context:
                self.session_manager.update_context(session_context)

            # Safety and crisis detection
            safety_check = await self.safety_checker.comprehensive_check(message)
            if safety_check['crisis_level'] >= 8:  # High crisis level
                return await self.handle_crisis(message, safety_check)

            # Advanced emotional analysis
            emotional_analysis = await self.emotion_detector.comprehensive_analyze(message)

            # Update memories and context
            await self._update_user_state(message, emotional_analysis)

            # Mental state monitoring
            mental_state = await self.mental_state_monitor.assess_current_state(
                message, emotional_analysis, self.user_context
            )

            # Determine optimal response strategy
            response_strategy = await self._determine_response_strategy(
                message, emotional_analysis, mental_state
            )

            # Generate personalized response
            response = await self._generate_response(message, response_strategy)

            # Add wellness recommendations if appropriate
            wellness_suggestions = await self._get_wellness_suggestions(mental_state)

            # Community matching for peer support
            community_suggestions = await self._get_community_suggestions()

            # Compile comprehensive response
            final_response = {
                'response': response,
                'emotional_state': emotional_analysis,
                'mental_state_score': mental_state['overall_score'],
                'wellness_suggestions': wellness_suggestions,
                'community_suggestions': community_suggestions,
                'safety_status': safety_check,
                'session_insights': await self._get_session_insights()
            }

            # Log interaction for learning
            await self._log_interaction(message, final_response)

            return final_response

        except Exception as e:
            # Fallback response with safety
            return await self._handle_error_response(str(e), message)

    async def handle_crisis(self, message, safety_check):
        """Enhanced crisis handling with immediate intervention"""
        # Create crisis intervention crew
        crisis_crew = await self._get_or_create_crew('crisis_intervention')

        # Enhanced crisis task
        crisis_task = Task(
            description=f"""URGENT CRISIS INTERVENTION NEEDED:
            User message: {message}
            Crisis indicators: {safety_check['crisis_indicators']}
            Crisis level: {safety_check['crisis_level']}/10
            User context: {self.user_context.get_crisis_context()}
            
            Provide immediate support, safety planning, and resource connections.
            """,
            agent=crisis_crew.agents[0],
            expected_output="Immediate crisis response with safety plan and resources"
        )

        # Execute crisis intervention
        crisis_response = await crisis_crew.kickoff_async(
            inputs={
                'message': message,
                'user_context': self.user_context,
                'crisis_level': safety_check['crisis_level']
            }
        )

        # Immediate notifications and escalations
        await self._trigger_crisis_protocols(safety_check['crisis_level'])

        return {
            'response': crisis_response,
            'crisis_level': safety_check['crisis_level'],
            'immediate_resources': await self._get_crisis_resources(),
            'safety_plan': await self._generate_safety_plan(),
            'emergency_contacts': await self._get_emergency_contacts()
        }

    async def _determine_response_strategy(self, message, emotional_analysis, mental_state):
        """Determine optimal response strategy based on user state"""
        # Analyze patterns and context
        conversation_history = self.conversation_memory.get_recent_context(limit=10)
        emotional_trajectory = self.emotional_memory.get_emotional_trajectory(days=7)
        user_preferences = await self.user_preferences.get_current_preferences()

        # Strategy selection algorithm
        if mental_state['depression_indicators'] > 0.7:
            return 'depression_focused'
        elif mental_state['anxiety_indicators'] > 0.7:
            return 'anxiety_management'
        elif mental_state['stress_indicators'] > 0.6:
            return 'stress_reduction'
        elif emotional_analysis['dominant_emotion'] in ['loneliness', 'isolation']:
            return 'social_connection'
        elif mental_state['motivation_level'] < 0.3:
            return 'motivation_building'
        else:
            return 'general_support'

    async def _generate_response(self, message, strategy):
        """Generate personalized therapeutic response using appropriate crew"""
        # Select optimal crew based on strategy
        crew_type = self._map_strategy_to_crew(strategy)
        crew = await self._get_or_create_crew(crew_type)

        # Create personalized task
        task = await self._create_personalized_task(message, strategy, crew_type)

        # Execute with personalization
        response = await crew.kickoff_async(inputs={
            'message': message,
            'user_context': self.user_context,
            'strategy': strategy,
            'personalization': await self.personalization_engine.get_personalization_profile()
        })

        return response

    async def _get_wellness_suggestions(self, mental_state):
        """Get personalized wellness activity suggestions"""
        user_profile = await self.user_preferences.get_wellness_profile()

        suggestions = []

        # Mindfulness and meditation
        if mental_state['stress_indicators'] > 0.6:
            mindfulness_activities = await self.wellness_recommender.get_mindfulness_activities(
                stress_level=mental_state['stress_indicators'],
                user_preferences=user_profile
            )
            suggestions.extend(mindfulness_activities)

        # Physical activities (yoga, exercise)
        if mental_state['energy_level'] < 0.4:
            physical_activities = await self.wellness_recommender.get_physical_activities(
                energy_level=mental_state['energy_level'],
                fitness_level=user_profile.get('fitness_level', 'moderate')
            )
            suggestions.extend(physical_activities)

        # Spiritual/worship activities
        if user_profile.get('spiritual_interests'):
            spiritual_activities = await self.wellness_recommender.get_spiritual_activities(
                spiritual_preferences=user_profile['spiritual_interests']
            )
            suggestions.extend(spiritual_activities)

        # Nutrition recommendations
        if mental_state['mood_indicators'] < 0.5:
            nutrition_suggestions = await self.wellness_recommender.get_nutrition_recommendations(
                mood_state=mental_state['mood_indicators']
            )
            suggestions.extend(nutrition_suggestions)

        # Travel and adventure therapy
        if mental_state['stagnation_indicators'] > 0.6:
            travel_suggestions = await self.wellness_recommender.get_travel_therapy_suggestions(
                budget=user_profile.get('budget_range', 'moderate'),
                location=user_profile.get('location')
            )
            suggestions.extend(travel_suggestions)

        return suggestions

    async def _get_community_suggestions(self):
        """Get community connection suggestions for peer support"""
        user_profile = await self.user_preferences.get_community_profile()
        current_struggles = await self.mental_state_monitor.get_current_struggles()

        # Find matching support groups
        support_groups = await self.community_matcher.find_matching_groups(
            struggles=current_struggles,
            demographics=user_profile.get('demographics', {}),
            preferences=user_profile.get('group_preferences', {})
        )

        # Find peer mentors
        peer_mentors = await self.community_matcher.find_peer_mentors(
            current_state=current_struggles,
            recovery_stage=user_profile.get('recovery_stage', 'beginning')
        )

        return {
            'support_groups': support_groups,
            'peer_mentors': peer_mentors,
            'community_events': await self.community_matcher.get_upcoming_events()
        }

    async def _get_or_create_crew(self, crew_type):
        """Efficiently manage crew instances with caching"""
        if crew_type in self._crews_cache:
            return self._crews_cache[crew_type]

        # Create agents for the crew
        agents = []
        crew_config = crew_configs[crew_type]

        for agent_name in crew_config['agents']:
            if agent_name in self._agents_cache:
                agents.append(self._agents_cache[agent_name])
            else:
                agent_config = agent_configs[agent_name]
                agent = Agent(
                    role=agent_config['role'],
                    goal=agent_config['goal'],
                    backstory=agent_config['backstory'],
                    llm=llm,
                    verbose=True,
                    allow_delegation=agent_config.get('allow_delegation', False),
                    tools=await self._get_agent_tools(agent_config.get('tools', [])),
                    memory=True,
                    max_iter=5,
                    max_execution_time=30
                )
                self._agents_cache[agent_name] = agent
                agents.append(agent)

        # Create the crew with optimization
        crew = Crew(
            agents=agents,
            tasks=[],
            verbose=2,
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=30,
            share_crew=True
        )

        self._crews_cache[crew_type] = crew
        return crew

    async def _create_personalized_task(self, message, strategy, crew_type):
        """Create a personalized task based on user context and strategy"""
        base_config = task_configs[crew_type]
        personalization = await self.personalization_engine.get_task_personalization(strategy)

        enhanced_description = f"""
        {base_config['description']}
        
        PERSONALIZATION CONTEXT:
        - User's preferred communication style: {personalization['communication_style']}
        - Cultural considerations: {personalization['cultural_factors']}
        - Previous successful interventions: {personalization['successful_approaches']}
        - Current life situation: {personalization['life_context']}
        - Therapeutic goals: {personalization['therapeutic_goals']}
        
        USER MESSAGE: {message}
        RESPONSE STRATEGY: {strategy}
        
        Provide a response that is culturally sensitive, matches their communication preferences,
        and builds on previous successful interventions while addressing their current needs.
        """

        return Task(
            description=enhanced_description,
            expected_output=base_config['expected_output'],
            context=await self._get_task_context()
        )

    async def _update_user_state(self, message, emotional_analysis):
        """Update user state across all memory systems"""
        # Update conversation memory
        await self.conversation_memory.add_message_async(message)

        # Update emotional memory with detailed analysis
        await self.emotional_memory.update_emotional_state_async(emotional_analysis)

        # Update user context
        await self.user_context.update_context_async({
            'latest_message': message,
            'emotional_state': emotional_analysis,
            'timestamp': datetime.now().isoformat()
        })

        # Update personalization engine
        await self.personalization_engine.learn_from_interaction(message, emotional_analysis)

    async def _get_session_insights(self):
        """Generate session insights for user awareness"""
        return {
            'emotional_progress': await self.emotional_memory.get_progress_summary(),
            'conversation_patterns': await self.conversation_memory.get_pattern_analysis(),
            'wellness_streaks': await self.wellness_recommender.get_activity_streaks(),
            'support_network_engagement': await self.community_matcher.get_engagement_metrics()
        }

    async def _trigger_crisis_protocols(self, crisis_level):
        """Trigger appropriate crisis intervention protocols"""
        if crisis_level >= 9:
            # Immediate intervention required
            await self._notify_emergency_contacts()
            await self._log_crisis_incident('high_risk')
        elif crisis_level >= 7:
            # Elevated support needed
            await self._schedule_follow_up()
            await self._log_crisis_incident('moderate_risk')

    def _map_strategy_to_crew(self, strategy):
        """Map response strategy to appropriate crew type"""
        strategy_mapping = {
            'depression_focused': 'depression_support',
            'anxiety_management': 'anxiety_intervention',
            'stress_reduction': 'stress_management',
            'social_connection': 'community_building',
            'motivation_building': 'motivation_enhancement',
            'general_support': 'mental_support'
        }
        return strategy_mapping.get(strategy, 'mental_support')

    async def _get_agent_tools(self, tool_names):
        """Load and return agent tools"""
        tools = []
        for tool_name in tool_names:
            tool_module = __import__(f'tools.{tool_name}', fromlist=[tool_name])
            tools.append(getattr(tool_module, tool_name.title().replace('_', '') + 'Tool')())
        return tools

    async def _handle_error_response(self, error, message):
        """Provide safe fallback response in case of errors"""
        return {
            'response': "I'm here to listen and support you. Sometimes I need a moment to process everything properly. Could you share a bit more about how you're feeling right now?",
            'error': error,
            'safety_status': {'safe': True, 'crisis_level': 0},
            'fallback_resources': await self._get_general_resources()
        }

    async def _log_interaction(self, message, response):
        """Log interaction for learning and improvement"""
        interaction_log = {
            'user_id': self.user_id,
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response_quality': response.get('quality_metrics', {}),
            'emotional_state': response.get('emotional_state', {}),
            'intervention_type': response.get('intervention_type', 'general')
        }

        # Store in memory system for learning
        await self.conversation_memory.log_interaction_async(interaction_log)

    # Additional helper methods for crisis resources, safety plans, etc.
    async def _get_crisis_resources(self):
        """Get immediate crisis intervention resources"""
        return [
            {
                'type': 'hotline',
                'name': 'National Suicide Prevention Lifeline',
                'contact': '988',
                'available': '24/7'
            },
            {
                'type': 'text_support',
                'name': 'Crisis Text Line',
                'contact': 'Text HOME to 741741',
                'available': '24/7'
            }
        ]

    async def _generate_safety_plan(self):
        """Generate personalized safety plan"""
        user_resources = await self.user_preferences.get_support_network()
        coping_strategies = await self.wellness_recommender.get_emergency_coping_strategies()

        return {
            'warning_signs': await self._identify_personal_warning_signs(),
            'coping_strategies': coping_strategies,
            'support_contacts': user_resources.get('emergency_contacts', []),
            'safe_environment_steps': await self._get_environment_safety_steps(),
            'professional_contacts': await self._get_professional_contacts()
        }
