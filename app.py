from flask import Flask, request, jsonify
import tweepy
import os

app = Flask(__name__)
print("🚀 CLEAN Mystic Bot Loaded — no auth")

client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

@app.route('/tweet', methods=['POST'])
def post_tweet():
    try:
        data = request.get_json()
        tweet_text = data.get('tweet')
        if not tweet_text:
            return jsonify({"error": "Missing tweet"}), 400
        client.create_tweet(text=tweet_text)
        return jsonify({"status": "Tweet posted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "Mystic Tweet Bot is running 🌙", 200
