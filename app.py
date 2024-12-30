from flask_socketio import SocketIO
import eventlet
from flask import Flask

# Initialize Flask and SocketIO
app = Flask(__name__)

socketio = SocketIO(
    app, cors_allowed_origins="*", async_mode="eventlet", path="socket.io"
)


if __name__ == "__main__":
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)
