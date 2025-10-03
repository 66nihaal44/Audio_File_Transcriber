from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel 
import tempfile
import os
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://66nihaal44.github.io"}})
model = WhisperModel("base", device="cpu", compute_type="int8")
@app.route("/transcribe", methods=["POST"])
def transcribe():
  print("Request.files.keys: ", request.files.keys())
  print("Request.form.keys: ", request.form.keys())
  if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400
  print("Files recieved: ", request.files);
  file = request.files["file"]
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
    file.save(tmp.name)
    segments, info = model.transcribe(tmp.name, beam_size=5)
  text = " ".join([segment.text for segment in segments])
  return jsonify({"text": "text"})
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  
