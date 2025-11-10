from flask import Flask, render_template, json, request, Response, redirect, url_for, flash
from werkzeug.utils import secure_filename
from openai import OpenAI
import config
import json
import os
import tempfile
from datetime import datetime
from transcricao import transcrever_audio

app = Flask(__name__)

def rodar_transcricao(caminho_audio: str):
    return transcrever_audio(caminho_audio)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.route("/transcrever", methods=["POST"])
def transcrever():
    if 'audio' not in request.files:
        flash("Nenhum arquivo recebido (campo 'audio' ausente).")
        return redirect(url_for("index"))

    file = request.files['audio']
    if file.filename == '':
        flash("Nenhum arquivo selecionado.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    _, ext = os.path.splitext(filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        temp_path = tmp.name

    try:
        resultado = rodar_transcricao(temp_path)

        if isinstance(resultado, str):
            resultado_dict = {"transcricao": resultado}
        else:
            resultado_dict = resultado

        return render_template(
            "index/index.html",
            hoje=datetime.today().strftime("%Y-%m-%d"),
            resultado=resultado_dict
        )
    except Exception as e:
        flash(f"Erro ao transcrever: {e}")
        return redirect(url_for("index"))
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
