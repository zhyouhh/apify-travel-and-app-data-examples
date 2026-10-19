"""Recent 1-2 star Google Play reviews, and how many of them the developer answered."""
import json
import os
from decimal import Decimal

from apify_client import ApifyClient

with open("inputs/google-play-complaints.json") as f:
    run_input = json.load(f)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zhyou/google-play-scraper").call(
    run_input=run_input,
    max_total_charge_usd=Decimal("0.50"),  # $0.10 per 1,000 reviews
)

reviews = list(client.dataset(run.default_dataset_id).iterate_items())
answered = sum(1 for r in reviews if r.get("developerReply"))
print(f"{len(reviews)} low-star reviews in the last 30 days, {answered} answered by the developer")
for r in reviews[:10]:
    print(f"- {r['rating']}★ {r['date'][:10]} v{r.get('appVersion') or '?'}: {r['text'][:120]!r}")
