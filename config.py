"""
Configuration file for the CLI Chatbot.
Contains all configurable constants and settings.
"""

# Request Configuration
REQUEST_TIMEOUT = 60
MAX_RETRIES = 5
BASE_BACKOFF_DELAY = 1  # seconds

# Conversation Configuration
MAX_HISTORY = 20  # Keep system prompt + last 20 messages
SYSTEM_PROMPT = "You are a helpful assistant."

# Logging Configuration
LOGS_DIR = "logs"
APP_LOG_FILE = f"{LOGS_DIR}/app.log"
ERROR_LOG_FILE = f"{LOGS_DIR}/error.log"

# Provider Fallback Order (if primary provider fails)
FALLBACK_PROVIDERS = ["nvidia", "openrouter", "gemini"]

# Token estimation constants (for when API doesn't provide token counts)
AVG_CHARS_PER_TOKEN = 4  # Rough estimate: 4 characters per token