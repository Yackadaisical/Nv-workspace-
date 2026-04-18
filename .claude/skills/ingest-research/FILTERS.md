# FILTERS.md — what to strip from research docs

Research PDFs (especially broker reports) are 30-50% boilerplate. Strip it
before reasoning. Do not quote stripped content back to the user.

---

## Always strip

### Regulatory / legal
- "Important Disclosures" sections
- "Analyst Certification" (Regulation AC)
- "Distribution of Ratings / Investment Banking Services" matrices
- "Conflicts of Interest" tables
- Country-by-country regulatory footnotes (UK FCA, Hong Kong SFC, Singapore
  MAS, Australia ASIC, etc.)
- "For Institutional Investors Only" / "Not for Retail Distribution"
  stickers
- Copyright and redistribution notices

### Firm boilerplate
- "About <firm>" pages
- Office addresses
- List of global contacts
- Ratings definitions ("Overweight means expected total return of...")
- Sector coverage list

### Structural noise
- Table of contents
- List of exhibits / figures / tables
- Page numbers and running headers
- "Continued on next page" / "See page X" cross-references
- Blank or cover pages

### Not-NVDA-specific in an NVDA note
- Firm-wide macro outlook sections
- Sector overviews that don't mention NVDA by name
- Full universe of ratings / price targets (keep only NVDA row +
  any NVDA-related ticker: TSM, AMD, AVGO, ARM, MRVL, HBM names)

### Repetitive content from prior reports
- If the analyst's boilerplate thesis paragraph is verbatim the same as a
  prior report on file, don't re-ingest it — reference the prior file.

---

## Keep (these are the signal)

- The summary / investment thesis / "our view"
- Any quantitative forecast or estimate (revenue, EPS, margins, TAM, unit
  volumes)
- Channel checks and supply-chain datapoints
- Named sources (e.g. "per TSMC conference", "per Big-Cloud mgmt meeting")
- Price target logic / multiple applied
- Any call-out on hyperscaler capex, AI accelerator TAM share, next-gen
  chip ramp
- Risk section IF it introduces a specific new risk (not generic "macro /
  geopolitical" bullets)

---

## PDF extraction tips

- Use `pypdf` for text. If extraction yields mostly garbage, the PDF is
  image-only — flag to the user that OCR is needed; do not guess.
- Many broker PDFs have a clear 2-column layout — pypdf often produces
  interleaved lines. Re-flow by paragraph if needed; most of the signal is
  in the first 2-4 pages of analytical content anyway.

---

## Meeting notes & internal docs

For meeting notes and internal documents the filter is lighter — the
content is already distilled. Just extract data points + view implications.

## News items

For news articles, strip:
- Advertisement blocks / "related stories" / paywall preambles
- Reporter bio / "follow us on social"
- Unrelated headlines in a wire digest

Keep:
- Headline + lede
- Quoted numbers or named executives
- Any direct implication for NVDA supply, demand, competition, or geo

---

## Target length

Canonical research markdown should be ≤300 lines. If you can't get below
that, you're probably keeping boilerplate or writing too much commentary.
Ten high-signal bullets beats a 500-line quote.
