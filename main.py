from flask import request, render_template
from flask_socketio import emit
from flask_cors import CORS
from utils.chat_request_handler import handle_chat
import eventlet
from app import socketio, app

CORS(app, resources={r"/*": {"origins": "*"}})


@socketio.on("connect")
def handle_connect():
    print(f"Client connected with sid: {request.sid}")
    emit("connected", {"data": "Connected to server"})


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")


@socketio.on("chat")
def handle_chat_request(data):
    handle_chat(data)


if __name__ == "__main__":
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)
