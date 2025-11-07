import os
import sys
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ai_chatbot.main_orchestrator import MainOrchestrator

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import route modules
from routes import chat_routes, analysis_routes, room_routes, auth_routes

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aegis-secret-key')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(chat_routes.bp)
app.register_blueprint(analysis_routes.bp)
app.register_blueprint(room_routes.bp)
app.register_blueprint(auth_routes.bp)

# Initialize for a user
orchestrator = MainOrchestrator(user_id="user123")


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Aegis Mental Wellness API',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Welcome to Aegis Mental Wellness API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'ai_chat': '/api/chat/message',
            'analysis': '/api/analysis/*',
            'chatrooms': '/api/rooms/*',
            'auth': '/api/auth/*'
        }
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    print(f"🚀 Starting Aegis Mental Wellness API on {host}:{port}")
    print(f"📝 Debug mode: {debug}")
    print(f"🔑 API Key configured: {bool(os.getenv('GOOGLE_API_KEY'))}")

    # Process a message
    response = orchestrator.process_message("I've been feeling really anxious lately")
    print(response)

    app.run(host=host, port=port, debug=debug)
