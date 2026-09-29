# Airbnb's hidden marketing metrics

**Live page:** https://asmaaziz.github.io/airbnb-marketing-metrics/

A single-page analysis of marketing efficiency metrics Airbnb doesn't report, derived from its public annual filings (FY2019–FY2025).

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

## Data sources
Every number comes from Airbnb's own filings. Each report covers the year it's named for plus earlier years for comparison.

| Years | Figures | Source | Where to look in it |
|---|---|---|---|
| 2019, 2020 | Revenue, S&M | [Form 10-K, FY2020](https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm) | "Revenue" and "Sales and Marketing" tables in Item 7 |
| 2019, 2020, 2021 | Nights, GBV | [Form 10-K, FY2021](https://www.sec.gov/Archives/edgar/data/1559720/000155972022000006/abnb-20211231.htm) | "Key Business Metrics" in Item 7 |
| 2021, 2022 | Revenue, Nights, GBV, S&M | [Form 10-K, FY2022](https://www.sec.gov/Archives/edgar/data/1559720/000155972023000003/abnb-20221231.htm) | "Key Business Metrics" and "Sales and Marketing" in Item 7 |
| 2022, 2023 | S&M (cross-check) | [Form 10-K, FY2023](https://www.sec.gov/Archives/edgar/data/1559720/000155972024000006/abnb-20231231.htm) | "Sales and Marketing" in Item 7 |
| 2023, 2024 | Revenue, Nights, GBV, S&M | [Form 10-K, FY2024](https://www.sec.gov/Archives/edgar/data/1559720/000155972025000010/abnb-20241231.htm) | "Key Business Metrics" and "Sales and Marketing" in Item 7 |
| 2025 | Revenue, Nights, GBV, S&M | [Q4 2025 shareholder letter](https://s26.q4cdn.com/656283129/files/doc_financials/2025/q4/Airbnb_Q4-2025-Shareholder-Letter.pdf) | Financial tables near the end |

All Airbnb annual reports: [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001559720&type=10-K). Shareholder letters: [investors.airbnb.com](https://investors.airbnb.com).

## Caveats
- 2020 S&M includes about $435M of one-time stock-based compensation from the IPO, so 2020 marketing cost looks inflated.
- Airbnb doesn't publicly split brand vs. performance spend by channel.
- Year-over-year deltas attribute all new bookings to marketing, so the marginal metric is an upper bound, not a true CAC.
- Nights include experience seats (renamed "Nights and Seats Booked" in 2025).

---
By [Asma Aziz](https://github.com/asmaaziz). Other work: [flight-delays](https://github.com/asmaaziz/flight-delays), [sentiment-analysis](https://github.com/asmaaziz/sentiment-analysis), [text-mining](https://github.com/asmaaziz/text-mining).
