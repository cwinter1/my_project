# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 1  |  WORKING WITH LLM APIS (OpenAI / Anthropic)
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what an LLM API is and how it works
#  2. Make a basic API call to an LLM (OpenAI or Anthropic)
#  3. Pass a system prompt and a user message
#  4. Extract and use the text response in your Python code
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "OpenAI API Python tutorial beginners"
#  Search: "Anthropic Claude API Python tutorial"
#  Search: "what is an LLM large language model explained"
#
#  INSTALL:
#    pip install openai           (for OpenAI GPT models)
#    pip install anthropic        (for Anthropic Claude models)
#
#  API KEYS:
#    Get a free OpenAI key:    https://platform.openai.com/api-keys
#    Get an Anthropic key:     https://console.anthropic.com/
#
#    NEVER hardcode your API key in the file.
#    Store it as an environment variable:
#      Windows:  setx OPENAI_API_KEY "your-key-here"
#      Mac/Linux: export OPENAI_API_KEY="your-key-here"
#
# ══════════════════════════════════════════════════════════════

import os


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS AN LLM API?
# ══════════════════════════════════════════════════════════════
#
# LLM = Large Language Model (GPT-4, Claude, Gemini, Llama, etc.)
# API = a way for your Python code to send a message to the model and get a reply.
#
# Think of it like texting a very smart assistant:
#   You send:  "Summarize this text: [your text]"
#   It replies: "Here is a summary..."
#
# The two most important concepts:
#
# SYSTEM PROMPT  — instructions given to the model before the conversation starts
#                  "You are a data analyst. Always respond with concise JSON."
#
# USER MESSAGE   — what the user (your code) sends
#                  "Classify this customer review as positive, negative, or neutral."
#
# TOKENS         — LLMs measure text in tokens, not words.
#                  ~1 token = ~0.75 words.  You pay per token used.
#                  Keep prompts concise to reduce cost.
#
# HOW THE CALL WORKS:

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: LLM API Architecture")
print("=" * 55)
print()
print("Your code  →  API request  →  LLM server  →  API response  →  Your code")
print()
print("Request contains:")
print("  - model name     (e.g. 'gpt-4o-mini' or 'claude-haiku-4-5-20251001')")
print("  - messages list  (system + user message)")
print("  - max_tokens     (limit the response length)")
print()
print("Response contains:")
print("  - choices[0].message.content  (OpenAI)")
print("  - content[0].text             (Anthropic)")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Good prompt design is critical — the quality of your output depends on it.
# Write a system prompt and user message for each of these tasks.
# Answer as comments (no API call yet).
#
# Task A: Classify a customer review as "positive", "negative", or "neutral"
#   System prompt: ?
#   User message:  "The delivery was late and the product was broken."
#
# Task B: Extract structured data from free text
#   System prompt: ?
#   User message:  "John Smith, age 34, lives in Tel Aviv, salary 120,000 NIS"
#   Expected output: JSON with name, age, city, salary
#
# Task C: Translate a Python error message into plain English for a beginner
#   System prompt: ?
#   User message:  "TypeError: 'NoneType' object is not subscriptable"
#
# Expected output:
#     Task A system: a prompt instructing classification into 3 categories
#     Task B system: a prompt requesting JSON extraction
#     Task C system: a prompt for plain-English error translation





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — MAKING AN API CALL (OpenAI)
# ══════════════════════════════════════════════════════════════
#
# NOTE: This code requires a valid OpenAI API key.
#       If you don't have one yet, read through the code and continue.
#       You'll use the same pattern in all future AI lessons.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: OpenAI API Call")
print("=" * 55)

# To run this example, uncomment the code below and set your API key.

# from openai import OpenAI
#
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#
# response = client.chat.completions.create(
#     model="gpt-4o-mini",          # fast and cheap model — good for practice
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a data analyst assistant. Give short, direct answers."
#         },
#         {
#             "role": "user",
#             "content": "What are the 3 most important skills for a data engineer in 2025?"
#         }
#     ],
#     max_tokens=200
# )
#
# answer = response.choices[0].message.content
# print("Response:")
# print(answer)
# print()
# print(f"Tokens used: {response.usage.total_tokens}")

print("(Uncomment the OpenAI code above once you have an API key)")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — MAKING AN API CALL (Anthropic Claude)
# ══════════════════════════════════════════════════════════════
#
# Same concept, slightly different syntax.
# Claude models are: claude-haiku (fast/cheap), claude-sonnet (balanced), claude-opus (smart)

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 3: Anthropic Claude API Call")
print("=" * 55)

# To run this example, uncomment the code below and set your API key.

# import anthropic
#
# client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
#
# message = client.messages.create(
#     model="claude-haiku-4-5-20251001",   # fast and cheap — good for practice
#     max_tokens=200,
#     system="You are a data analyst assistant. Give short, direct answers.",
#     messages=[
#         {
#             "role": "user",
#             "content": "What are the 3 most important skills for a data engineer in 2025?"
#         }
#     ]
# )
#
# answer = message.content[0].text
# print("Response:")
# print(answer)
# print()
# print(f"Input tokens:  {message.usage.input_tokens}")
# print(f"Output tokens: {message.usage.output_tokens}")

print("(Uncomment the Anthropic code above once you have an API key)")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Once you have an API key (either OpenAI or Anthropic),
# write a Python function called classify_sentiment(text) that:
#   1. Sends the text to an LLM with a system prompt asking for sentiment classification
#   2. Returns ONLY the word: "positive", "negative", or "neutral"
#
# Then test it with these 3 reviews:
#   "The product is amazing, I love it!"
#   "Worst purchase ever, complete waste of money."
#   "It arrived on time and does what it says."
#
# Expected output:
#     positive
#     negative
#     neutral

reviews_to_classify = [
    "The product is amazing, I love it!",
    "Worst purchase ever, complete waste of money.",
    "It arrived on time and does what it says.",
]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 — HANDLING API RESPONSES AND ERRORS
# ══════════════════════════════════════════════════════════════
#
# When calling LLM APIs in production, always handle errors:
#   - Network errors (timeout, connection refused)
#   - Rate limiting (too many requests per minute)
#   - Invalid API key
#   - Token limit exceeded
#
# Best practices:
#   - Wrap API calls in try/except
#   - Log every request and response for debugging
#   - Set a timeout to avoid hanging
#   - Cache responses when possible to save money

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 4: Error Handling for API Calls")
print("=" * 55)

def safe_llm_call(prompt, system="You are a helpful assistant."):
    """Template for a safe LLM API call with error handling."""
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[
    #             {"role": "system", "content": system},
    #             {"role": "user",   "content": prompt}
    #         ],
    #         max_tokens=200,
    #         timeout=30
    #     )
    #     return {"success": True, "text": response.choices[0].message.content}
    # except Exception as e:
    #     return {"success": False, "error": str(e)}

    # Placeholder:
    return {"success": True, "text": f"[Placeholder response for: {prompt[:50]}...]"}

result = safe_llm_call("What is a data pipeline?")
print(f"  Success: {result['success']}")
print(f"  Text:    {result.get('text', result.get('error', 'N/A'))}")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function extract_contact_info(text) that sends text to the LLM
# and asks it to return a JSON with: name, email, phone (if found).
#
# Test with:
#   text = "Hi, I'm Sarah Levi. You can reach me at sarah.levi@email.com or 054-1234567"
#
# Parse the JSON response using json.loads() and print each field.
#
# Use safe_llm_call() or your own API call function.
# In your system prompt, say "Respond ONLY with valid JSON, no extra text."
#
# Expected output:
#     Name:  Sarah Levi
#     Email: sarah.levi@email.com
#     Phone: 054-1234567

contact_text = "Hi, I'm Sarah Levi. You can reach me at sarah.levi@email.com or 054-1234567"




