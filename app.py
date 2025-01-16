import os
import logging
from logging import Formatter, FileHandler, StreamHandler
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# ------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

console_handler = StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

info_file_handler = FileHandler("app.log")
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(formatter)

debug_file_handler = FileHandler("debug.log")
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(info_file_handler)
logger.addHandler(debug_file_handler)

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")

# ------------------------------------------------------------------------------
# FLASK ROUTES
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """
    Health-check endpoint
    """
    app.logger.info("Health-check on / endpoint.")
    return "Webhook receiver is running!", 200

@app.route("/copilot", methods=["POST"])
def copilot():
    """
    Receives JSON data and sends a formatted message to Telegram.
    Specifically looks for these top-level fields:
      - 'copilot_title'
      - 'amount'
      - 'comment'
    """
    app.logger.debug("Entered /copilot endpoint.")

    data = request.json
    if not data:
        app.logger.error("No JSON data received.")
        return jsonify({"error": "No JSON data"}), 400

    # Extract the needed fields from the top-level JSON
    copilot_title = data.get("copilot_title", "")
    amount        = data.get("amount", "")
    comment       = data.get("comment", "") or data.get("memo", "")

    # Build the message
    message = (
        "**New Payment Received**\n\n"
        f"🎯 **Title:** {copilot_title}\n"
        f"💰 **Amount:** {amount}\n"
        f"✏️ **Comment:** {comment if comment else 'No comment'}"
    )

    # Send message to Telegram
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
    app.run(host="0.0.0.0", port=5005, debug=False)
