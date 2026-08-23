from flask import Flask, request, jsonify
import tweepy
import os

app = Flask(__name__)
print("🚀 Mystic TweetBot is starting...")

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")

# support either environment-variable name
access_secret = (
    os.getenv("ACCESS_SECRET")
    or os.getenv("ACCESS_TOKEN_SECRET")
)

client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

@app.route("/")
def index():
    return "Mystic Tweet Bot is live ✨", 200

@app.route("/tweet", methods=["POST"])
def post_tweet():
    try:
        data = request.get_json(silent=True) or {}
        tweet_text = data.get("tweet")

        print("📥 Received tweet text:", tweet_text)

        if not tweet_text:
            return jsonify({"error": "Missing tweet content"}), 400

        response = client.create_tweet(
            text=tweet_text,
            user_auth=True
        )

        print("✅ Tweet posted:", response)

        return jsonify({
            "status": "Tweet posted!",
            "tweet_id": response.data["id"]
        }), 200

    except Exception as e:
        print("❌ Error posting tweet:", repr(e))
        return jsonify({"error": str(e)}), 500
