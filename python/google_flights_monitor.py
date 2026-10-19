import json
import os

from apify_client import ApifyClient

with open("inputs/google-flights-monitor.json") as f:
    run_input = json.load(f)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zhyou/google-flights-scraper").call(run_input=run_input)

for row in client.dataset(run.default_dataset_id).iterate_items():
    old, new = row.get("previousPrice"), row.get("price")
    if row.get("monitorStatus") == "changed" and old is not None and new is not None and new < old:
        print(
            f"DROP {row['origin']}-{row['destination']} {row['departureDate']} "
            f"{', '.join(row['flightNumbers'])}: {old} -> {new} {row['currency']}  "
            f"{row['googleFlightsUrl']}"
        )
