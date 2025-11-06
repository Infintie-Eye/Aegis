from transformers import pipeline

class EmotionalDetector:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

    def detect(self, text):
        # Sentiment analysis
        sentiment = self.sentiment_pipeline(text)[0]
        
        # Emotion classification
        emotions = self.emotion_pipeline(text)[0]
        
        # Determine if there's a crisis (simplified)
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hopeless', 'worthless']
        crisis = any(keyword in text.lower() for keyword in crisis_keywords)
        
        return {
            'sentiment': sentiment['label'],
            'sentiment_score': sentiment['score'],
            'emotion': emotions['label'],
            'emotion_score': emotions['score'],
            'crisis': crisis
        }