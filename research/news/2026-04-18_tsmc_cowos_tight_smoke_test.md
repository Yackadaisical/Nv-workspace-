---
source_type: news
firm_or_author: smoke-test (fabricated)
date: 2026-04-18
title: TSMC CoWoS capacity tighter than expected for CY2026
tickers: [NVDA, TSM, AMD]
topics: [supply, packaging]
link: (smoke-test — not a real source)
impact: High
---

## Summary
Smoke-test entry to validate the ingestion pipeline. In a scenario where
TSMC's CoWoS advanced-packaging capacity for CY2026 is revised down from
~600k wafer-equivalents to ~520k due to substrate constraints, this would
bind NVDA's unit supply ceiling. This is a fabricated input used only to
exercise the ingest-research → update-projection → changelog flow end to
end; do NOT treat the numbers as real.

## Key data points
- CoWoS wafer-equivalent capacity CY2026: 520k (prior 600k) — fabricated
- Tightness attributed to substrate (ABF) supply — fabricated
- Impacts NVDA, AMD MI-series, and custom silicon that share CoWoS-L
  packaging

## View impact (NVDA model)
- `supply.cowos_wafers.fy27`: prior 600000 → new 520000 (Base)
- Expect downstream effect on DC revenue ceiling for FY27, flowing through
  `nv.bu.total_rev.*` via supply cap logic in Dashboard.
- No direct ASP or GM impact unless HBM allocation also shifts.

## Open questions
- Does the shortfall clear in CY2027 or persist? Need TSMC fiscal color.
- Does NVDA get preferential allocation vs AMD / custom silicon?
