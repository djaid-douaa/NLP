import base64
from flask import request, copy_current_request_context, jsonify
from flask_socketio import emit
import asyncio
from utils.voice import get_voice
import requests
import os
from utils.chat import chat_with_model
from app import socketio

FLASK_SERVER_URL = "http://localhost:5000/voice"


def handle_chat(data):
    required_fields = ["user_prompt", "age_category", "moral"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        emit("error", {"error": f"Missing fields: {', '.join(missing_fields)}"})
        return

    user_prompt = data["user_prompt"]
    age_category = data["age_category"]
    moral = data["moral"]

    sid = request.sid

    @copy_current_request_context
    def async_chat():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Generate chat response
            emit("progress", {"message": "Generating chat response..."}, room=sid)
            response = loop.run_until_complete(
                chat_with_model(user_prompt, age_category, moral, sid)
            )

            # Get the audio from get_voice(response). If it returns a generator, join it.
            audio_generator = get_voice(
                response
            )  # Assume this returns a generator yielding bytes
            # Convert the generator into a single bytes object
            audio_bytes = b"".join(audio_generator)

            # Encode the audio bytes to a Base64 string
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

            # Emit the final response with both text and audio
            socketio.emit(
                "final_response", {"response": response, "audio": audio_b64}, room=sid
            )

        except Exception as e:
            print(f"Error in async_chat: {str(e)}")
            socketio.emit("error", {"error": str(e)}, room=sid)
        finally:
            loop.close()

    socketio.start_background_task(async_chat)
