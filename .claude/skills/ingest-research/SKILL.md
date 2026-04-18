---
name: ingest-research
description: Ingest a broker report, meeting note, news item, or transcript (via paste, file drop, or URL) — strip boilerplate, write a canonical markdown file, and propose assumption deltas for user review.
---

# ingest-research

Trigger: user pastes research text, drops a file in `research/inbox/`, or
shares a URL. Also triggered when sweeping `research/inbox/` during a
quarterly refresh.

## Always consult `FILTERS.md` first

Open `.claude/skills/ingest-research/FILTERS.md` and apply the strip list
BEFORE you start reasoning about the content. Do not quote boilerplate
sections back in conversation. Research PDFs often have 30-50% disclosure
pages — ignore them.

## Steps

1. **Determine source type** from user cue or content:
   `broker | meeting-note | transcript | news | presentation | filing`.

2. **Ingest source content:**
   - **Paste:** save raw text to
     `research/inbox/<YYYY-MM-DD>_<slug>.txt` first.
   - **File drop (`research/inbox/`):** read the file. For PDFs, use `pypdf`
     to extract text.
   - **URL:** use WebFetch with a prompt scoped to the relevant content
     (e.g. "extract the NVDA-specific thesis, numbers, and upstream/
     downstream reads; skip disclaimers and rating matrices").

3. **Apply `FILTERS.md`.** Strip disclaimers, rating matrices, company
   descriptions, TOCs, exhibits. If the post-strip content is still >300
   lines, summarize to ≤300 lines — quality over completeness.

4. **Write the canonical markdown** to the correct subfolder:
   - `research/broker/<firm>_<YYYY-MM-DD>_<slug>.md`
   - `research/meeting-notes/<YYYY-MM-DD>_<slug>.md`
   - `research/news/<YYYY-MM-DD>_<source>_<slug>.md`
   - Same for `transcript` / `presentation` if not already under
     `filings/`.

   Use the front-matter schema below.

5. **Append a row to `research/INDEX.md`** with date, type, firm, title,
   tickers, topics, impact (Low/Med/High), and the file path.

6. **Remove from inbox** if the input came from `research/inbox/` (move or
   delete after the canonical md is written).

7. **Propose — do not auto-apply — assumption deltas** to the user.
   Format:

   ```
   ## Proposed assumption deltas from <file>

   1. `<base.yaml key or named range>`:
      current = X → proposed = Y
      rationale: <1 sentence>
      confidence: Low | Medium | High

   2. ...

   Approve with: "apply" / "apply 1,3" / "skip" / "apply with changes: ..."
   ```

   Wait for user approval. On approval, call `update-projection` with the
   approved deltas.

## Canonical markdown schema

```markdown
---
source_type: broker | meeting-note | transcript | news | presentation | filing
firm_or_author: <e.g. Morgan Stanley, Reuters, internal>
date: 2026-04-18
title: <short title>
tickers: [NVDA, TSM, MSFT]
topics: [supply, demand, pricing, geo, competition, margins, capex]
link: <url or local path to raw source>
impact: Low | Medium | High
---

## Summary
<≤150 words, plain prose>

## Key data points
- <metric>: <value> — <citation: page/section/speaker>
- ...

## View impact (NVDA model)
- <specific assumption key or named range to change> — <direction & magnitude>
- ...

## Open questions
- <what this doesn't resolve>
```

## Impact tagging

- **High** — would move Base FY revenue >2% or GM >50 bps, or is a binary
  supply/demand datapoint (TSMC CoWoS re-allocation, hyperscaler order
  cancellation, major export control change).
- **Medium** — moves assumptions by <2% rev / <50 bps GM individually, but
  could stack with other items.
- **Low** — corroborates existing view; color only.

## Common content strips (reminders; full list in FILTERS.md)

- Regulatory disclosures pages ("This report is distributed by...", "Analyst
  certification under Regulation AC", "Important Disclosures")
- Ratings/PT matrix for the firm's whole coverage universe
- Firm-wide economic outlook sections in a single-stock note
- TOCs, list of exhibits, "About <firm>" pages
- Identical boilerplate from prior reports (only the new analytical content
  matters)

## Anti-patterns

- **Don't** paste the disclaimer back. Don't even summarize it.
- **Don't** apply assumption changes without user approval.
- **Don't** create a canonical file without an `INDEX.md` row.
- **Don't** read the full PDF if you can find the summary / investment
  thesis section and derive the whole view from it.
