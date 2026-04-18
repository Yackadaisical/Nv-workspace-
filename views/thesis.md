# NVDA — Current View

_Last updated: 2026-04-18 (initial seed from FY25 10-K + FY26 Q1–Q4 + FY26 10-K)_
_Scenario: Base_

## One-line view
NVDA exited FY26 at $215.9B revenue (+65% YoY) with Data Center at $197.3B
(+71%) and GM stepping back up to 75% by Q4 as the H20 China write-down in
Q1 washed through. Q1 FY27 guide of $78.0B ±2% implies continued Blackwell
ramp; the forward view is entirely about whether supply (TSMC CoWoS + HBM)
keeps pace with demand, and whether hyperscaler capex digestion begins in
FY28.

## Revenue path (Base) — historical + placeholder forecast
| | FY25A | FY26A | FY27E | FY28E | FY29E |
| --- | --- | --- | --- | --- | --- |
| Revenue ($B) | 130.5 | 215.9 | _tbd_ | _tbd_ | _tbd_ |
| YoY% | +114% | +65% | _tbd_ | _tbd_ | _tbd_ |
| Data Center ($B) | 115.2 | 197.3 | _tbd_ | _tbd_ | _tbd_ |
| Data Center % of rev | 88% | 91% | _tbd_ | _tbd_ | _tbd_ |

## Margin & EPS (Base)
| | FY25A | FY26A | FY27E | FY28E | FY29E |
| --- | --- | --- | --- | --- | --- |
| GM% (GAAP) | 75.0% | 71.1% | _tbd_ | _tbd_ | _tbd_ |
| GM% (non-GAAP) | _tbd_ | 71.3% | _tbd_ | _tbd_ | _tbd_ |
| Operating income (GAAP, $B) | _tbd_ | 130.4 | _tbd_ | _tbd_ | _tbd_ |
| Net income (GAAP, $B) | 72.9 | 120.1 | _tbd_ | _tbd_ | _tbd_ |

## Quarterly walk through FY26
| | Q1 | Q2 | Q3 | Q4 |
| --- | --- | --- | --- | --- |
| Revenue ($B) | 44.1 | 46.7 | 57.0 | 68.1 |
| Data Center ($B) | 39.1 | 41.1 | 51.2 | 62.3 |
| GM% (GAAP) | 60.5% | 72.4% | 73.4% | 75.0% |
| GM% (non-GAAP) | 61.0% | 72.7% | 73.6% | 75.2% |
| Guide for next Q ($B) | 45.0±2% | 54.0±2% | 65.0±2% | 78.0±2% |
| Actual next Q ($B) | 46.7 (+3.9%) | 57.0 (+5.6%) | 68.1 (+4.8%) | pending |

**Observations.**
- Management has beaten the revenue midpoint by 4–6% for three consecutive
  quarters. That's a consistent pattern of conservative guidance, not a
  fluke. Absent a supply shock, assume Q1 FY27 prints above the $78.0B
  midpoint.
- GM% trough was Q1 FY26 at 60.5% GAAP from the $4.5B H20 write-down;
  recovered to 75% by Q4 FY26 as the headwind rolled off.
- FY26 full-year GM (71.1% GAAP / 71.3% non-GAAP) is below Q4 exit run-rate
  (~75%) — suggests FY27 GM should average ~75% if mix and HBM cost stay
  stable.

## Key drivers (watchlist)
- **Demand:** hyperscaler capex path (MSFT / META / GOOG / AMZN / ORCL);
  Q2 FY26 disclosed 2 unnamed customers ≈ 39% of revenue — concentration
  risk to track each quarter.
- **Supply:** TSMC CoWoS wafer availability and HBM allocation
  (SK Hynix / Micron / Samsung). Blackwell → Rubin transition puts
  pressure on advanced packaging.
- **Mix:** GB200 / GB300 NVL72 rack-scale systems vs board shipments;
  higher ASP but more complex supply chain.
- **Competition:** AMD MI-series ramp; hyperscaler internal silicon (TPU,
  MTIA, Trainium, MAIA).
- **Geo / regulation:** China export control regime — H20 was a $4.5B hit
  in Q1 FY26. Any further restrictions flow through similarly.

## Key risks
- Supply ceiling binding earlier than expected (CoWoS or HBM)
- Hyperscaler capex digestion in late FY27 / FY28
- ASP compression as AMD/custom silicon scales
- Further China export restrictions

## Forecast framework status
The projection workbook (`workbooks/NVDA_Projections.xlsx`) is built with
named input cells for bottom-up (customer × GB200 units × ASP per quarter),
top-down (TAM × share), supply (CoWoS / HBM), margins, and opex. All
assumption cells are currently empty — the Base scenario has not yet been
seeded. First Base seed will be set after the user confirms initial
assumption ranges (suggest framing it around the Q1 FY27 guide of $78B).

## Open items
See `views/open_questions.md`.
