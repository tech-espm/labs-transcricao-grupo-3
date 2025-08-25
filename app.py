from openai import OpenAI
from config import api_key

client = OpenAI(api_key=api_key)
audio_file= open("audioaqui/AudioProLab.ogg", "rb") 

transcription = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["word", "segment"]
)

for w in (transcription.words or []):
    print(f"\t {(w.start * 1000):.0f}\t {(w.end * 1000):.0f}\t {w.word}")

print(f"\n A transcrição completa do áudio é: {transcription.text} ")




