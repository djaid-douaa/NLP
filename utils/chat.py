from ollama import AsyncClient
from flask_socketio import SocketIO

from flask import Flask
import re
from app import socketio

system_promt = """
أنت نموذج ذكاء اصطناعي متخصص في إنشاء قصص موجهة للأطفال تعزز القيم الإسلامية. تتمثل مهمتك في كتابة قصة جذابة ومناسبة للفئة العمرية المحددة، مع التركيز على القيمة الأخلاقية المطلوبة. يجب أن تكون القصة مكتوبة بلغة عربية سهلة ومبسطة للأطفال، وتتضمن شخصيات وأحداث تُشجع الأطفال على تبني هذه القيمة في حياتهم اليومية.

YOU SHOULD FOLLOW THE VALUE AND THE AGE CATEGORY

"""


async def chat_with_model(user_prompt, age_category, moral, sid):
    client = AsyncClient()
    try:

        messages = [
            {
                "role": "system",
                "content": system_promt,
            },
            {
                "role": "user",
                "content": f"الفئة العمرية: {age_category}, القيمة الأخلاقية: {moral}, {user_prompt}",
            },
        ]
        response = ""
        stream = await client.chat(
            model="hf.co/Raido/qween7.5-arabic-story-teller-GGUF",
            messages=messages,
            stream=True,
        )

        async for part in stream:
            socketio.emit("partial_response", {"content": response}, room=sid)
            if (
                re.search(r"\n### القصة:", response)
                and "\n" in part["message"]["content"]
            ):

                response += part["message"]["content"] + "." + "\n"

                break
            else:
                response += part["message"]["content"]

        return response
    except Exception as e:
        print(f"Error in chat_with_model: {str(e)}")
        socketio.emit("error", {"error": str(e)}, room=sid)
        raise
