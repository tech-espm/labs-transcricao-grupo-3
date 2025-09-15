from openai import OpenAI
from config import api_key
import json

client = OpenAI(api_key=api_key)
audio_file= open("audioaqui/audio2.ogg", "rb") 

transcription = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["word", "segment"]
)

for w in (transcription.words or []):
    print(f"\t {(w.start * 1000):.0f}\t {(w.end * 1000):.0f}\t {w.word}")

print(f"\n A transcrição completa do áudio é: {transcription.text} ")
 
with open("teste.json", "w", encoding="utf-8") as arquivo_json:
	lista = []
	for word in transcription.words:
		lista.append({
			"start": word.start,
			"end": word.end,
			"word": word.word
		})
	arquivo_json.write(json.dumps(lista))