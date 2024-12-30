from flask import request, copy_current_request_context, jsonify
from flask_socketio import emit
import asyncio
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
    include_voice = data.get("include_voice", False)
    speaker = data.get("speaker", "raid")
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
            socketio.emit("final_response", {"response": response}, room=sid)

            # Handle voice generation
            if include_voice:
                print("processing the text as audio")
                emit(
                    "progress", {"message": "Sending text to voice server..."}, room=sid
                )
                payload = {"text": response, "speaker": speaker}

                flask_response = requests.post(FLASK_SERVER_URL, json=payload)
                if not flask_response.ok:
                    raise Exception(f"Voice server error: {flask_response.text}")

                audio_bytes = flask_response.json().get("message")
                emit("audio_chunk", {"chunk": jsonify(audio_bytes)}, room=sid)
                emit("audio_complete", {"message": "Audio file sent"}, room=sid)

        except Exception as e:
            print(f"Error in async_chat: {str(e)}")
            socketio.emit("error", {"error": str(e)}, room=sid)
        finally:
            loop.close()

    socketio.start_background_task(async_chat)
