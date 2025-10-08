from transformers import pipeline
sentModel = pipeline("sentiment-analysis")
@app.route("/analyze", methods=["POST"])
def analyze_sentiment(text):
  result = sentModel(text)[0]
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
