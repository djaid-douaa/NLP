from flask import Flask, request, jsonify
from TTS.api import TTS
import uuid
import os
import torch

speakers_map = {
    "raid": "/home/raid/Desktop/studies/nlp/project/backend/speakers/raid.wav"
}

app = Flask(__name__)
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def text_to_wav(text, speaker="raid"):

    speaker_wav = speakers_map[speaker]
    print("here")
    wav_bytes = tts.tts(text=text, speaker_wav=speaker_wav, language="ar")
    print(f"Generated wav file: {wav_bytes}")
    return jsonify(wav_bytes)


@app.route("/voice", methods=["POST"])
def convert_text_to_voice():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        text = data.get("text")
        speaker = data.get("speaker", "raid")

        # Validate the input
        if not text:
            return (
                jsonify({"error": "'text'  is  are required field ."}),
                400,
            )
        result = text_to_wav(text, speaker)
        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
