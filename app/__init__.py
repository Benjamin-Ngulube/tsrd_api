from flask import Flask
from flask_cors import CORS
from app.socket_setup import socketio
from app.routes.violation_data_route import  violation_bp
from app.routes.locations_data_route import location_read_bp

app = Flask(__name__)

# Initialize socketio with the Flask app
socketio.init_app(app,cors_allowed_origins="*")

app.register_blueprint(violation_bp)
app.register_blueprint(location_read_bp)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})