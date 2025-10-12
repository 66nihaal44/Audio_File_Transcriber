from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel
import requests
import tempfile
import os
app = Flask(__name__)
CORS(app)# , resources={r"/*": {"origins": "https://66nihaal44.github.io"}})
model = WhisperModel("base", device="cpu", compute_type="int8")
@app.route("/transcribe", methods=["POST"])
def transcribe():
  print("Request.files.keys: ", request.files.keys(), flush=True)
  print("Request.form.keys: ", request.form.keys(), flush=True)
  if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400
  print("Files recieved: ", request.files, flush=True);
  try:
    file = request.files["file"]
    if len(file.read()) > 5 * 1024 * 1024:
      return jsonify({"error": "File too large"}), 400
    file.seek(0);
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
      file.save(tmp.name)
      segments, info = model.transcribe(tmp.name, beam_size=5, language="en")
    text = " ".join([segment.text for segment in segments])
    try:
      sentimentResponse = requests.post(
        "https://audio-file-transcriber-sentiment.onrender.com/analyze",
        json={"text": text},
        timeout=(5, 60)
      )
      print("Sentiment analysis status: ", sentimentResponse.status_code, flush=True)
      sentiment = sentimentResponse.json()
    except requests.exceptions.RequestException as e:
      print("Sentiment analysis request failure: ", e, flush=True);
      sentiment = {"error": "Sentiment analysis failed"}
    except Exception as e:
      print("Sentiment analysis failure: ", e);
      sentiment = {"error": "Sentiment analysis failed"}
    print(text, sentiment, flush=True)
    return jsonify({"text": text, "sentiment": sentiment})
  except MemoryError:
    return jsonify({"error": "Server ran out of memory."}), 500
  except Exception as e:
    print("Backend Error: ", e, flush=True)
    return jsonify({"error": "Unexpected backend error"}), 500
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)

