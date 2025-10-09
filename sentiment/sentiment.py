from flask import Flask, request
from flask_cors import CORS
import torch
import os
from transformers import pipeline
app = Flask(__name__)
CORS(app)
sentModel = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
@app.route("/analyze", methods=["POST"])
def analyze_sentiment(text):
  # add request for file here
  result = sentModel(text)[0]
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
