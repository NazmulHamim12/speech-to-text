from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_audio():
    try:
        # Save uploaded audio
        audio_file = request.files["audio"]
        input_path = "input.webm"
        output_path = "output.wav"

        audio_file.save(input_path)

        # Convert webm → wav
        sound = AudioSegment.from_file(input_path, format="webm")
        sound.export(output_path, format="wav")

        # Speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(output_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="bn-BD")

        # Cleanup
        os.remove(input_path)
        os.remove(output_path)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"text": "Error: " + str(e)})

if __name__ == "__main__":
    app.run()

