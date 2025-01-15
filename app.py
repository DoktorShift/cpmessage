import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# Create a custom logger (root-level)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # set to DEBUG so it captures all levels

# Create a formatter
formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Handler 1: For INFO and above -> writes to app.log
info_handler = FileHandler("app.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# Handler 2: For DEBUG and above -> writes to debug.log
debug_handler = FileHandler("debug.log")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(debug_handler)

# Optionally, remove existing handlers from Flask's default logger if you prefer
# for h in app.logger.handlers:
#     app.logger.removeHandler(h)
# app.logger.handlers = logger.handlers

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------
# These values should ideally come from environment variables or a .env file.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")

# ------------------------------------------------------------------------------
# FLASK ROUTES
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """
    Health-check endpoint.
    """
    app.logger.info("Health-check endpoint called.")
    return "Webhook receiver is running!", 200

@app.route("/copilot", methods=["POST"])
def copilot():
    """
    Receives JSON data and sends a formatted message to Telegram.
    Displays only:
      1. Copilot Title
      2. Amount
      3. Comment (found in 'extra' -> 'comment') or memo as a fallback
    """
    app.logger.debug("Entered /copilot endpoint.")
    data = request.json

    if not data:
        app.logger.error("No JSON data received.")
        return jsonify({"error": "No JSON data"}), 400

    # Extract required fields
    copilot_title = data.get("copilot_title", "")
    amount = data.get("amount", "")

    # Look for 'comment' inside 'extra' or use 'memo'
    extra_data = data.get("extra", {})
    comment = extra_data.get("comment", "") or data.get("memo", "")

    # Build the message (Markdown)
    message = (
        "**New Payment Received**\n\n"
        f"🎬 **Title:** {copilot_title}\n"
        f"💰 **Amount:** {amount}\n"
        f"✏️ **Comment:** {comment if comment else 'No comment'}"
    )

    # Send to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(telegram_url, json=payload, timeout=10)
        response.raise_for_status()
        app.logger.info("Message successfully sent to Telegram.")
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error sending message to Telegram: {e}")
        return jsonify({"error": "Failed to send message"}), 500

    return "Message sent to Telegram successfully!", 200

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # For production, consider using a production-grade server (e.g., gunicorn).
    # Running on port 5005 to meet your requirement.
    app.run(host="0.0.0.0", port=5005, debug=False)
