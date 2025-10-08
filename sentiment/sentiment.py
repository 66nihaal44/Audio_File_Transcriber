from transformers import pipeline
sentModel = pipeline("sentiment-analysis")
def analyze_sentiment(text):
  result = sentModel(text)[0]
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
