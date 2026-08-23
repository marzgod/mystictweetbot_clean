from flask import Flask, request, jsonify
import tweepy
import os

app = Flask(__name__)

print("🚀 Mystic TweetBot is starting...")

# X / Twitter credentials from Render environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")

# Supports either environment variable name
access_secret = (
    os.getenv("ACCESS_SECRET")
    or os.getenv("ACCESS_TOKEN_SECRET")
)

# OAuth 1.0a user-authenticated Tweepy client
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)


@app.route("/")
def index():
    return "Mystic Tweet Bot is live ✨", 200


@app.route("/auth-test")
def auth_test():
    try:
        me = client.get_me(user_auth=True)

        print("✅ Auth test successful:", me)

        return jsonify({
            "status": "ok",
            "username": me.data.username
        }), 200

    except Exception as e:
        print("❌ Auth test failed:", repr(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/tweet", methods=["POST"])
def post_tweet():
    try:
        data = request.get_json(silent=True) or {}
        tweet_text = data.get("tweet")

        print("📥 Received tweet text:", tweet_text)

        if not tweet_text:
            print("❌ No tweet content received.")
            return jsonify({
                "error": "Missing tweet content"
            }), 400

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

        return jsonify({
            "error": str(e)
        }), 500
