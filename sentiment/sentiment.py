from flask import Flask, request
from flask_cors import CORS
import requests, tempfile, os
app = Flask(__name__)
CORS(app)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
  if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400
  print("Files recieved: ", request.files);
  try:
    file = request.files["file"]
    if len(file.read()) > 5 * 1024 * 1024:
      return jsonify({"error": "File too large"}), 400
    file.seek(0);
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
      file.save(tmp.name)
      result = sentModel(text)[0]
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
