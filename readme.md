# Arabic Story Generator for Children

A small web app that writes short children's stories in Arabic. The user describes the story they want, picks an age group and a moral value (honesty, respect, ...), and the app streams the story back as it is generated, then reads it aloud.

## How it works

1. **Prompting:** the request is wrapped in an Arabic system prompt that fixes the format (title, characters, then the story), keeps the language simple for the chosen age group, and makes the story revolve around the requested value.
2. **Guardrail:** topics that go against the values the stories are meant to teach are refused instead of written.
3. **Generation:** a local Arabic storytelling LLM runs through [Ollama](https://ollama.com). Tokens are pushed to the browser over Socket.IO, so the story appears while it is being written.
4. **Narration:** the finished story is converted to speech with ElevenLabs' multilingual model.

The research side of the project (experiments and write-up) is in [`nlp_project/`](nlp_project/).

## Stack

Python · Flask · Flask-SocketIO · Ollama · ElevenLabs TTS · HTML/JS templates

## Run it

```bash
pip install -r requirements.txt
export ELEVENLABS_API_KEY=your_key
python main.py      # serves on http://localhost:8000
```

Ollama must be running locally with the storytelling model pulled (see `utils/chat.py`).

## Structure

```
main.py                     Socket.IO events (connect, chat)
app.py                      Flask + Socket.IO setup
utils/chat.py               prompt, guardrail and streaming generation
utils/chat_request_handler.py  request validation, generation + narration
utils/voice.py              text-to-speech
templates/                  landing, prompt and story pages
nlp_project/                notebook and paper
```
