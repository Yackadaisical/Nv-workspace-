# NVDA Forecast Changelog

Append-only. Every material change to `data/assumptions/base.yaml` or to
`NVDA_Projections.xlsx` input cells must be logged here in the same turn,
using the template below.

---

## Entry template

```
## YYYY-MM-DD — <short title>
- **Trigger:** <path to research file or filing that motivated the change>
- **Prior view:** <what we believed>
- **New view:** <what we now believe>
- **Cells / keys touched:** <named ranges in NVDA_Projections.xlsx and/or keys in base.yaml>
- **Thesis delta:** <quantified impact on FY rev / GM / EPS, and scenario if not Base>
- **Confidence:** Low | Medium | High — <rationale, what would confirm/refute>
```

---

## 2026-04-18 — Smoke-test: TSMC CoWoS FY27 capacity tightened
- **Trigger:** research/news/2026-04-18_tsmc_cowos_tight_smoke_test.md (fabricated, for pipeline verification only)
- **Prior view:** CoWoS wafers FY27 = 600k (hypothetical); supply ceiling loose
- **New view:** CoWoS wafers FY27 = 520k (Base); supply ceiling tightens
- **Cells / keys touched:** `supply.cowos_wafers.fy27` → `Supply_Model!B4` (named `nv.supply.cowos_wafers.fy27`)
- **Thesis delta:** n/a — other drivers still null so Dashboard doesn't yet compute a full revenue impact. Once BU units / ASP and TD TAM/share are seeded, the supply cap will bind automatically via MIN(demand, supply) logic in the supply model.
- **Confidence:** n/a — this is a smoke test, not a real signal. Fabricated numbers.

---

## 2026-04-18 — Initial workspace seed (FY25 + FY26 Q1-Q4 + FY26 annual)
- **Trigger:** initial build of the DD workspace
- **Prior view:** n/a
- **New view:** FY25 revenue $130.5B (DC $115.2B). FY26 revenue $215.9B
  (+65% YoY; DC $197.3B, +71% YoY). FY26 exit GM 75.0% GAAP / 75.2% non-GAAP.
  Q1 FY26 absorbed a $4.5B H20 charge taking GM to 60.5% GAAP; GM recovered
  to 75% by Q4. Mgmt has beaten revenue guide by 4–6% three consecutive
  quarters. Q1 FY27 guide: $78.0B ±2%.
- **Cells / keys touched:** none yet — Base projection assumptions still
  null; user to seed FY27 drivers next.
- **Thesis delta:** n/a (baseline establishment)
- **Confidence:** High — sourced from NVDA press releases + 10-K + CFO
  commentary for each quarter. Some line items (FY26 segment sub-totals
  for Gaming/OEM, balance-sheet detail, cash-flow lines) left null pending
  direct 10-K extraction; flag to fill on next refresh.
