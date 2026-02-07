import csv
from database import insert_review

with open("reviews_dataset.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        insert_review(
            row["brand"],
            row["review"],
            row["language"],
            row["sentiment"]
        )

print("✅ Dataset inserted successfully")