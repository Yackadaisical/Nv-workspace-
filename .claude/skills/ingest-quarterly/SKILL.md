---
name: ingest-quarterly
description: Ingest a newly reported NVDA fiscal quarter — populate quarterly financials and guidance YAMLs, regenerate workbooks, score prior quarter's guidance, and log any resulting forecast change.
---

# ingest-quarterly

Trigger: user says "NVDA reported FY<YY> Q<q>" or shares a press release /
CFO commentary / 10-Q / transcript for a new quarter.

## Always consult `SOURCES.md` first

Before reading any document, open
`.claude/skills/ingest-quarterly/SOURCES.md` for the whitelist of
documents and sections to read, and the list of boilerplate to skip. The
10-Q is large; only the whitelisted sections are worth reading.

## Steps

1. **Identify the period.** NVDA fiscal convention: `FY<YY>Q<q>` where FY<YY>
   ends in late January of calendar year `20<YY>`. FY26 Q1 ended ~Apr 2025.

2. **Archive raw inputs** under:
   - `filings/8-K-press-releases/FY<YY>Q<q>_press_release.pdf|.txt`
   - `filings/cfo-commentary/FY<YY>Q<q>_cfo_commentary.pdf|.txt`
   - `filings/10-Q/FY<YY>Q<q>_10Q.pdf|.txt` (skip if this is Q4 — it's rolled
     into the 10-K; use `ingest-annual` for Q4)
   - `filings/transcripts/FY<YY>Q<q>_earnings_call.txt`

3. **Read ONLY the whitelisted sections** per `SOURCES.md`. The press release
   and CFO commentary are read in full — they are short and dense. For the
   10-Q, extract only MD&A segment discussion, Segment Reporting note,
   Revenue Disaggregation, Purchase Commitments note, Concentration of Credit
   Risk, and Subsequent Events. Do NOT read Risk Factors, Legal Proceedings,
   Controls & Procedures, safe-harbor preambles, or accounting-policy
   boilerplate.

4. **Populate `data/financials/quarterly/FY<YY>Q<q>.yaml`** using the schema
   at the bottom of this file. Cite sources per line item (doc + section).
   Keep the lean scope defined in `CLAUDE.md` — main P&L, cash & debt,
   essential cash flow. No working-capital detail, no SBC bridge.

5. **Populate `data/guidance/FY<YY>Q<q>.yaml`** with the outlook issued in
   this quarter's press release for the NEXT quarter (revenue midpoint ±,
   GAAP/non-GAAP GM%, GAAP/non-GAAP opex, tax rate), plus any qualitative
   promises from prepared remarks (track under `management_promises:`).

6. **Score the PRIOR quarter's guidance** against the actuals we just
   ingested. Update the prior quarter's
   `data/guidance/FY<YY>Q<(q-1)>.yaml` (or Q4 of prior FY) by filling in
   `actuals:` and `variance:` fields. Set `status:` for each qualitative
   promise to Delivered / Partial / Missed / Pending.

7. **Regenerate the workbooks:**
   ```bash
   python scripts/build_financials_xlsx.py
   python scripts/build_guidance_xlsx.py
   ```

8. **Check for forecast impact.** Compare actuals vs Base forecast in
   `data/assumptions/base.yaml`. If variance is material (>2% on FY revenue,
   >50 bps on GM, or explicit mix/supply information), trigger
   `update-projection` to adjust assumptions and append a `views/changelog.md`
   entry. Otherwise note in the summary that the quarter was in-line and no
   forecast change was made.

9. **Output a one-paragraph summary** to the user: headline P&L vs guide,
   segment color, notable disclosures (significant customer concentration
   changes, purchase commitment step-ups, subsequent events), and whether
   the Base forecast was adjusted.

## Financials YAML schema

```yaml
period: FY26Q1          # NVDA fiscal quarter
period_end: 2025-04-27  # actual quarter-end date
reported_on: 2025-05-28 # press release date
source_urls:
  press_release: https://nvidianews.nvidia.com/news/...
  cfo_commentary: https://s201.q4cdn.com/...
  ten_q: https://www.sec.gov/Archives/edgar/data/1045810/...
  transcript: <url or local path>

# All $ in millions unless noted
income_statement:
  revenue_total:
    value: 44062
    source: press_release_table
  revenue_by_segment:
    data_center: { value: 39112, source: press_release_segments }
    gaming:      { value: 3763,  source: press_release_segments }
    pro_viz:     { value: 509,   source: press_release_segments }
    auto:        { value: 567,   source: press_release_segments }
    oem:         { value: 111,   source: press_release_segments }
  gross_profit_gaap:     { value: null, source: "" }
  gross_margin_gaap_pct: { value: null, source: "" }
  gross_margin_nongaap_pct: { value: null, source: "" }
  opex_rd:               { value: null, source: "" }
  opex_sga:              { value: null, source: "" }
  operating_income_gaap: { value: null, source: "" }
  net_income_gaap:       { value: null, source: "" }
  eps_diluted_gaap:      { value: null, source: "" }
  eps_diluted_nongaap:   { value: null, source: "" }

balance_sheet:
  cash_and_marketable_securities: { value: null, source: "" }
  total_debt:                     { value: null, source: "" }
  inventory:                      { value: null, source: "" }
  purchase_commitments:           { value: null, source: "10q_purchase_commitments_note" }

cash_flow:
  operating_cash_flow: { value: null, source: "" }
  capex:               { value: null, source: "" }
  buybacks:            { value: null, source: "" }
  dividends:           { value: null, source: "" }

notes:
  significant_customers: "<text from concentration of credit risk note>"
  subsequent_events: "<text>"
  mgmt_color: "<1-3 sentence summary of segment/mix drivers from CFO commentary>"
```

## Guidance YAML schema

```yaml
period: FY26Q1                # the quarter that ISSUED the guide
issued_on: 2025-05-28
guides_for: FY26Q2

quantitative:
  revenue:
    midpoint: null
    range_pct: 2.0            # e.g. ±2%
    actual: null              # filled when next quarter ingested
    variance_pct: null
  gm_gaap_pct:
    midpoint: null
    range_bps: 50
    actual: null
    variance_bps: null
  gm_nongaap_pct:
    midpoint: null
    range_bps: 50
    actual: null
    variance_bps: null
  opex_gaap:
    midpoint: null
    actual: null
  opex_nongaap:
    midpoint: null
    actual: null
  tax_rate_pct:
    midpoint: null
    actual: null

management_promises:
  - id: FY26Q1-p1
    quote: "<short quote from prepared remarks>"
    speaker: Jensen | Colette
    timeframe: "<e.g. 'through 2H FY26'>"
    status: Pending           # updated later: Delivered | Partial | Missed
    evidence: ""              # path/URL to evidence when updated
```

## Edge cases

- **Q4 quarter:** the standalone Q4 press release and CFO commentary are the
  primary source; there is no 10-Q (Q4 is covered by the 10-K). Use
  `ingest-annual` after the 10-K is filed to book FY-level totals.
- **Restatements:** if a prior-period number is restated, do not edit the old
  YAML. Instead add a `restatement:` block to the new quarter's YAML pointing
  to the restated prior period, and log a changelog entry.
- **Mid-cycle press releases** (e.g. pre-announcement, capital return updates):
  these are 8-Ks; file under `filings/8-K-press-releases/` with an informative
  filename but do NOT create a new quarterly YAML.
