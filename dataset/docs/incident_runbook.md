# Incident Runbook

## Revenue Drop Investigation
1. Compare actual revenue with forecast and comparable historical periods.
2. Break variance down by country, channel and category.
3. Validate data freshness before concluding the business actually declined.
4. Check pipeline runs and source availability timestamps.
5. If a partition is late, classify the event as a data-quality incident.
6. Backfill the partition and rerun downstream transformations.

## Payment Investigation
Check payment status distribution, ingestion health, provider rate limits and pending-record reconciliation.

## Delivery Delay Investigation
Compare delay rate by carrier and market, then separate warehouse dispatch delay from carrier transit delay.
