# Conversational Chatbot

## Overview
This project is a simple multi-turn conversational chatbot built with Python and the OpenAI-compatible chat completions API.

It demonstrates:
- Maintaining conversation history across turns
- Comparing stateful vs stateless chatbot behavior
- Running a small test flow to validate memory in responses

## Features
- Loads API key from `OPENAI_API_KEY`
- Supports:
  - OpenAI API (default model: `gpt-3.5-turbo`)
  - Groq OpenAI-compatible API when the key starts with `gsk_`
- Auto-selects a working Groq chat model (excluding non-chat model families)
- Includes:
  - `chat(user_input)` for history-aware conversation
  - `chat_without_history(user_input)` for stateless comparison

## Project Structure
```text
Conversational-Chatbot/
├── chatbot.py         # Main chatbot script and experiment flow
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Prerequisites
- Python 3.9+ (recommended)
- An API key set in environment variable:
  - OpenAI: `OPENAI_API_KEY=<your_openai_key>`
  - Groq: `OPENAI_API_KEY=<your_groq_key_starting_with_gsk_>`

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Export your API key:
   ```bash
   export OPENAI_API_KEY="your_actual_key"
   ```
2. Run the chatbot script:
   ```bash
   python chatbot.py
   ```

## What the Script Runs
The script executes two experiments:

1. **Multi-turn memory test** (stateful):  
   Sends three related prompts while preserving full message history.

2. **Control experiment** (stateless):  
   Sends the same prompts without preserving prior turns.

This helps illustrate the effect of conversation history on response quality and continuity.

## Notes
- If `OPENAI_API_KEY` is missing or left as a placeholder, the script raises a clear error.
- The script currently runs predefined prompts rather than interactive terminal input.