from textblob import TextBlob
from langdetect import detect

def analyze_review(text):
    try:
        language = detect(text)
    except:
        language = "unknown"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return language, sentiment
