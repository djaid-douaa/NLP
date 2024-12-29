from flask_socketio import SocketIO
from flask import Flask

# Initialize Flask and SocketIO
app = Flask(__name__)

socketio = SocketIO(
    app, cors_allowed_origins="*", async_mode="eventlet", path="socket.io"
)
