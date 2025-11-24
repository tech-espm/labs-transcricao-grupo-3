from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, tempfile
from datetime import datetime
from transcricao import transcrever_audio
import config

app = Flask(__name__)

def rodar_transcricao(caminho_audio: str):
    return transcrever_audio(caminho_audio)

@app.get('/')
def index():
    return render_template('index/index.html', hoje=datetime.today().strftime('%Y-%m-%d'))

@app.post('/transcrever')
def transcrever():
    if 'audio' not in request.files:
        return jsonify({"error": "Nenhum arquivo recebido."}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    filename = secure_filename(file.filename)
    _, ext = os.path.splitext(filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        temp_path = tmp.name

    try:
        resultado = rodar_transcricao(temp_path)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
