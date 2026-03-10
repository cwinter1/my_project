# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 3  |  SPEECH RECOGNITION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Transcribe audio to text using OpenAI Whisper
#  2. Record audio from a microphone in Python
#  3. Build a simple voice-to-text pipeline
#  4. Know the main use cases for speech recognition in data roles
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "OpenAI Whisper Python tutorial transcription"
#  Search: "Python speech recognition whisper microphone"
#  Search: "speech to text Python beginners 2025"
#
#  INSTALL:
#    pip install openai-whisper pyaudio SpeechRecognition
#    (Whisper also needs: pip install torch  — may take a while to download)
#    OR use the Whisper API (no local install):
#    pip install openai
#
# ══════════════════════════════════════════════════════════════

import os


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS SPEECH RECOGNITION?
# ══════════════════════════════════════════════════════════════
#
# Speech Recognition = convert audio (voice) to text
#
# Main approaches:
#   1. Cloud API   -- send audio to a server, get text back (easy, costs money)
#                     Examples: OpenAI Whisper API, Google Speech-to-Text
#   2. Local model -- run the model on your machine (free, slower)
#                     Examples: whisper (local), vosk
#
# OpenAI WHISPER is the current best-in-class open-source model.
#   - Supports 99 languages including Hebrew
#   - Very accurate even with background noise
#   - Available as: local model OR cloud API (cheaper for occasional use)
#
# USE CASES FOR DATA ROLES:
#   - Transcribe recorded meetings/interviews automatically
#   - Build voice-activated data query systems ("show me sales for Q3")
#   - Process call center recordings for sentiment analysis
#   - Accessibility features in data dashboards

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 55)
print("CONCEPT 1: Speech Recognition Options")
print("=" * 55)
print()
print("Option A — Whisper API (cloud):")
print("  import openai")
print("  client = openai.OpenAI()")
print("  with open('audio.mp3', 'rb') as f:")
print("      result = client.audio.transcriptions.create(model='whisper-1', file=f)")
print("  print(result.text)")
print()
print("Option B — Whisper local (offline):")
print("  import whisper")
print("  model = whisper.load_model('base')  # or 'small', 'medium', 'large'")
print("  result = model.transcribe('audio.mp3')")
print("  print(result['text'])")
print()
print("Option C — SpeechRecognition (microphone):")
print("  import speech_recognition as sr")
print("  r = sr.Recognizer()")
print("  with sr.Microphone() as source:")
print("      audio = r.listen(source)")
print("  text = r.recognize_google(audio)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Choose the Right Tool
# ══════════════════════════════════════════════════════════════
#
# For each scenario, choose the best speech recognition approach (A, B, or C)
# and explain why. Write answers as comments.
#
# Scenario 1: You need to transcribe 500 hours of old customer call recordings
#             stored as MP3 files on a server. Budget is limited.
#   Best approach: ? Why: ?
#
# Scenario 2: You are building a live voice assistant that runs on a laptop
#             with no internet connection.
#   Best approach: ? Why: ?
#
# Scenario 3: You need to quickly transcribe a single 5-minute meeting recording
#             in Hebrew and already have an OpenAI API key.
#   Best approach: ? Why: ?
#
# Expected output:
#     (comment-based answers for all 3 scenarios)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — TRANSCRIBE AUDIO WITH WHISPER API
# ══════════════════════════════════════════════════════════════
#
# The Whisper API is the simplest option — just send the audio file, get text back.
# Supports: mp3, mp4, wav, m4a, webm, ogg, flac
# Max file size: 25 MB
# Cost: ~$0.006 per minute of audio (very cheap)
#
# Code pattern (requires OPENAI_API_KEY):
#
#   import openai
#   client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#
#   with open("audio.mp3", "rb") as audio_file:
#       response = client.audio.transcriptions.create(
#           model="whisper-1",
#           file=audio_file,
#           language="en"       # optional ISO code: "en", "he", "es"
#       )
#   print(response.text)

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Whisper API Transcription")
print("=" * 55)

def transcribe_file(audio_path, language=None):
    """
    Transcribe an audio file using OpenAI Whisper API.
    Returns the transcript text.
    (Placeholder — uncomment API call when you have a key)
    """
    # import openai
    # client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # with open(audio_path, "rb") as audio_file:
    #     response = client.audio.transcriptions.create(
    #         model="whisper-1",
    #         file=audio_file,
    #         language=language
    #     )
    # return response.text

    # Placeholder for demo:
    return f"[Transcript of {os.path.basename(audio_path)}] This is a placeholder."

print("transcribe_file() defined — uncomment API call after setting OPENAI_API_KEY")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Build a Transcription Pipeline
# ══════════════════════════════════════════════════════════════
#
# Write a function called process_audio_folder(folder_path) that:
#   1. Finds all .mp3 and .wav files in the folder
#   2. Transcribes each one using transcribe_file()
#   3. Saves each transcript to a .txt file with the same name
#   4. Returns a dict: {filename: transcript_text}
#
# Use os.listdir() to find files and check the extension with .endswith()
#
# Note: you can write and test this function without audio files —
# just use the placeholder transcribe_file() defined above.
#
# Expected output:
#     Processing: meeting_01.mp3
#     Saved transcript to: meeting_01.txt
#     Processing: call_02.wav
#     Saved transcript to: call_02.txt
#     Result: {'meeting_01.mp3': '[Transcript...]', 'call_02.wav': '[Transcript...]'}





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — VOICE PIPELINE: SPEAK, TRANSCRIBE, PROCESS, RESPOND
# ══════════════════════════════════════════════════════════════
#
# Combining speech recognition with LLMs creates a voice assistant:
#
#   [Microphone] -> [Whisper] -> [text] -> [LLM] -> [answer text] -> [display/TTS]
#
# Real-world data example:
#   User says: "Show me the top 5 customers by revenue this quarter"
#   Whisper transcribes it
#   LLM converts it to SQL or pandas code
#   Code runs and returns data
#   Result displayed or spoken back

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Voice -> Text -> LLM Pipeline")
print("=" * 55)

def voice_to_query_pipeline(audio_text_input):
    """
    Simulated pipeline:
      audio -> transcript -> LLM converts to SQL -> return query
    """
    # In production: replace audio_text_input with actual Whisper transcription

    # LLM call (uncomment with real API key):
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system",
    #          "content": "Convert the user's question into a SQL SELECT query. "
    #                     "Table: sales(customer_id, customer_name, revenue, quarter, city). "
    #                     "Return ONLY the SQL, no explanation."},
    #         {"role": "user", "content": audio_text_input}
    #     ],
    #     max_tokens=100
    # )
    # return response.choices[0].message.content.strip()

    # Placeholder:
    return f"SELECT * FROM sales WHERE ... -- (would be generated by LLM from: '{audio_text_input}')"

# Test the pipeline
voice_inputs = [
    "Show me top 5 customers by revenue this quarter",
    "How many sales were made in Tel Aviv last month?",
    "What is the average revenue per city?",
]

print()
for voice_input in voice_inputs:
    query = voice_to_query_pipeline(voice_input)
    print(f"Voice: '{voice_input}'")
    print(f"SQL:   {query}")
    print()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Extend the Voice Pipeline
# ══════════════════════════════════════════════════════════════
#
# Extend voice_to_query_pipeline() to handle two types of requests:
#
#   Type 1: "data question" (show me, how many, what is...)
#           -> convert to SQL query (as above)
#
#   Type 2: "action request" (send email, create report, schedule job...)
#           -> return a description of the action to take
#
# Add a classification step BEFORE the SQL conversion that decides the type.
# If it is a data question -> generate SQL
# If it is an action -> return "Action: [description of action]"
#
# Test with:
#   "Show me total revenue by region"           -> SQL query
#   "Send the Q3 report to the management team" -> Action description
#
# Expected output:
#     Input: "Show me total revenue by region"
#     Type:  data_question
#     Output: SELECT ... FROM sales ...
#
#     Input: "Send the Q3 report to the management team"
#     Type:  action_request
#     Output: Action: Send Q3 report to management team via email




