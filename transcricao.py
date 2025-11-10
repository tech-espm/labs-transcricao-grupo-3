from openai import OpenAI
from config import api_key
from pathlib import Path

client = OpenAI(api_key=api_key)

def transcrever_audio(caminho_audio: str):
    audio_path = Path(caminho_audio)
    if not audio_path.exists():
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

    with audio_path.open("rb") as audio_file:
        tr = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )

    words = []
    if getattr(tr, "words", None):
        for w in tr.words:
            words.append({
                "start": float(w.start),
                "end": float(w.end),
                "word": w.word
            })

    segments = []
    if getattr(tr, "segments", None):
        for s in tr.segments:
            segments.append({
                "start": float(s.start),
                "end": float(s.end),
                "text": s.text
            })

    return {
        "text": tr.text,
        "words": words,
        **({"segments": segments} if segments else {})
    }
