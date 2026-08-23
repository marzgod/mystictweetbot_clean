from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

print("🚀 Mystic TweetBot is starting...")

X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_REFRESH_TOKEN = os.getenv("X_REFRESH_TOKEN")
X_CLIENT_ID = os.getenv("X_CLIENT_ID")
X_CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")

TWEET_URL = "https://api.x.com/2/tweets"
TOKEN_URL = "https://api.x.com/2/oauth2/token"


def refresh_access_token():
    global X_ACCESS_TOKEN, X_REFRESH_TOKEN

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": X_REFRESH_TOKEN,
            "client_id": X_CLIENT_ID,
        },
        auth=(X_CLIENT_ID, X_CLIENT_SECRET),
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if not response.ok:
        print("❌ Token refresh failed:", response.text)
        return False

    token_data = response.json()

    X_ACCESS_TOKEN = token_data.get("access_token", X_ACCESS_TOKEN)
    X_REFRESH_TOKEN = token_data.get("refresh_token", X_REFRESH_TOKEN)

    print("✅ OAuth 2.0 access token refreshed")
    return True


def send_tweet(tweet_text):
    response = requests.post(
        TWEET_URL,
        headers={
            "Authorization": f"Bearer {X_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "text": tweet_text
        }
    )

    # If access token expired, refresh and retry once
    if response.status_code == 401:
        print("🔄 Access token rejected. Trying refresh...")

        if refresh_access_token():
            response = requests.post(
                TWEET_URL,
                headers={
                    "Authorization": f"Bearer {X_ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "text": tweet_text
                }
            )

    return response


@app.route("/")
def index():
    return "Mystic Tweet Bot is live ✨", 200


@app.route("/auth-test")
def auth_test():
    response = requests.get(
        "https://api.x.com/2/users/me",
        headers={
            "Authorization": f"Bearer {X_ACCESS_TOKEN}"
        }
    )

    return jsonify(response.json()), response.status_code


@app.route("/tweet", methods=["POST"])
def post_tweet():
    try:
        data = request.get_json(silent=True) or {}
        tweet_text = data.get("tweet")

        print("📥 Received tweet text:", tweet_text)

        if not tweet_text:
            return jsonify({
                "error": "Missing tweet content"
            }), 400

        response = send_tweet(tweet_text)

        print("📤 X response:", response.status_code, response.text)

        return jsonify(response.json()), response.status_code

    except Exception as e:
        print("❌ Tweet error:", repr(e))

        return jsonify({
            "error": str(e)
        }), 500
