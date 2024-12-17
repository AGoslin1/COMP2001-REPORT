import pyodbc
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    'server': 'dist-6-505.uopnet.plymouth.ac.uk',
    'database': 'COMP2001_AGoslin',
    'username': 'AGoslin',
    'password': 'VisI488*'
}

def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"Encrypt=no;"
    )
    return conn

@app.route('/trails', methods=['POST'])
def create_trail():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "EXEC CW2.CreateTrail ?, ?, ?, ?, ?, ?, ?, ?, ?",
        data['TrailName'], data['Location'], data['TrailLength'], data['TrailTime'],
        data['TrailType'], data['Difficulty'], data['StartPoint'], data['EndPoint'], data['UserID']
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Trail created successfully'}), 201

@app.route('/trails', methods=['GET'])
def get_trails():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail")
    trails = cursor.fetchall()
    conn.close()
    return jsonify([{
        'TrailID': row[0],
        'TrailName': row[1],
        'Location': row[2],
        'TrailLength': float(row[3]),
        'TrailTime': str(row[4]),
        'TrailType': row[5],
        'Difficulty': row[6],
        'StartPoint': row[7],
        'EndPoint': row[8],
        'UserID': row[9]
    } for row in trails])

@app.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "EXEC CW2.UpdateTrail ?, ?, ?, ?, ?, ?, ?, ?, ?",
        trail_id, data['TrailName'], data['Location'], data['TrailLength'],
        data['TrailTime'], data['TrailType'], data['Difficulty'],
        data['StartPoint'], data['EndPoint']
    )
    conn.commit()
    conn.close()
    return jsonify({'message': f'Trail with ID {trail_id} updated successfully'})

@app.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CW2.Trail WHERE TrailID = ?", trail_id)
    conn.commit()
    conn.close()
    return jsonify({'message': f'Trail with ID {trail_id} deleted successfully'})

@app.route('/trails/<int:trail_id>/waypoints', methods=['POST'])
def add_waypoint(trail_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "EXEC CW2.CreateWaypoint ?, ?, ?",
        trail_id, data['WaypointLatitude'], data['WaypointLongitude']
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Waypoint added successfully'}), 201

@app.route('/trails/<int:trail_id>/waypoints', methods=['GET'])
def get_waypoints(trail_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC CW2.GetWaypointsByTrail ?", trail_id)
    waypoints = cursor.fetchall()
    conn.close()
    return jsonify([
        {'WaypointID': row[0], 'Latitude': float(row[1]), 'Longitude': float(row[2])}
        for row in waypoints
    ])

@app.route('/waypoints/<int:waypoint_id>', methods=['PUT'])
def update_waypoint(waypoint_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "EXEC CW2.UpdateWaypoint ?, ?, ?",
        waypoint_id, data['WaypointLatitude'], data['WaypointLongitude']
    )
    conn.commit()
    conn.close()
    return jsonify({'message': f'Waypoint {waypoint_id} updated successfully'})

@app.route('/waypoints/<int:waypoint_id>', methods=['DELETE'])
def delete_waypoint(waypoint_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC CW2.DeleteWaypoint ?", waypoint_id)
    conn.commit()
    conn.close()
    return jsonify({'message': f'Waypoint {waypoint_id} deleted successfully'})

@app.route('/trail_logs', methods=['GET'])
def get_trail_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC CW2.GetTrailLogs")
    logs = cursor.fetchall()
    conn.close()
    return jsonify([{
        'LogID': row[0],
        'TrailID': row[1],
        'ActionType': row[2],
        'ActionTime': str(row[3]),
        'UserID': row[4]
    } for row in logs])

if __name__ == '__main__':
    app.run(debug=True)
