# apify-travel-and-app-data-examples

Runnable Python and Node.js examples for three Apify Actors:

- **[Google Flights Scraper & Price Tracker](https://apify.com/zhyou/google-flights-scraper)** (`zhyou/google-flights-scraper`): fares for many routes × dates, Google's low/typical/high price level, return flights for round trips, and a monitor mode that returns only new or changed fares with the previous price. $0.002 per search (one route on one date).
- **[Apple App Store Scraper](https://apify.com/zhyou/apple-app-store-scraper)** (`zhyou/apple-app-store-scraper`): reviews past the 500-per-country RSS limit, four sort orders, star and date filters, monitor mode for new reviews, app details with rating histogram and privacy labels, keyword search and top charts. $0.10 per 1,000 reviews, $0.50 per 1,000 app rows.
- **[Google Play Scraper](https://apify.com/zhyou/google-play-scraper)** (`zhyou/google-play-scraper`): reviews with developer replies and app versions, star and date filters, monitor mode, app details with installs and rating histogram, keyword search. $0.10 per 1,000 reviews, $0.50 per 1,000 app rows.

I built these Actors; this repo is the example code I point people to. Every example here was run against the live Actors before it was committed. Issues and PRs welcome.

## Setup

You need an Apify account (the free plan includes monthly usage credit) and an API token from **Apify Console → Settings → API & Integrations**.

```bash
export APIFY_TOKEN=your_token_here
pip install -r requirements.txt   # Python 3.10+, apify-client 3.x
npm install                       # Node.js 18+
```

Each Actor also charges $0.00005 per run start. You can cap the cost of any run with `max_total_charge_usd` in Python (see the scripts), or the maximum cost per run in the Console's run options.

## What's here

| File | What it does |
|---|---|
| `python/run_actor.py` | Run any of the Actors with any input file and save the dataset to JSON: `python python/run_actor.py zhyou/google-play-scraper inputs/google-play-search.json out.json` |
| `python/google_flights_cheapest.py` | Cheapest fare per route and date for the next week of departures 30 days out, with Google's price level |
| `python/google_flights_monitor.py` | Run it daily: prints fares that dropped since the previous run |
| `python/app_store_reviews_to_csv.py` | Export App Store reviews (2 apps × 2 countries, 2,000 each) to `reviews.csv` |
| `python/google_play_complaints.py` | Recent 1-2 star Google Play reviews and how many the developer answered |
| `node/google-flights.mjs` | Ten cheapest nonstop JFK-LAX fares 30-36 days out |
| `node/app-store-reviews.mjs` | Star distribution of an app's latest 1,000 App Store reviews |

Run the scripts from the repository root (they read `inputs/…`). The free Apify plan allows 5 concurrent runs, so run them one after another.

## Inputs

All field names are the Actors' real input fields; anything you leave out uses the Actor's default.

**Google Flights**

- `inputs/google-flights-basic.json`: 2 routes × 7 dates (30 days out, plus the next 6 days) = 14 searches.
- `inputs/google-flights-monitor.json`: monitor mode. Dates written as `+N` are compared run to run as "N days out" (same flight number and departure time), so a daily schedule tracks how the price for that distance moves. Fixed dates (`2026-12-18`) track one trip.
- `inputs/google-flights-round-trip.json`: round trip with the return options for the first 3 outbound flights (`returnFlightsFor`). Each return lookup counts as one search; return rows have `direction: "return"` and the round-trip total as `price`.

Other useful fields: `airlines` (`["AA", "DL"]` or `["STAR_ALLIANCE"]`), `maxStops`, `cabinClass`, `country` (point of sale), `language`, `children`, `infantsInSeat`, `infantsOnLap`, `maxItinerariesPerSearch`, `includePriceHistory`.

**App Store**

- `inputs/app-store-reviews-all.json`: latest 2,000 reviews per app and country (`maxReviewsPerApp: 0` means every review Apple serves).
- `inputs/app-store-reviews-complaints.json`: 1-2 star reviews from the last 90 days. Filtered-out reviews are not charged.
- `inputs/app-store-reviews-monitor.json`: schedule it; later runs return only reviews posted since the previous run.
- `inputs/app-store-app-details.json`: one row per app and country with `ratingHistogram`, `privacyLabels`, `inAppPurchases`, `versionHistory`, `chartPosition` and more.
- `inputs/app-store-search.json`: up to 200 results per term, each with `searchTerm` and `rank`.
- `inputs/app-store-charts.json`: top grossing games in the UK (`chart`: `top-free`, `top-paid`, `top-grossing`, and the `-ipad` variants; `chartGenre`: `all` or a genre ID, `6014` = Games).

Apps can be given as App Store URLs, numeric IDs or bundle IDs.

**Google Play**

- `inputs/google-play-reviews.json`: latest 1,000 English reviews for two apps (package names or Play Store URLs).
- `inputs/google-play-complaints.json`: 1-2 star reviews from the last 30 days.
- `inputs/google-play-app-details.json`: details in the US and Germany (prices in local currency).
- `inputs/google-play-search.json`: about 30 apps per search term.

Google Play keeps reviews per language, not per country, so reviews are fetched per app × `languages`.

## Output fields (short version)

- **Google Flights**, one row per itinerary: `origin`, `destination`, `departureDate`, `dateSpec`, `direction`, `price`, `currency`, `priceLevel`, `typicalPriceLow`, `typicalPriceHigh`, `airlines`, `flightNumbers`, `departure`, `arrival` (local times), `durationMinutes`, `stops`, `layovers`, `legs`, `co2Grams`, `googleFlightsUrl`. Monitor mode adds `monitorStatus` and `previousPrice`. `price` is `null` when Google shows no fare for that carrier.
- **App Store reviews**: `appId`, `appName`, `country`, `reviewId`, `rating`, `title`, `text`, `date`, `isEdited`.
- **Google Play reviews**: `appId`, `appName`, `language`, `reviewId`, `rating`, `text`, `date`, `thumbsUp`, `appVersion`, `developerReply`, `developerReplyDate`.

Reviewer names are not collected by either review scraper. Full field lists and example rows are in each Actor's README on Apify.

With `apify-client` 3.x for Python, `call()` returns a model object (`run.default_dataset_id`, `run.status`); older versions return a dict (`run["defaultDatasetId"]`).

## Links

- Actors: [Google Flights](https://apify.com/zhyou/google-flights-scraper) · [Apple App Store](https://apify.com/zhyou/apple-app-store-scraper) · [Google Play](https://apify.com/zhyou/google-play-scraper)
- [apify-client for Python](https://docs.apify.com/api/client/python) · [apify-client for JavaScript](https://docs.apify.com/api/client/js)
- [Apify schedules](https://docs.apify.com/platform/schedules) · [Integrations (Slack, email, Make, Zapier, n8n, webhooks)](https://docs.apify.com/platform/integrations)

Not affiliated with or endorsed by Google or Apple.

## License

MIT
