from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('rooms', __name__, url_prefix='/api/rooms')

# In-memory storage (replace with database in production)
chatrooms = {
    'depression': {
        'id': 'depression',
        'name': 'Depression Support',
        'description': 'A safe space for those dealing with depression',
        'category': 'mental_health',
        'members_count': 45,
        'active': True
    },
    'anxiety': {
        'id': 'anxiety',
        'name': 'Anxiety Support',
        'description': 'Share and cope with anxiety together',
        'category': 'mental_health',
        'members_count': 67,
        'active': True
    },
    'academic': {
        'id': 'academic',
        'name': 'Academic Stress',
        'description': 'Dealing with school and study pressures',
        'category': 'life_challenges',
        'members_count': 89,
        'active': True
    },
    'work': {
        'id': 'work',
        'name': 'Work Stress',
        'description': 'Managing workplace challenges',
        'category': 'life_challenges',
        'members_count': 54,
        'active': True
    },
    'relationship': {
        'id': 'relationship',
        'name': 'Relationship Issues',
        'description': 'Navigate relationship challenges',
        'category': 'relationships',
        'members_count': 72,
        'active': True
    },
    'loneliness': {
        'id': 'loneliness',
        'name': 'Loneliness & Isolation',
        'description': 'Connect with others feeling lonely',
        'category': 'social',
        'members_count': 38,
        'active': True
    }
}


@bp.route('/list', methods=['GET'])
def list_rooms():
    """Get list of all available chatrooms"""
    try:
        category = request.args.get('category')

        rooms_list = list(chatrooms.values())

        if category:
            rooms_list = [r for r in rooms_list if r['category'] == category]

        return jsonify({
            'status': 'success',
            'rooms': rooms_list,
            'count': len(rooms_list)
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/<room_id>', methods=['GET'])
def get_room_details(room_id):
    """Get details of a specific chatroom"""
    try:
        if room_id not in chatrooms:
            return jsonify({
                'status': 'error',
                'error': 'Room not found'
            }), 404

        room = chatrooms[room_id]

        return jsonify({
            'status': 'success',
            'room': room
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/<room_id>/join', methods=['POST'])
def join_room(room_id):
    """Join a chatroom"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')

        if room_id not in chatrooms:
            return jsonify({
                'status': 'error',
                'error': 'Room not found'
            }), 404

        # In production, verify user and update database
        chatrooms[room_id]['members_count'] += 1

        return jsonify({
            'status': 'success',
            'message': f'Successfully joined {chatrooms[room_id]["name"]}',
            'room_id': room_id,
            'user_id': user_id
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/<room_id>/leave', methods=['POST'])
def leave_room(room_id):
    """Leave a chatroom"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')

        if room_id not in chatrooms:
            return jsonify({
                'status': 'error',
                'error': 'Room not found'
            }), 404

        # In production, verify user and update database
        if chatrooms[room_id]['members_count'] > 0:
            chatrooms[room_id]['members_count'] -= 1

        return jsonify({
            'status': 'success',
            'message': f'Successfully left {chatrooms[room_id]["name"]}',
            'room_id': room_id,
            'user_id': user_id
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get list of room categories"""
    try:
        categories = {}

        for room in chatrooms.values():
            cat = room['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': room['id'],
                'name': room['name'],
                'members_count': room['members_count']
            })

        return jsonify({
            'status': 'success',
            'categories': categories
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
