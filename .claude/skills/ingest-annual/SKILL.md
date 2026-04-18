---
name: ingest-annual
description: Ingest a newly filed NVDA 10-K — populate annual financials YAML, cross-check against the sum of quarterly YAMLs, and flag any reclassifications.
---

# ingest-annual

Trigger: user says "NVDA filed FY<YY> 10-K" or shares the 10-K document.

## Always consult `../ingest-quarterly/SOURCES.md`

The 10-K is large (~150 pages). Read only the whitelisted sections. The
whitelist for 10-K is the same as 10-Q, plus:
- **Item 1 — Business** (skim once per year for strategy framing; skip if
  unchanged vs prior year)
- **Exec comp table in DEF 14A** (separate filing, already covered in
  `SOURCES.md` — update the exec-comp reference once/year)

Do not read: Risk Factors, Legal Proceedings, Properties, Controls,
Accounting Policies, SBC mechanics, Safe Harbor.

## Steps

1. **Archive the 10-K** under `filings/10-K/FY<YY>_10K.pdf|.txt`.

2. **Ingest Q4 quarterly** first using `ingest-quarterly` if not already
   done (Q4 data is in the 10-K, not a standalone 10-Q).

3. **Populate `data/financials/annual/FY<YY>.yaml`** using the schema below.
   For each line item, source from the 10-K's consolidated statements —
   these are the standalone audited numbers.

4. **Cross-check against sum of quarters.** Load the four
   `data/financials/quarterly/FY<YY>Q1..Q4.yaml`, sum each line item, and
   compare to the annual YAML. Any discrepancy > $50M or > 1% on a line
   item indicates a reclassification or rounding — document it under
   `reclassifications:` with the specific line item and delta.

5. **Regenerate the workbook:**
   ```bash
   python scripts/build_financials_xlsx.py
   ```

6. **Update `data/assumptions/base.yaml`** if the 10-K discloses new
   long-term framing (e.g. data-center TAM update, capital return policy
   change, segment reorganization). Any such change triggers a
   `views/changelog.md` entry via `update-projection`.

7. **Output a one-paragraph summary:** FY revenue/GM/EPS, YoY growth, any
   reclassifications, any new 10-K disclosures that shifted the view.

## Annual YAML schema

```yaml
period: FY26
period_end: 2026-01-25
filed_on: 2026-02-25
source_urls:
  ten_k: https://www.sec.gov/Archives/edgar/data/1045810/...

# All $ in millions
income_statement:
  revenue_total:          { value: null, source: ten_k_income_statement }
  revenue_by_segment:
    data_center:          { value: null, source: ten_k_segment_note }
    gaming:               { value: null, source: ten_k_segment_note }
    pro_viz:              { value: null, source: ten_k_segment_note }
    auto:                 { value: null, source: ten_k_segment_note }
    oem:                  { value: null, source: ten_k_segment_note }
  gross_profit_gaap:        { value: null, source: "" }
  gross_margin_gaap_pct:    { value: null, source: "" }
  gross_margin_nongaap_pct: { value: null, source: "" }
  opex_rd:                  { value: null, source: "" }
  opex_sga:                 { value: null, source: "" }
  operating_income_gaap:    { value: null, source: "" }
  net_income_gaap:          { value: null, source: "" }
  eps_diluted_gaap:         { value: null, source: "" }
  eps_diluted_nongaap:      { value: null, source: "" }

balance_sheet:
  cash_and_marketable_securities: { value: null, source: "" }
  total_debt:                     { value: null, source: "" }
  inventory:                      { value: null, source: "" }
  purchase_commitments:           { value: null, source: ten_k_purchase_commitments_note }

cash_flow:
  operating_cash_flow: { value: null, source: "" }
  capex:               { value: null, source: "" }
  buybacks:            { value: null, source: "" }
  dividends:           { value: null, source: "" }

cross_check:
  sum_of_quarters_matches: true
  reclassifications: []          # list of {line_item, annual, sum_of_q, delta, note}

long_term_framing:
  tam_statement: "<verbatim from 10-K, if any updated TAM framing>"
  capital_return_policy: "<verbatim>"
  segment_changes: "<any segment redefinition>"
```
