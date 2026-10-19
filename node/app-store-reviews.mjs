import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('zhyou/apple-app-store-scraper').call({
    mode: 'reviews',
    appIds: ['310633997'],
    countries: ['us'],
    maxReviewsPerApp: 1000,
    reviewSort: 'recent',
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();

const byStars = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
for (const review of items) byStars[review.rating] += 1;

console.log(`${items.length} reviews`);
for (const stars of [5, 4, 3, 2, 1]) console.log(`${stars}★ ${byStars[stars]}`);
