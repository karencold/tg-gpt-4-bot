import os
import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

openai.api_key = os.environ.get("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Function to start the bot
async def start(message: types.Message):
    await message.reply("Hello! I'm a GPT-4 powered Telegram bot. Send me a message to get started.")

# Function to handle the new context command
async def new_context(message: types.Message):
    chat_id = message.chat.id
    if not hasattr(dp, "chat_data"):
        dp.chat_data = {}
    dp.chat_data[chat_id] = []
    await message.reply("New context started. Send me a message to continue.")

# Function to handle messages and generate responses using GPT-4
async def chat(message: types.Message):
    user_text = message.text
    chat_id = message.chat.id

    if not hasattr(dp, "chat_data"):
        dp.chat_data = {}
    if chat_id not in dp.chat_data:
        dp.chat_data[chat_id] = []

    dp.chat_data[chat_id].append({"role": "system", "content": "You are chatting with a GPT-4 powered Telegram bot."})
    dp.chat_data[chat_id].append({"role": "user", "content": user_text})

    # Generate a response using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=dp.chat_data[chat_id],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=None,
    )

    gpt_response = response.choices[0].message['content'].strip()
    dp.chat_data[chat_id].append({"role": "assistant", "content": gpt_response})
    await message.reply(gpt_response)




# Command handlers
dp.register_message_handler(start, commands=["start"])
dp.register_message_handler(new_context, commands=["new"])
dp.register_message_handler(chat, content_types=types.ContentTypes.TEXT)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
