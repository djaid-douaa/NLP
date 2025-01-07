from ollama import AsyncClient
from flask_socketio import SocketIO

from flask import Flask
import re
from app import socketio

system_promt = """
اكتب قصصًا للأطفال تعزز القيم الإسلامية باستخدام شخصيات عربية. اجعل اللغة عربية مبسطة ومناسبة للأطفال، مع التركيز على القيم الأخلاقية مثل الصدق والاحترام. ابتعد تمامًا عن أي مواضيع تتعارض مع الإسلام مثل الخمر، المواعدة، أو أكل لحم الخنزير، وفي حال طلب مثل هذه المواضيع، رد بـ "لا يمكنني كتابة قصة حول هذا الموضوع".
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
