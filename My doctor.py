import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CallbackContext, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def respond(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    logger.info(f"Received message: {user_input}")

    url = "https://app.mu.chat/api/agents/cm7ykdoju01tjtoi8g8x8u5d9/query"
    payload = {
        "query": user_input,
        "conversationId": "conv_123",
        "visitorId": "visitor_123",
        "temperature": 0.2,
        "streaming": False,
        "modelName": "gpt_4o_mini",
        "maxTokens": 500,
        "presencePenalty": 0,
        "frequencyPenalty": 0,
        "topP": 1,
        "filters": {},
        "systemPrompt": "",
        "userPrompt": "",
        "promptType": "raw",
        "promptTemplate": ""
    }
    headers = {
        "Authorization": "Bearer cm7ykdoju01tjtoi8g8x8u5d9",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    response_text = response_json.get("answer", "Sorry, I couldn't understand that.")

    await update.message.reply_text(response_text)

def main():
    application = Application.builder().token("YOUR TOKEN ").build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    application.run_polling()

if __name__ == '__main__':
    main()

