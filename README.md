# Telegran Ollama Business Bot

AI-Powered Chatbot with User History

The project is a Telegram chatbot powered by Ollama AI, introduced in the Telegram Bot API 7.2 update, that maintains chat history with users and provides AI-generated responses. It uses the `aiogram` library for handling Telegram bot interactions, `aiohttp` for asynchronous HTTP requests, and stores user chat history in a JSON file.

![Usage example](https://telegram.org/blog/telegram-business)

## Features

- Maintains a chat history for each user.
- Integrates with an external AI service to generate responses.
- Ignores messages from a specific admin user but still logs them.
- Handles messages asynchronously for better performance.

## Requirements

- Python 3.8+
- `aiogram` library
- `aiohttp` library

## Installation

1. **Setup local ollama:**
   [Setup Guide](https://github.com/ollama/ollama)

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run bot:**
   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
