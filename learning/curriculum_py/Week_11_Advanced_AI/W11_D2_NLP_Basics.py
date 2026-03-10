# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 2  |  NLP BASICS (Text Processing)
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Clean and preprocess text (lowercase, punctuation, stopwords)
#  2. Tokenize text and extract features
#  3. Perform basic sentiment analysis (rule-based and model-based)
#  4. Extract named entities from text (NER)
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "NLP natural language processing Python tutorial beginners"
#  Search: "spaCy Python tutorial named entity recognition"
#  Search: "sentiment analysis Python VADER TextBlob"
#
#  INSTALL:
#    pip install spacy textblob
#    python -m spacy download en_core_web_sm
#
# ══════════════════════════════════════════════════════════════

import re
import string
from collections import Counter


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — TEXT CLEANING
# ══════════════════════════════════════════════════════════════
#
# Raw text from files, APIs, and web scraping is messy.
# Before any NLP task, you clean it:
#   - Lowercase everything (so "Python" and "python" are the same)
#   - Remove punctuation (.,!?'"...)
#   - Remove extra whitespace
#   - Remove stopwords (very common words that add no meaning: "the", "is", "a")

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 55)
print("CONCEPT 1: Text Cleaning")
print("=" * 55)

raw_text = "   The SALES pipeline processed 1,500 records!!! Some records had NULL values... Fix them ASAP.  "

# Step 1: lowercase
step1 = raw_text.lower()
print("Lowercase:  ", step1.strip())

# Step 2: remove punctuation
step2 = step1.translate(str.maketrans("", "", string.punctuation))
print("No punct:   ", step2.strip())

# Step 3: remove extra whitespace
step3 = " ".join(step2.split())
print("Clean:      ", step3)

# Step 4: tokenize (split into words)
tokens = step3.split()
print("Tokens:     ", tokens)

# Step 5: remove stopwords
stopwords = {"the", "a", "an", "is", "are", "was", "were", "had", "them", "some"}
filtered = [word for word in tokens if word not in stopwords]
print("No stops:   ", filtered)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Clean a Customer Review
# ══════════════════════════════════════════════════════════════
#
# Clean the following review text using all 5 steps above.
# Print the cleaned token list.
#
# Expected output (approximately):
#     ['wow', 'product', 'amazing', 'ive', 'using', '3', 'months', 'best',
#      'purchase', 'ive', 'ever', 'made', 'highly', 'recommend', 'everyone']

# --- starting data ---
review = "WOW!! This product is AMAZING... I've been using it for 3 months and it's the BEST purchase I've ever made!!! Highly recommend it to everyone."





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WORD FREQUENCY ANALYSIS
# ══════════════════════════════════════════════════════════════
#
# After cleaning, count how often each word appears.
# The most frequent words often reveal the main topics.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Word Frequency")
print("=" * 55)

support_tickets = """
    My order was delayed again. The delivery took 2 weeks.
    Tracking shows my package is still in transit.
    I ordered 10 days ago but no delivery yet.
    The package was damaged when it finally arrived.
    Delivery was delayed by 5 days with no explanation.
    My order is missing one item from the package.
"""

# Clean
cleaned = re.sub(r'[^\w\s]', '', support_tickets.lower())
words   = cleaned.split()

# Remove stopwords
stops   = {"my", "the", "was", "is", "it", "in", "by", "a", "an", "with",
           "when", "but", "no", "from", "one", "i", "still", "yet", "took"}
words   = [w for w in words if w not in stops]

# Count
freq = Counter(words)
print("Top 10 words in support tickets:")
for word, count in freq.most_common(10):
    bar = "=" * count
    print(f"  {word:15}: {count:2}  {bar}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Analyze Product Reviews
# ══════════════════════════════════════════════════════════════
#
# Analyze these 5 reviews to find the most mentioned topics.
#
# 1. Combine all reviews into one text, clean it
# 2. Count word frequency
# 3. Print the top 8 words
# 4. As a comment: what are the main topics customers talk about?

# --- starting data ---
reviews = [
    "Fast delivery but poor quality product. The screen broke after one week.",
    "Great quality! Screen is excellent. Battery lasts all day. Fast charging too.",
    "Battery drains fast. Screen is great but battery life is terrible.",
    "Poor packaging. Product quality is amazing but delivery was slow.",
    "Excellent screen and battery. Fast delivery. Great quality overall."
]





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════
#
# Sentiment analysis = classify text as positive, negative, or neutral.
#
# Two approaches:
#   1. Rule-based (VADER): uses a dictionary of positive/negative words + rules
#      Fast, no model needed, works well for short texts like social media
#
#   2. Model-based (transformer): uses a fine-tuned ML model
#      More accurate, handles context better, slower
#
# TextBlob example (rule-based, simple):
#
#   from textblob import TextBlob
#   blob = TextBlob("This product is amazing!")
#   polarity = blob.sentiment.polarity   # -1 (negative) to +1 (positive)
#   sentiment = "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Sentiment Analysis")
print("=" * 55)

# Rule-based fallback (no install needed):
positive_words = {"amazing", "great", "excellent", "love", "perfect", "best", "good", "fast"}
negative_words = {"terrible", "worst", "broken", "bad", "poor", "slow", "damaged", "missing"}

def simple_sentiment(text):
    words = text.lower().split()
    pos = sum(1 for w in words if w in positive_words)
    neg = sum(1 for w in words if w in negative_words)
    if pos > neg:   return "positive"
    if neg > pos:   return "negative"
    return "neutral"

test_reviews = [
    "Amazing product! Great quality and fast delivery.",
    "Terrible experience. Product was broken and missing parts.",
    "It arrived. Works as expected.",
]

print()
print("Simple rule-based sentiment:")
for r in test_reviews:
    print(f"  {simple_sentiment(r):10}  |  {r}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Analyze Support Ticket Sentiment
# ══════════════════════════════════════════════════════════════
#
# Using the simple_sentiment() function above,
# analyze these 6 customer reviews and count how many are positive,
# negative, and neutral. Print a summary.
#
# Expected output:
#     Positive: 2
#     Negative: 3
#     Neutral:  1

# --- starting data ---
customer_reviews = [
    "Great product, amazing quality and very fast shipping!",
    "Broken on arrival. Terrible packaging. Worst purchase.",
    "Product is OK. Nothing special but works fine.",
    "Poor quality. The item is missing parts. Bad experience.",
    "Best product I ever bought. Great value for money.",
    "Slow delivery but product quality is good.",
]




