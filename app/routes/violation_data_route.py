from flask import Blueprint, jsonify, request
from utils import get_database_connection
from app.socket_setup import socketio
from datetime import datetime

violation_bp = Blueprint('api/violation', __name__)



@violation_bp.route('/violation-data', methods=['POST'])
def insert_violation_data():
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        # Corrected line
        data = request.get_json()  # Make sure to call get_json() as a method

        violation_id = data['violation_id']
        vehicle_id = data['vehicle_id']
        user_id = data['user_id']
        location_id = data['location_id']
        longitude = data['longitude']
        latitude = data['latitude']
        speed_limit = data['speed_limit']
        recorded_speed = data['recorded_speed']
        timestamp = datetime.now().timestamp()
        violation_type = data['violation_type']


        # Insert data into locations table
        cur.execute("""INSERT INTO locations (location_id, longitude, latitude) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(location_id) DO UPDATE SET
                    longitude = EXCLUDED.longitude,
                    latitude = EXCLUDED.latitude
                    """, (location_id, longitude, latitude))


        # Insert data into the violations table
        cur.execute("""
            INSERT INTO violations 
            (violation_id, vehicle_id, user_id, location_id, speed_limit, recorded_speed, timestamp, violation_type) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (violation_id, vehicle_id, user_id, location_id, speed_limit, recorded_speed, timestamp, violation_type))
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Emit the new violation data to connected clients
        socketio.emit('new_violation',[ {
            'violation_id': violation_id,
            'vehicle_id': vehicle_id,
            'user_id': user_id,
            'location_id': location_id,
            'longitude' : longitude,
            'latitude' : latitude,
            'speed_limit': speed_limit,
            'recorded_speed': recorded_speed,
            'timestamp': timestamp,
            'violation_type': violation_type
        }])
        
        return jsonify({'status': 201, 'message': 'Violation data inserted successfully'})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Error inserting violation data: {str(e)}'})

########################################################
# Get the user reading of the latest violation recording
@violation_bp.route('/violations', methods=['GET'])
def get_violations():
    conn = get_database_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM violations")
    violations = cur.fetchall()

    violations_list = []
    if violations:
        for violation in violations:
            violations_dict = {
                'violation_id': violation[0],
                'vehicle_id': violation[1],
                'user_id': violation[2],
                'location_id': violation[3],
                'longitude' : violation[4],
                'latitude' : violation[5],
                'speed_limit': violation[6],
                'recorded_speed': violation[7],
                'timestamp': violation[8],
                'violation_type': violation[9],
            }
            violations_list.append(violations_dict)
        cur.close()
        conn.close()
        return jsonify(violations_list)
    else:
        return jsonify({'error': 'No violations found'}), 404
    
