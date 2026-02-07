from flask import Flask, render_template, request
from database import insert_review, fetch_all_reviews
from analyzer import analyze_review_complete  # Use the new unified analyzer

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home")
def home():
    reviews = fetch_all_reviews()
    return render_template("dashboard.html", page="dashboard", reviews_data=reviews)

@app.route("/page/<name>", methods=["GET", "POST"])
def page(name):
    submitted_data = None

    if request.method == "POST" and name == "new":
        brand = request.form.get("brand")
        review = request.form.get("review")

        try:
            # Use the unified analyzer
            analysis = analyze_review_complete(review)
            
            # Extract results
            sentiment = analysis.get("sentiment", "Neutral")
            language = analysis.get("language", "Unknown")
            source = analysis.get("sentiment_source", "Unknown")
            
            # Format language with source info
            formatted_language = f"{language} ({source})"
            
            insert_review(brand, review, formatted_language, sentiment)
            
            submitted_data = {
                "brand": brand,
                "review": review,
                "language": formatted_language,
                "sentiment": sentiment
            }
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            submitted_data = {
                "brand": brand,
                "review": review,
                "language": "Analysis Error",
                "sentiment": "Failed"
            }

    reviews = fetch_all_reviews()

    return render_template(
        "dashboard.html",
        page=name,
        submitted_data=submitted_data,
        reviews_data=reviews
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)