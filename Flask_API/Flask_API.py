from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

tesla_related_classifier = pipeline(
    "sentiment-analysis", model="BLACKBUN/tesla-related-unrelated-classification"
)
stock_sentiment_classifier = pipeline(
    "sentiment-analysis", model="zhayunduo/roberta-base-stocktwits-finetuned"
)


def get_influence(text):
    text = text.lower()

    entities = ["model s", "model 3", "model x", "model y", "solar roof"]
    for entity in entities:
        text = text.replace(entity, entity.replace(" ", "_"))

    tesla_keywords = [
        "tesla",
        "model_s",
        "model_3",
        "model_x",
        "model_y",
        "elon",
        "musk",
        "gigafactory",
        "cell",
        "fsd",
        "supercharger",
        "autopilot",
        "cybertruck",
        "solar_roof",
        "powerwall",
    ]

    tesla_related_result = tesla_related_classifier(text)
    stock_sentiment_result = stock_sentiment_classifier(text)

    if tesla_related_result[0]["label"] == "Unrelated":
        flag = False
        for keyword in tesla_keywords:
            if keyword in text:
                flag = True
                break
        if flag == False:
            return "This tweet is not related to Tesla"
    if (
        stock_sentiment_result[0]["label"] == "Positive"
        and stock_sentiment_result[0]["score"] > 0.7
    ):
        return "This tweet is positive and may influence Tesla's stock price"
    elif (
        stock_sentiment_result[0]["label"] == "Negative"
        and stock_sentiment_result[0]["score"] > 0.7
    ):
        return "This tweet is negative and may influence Tesla's stock price"
    else:
        return "This tweet is related but neutral. This may not influence Tesla's stock price"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["inputString"]
        response = get_influence(text)
        return jsonify({"result": response})
    return render_template("form.html")


@app.route("/process_tweet", methods=["POST"])
def process_tweet():
    text = request.form["inputString"]
    response = get_influence(text)
    return jsonify({"result": response})


if __name__ == "__main__":
    app.run(debug=True)
