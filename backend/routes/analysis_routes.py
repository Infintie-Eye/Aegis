from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random
from typing import TypedDict

class MoodEntry(TypedDict):
    timestamp: str
    mood: str
    intensity: int
    notes: str

bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

# In-memory storage (replace with database in production)
mood_data = {}
progress_data = {}


@bp.route('/mood', methods=['POST'])
def track_mood():
    """Track user mood"""
    try:
        data = request.get_json()

        user_id = data.get('user_id', 'anonymous')
        mood = data.get('mood')
        intensity = data.get('intensity', 5)
        notes = data.get('notes', '')

        mood_entry: MoodEntry = {
            'timestamp': datetime.now(datetime.timezone.utc).isoformat(),
            'mood': mood,
            'intensity': intensity,
            'notes': notes
        }

        mood_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'mood': mood,
            'intensity': intensity,
            'notes': notes
        }

        mood_data[user_id].append(mood_entry)

        return jsonify({
            'status': 'success',
            'message': 'Mood tracked successfully',
            'data': mood_entry
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/mood/<user_id>', methods=['GET'])
def get_mood_history(user_id):
    """Get mood history for a user"""
    try:
        days = request.args.get('days', 30, type=int)

        user_moods = mood_data.get(user_id, [])

        # Filter by date range
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        filtered_moods = [
            m for m in user_moods
            if datetime.fromisoformat(m['timestamp']) > cutoff_date
        ]

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'moods': filtered_moods,
            'count': len(filtered_moods),
            'period_days': days
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/progress/<user_id>', methods=['GET'])
def get_progress_analysis(user_id):
    """Get progress analysis for a user"""
    try:
        # Generate progress insights
        user_moods = mood_data.get(user_id, [])

        if not user_moods:
            return jsonify({
                'status': 'success',
                'user_id': user_id,
                'message': 'No data available yet',
                'analysis': {}
            }), 200

        # Calculate statistics
        total_entries = len(user_moods)
        avg_intensity = sum(m['intensity'] for m in user_moods) / total_entries

        # Mood distribution
        mood_counts = {}
        for m in user_moods:
            mood_counts[m['mood']] = mood_counts.get(m['mood'], 0) + 1

        # Trend analysis (simplified)
        recent_moods = user_moods[-7:] if len(user_moods) >= 7 else user_moods
        recent_avg = sum(m['intensity'] for m in recent_moods) / len(recent_moods)

        trend = 'improving' if recent_avg > avg_intensity else 'declining' if recent_avg < avg_intensity else 'stable'

        analysis = {
            'total_entries': total_entries,
            'average_intensity': round(avg_intensity, 2),
            'recent_average': round(recent_avg, 2),
            'trend': trend,
            'mood_distribution': mood_counts,
            'first_entry': user_moods[0]['timestamp'],
            'latest_entry': user_moods[-1]['timestamp']
        }

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'analysis': analysis
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/voice-analysis', methods=['POST'])
def analyze_voice():
    """Analyze voice for emotional state (placeholder)"""
    try:
        data = request.get_json()

        user_id = data.get('user_id', 'anonymous')
        audio_data = data.get('audio_data')

        if not audio_data:
            return jsonify({'error': 'Audio data is required'}), 400

        # Placeholder analysis (implement actual voice analysis)
        analysis = {
            'emotional_state': random.choice(['calm', 'stressed', 'anxious', 'happy', 'sad']),
            'stress_level': round(random.uniform(0, 1), 2),
            'confidence': round(random.uniform(0.7, 0.95), 2),
            'recommendations': [
                'Consider deep breathing exercises',
                'Take a short break',
                'Practice mindfulness'
            ]
        }

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'analysis': analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze text sentiment"""
    try:
        data = request.get_json()

        text = data.get('text', '')
        user_id = data.get('user_id', 'anonymous')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Placeholder sentiment analysis (implement actual NLP)
        # Simple keyword-based approach
        positive_words = ['happy', 'good', 'great', 'wonderful', 'excited', 'joy', 'love']
        negative_words = ['sad', 'bad', 'terrible', 'anxious', 'worried', 'depressed', 'angry']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            sentiment = 'positive'
            score = 0.7
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = 0.3
        else:
            sentiment = 'neutral'
            score = 0.5

        analysis = {
            'sentiment': sentiment,
            'score': score,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'text_length': len(text)
        }

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'analysis': analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
