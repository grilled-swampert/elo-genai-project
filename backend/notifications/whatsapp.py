import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse  # ✅ Correct import
from twilio.rest import Client
import openai

app = Flask(__name__)

# ✅ Twilio Credentials (Replace with actual values)
ACCOUNT_SID = "${ADMIN_ID}"
AUTH_TOKEN = "${ADMIN_TOKEN}"
TWILIO_WHATSAPP_NUMBER = "{WA_NUMBER}"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ✅ OpenAI API Key

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Handles incoming WhatsApp messages and chats with OpenAI."""
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From")

    resp = MessagingResponse()  # ✅ No more NameError
    msg = resp.message()

    if incoming_msg:
        # ✅ Chat with OpenAI
        ai_response = chat_with_openai(incoming_msg)
        msg.body(ai_response)
    else:
        msg.body("❌ Sorry, I didn't understand that. Please send a message.")

    return str(resp)


client = openai.OpenAI(api_key="${OPENAI_API_KEY}"
)

def chat_with_openai(user_message):
    """✅ Chat with OpenAI using the new API format."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}]
        )

        return response.choices[0].message.content  # ✅ Correct way to extract response

    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        return "❌ Sorry, I encountered an issue processing your request."


if __name__ == "__main__":
    app.run(port=5000, debug=True)
