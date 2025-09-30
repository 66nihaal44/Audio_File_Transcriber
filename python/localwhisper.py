from flask import Flask, request, jsonify
import whisper
import tempfile
import os
app = Flask(__name__)
model = whisper.load_model("tiny")
@app.route("/transcribe", methods=["POST"])
def transcribe():
  if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400
  print("Files recieved: ", request.files);
  file = request.files["file"]
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
    file.save(tmp.name)
    result = model.transcribe(tmp.name)
  return jsonify({"text": result["text"]})
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  
