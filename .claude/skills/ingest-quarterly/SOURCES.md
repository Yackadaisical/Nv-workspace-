# SOURCES.md — what to read, what to skip

The purpose of this file is **token discipline**. SEC filings and IR docs
contain a lot of boilerplate. Read this before you open a filing.

---

## NVIDIA IR site (investor.nvidia.com)

Per quarter, NVIDIA posts:

| Document | Read? | Why |
| --- | --- | --- |
| Earnings press release (8-K) | **Full** | Headline P&L, segment revenue, next-quarter outlook. Short and dense. |
| CFO Commentary (Colette Kress) | **Full** | Best 4-page summary of the quarter: segment color, one-timers, buyback/dividend pacing, qualitative forward color. |
| Earnings call transcript | **Prepared remarks + Q&A** | Source of qualitative promises & guidance nuance. Skip moderator intros and safe-harbor preambles. |
| Investor presentation slides | Skim, if posted | Usually restates press release; occasionally has new mgmt framing for TAM/targets. |
| Webcast / audio | Skip | Transcript covers it. |

## SEC EDGAR filings

| Form | Read? | Notes |
| --- | --- | --- |
| **10-K** | **Yes, whitelisted sections only** (see below) — annually |
| **10-Q** | **Yes, whitelisted sections only** — Q1/Q2/Q3 |
| **8-K** | Case-by-case | Earnings releases are 8-Ks (already read as press release above). Other 8-Ks: executive changes, material agreements, dividend/buyback announcements — scan headline only. |
| DEF 14A (proxy) | Once/year | Exec comp snapshot only. Skip the rest. |
| Form 3 / 4 / 5 | Quarterly aggregate only | Insider transactions. Track aggregate $ sold by insiders per quarter. Do not read individual filings. |
| S-8 | **Skip** | Employee stock plan registration. |
| SD | **Skip** | Conflict minerals. |
| 144 | **Skip** | Notice of proposed sale. |
| S-3 / 424B* | Only on capital raise | Prospectus — rare for NVDA; read only if they actually issue. |
| NT 10-Q / NT 10-K | **Skip** | Notification of late filing — NVDA isn't late. |
| SC 13G / 13D | Skip routine | Only read if a new >5% holder files for the first time. |

## 10-K / 10-Q sections to READ

In order of importance:

1. **Item 2 — Management's Discussion and Analysis (MD&A)**, specifically the
   **segment revenue discussion** and any commentary on one-timers, mix, or
   guidance variance.
2. **Segment Reporting note** (usually Note 17-19 range) — Data Center /
   Gaming / Pro Viz / Auto / OEM breakdown with YoY comparisons. For Data
   Center, look for any Compute vs Networking split.
3. **Revenue Disaggregation note** — geographic mix (US / China / Taiwan /
   Singapore / Other) and segment mix.
4. **Commitments and Contingencies note → Purchase Commitments** — the $
   amount of supply prepayments to TSMC, HBM vendors, and other suppliers.
   This is a leading indicator of near-term supply capacity. Track total,
   plus any >$1B counterparty call-outs.
5. **Concentration of Credit Risk / Significant Customers** — discloses
   count of customers representing >10% of revenue (typically unnamed). The
   count itself is the signal — if 2-4 customers = 30-50% of revenue, that's
   concentration risk.
6. **Subsequent Events** — rarely interesting but cheap to scan.

## 10-K / 10-Q sections to SKIP

Do not read these. Do not quote from them. Do not summarize them.

- **Item 1A — Risk Factors** (10-K) / **Part II Item 1A** (10-Q). Identical
  quarter-to-quarter; flag only if a new risk factor is added (rare).
- **Legal Proceedings** — standard litigation language. Flag only if NVDA
  discloses a material adverse outcome.
- **Controls and Procedures** — always "we have effective internal controls".
- **Stock-based compensation footnote mechanics** — use the aggregate $ of
  SBC from the cash flow statement; do not read the fair-value Black-Scholes
  table.
- **Basis of Presentation / Recent Accounting Pronouncements** — boilerplate.
- **Forward-Looking Statements Safe Harbor** — boilerplate.
- **Properties** (Item 2 of 10-K) — boilerplate.

## Earnings call transcript

Read:
- **Prepared remarks** — Jensen + Colette. Pull the 3-5 quotes that
  represent forward-looking promises or quantitative targets.
- **Q&A** — skip the first exchange of pleasantries. Focus on analyst
  questions about: supply, demand cadence, ASPs, competition, China/export
  controls, next-gen ramp timing. Extract any *quantitative* answer.

Skip:
- Operator intro / safe-harbor read.
- Closing remarks thanking everyone.

## Where to find things

- NVIDIA IR: https://investor.nvidia.com/financial-info/financial-reports/default.aspx
- NVIDIA News (press releases): https://nvidianews.nvidia.com/news
- SEC EDGAR (NVIDIA, CIK 0001045810): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810

## Fiscal calendar reference

| FY | Q1 ends | Q2 ends | Q3 ends | Q4 ends (= FY end) |
| --- | --- | --- | --- | --- |
| FY25 | ~Apr 28 2024 | ~Jul 28 2024 | ~Oct 27 2024 | Jan 26 2025 |
| FY26 | Apr 27 2025 | Jul 27 2025 | Oct 26 2025 | Jan 25 2026 |
| FY27 | ~Apr 26 2026 | ~Jul 26 2026 | ~Oct 25 2026 | ~Jan 31 2027 |

10-Q typically filed ~4 weeks after quarter-end. 10-K typically filed ~4-5
weeks after FY-end.
