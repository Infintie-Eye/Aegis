import os
import sys
import asyncio
from flask import Blueprint, request, jsonify
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_chatbot.main_orchestrator import MainOrchestrator

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Store orchestrators per user (in production, use Redis or similar)
orchestrators = {}


def get_orchestrator(user_id):
    """Get or create orchestrator for a user"""
    if user_id not in orchestrators:
        orchestrators[user_id] = MainOrchestrator(user_id)
    return orchestrators[user_id]


@bp.route('/message', methods=['POST'])
def send_message():
    """Handle incoming chat messages from users"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        session_context = data.get('session_context', {})

        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Get orchestrator for user
        orchestrator = get_orchestrator(user_id)

        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            orchestrator.process_message(message, session_context)
        )
        loop.close()

        # Format response for frontend
        formatted_response = {
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'message': message,
            'response': response.get('response', ''),
            'emotional_state': response.get('emotional_state', {}),
            'mental_state_score': response.get('mental_state_score', 0),
            'wellness_suggestions': response.get('wellness_suggestions', []),
            'community_suggestions': response.get('community_suggestions', {}),
            'safety_status': response.get('safety_status', {}),
            'session_insights': response.get('session_insights', {})
        }

        return jsonify(formatted_response), 200

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to process message',
            'message': str(e),
            'fallback_response': "I'm here to listen and support you. Could you share more about what's on your mind?"
        }), 500


@bp.route('/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get chat history for a user"""
    try:
        orchestrator = get_orchestrator(user_id)

        # Get conversation history
        history = orchestrator.conversation_memory.get_recent_context(limit=50)

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'history': history,
            'count': len(history)
        }), 200

    except Exception as e:
        print(f"Error fetching history: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to fetch chat history',
            'message': str(e)
        }), 500


@bp.route('/insights/<user_id>', methods=['GET'])
def get_user_insights(user_id):
    """Get user insights and progress"""
    try:
        orchestrator = get_orchestrator(user_id)

        # Get insights asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        insights = loop.run_until_complete(
            orchestrator._get_session_insights()
        )
        loop.close()

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'insights': insights,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        print(f"Error fetching insights: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to fetch insights',
            'message': str(e)
        }), 500


@bp.route('/clear/<user_id>', methods=['DELETE'])
def clear_user_data(user_id):
    """Clear user chat data"""
    try:
        if user_id in orchestrators:
            del orchestrators[user_id]

        return jsonify({
            'status': 'success',
            'message': 'User data cleared successfully',
            'user_id': user_id
        }), 200

    except Exception as e:
        print(f"Error clearing data: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to clear user data',
            'message': str(e)
        }), 500


@bp.route('/wellness/<user_id>', methods=['GET'])
def get_wellness_suggestions(user_id):
    """Get personalized wellness suggestions"""
    try:
        orchestrator = get_orchestrator(user_id)

        # Get wellness suggestions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Get mental state first
        mental_state = {
            'stress_indicators': 0.5,
            'energy_level': 0.6,
            'mood_indicators': 0.7,
            'stagnation_indicators': 0.3
        }

        suggestions = loop.run_until_complete(
            orchestrator._get_wellness_suggestions(mental_state)
        )
        loop.close()

        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'suggestions': suggestions,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        print(f"Error fetching wellness suggestions: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to fetch wellness suggestions',
            'message': str(e)
        }), 500
