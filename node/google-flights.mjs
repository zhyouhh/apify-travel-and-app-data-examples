import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('zhyou/google-flights-scraper').call({
    routes: ['JFK-LAX'],
    departureDates: ['+30'],
    additionalDays: 6,
    maxStops: '0',
    currency: 'USD',
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
const priced = items.filter((row) => row.price !== null);
priced.sort((a, b) => a.price - b.price);

for (const row of priced.slice(0, 10)) {
    console.log(
        `${row.departureDate} ${row.flightNumbers.join(', ')} ` +
        `${row.price} ${row.currency} (${row.priceLevel ?? 'n/a'})`,
    );
}
