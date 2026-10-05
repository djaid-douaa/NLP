import os
from elevenlabs.client import ElevenLabs

# Set ELEVENLABS_API_KEY in your environment before running the app.
API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def get_voice(text):

    client = ElevenLabs(api_key=API_KEY)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    return audio
