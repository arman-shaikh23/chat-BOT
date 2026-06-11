# Change Log

## Template for Future Updates

Record each change here after you modify the project.

## Format

- Date: YYYY-MM-DD
- File(s) changed: [file names]
- What changed: short summary of the edit
- Why it changed: the reason for the update
- Purpose: what the change improves or enables
- Notes: any follow-up work or limitations

## Current Project State

- Migrated from Gemini to NVIDIA NIM (Llama 3.1)
- Added streaming responses for real-time interaction
- Updated history management to use a manual list (OpenAI-compatible)
- Refined code to ~50 lines for simplicity
- Updated documentation (README, .env.example, prompt.md)

- Date: 2026-06-09
- File(s) changed: chatbot.py, .env.example, README.md, prompt.md, changeble-log.md
- What changed: Switched provider from Google GenAI to NVIDIA NIM.
- Why it changed: User requested transition to NVIDIA key.
- Purpose: Enable usage of NVIDIA NIM while improving UI with streaming.
- Notes: Requires NVIDIA_API_KEY in .env.

- Date: 2026-06-10
- File(s) changed: chatbot.py, README.md, .gitignore, changeble-log.md
- What changed: Fixed "list index out of range" error in streaming logic and added .gitignore.
- Why it changed: To improve robustness against varied API response formats and keep the repository clean.
- Purpose: Prevent script crashes during interaction and exclude unnecessary files from version control.
- Notes: Added safety checks for JSON decoding and list indexing in streaming chunks.

- Date: 2026-06-10
- File(s) changed: chatbot.py, README.md, .env.example, changeble-log.md
- What changed: Refactored CLI to support NVIDIA, OpenRouter, and Gemini via `--provider` flag.
- Why it changed: User requested support for multiple API providers.
- Purpose: Increase flexibility and allow switching between different AI models.
- Notes: Implemented custom streaming logic for Gemini's specific API format. Added argparse for CLI flags.

- Date: 2026-06-10
- File(s) changed: chatbot.py
- What changed: Fixed 404 errors for Gemini and OpenRouter.
- Why it changed: Gemini URL was missing '?' for the API key, and OpenRouter required redirect following.
- Purpose: Ensure reliable connections to all providers.
- Notes: Manually constructed Gemini URL with key and enabled `follow_redirects=True` in httpx. Refined Gemini streaming JSON parsing.

- Date: 2026-06-10
- File(s) changed: chatbot.py, config.py, README.md, changeble-log.md
- What changed: Added codebase explainer tool and CSV usage logging for NVIDIA, Gemini, and OpenRouter.
- Why it changed: User requested project analysis and usage tracking for their existing API setup.
- Purpose: Enable project analysis and usage tracking without requiring Anthropic.
- Notes: CSV dashboard is in `logs/usage_dashboard.csv`. The `--explain` tool works with all supported providers.