import os
import json

import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types

TOKEN = "TOKEN"
dp = Dispatcher()


def read_chat_history():
    if not os.path.exists('users_history.json'):
        return {}
    with open('users_history.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# Function to write chat history to a JSON file
def write_chat_history(chat_history):
    with open('users_history.json', 'w', encoding='utf-8') as file:
        json.dump(chat_history, file, indent=4, ensure_ascii=False)


async def handle_business_message(message: types.Message):
    user_id = str(message.from_user.id)

    message_from_user = message.text

    # Read the current chat history
    chat_history = read_chat_history()

    # Initialize user history if not present
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Update the chat history with the new message
    chat_history[user_id].append({"role": "user", "content": message_from_user})

    # Save the updated chat history
    write_chat_history(chat_history)

    # Ignore requests from a specific user ID but save the message
    if user_id == 'ADMIN_ID':
        return
    print(chat_history[user_id])
    # Prepare the payload for the API request
    payload = {
        "model": "MODEL_NAME",
        "messages": chat_history[user_id]
    }

    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:11434/api/chat'
        headers = {
            'Content-Type': 'application/json'
        }

        async with session.post(url, json=payload, headers=headers) as response:
            # Read the ndjson response line by line and accumulate the assistant's content
            ai_response = ""
            async for line in response.content:
                if line:
                    response_data = json.loads(line.decode('utf-8'))
                    if response_data.get('message', {}).get('role') == 'assistant':
                        ai_response += response_data['message']['content']

    # Update the chat history with the AI's response
    chat_history[user_id].append({"role": "assistant", "content": ai_response})

    # Save the final chat history
    write_chat_history(chat_history)

    # Send the AI's response back to the user
    await message.answer(ai_response)


async def start():
    api = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.business_message.register(handle_business_message)

    try:
        await dp.start_polling(api)
    finally:
        await api.session.close()


if __name__ == "__main__":
    asyncio.run(start())
