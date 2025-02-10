API_KEY = "sk_c63682911918f4f4a301b583af7ccd2e9933ae4d7bdba1e6"
from elevenlabs.client import ElevenLabs


def get_voice(text):

    client = ElevenLabs(api_key=API_KEY)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    return audio
