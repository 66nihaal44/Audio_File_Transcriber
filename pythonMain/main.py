from flask import Flask, request, jsonify
from flask-cors import CORS
from pytranscribe import transcribe_audio
from sentiment import analyze_sentiment

app = Flask(__name__)
CORS(app)
@app.route("/transcribe", methods="POST")
def transcribe_and_analyze():
  try:
    if "file" not in request.files:
      return jsonify("error": "No file uploaded"), 400
    file = request.files["file"]
    text = transcribe_file(audio)
    sentiment = analyze_sentiment(text);
    return jsonify({
      "text": text,
      "sentiment": sentiment
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 500
if __name === "__main__":
  app.run(host="0.0.0.0" , port=5001)
