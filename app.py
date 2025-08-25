from openai import OpenAI
from config import api_key

client = OpenAI(api_key=api_key)
audio_file= open("audioaqui/AudioProLab.ogg", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language="pt",
    response_format="verbose_json"
)

print("Transcrição:", transcription.text)
