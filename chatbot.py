import os
from openai import OpenAI

# Task 1: Read the API key from the OPENAI_API_KEY environment variable
api_key = os.environ.get("OPENAI_API_KEY", "").strip()

if not api_key or api_key == "PASTE_YOUR_KEY_HERE":
    raise ValueError("ERROR: Please run export OPENAI_API_KEY='your_actual_key' in the terminal first!")

# Create the OpenAI client and dynamically find a working chat model
if api_key.startswith("gsk_"):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    all_models = [m.id for m in client.models.list().data]
    MODEL_NAME = None
    for candidate in all_models:
        if any(x in candidate.lower() for x in ["whisper", "tts", "orpheus", "guard", "embed"]):
            continue
        try:
            # Test the model with a tiny 1-token request to ensure it works
            client.chat.completions.create(
                model=candidate,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1
            )
            MODEL_NAME = candidate
            break
        except Exception:
            continue
    if not MODEL_NAME:
        raise RuntimeError(f"Could not find an active chat model. Available models: {all_models}")
else:
    client = OpenAI(api_key=api_key)
    MODEL_NAME = "gpt-3.5-turbo"

# Task 2: Initialize conversation history with one system message
messages = [
    {"role": "system", "content": "You are a friendly and concise college lab assistant."}
]

print("Step 2 Success: Client connected using verified model:", MODEL_NAME)
print("Initial messages list:", messages)
print("Initial history length:", len(messages))

# Task 3: Define chat(user_input) to maintain conversation history
def chat(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )
    reply_text = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply_text})
    return reply_text

print("Step 3 Success: chat(user_input) function is ready!")

# Task 4: Run the three test prompts in order to verify multi-turn memory
test_prompts = [
    "What is supervised learning?",
    "Give one real-world example of it.",
    "Which of the models we discussed uses labels?"
]

print("\n" + "="*65)
print("TASK 4: MULTI-TURN CONVERSATION TEST (WITH HISTORY)")
print("="*65)

for turn, prompt in enumerate(test_prompts, start=1):
    print(f"\n--- Turn {turn} ---")
    print(f"User: {prompt}")
    reply = chat(prompt)
    print(f"Assistant: {reply}")
    print(f"[History Check] len(messages) after Turn {turn}: {len(messages)}")

print("\n" + "="*65)
print("Step 4 Success: All three turns completed with conversation memory!")
print("="*65)

# Task 5: Control Experiment (Sending ONLY system message + latest question, NO history)
def chat_without_history(user_input):
    temp_messages = [
        {"role": "system", "content": "You are a friendly and concise college lab assistant."},
        {"role": "user", "content": user_input}
    ]
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=temp_messages
    )
    return response.choices[0].message.content

print("\n" + "="*65)
print("TASK 5: CONTROL EXPERIMENT (STATELESS - NO HISTORY SENT)")
print("="*65)

for turn, prompt in enumerate(test_prompts, start=1):
    print(f"\n--- Control Turn {turn} (No History) ---")
    print(f"User: {prompt}")
    reply = chat_without_history(prompt)
    print(f"Assistant: {reply}")

print("\n" + "="*65)
print("Step 5 Success: Experiment 07 Complete!")
print("="*65)
