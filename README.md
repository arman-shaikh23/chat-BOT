# CLI Chatbot (NVIDIA NIM)

A terminal-based multi-turn chatbot built with Python and NVIDIA NIM (Llama 3.1).

## Tech Stack

- Python 3.10+
- `httpx` (for API requests)
- NVIDIA NIM (Llama 3.1 8B)
- ANSI terminal colors for a simple CLI UI

## Features

- Multi-turn conversation with manual history maintenance
- **Streaming responses** for a better user experience
- Clean terminal prompts for user and AI messages
- Graceful exit with `exit`, `quit`, `Ctrl+C`, or `Ctrl+D`
- Minimal code footprint (~50 lines)

## Setup

1. Ensure dependencies are installed:

```bash
pip install httpx
```

2. Set your NVIDIA API key:

Create a file named `.env` in the project root and add this line:

```env
NVIDIA_API_KEY=your_api_key_here
```

You can also copy `.env.example` to `.env` and replace the placeholder value.

3. Run the chatbot:

```bash
python chatbot.py
```

## How It Works

The script uses the `httpx` library to send requests to the NVIDIA NIM OpenAI-compatible endpoint. Conversation history is maintained in a simple list of messages, which is passed back to the model with each turn to preserve context.

## Usage

- Type a message and press Enter.
- Read the streaming AI response.
- Keep chatting as long as you want.
- Type `exit` or `quit` to close the session.

## Project Files

- `chatbot.py`: main CLI chatbot script
- `README.md`: project overview and setup instructions
- `prompt.md`: reusable prompt ideas
- `changeble-log.md`: change tracking notes
- `.gitignore`: files and folders to exclude from version control
