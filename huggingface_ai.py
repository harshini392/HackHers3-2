from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        device=-1
    )
    print("Hugging Face model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    sentiment_pipeline = None

def analyze_sentiment(text):
    if sentiment_pipeline is None:
        print("Model not loaded!")
        return "Neutral"
    
    try:
        # Clean the text
        if not text or len(text.strip()) == 0:
            return "Neutral"
            
        # Limit text length for the model
        truncated_text = text[:512]
        print(f"Analyzing text: {truncated_text[:100]}...")
        
        result = sentiment_pipeline(truncated_text)[0]
        print(f"Raw model output: {result}")
        
        # Try different label mappings
        label = result["label"]
        
        # Check if label is numeric (LABEL_0, LABEL_1, LABEL_2)
        if label.startswith("LABEL_"):
            label_map = {
                "LABEL_0": "Negative",
                "LABEL_1": "Neutral",
                "LABEL_2": "Positive"
            }
            sentiment = label_map.get(label, "Neutral")
        else:
            # Handle text labels
            label_lower = label.lower()
            if "negative" in label_lower:
                sentiment = "Negative"
            elif "neutral" in label_lower:
                sentiment = "Neutral"
            elif "positive" in label_lower:
                sentiment = "Positive"
            else:
                sentiment = "Neutral"
        
        print(f"Final sentiment: {sentiment}")
        return sentiment
        
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral"