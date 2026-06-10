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