from flask import Flask, request, jsonify
from pyngrok import ngrok
from datetime import time
from models import db, DataEntry

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///live_data.db'
db.init_app(app)

# POST method


@app.route('/put_method', methods=['PUT'])
def put_data():
    # Extract data from the incoming request
    data = request.get_json()

    # Create a new DataEntry object with the received data
    new_entry = DataEntry(
        timestamp=data['timestamp'],
        voltage=data['voltage'],
        throttle_mv=data['throttle_mv'],
        throttle_percentage=data['throttle_percentage'],
        rpm=data['RPM'],
        torque=data['torque'],
        motor_temp=data['motor_temp'],
        current=data['current']
    )

    # Insert the new entry into the database
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(message="Data stored successfully."), 201


@app.route('/get_data', methods=['GET'])
def get_data():
    # most recent timestamp value.
    entry = DataEntry.query.order_by(
        DataEntry.timestamp.desc()).first()
    if entry:
        return jsonify({
            'timestamp': entry.timestamp,
            'voltage': entry.voltage,
            'throttle_mv': entry.throttle_mv,
            'throttle_percentage': entry.throttle_percent,
            'RPM': entry.rpm,
            'torque': entry.torque,
            'motor_temp': entry.motor_temp,
            'current': entry.current
        })
    else:
        return jsonify(message="No data available."), 404


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    # Setup ngrok
    ngrok_tunnel = ngrok.connect(
        addr=5000, hostname="hugely-dashing-lemming.ngrok-free.app")
    print('NGROK Tunnel URL:', ngrok_tunnel.public_url)

    # Run Flask app
    app.run(port=5000)
