from flask import request
from flask_socketio import emit
import asyncio
from utils.chat import chat_with_model
from app import socketio


def handle_chat(data):
    try:
        required_fields = ["user_prompt", "age_category", "moral"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            emit("error", {"error": f"Missing fields: {', '.join(missing_fields)}"})
            return

        user_prompt = data["user_prompt"]
        age_category = data["age_category"]
        moral = data["moral"]
        sid = request.sid

        def async_chat():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(
                    chat_with_model(user_prompt, age_category, moral, sid)
                )
                socketio.emit("final_response", {"response": response}, room=sid)
            except Exception as e:
                print(f"Error in async_chat: {str(e)}")
                socketio.emit("error", {"error": str(e)}, room=sid)
            finally:
                loop.close()

        socketio.start_background_task(async_chat)

    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")
        emit("error", {"error": str(e)})
