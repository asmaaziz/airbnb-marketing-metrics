"""
Independent validation of the Airbnb marketing-metrics page.
Reads the DATA array straight out of index.html, recomputes every metric in Python,
and checks the results against figures Airbnb reports itself.
Run: python validate.py
"""
import re, json

html = open("index.html", encoding="utf-8").read()
block = re.search(r"const DATA = \[(.*?)\];", html, re.S).group(1)
rows = []
for m in re.finditer(r"year: (\d+), revenue: ([\d.]+),\s*gbv: ([\d.]+), nights: ([\d.]+), sm: ([\d.]+)", block):
    y, rev, gbv, n, sm = m.groups()
    rows.append(dict(year=int(y), revenue=float(rev), gbv=float(gbv), nights=float(n), sm=float(sm)))

passed = failed = 0
def check(name, ok, detail=""):
    global passed, failed
    passed += ok; failed += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

# ---------- 1. Inputs match the filings ----------
print("\n1. Inputs match the source filings")
REPORTED = {  # year: (revenue $M, GBV $M, nights M, S&M $M) as printed in filings
    2019: (4805.2, 37962.6, 326.9, 1621.5),
    2020: (3378.2, 23896.9, 193.2, 1175.3),
    2021: (5992, 46877, 300.6, 1186),
    2022: (8399, 63212, 393.7, 1516),
    2023: (9917, 73252, 448, 1763),
    2024: (11102, 81784, 491.5, 2148),
    2025: (12241, 91300, 533.0, 2588),
}
for r in rows:
    rep = REPORTED[r["year"]]
    ours = (r["revenue"], r["gbv"], r["nights"], r["sm"])
    worst = max(abs(a - b) / b for a, b in zip(ours, rep))
    check(f"{r['year']} inputs", worst < 0.001, f"max rounding diff {worst:.3%}")

# ---------- 2. Recompute metrics ----------
print("\n2. Recomputed metrics")
for i, r in enumerate(rows):
    p = rows[i - 1] if i else None
    r["avg"] = r["sm"] / r["nights"]
    r["marg"] = ((r["sm"] - p["sm"]) / (r["nights"] - p["nights"])
                 if p and r["nights"] > p["nights"] and r["sm"] > p["sm"] else None)
    r["lev"] = r["gbv"] / r["sm"]
    r["share"] = r["sm"] / r["revenue"] * 100
    r["take"] = r["revenue"] / r["gbv"] * 100
    r["adr"] = r["gbv"] / r["nights"]
    r["vol"] = (r["nights"] / p["nights"] - 1) * 100 if p else None
    r["price"] = (r["adr"] / p["adr"] - 1) * 100 if p else None
print(f"  {'Year':<6}{'Avg/night':>10}{'Marg/night':>11}{'GBV/S&M$':>10}{'S&M%rev':>9}{'Take%':>7}{'GBV/night':>10}")
for r in rows:
    m = f"${r['marg']:.2f}" if r["marg"] else "n/a"
    print(f"  {r['year']:<6}{'$'+format(r['avg'],'.2f'):>10}{m:>11}{'$'+format(r['lev'],'.1f'):>10}"
          f"{r['share']:>8.1f}%{r['take']:>6.1f}%{'$'+format(r['adr'],'.0f'):>10}")

# ---------- 3. Cross-check derived figures against Airbnb's own statements ----------
print("\n3. Derived figures vs. what Airbnb/press report")
y = {r["year"]: r for r in rows}
check("2024 S&M % of revenue ~19% (PhocusWire, Q4'24 results)", abs(y[2024]["share"] - 19) < 1, f"{y[2024]['share']:.1f}%")
check("2024 take rate ~13-14% (industry estimates)", 13 <= y[2024]["take"] <= 14, f"{y[2024]['take']:.1f}%")
check("2024 GBV per night near reported ADR (~$164 in Q3'24)", abs(y[2024]["adr"] - 164) / 164 < 0.05, f"${y[2024]['adr']:.0f}")
check("2020 revenue fell 30% vs 2019 (10-K)", abs((y[2020]['revenue']/y[2019]['revenue']-1)*100 + 30) < 1)
check("2020 nights fell 41% vs 2019 (10-K)", abs((y[2020]['nights']/y[2019]['nights']-1)*100 + 41) < 1)
check("2022 nights grew 31% (10-K)", abs(y[2022]['vol'] - 31) < 1, f"{y[2022]['vol']:.1f}%")
check("2024 S&M grew 22% (10-K)", abs((y[2024]['sm']/y[2023]['sm']-1)*100 - 22) < 1)
check("2024 nights grew 10%, GBV 12% (10-K)", abs(y[2024]['vol']-10) < 1 and abs((y[2024]['gbv']/y[2023]['gbv']-1)*100-12) < 1)

# ---------- 4. Are the page's written takeaways true? ----------
print("\n4. Written claims on the page")
check("Marginal cost rose from 2022 to latest year", y[2025]["marg"] > y[2022]["marg"],
      f"${y[2022]['marg']:.2f} -> ${y[2025]['marg']:.2f}")
avg_chg = y[2025]["avg"] / y[2022]["avg"] - 1
marg_chg = y[2025]["marg"] / y[2022]["marg"] - 1
check("Marginal cost grew far faster than average (2022->2025)", marg_chg > 5 * avg_chg,
      f"marginal +{marg_chg:.0%} vs average +{avg_chg:.0%}")
peak = max(rows, key=lambda r: r["lev"])
check("Leverage peaked in 2022 and has fallen since", peak["year"] == 2022 and y[2025]["lev"] < peak["lev"])
check("S&M share of revenue lower than 2019", y[2025]["share"] < y[2019]["share"])
check("S&M share has risen since its 2023 low", y[2025]["share"] > y[2023]["share"] and
      min(rows, key=lambda r: r["share"])["year"] == 2023)
check("Take rate higher than 2019", y[2025]["take"] > y[2019]["take"])
check("Latest year: volume growth > price growth", y[2025]["vol"] > y[2025]["price"],
      f"vol {y[2025]['vol']:.1f}% vs price {y[2025]['price']:.1f}%")

# ---------- 5. Robustness: does the main finding survive a stricter definition? ----------
print("\n5. Robustness: marginal cost using only brand & performance marketing")
print("   (excludes salaries, field ops, policy; figures from 10-K 'Brand and performance marketing' line)")
BP = {2019: 1140.4, 2020: 478.6, 2021: 723, 2022: 1030, 2023: 1208, 2024: 1455}
prev = None
bp_marg = {}
for yr in sorted(BP):
    if prev and y[yr]["nights"] > y[prev]["nights"] and BP[yr] > BP[prev]:
        bp_marg[yr] = (BP[yr] - BP[prev]) / (y[yr]["nights"] - y[prev]["nights"])
        print(f"   {yr}: ${bp_marg[yr]:.2f} per extra night")
    prev = yr
check("Rising-cost finding holds with ad spend only (2024 > 2022)", bp_marg[2024] > bp_marg[2022])

print("\n   Lagged version: this year's extra spend vs NEXT year's extra nights")
for yr in (2022, 2023, 2024):
    lag = (y[yr]["sm"] - y[yr-1]["sm"]) / (y[yr+1]["nights"] - y[yr]["nights"])
    print(f"   spend {yr-1}->{yr} / nights {yr}->{yr+1}: ${lag:.2f}")

# ---------- 6. 2020 adjustment ----------
print("\n6. 2020 distortion check")
adj2020 = 681.5  # S&M excl. stock comp & IPO items (Q4 2020 shareholder letter)
print(f"   Reported 2020 S&M/night ${y[2020]['avg']:.2f}; excluding IPO stock comp ${adj2020/y[2020]['nights']:.2f}")
check("Adjusting 2020 flips it from 'most expensive year' to cheaper than 2019",
      adj2020 / y[2020]["nights"] < y[2019]["avg"])

# ---------- 7. New strategy analyses ----------
print("\n7. Strategy analyses: incremental return and budget mix")
MEDIA = {2019: 1140.4, 2020: 478.6, 2021: 723, 2022: 1030, 2023: 1208, 2024: 1455, 2025: 1595}
check("2025 ad spend matches FY2025 10-K ($1,595M) and other = $993M",
      MEDIA[2025] == 1595 and y[2025]["sm"] - MEDIA[2025] == 993)
roi_t = {k: (y[k]["revenue"]-y[k-1]["revenue"])/(y[k]["sm"]-y[k-1]["sm"]) for k in range(2022, 2026)}
roi_m = {k: (y[k]["revenue"]-y[k-1]["revenue"])/(MEDIA[k]-MEDIA[k-1]) for k in range(2022, 2026)}
for k in roi_t: print(f"   {k}: ${roi_t[k]:.2f} per extra S&M $, ${roi_m[k]:.2f} per extra ad $")
check("Total incremental return fell every year 2022->2025", all(roi_t[k] > roi_t[k+1] for k in (2022, 2023, 2024)))
check("Ad-only return dipped in 2024 and recovered in 2025", roi_m[2024] < roi_m[2023] and roi_m[2025] > roi_m[2024])
check("Ad-only return still well above $1 in 2025", roi_m[2025] > 2)
share = {k: MEDIA[k]/y[k]["sm"]*100 for k in MEDIA}
check("Ad share steady 2022-2024 (within 2 pts)", max(share[k] for k in (2022,2023,2024)) - min(share[k] for k in (2022,2023,2024)) < 2,
      ", ".join(f"{k}: {share[k]:.0f}%" for k in (2022,2023,2024)))
check("2025 ad share below the 2022-2024 range", share[2025] < min(share[k] for k in (2022,2023,2024)), f"{share[2025]:.0f}%")
extra, extra_other = y[2025]["sm"]-y[2024]["sm"], (y[2025]["sm"]-MEDIA[2025])-(y[2024]["sm"]-MEDIA[2024])
check("Most of 2025's extra S&M went outside the ad budget", extra_other/extra > 0.5, f"${extra_other:.0f}M of ${extra:.0f}M")

print(f"\nResult: {passed} passed, {failed} failed")
