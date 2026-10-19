"""Usage: python python/run_actor.py zhyou/google-flights-scraper inputs/google-flights-basic.json out.json"""
import json
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

actor_id, input_path, output_path = sys.argv[1:4]
with open(input_path) as f:
    run_input = json.load(f)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor(actor_id).call(
    run_input=run_input,
    max_total_charge_usd=Decimal("1.00"),  # stop the run once it has cost $1
)
if run is None or run.status != "SUCCEEDED":
    sys.exit(f"Run did not succeed: {run and run.status}")

items = list(client.dataset(run.default_dataset_id).iterate_items())
with open(output_path, "w") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"{len(items)} rows -> {output_path}")
