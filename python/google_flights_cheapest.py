import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zhyou/google-flights-scraper").call(
    run_input={
        "routes": ["JFK-LAX", "SFO-NRT"],
        "departureDates": ["+30"],
        "additionalDays": 6,
        "currency": "USD",
    }
)

cheapest = {}
for row in client.dataset(run.default_dataset_id).iterate_items():
    if row["price"] is None:  # some carriers show no fare on Google Flights
        continue
    key = (row["origin"], row["destination"], row["departureDate"])
    if key not in cheapest or row["price"] < cheapest[key]["price"]:
        cheapest[key] = row

for (origin, dest, date), row in sorted(cheapest.items()):
    print(
        f"{origin}-{dest} {date}: {row['price']} {row['currency']} "
        f"({row.get('priceLevel') or 'no price level'}, {row['stops']} stops, "
        f"{', '.join(row['airlines'])})"
    )
