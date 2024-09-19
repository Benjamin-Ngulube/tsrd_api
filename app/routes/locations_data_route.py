############################################################
# Get the user location

from flask import Blueprint, jsonify, request
from utils import get_database_connection
from app.socket_setup import socketio
from datetime import datetime


location_read_bp = Blueprint('api/location', __name__)

@location_read_bp.route('/location/<location_id>', methods=['GET'])
def get_location(location_id):
    print(f"Received request for location_id: {location_id}")
    conn = get_database_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT longitude, latitude FROM locations WHERE location_id=?", (location_id,))
        location = cur.fetchone()
        if location:
            longitude, latitude = location
            return jsonify({
                'location_id': location_id,
                'longitude': longitude,
                'latitude': latitude
            })
        else:
            return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

