from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis")

    def analyze(self, text):
        result = self.pipeline(text)[0]
        return {
            'label': result['label'],
            'score': result['score']
        }