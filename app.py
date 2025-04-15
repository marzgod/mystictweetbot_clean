from flask import Flask, request, jsonify
import tweepy
import os

app = Flask(__name__)
print("🚀 Mystic TweetBot is starting...")

# Tweepy client setup using environment variables
client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

@app.route('/')
def index():
    return "Mystic Tweet Bot is live ✨", 200

@app.route('/tweet', methods=['POST'])
def post_tweet():
    try:
        data = request.get_json()
        tweet_text = data.get('tweet')

        print("📥 Received tweet text:", tweet_text)

        if not tweet_text:
            print("❌ No tweet content received.")
            return jsonify({"error": "Missing tweet content"}), 400

        response = client.create_tweet(text=tweet_text)
        print("✅ Tweet posted:", response)

        return jsonify({"status": "Tweet posted!"}), 200

    except Exception as e:
        print("❌ Error posting tweet:", str(e))
        return jsonify({"error": str(e)}), 500
