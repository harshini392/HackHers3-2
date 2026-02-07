import huggingface_ai
from sentiment_ai import analyze_review as textblob_analyze
from langdetect import detect, DetectorFactory
import logging

# For consistent language detection
DetectorFactory.seed = 0

def analyze_review_complete(text):
    """
    Complete analysis using both Hugging Face and TextBlob
    """
    results = {}
    
    # Try Hugging Face first
    try:
        sentiment_hf = huggingface_ai.analyze_sentiment(text)
        results["sentiment"] = sentiment_hf
        results["sentiment_source"] = "Hugging Face"
    except Exception as e:
        logging.error(f"Hugging Face failed: {e}")
        # Fallback to TextBlob
        try:
            _, sentiment_tb = textblob_analyze(text)
            results["sentiment"] = sentiment_tb
            results["sentiment_source"] = "TextBlob (Fallback)"
        except:
            results["sentiment"] = "Neutral"
            results["sentiment_source"] = "Default"
    
    # Language detection
    try:
        language_code = detect(text)
        # Map language codes to full names
        language_map = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        language = language_map.get(language_code, language_code.upper())
        results["language"] = f"{language} (Auto-detected)"
    except Exception as e:
        logging.error(f"Language detection failed: {e}")
        results["language"] = "Multilingual/Unknown"
    
    return results