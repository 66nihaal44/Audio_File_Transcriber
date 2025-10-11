from flask import Flask, request
from flask_cors import CORS
import requests, tempfile, os
app = Flask(__name__)
CORS(app)
print("Reached sentiment.py", flush=True)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
  if "file" not in request.files:
    print("No file recieved", flush=True);
    return jsonify({"error": "No file uploaded"}), 400
  print("Files recieved: ", request.files, flush=True);
  try:
    file = request.files["file"]
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
      file.save(tmp.name)
      result = requests.post(
        "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
        headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
        json={"inputs": tmp.name})
  except Exception as e:
    result["label"] = "Error"
    result["score"] = "0"
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
