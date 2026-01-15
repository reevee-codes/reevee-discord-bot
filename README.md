# Discord Bot Python

A simple, extensible Discord bot written in Python.

## Features
- Ready-to-use commands:
  - `!ping`
  - `!echo`
  - `!fact`
  - `!facts`
  - `!quote`
  - `!chat`
- Easy to expand with your own commands and services
- Clean codebase structure for quick development
- OpenAI integration (API key required)

## Setup

1. **Clone the repository**
2. **Install dependencies**  
   Make sure you're using Python 3.10+.  
   This project uses `pyproject.toml`, so install with:
   ```bash
   pip install .
   ```
   Alternatively, use a PEP 517-compatible tool like poetry or pipx.
3. **Set your Discord token and OpenAI API key**  
   Place your credentials in environment variables:
   ```bash
   set DISCORD_TOKEN=your-discord-token
   set OPENAI_API_KEY=your-openai-key
   ```
   (On Linux/Mac use `export` instead of `set`)
4. **Run the bot**
   ```bash
   python -m app.bot
   ```

---

Designed to be clean, fast, and easy to expand. The perfect starting point for your own Discord bot!
