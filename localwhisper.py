from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flash(_name_)
model = whisper.load_model("base")
@app.route("/transcribe", methods=["POST"])
def transcribe():
  if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400
  file = request.files["file"]
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
    file.save(tmp.name)
    result = model.transcribe(tmp.name)
  return jsonify({"text": result["text"]})
if _name_ == "_main_":
  app.run(host="0.0.0.0", port=3000)
  
