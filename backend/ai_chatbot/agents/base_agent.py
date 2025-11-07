from crewai import Agent
from typing import List, Dict
import google.generativeai as genai
from ..utils.safety_checker import SafetyChecker
from ..utils.sentiment_analyzer import SentimentAnalyzer
from ..utils.mental_state_monitor import MentalStateMonitor

class BaseAgent:
    def __init__(self, api_key: str, agent_config: Dict):
        """Initialize base agent with common functionality"""
        self.safety_checker = SafetyChecker()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.mental_state_monitor = MentalStateMonitor()
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.config = agent_config
        
    def create_agent(self) -> Agent:
        """Create a CrewAI agent with configured parameters"""
        return Agent(
            role=self.config["role"],
            goal=self.config["goal"],
            backstory=self.config["backstory"],
            verbose=self.config["verbose"],
            allow_delegation=self.config["allow_delegation"],
            tools=self.get_agent_tools()
        )
    
    async def analyze_message(self, message: str) -> Dict:
        """Analyze incoming message for sentiment and safety"""
        return {
            "sentiment": await self.sentiment_analyzer.analyze(message),
            "safety_check": await self.safety_checker.check_content(message),
            "mental_state": await self.mental_state_monitor.assess(message)
        }
    
    def get_agent_tools(self) -> List:
        """Override this method in specific agents to provide tools"""
        return []