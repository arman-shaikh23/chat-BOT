# CLI Chatbot (Multi-Provider)

A terminal-based multi-turn chatbot built with Python, supporting NVIDIA NIM, OpenRouter, and Gemini.

## Tech Stack

- Python 3.10+
- `httpx` (for API requests)
- NVIDIA NIM / OpenRouter / Google Gemini
- ANSI terminal colors for a simple CLI UI

## Features

- **Multi-Provider Support**: Switch between NVIDIA, OpenRouter, and Gemini.
- **Codebase Explainer**: Use `--explain` to get an architectural overview of your project.
- **Token Tracking Dashboard**: Every request is logged to `logs/usage_dashboard.csv`.
- **Robust Error Handling**: Handles rate limits (429) and server errors (5xx) with exponential backoff.
- **Streaming Responses**: Real-time interaction for a better UX.
- **Manual History Maintenance**: Preserves context across multiple turns.
- **Clean CLI UI**: Color-coded prompts and usage feedback.

## Setup

1. Ensure dependencies are installed:

```bash
pip install httpx
```

2. Set your API keys in a `.env` file:

```env
NVIDIA_API_KEY=your_key
OPENROUTER_API_KEY=your_key
GEMINI_API_KEY=your_key
```

3. Run the chatbot:

```bash
# Default (NVIDIA)
python chatbot.py

# Explain the current codebase
python chatbot.py --explain

# Specify provider
python chatbot.py --provider gemini
```

## How It Works

The script uses `httpx` to communicate with various LLM providers. It maintains conversation history in a list and manages retries with exponential backoff to ensure reliability. The `--explain` tool scans local files (respecting filters in `config.py`) to provide context-aware project analysis.

## Project Files

- `chatbot.py`: Main CLI application.
- `config.py`: Configuration constants (retries, timeouts, file filters).
- `logs/usage_dashboard.csv`: Automated usage logging.
- `README.md`: Project documentation.
- `prompt.md`: Reusable prompt ideas.
- `changeble-log.md`: Detailed change history.
