"""
Flask application for detecting emotions in text using the emotion_detector service.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/emotionDetector")
def detect_emotion():
    """
    Route to analyze text provided as a query parameter and
    return detected emotion values and dominant emotion.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    response = emotion_detector(text_to_analyze)

    if not response or response.get("dominant_emotion") == "None":
        return "Invalid text! Please try again!"

    anger = response.get("anger")
    disgust = response.get("disgust")
    fear = response.get("fear")
    joy = response.get("joy")
    sadness = response.get("sadness")
    dominant_emotion = response.get("dominant_emotion")

    result = (
        f"For the given statement, the system response is: "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return result


@app.route("/")
def render_index_page():
    """Render the index HTML page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    