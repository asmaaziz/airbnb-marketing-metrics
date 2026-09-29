# Airbnb's hidden marketing metrics

**Live page:** https://asmaaziz.github.io/airbnb-marketing-metrics/

A single-page analysis of marketing efficiency metrics Airbnb doesn't report, derived from its public annual filings (FY2019–FY2024).

**Metrics derived**
- Marginal marketing cost per incremental night booked
- Gross booking value per marketing dollar
- Sales & marketing as % of revenue vs. take rate
- Growth split into price (ADR) and volume (nights)

## Run it on GitHub Pages
1. Create a public repo named `airbnb-marketing-metrics` and upload `index.html` and this `README.md`.
2. Go to **Settings → Pages**, set Source to *Deploy from a branch*, branch `main`, folder `/ (root)`, and save.
3. After a minute or two the page is live at https://asmaaziz.github.io/airbnb-marketing-metrics/

## Update the data
Edit the `DATA` array near the top of the `<script>` in `index.html`. Every chart, table and takeaway sentence recalculates from it.

## Caveats
Sales & marketing figures are rounded from 10-K filings; verify before citing. Airbnb doesn't split brand vs. performance spend, and year-over-year deltas attribute all new bookings to marketing, so the marginal metric is an upper bound rather than a true CAC.

---
By [Asma Aziz](https://github.com/asmaaziz). Other work: [flight-delays](https://github.com/asmaaziz/flight-delays), [sentiment-analysis](https://github.com/asmaaziz/sentiment-analysis), [text-mining](https://github.com/asmaaziz/text-mining).
