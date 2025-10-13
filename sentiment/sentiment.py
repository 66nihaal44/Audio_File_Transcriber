from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os
app = Flask(__name__)
CORS(app)
print("Reached sentiment.py", flush=True)
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
  print("Reached /analyze", flush=True)
  try:
    data = request.get_json(force=True, silent=False)
  except Exception as e:
    return jsonify({"error": "Bad json", "detail": e}), 400
  if not data or "text" not in data:
    print("No json recieved", flush=True);
    return jsonify({"error": "No json uploaded"}), 400
  text = data["text"]
  print("Text recieved: ", text, flush=True);
  try:
    result = requests.post(
      "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
      headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
      json={"inputs": text})
  except Exception as e:
    result = {"label": "Error", "score": 0}
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
