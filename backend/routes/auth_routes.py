from flask import Blueprint, request, jsonify
from datetime import datetime
import hashlib
import secrets

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# In-memory storage (replace with database in production)
users = {}
sessions = {}


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        email = data.get('email', '').lower()
        password = data.get('password', '')
        name = data.get('name', '')

        if not email or not password:
            return jsonify({
                'status': 'error',
                'error': 'Email and password are required'
            }), 400

        if email in users:
            return jsonify({
                'status': 'error',
                'error': 'User already exists'
            }), 409

        # Hash password (use proper password hashing in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Create user
        user_id = secrets.token_urlsafe(16)
        users[email] = {
            'user_id': user_id,
            'email': email,
            'name': name,
            'password_hash': password_hash,
            'created_at': datetime.utcnow().isoformat(),
            'is_anonymous': False
        }

        # Create session
        session_token = secrets.token_urlsafe(32)
        sessions[session_token] = {
            'user_id': user_id,
            'email': email,
            'created_at': datetime.utcnow().isoformat()
        }

        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user_id': user_id,
            'session_token': session_token
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()

        email = data.get('email', '').lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({
                'status': 'error',
                'error': 'Email and password are required'
            }), 400

        if email not in users:
            return jsonify({
                'status': 'error',
                'error': 'Invalid credentials'
            }), 401

        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if users[email]['password_hash'] != password_hash:
            return jsonify({
                'status': 'error',
                'error': 'Invalid credentials'
            }), 401

        # Create session
        session_token = secrets.token_urlsafe(32)
        sessions[session_token] = {
            'user_id': users[email]['user_id'],
            'email': email,
            'created_at': datetime.utcnow().isoformat()
        }

        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user_id': users[email]['user_id'],
            'session_token': session_token
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/anonymous', methods=['POST'])
def create_anonymous():
    """Create anonymous user session"""
    try:
        # Generate anonymous user
        user_id = f"anon_{secrets.token_urlsafe(12)}"

        users[user_id] = {
            'user_id': user_id,
            'email': None,
            'name': 'Anonymous User',
            'created_at': datetime.utcnow().isoformat(),
            'is_anonymous': True
        }

        # Create session
        session_token = secrets.token_urlsafe(32)
        sessions[session_token] = {
            'user_id': user_id,
            'email': None,
            'created_at': datetime.utcnow().isoformat()
        }

        return jsonify({
            'status': 'success',
            'message': 'Anonymous session created',
            'user_id': user_id,
            'session_token': session_token
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/verify', methods=['POST'])
def verify_session():
    """Verify session token"""
    try:
        data = request.get_json()
        session_token = data.get('session_token', '')

        if session_token not in sessions:
            return jsonify({
                'status': 'error',
                'error': 'Invalid session'
            }), 401

        session = sessions[session_token]

        return jsonify({
            'status': 'success',
            'valid': True,
            'user_id': session['user_id']
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        data = request.get_json()
        session_token = data.get('session_token', '')

        if session_token in sessions:
            del sessions[session_token]

        return jsonify({
            'status': 'success',
            'message': 'Logged out successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
