import csv
import json
import os
from decimal import Decimal

from apify_client import ApifyClient

with open("inputs/app-store-reviews-all.json") as f:
    run_input = json.load(f)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zhyou/apple-app-store-scraper").call(
    run_input=run_input,
    max_total_charge_usd=Decimal("2.00"),  # $0.10 per 1,000 reviews -> up to ~20,000 reviews
)

fields = ["appId", "appName", "country", "reviewId", "rating", "title", "text", "date", "isEdited"]
count = 0
with open("reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for review in client.dataset(run.default_dataset_id).iterate_items():
        writer.writerow(review)
        count += 1
print(f"{count} reviews -> reviews.csv")
