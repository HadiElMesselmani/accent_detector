from flask import Flask, request, jsonify
from flask_cors import CORS
from helpers import extract_audio_from_url, transcribe_and_detect, load_accent_classifier , classify_accent, remove_audio_files
import os


app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "JSON body must contain 'url'"}), 400
    url = data["url"]
    try:
        print("Extracting audio from: ", url)
        audio_dest = "backend/temp_audio/audio.wav"
        trimmed_audio_dest = "backend/temp_audio/trimmed.wav"

        extract_audio_from_url(url, audio_dest)
        lang = transcribe_and_detect(audio_dest, trimmed_audio_dest)

        if lang == "en":
            classifier = load_accent_classifier()
            scores = classify_accent(classifier, trimmed_audio_dest)
            remove_audio_files(audio_dest, trimmed_audio_dest)
            return jsonify(scores)
        
        else:
            remove_audio_files(audio_dest, trimmed_audio_dest)
            return jsonify({"error": "The language in the video is not English."}), 400

        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)