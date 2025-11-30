from flask import Flask, request, jsonify
import json
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("emotionDetector")

@app.route("/emotionDetector")
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return "Invalid input! Please provide text to analyze.", 400

    try:
        response = emotion_detector(text_to_analyze)
        formatted_response = json.loads(response.text)
        emotions = formatted_response['emotionPredictions'][0]['emotion']
    except Exception as e:
        return f"Error processing response: {str(e)}", 500

    emotion_set = {
        'anger': emotions.get("anger", 0),
        'disgust': emotions.get("disgust", 0),
        'fear': emotions.get("fear", 0),
        'joy': emotions.get("joy", 0),
        'sadness': emotions.get("sadness", 0)
    }
    dominant_emotion = max(emotion_set.items(), key=lambda item: item[1])[0]

    return jsonify({
        "anger": emotion_set['anger'],
        "disgust": emotion_set['disgust'],
        "fear": emotion_set['fear'],
        "joy": emotion_set['joy'],
        "sadness": emotion_set['sadness'],
        "dominant_emotion": dominant_emotion
    })

if __name__ == "__main__":
    app.run(debug=True)