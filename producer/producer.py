from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google.cloud import pubsub_v1
import os

app = Flask(__name__)
CORS(app)

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_name = "my-topic"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.json.get("message")
        if message:
            publish_message(message)
            return jsonify({"message": "Message sent to Pub/Sub!"}), 200
        else:
            return jsonify({"error": "Message field is required"}), 400

    return render_template("index.html")

def publish_message(message):
    credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    data = message.encode("utf-8")
    
    try:
        future = publisher.publish(topic_path, data=data)
        future.result()
        print("Message published successfully.")
    except Exception as e:
        print(f"Failed to publish message: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
