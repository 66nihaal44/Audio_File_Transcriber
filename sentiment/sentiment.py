from transformers import pipeline
sentModel = pipeline("sentiment-analysis")
@app.route("/analyze", methods=["POST"])
def analyze_sentiment(text):
  result = sentModel(text)[0]
  return {
    "label": result["label"],
    "score": round(result["score"], 3)
  }
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
