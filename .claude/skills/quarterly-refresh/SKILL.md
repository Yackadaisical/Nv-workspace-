---
name: quarterly-refresh
description: Orchestrate an end-of-quarter refresh — ingest the new quarter (and 10-K if FY end), sweep research/inbox/, recompute projections, rewrite thesis, emit a refresh summary.
---

# quarterly-refresh

Trigger: user says "refresh NVDA" or "new quarter is out, do the full
update". Use this as the master workflow once per quarter; for mid-quarter
events use the individual skills directly.

## Steps

1. **ingest-quarterly** for the newly reported fiscal quarter.
   - Populates `data/financials/quarterly/FY<YY>Q<q>.yaml` and
     `data/guidance/FY<YY>Q<q>.yaml`.
   - Scores the prior quarter's guidance.
   - Regenerates `NVDA_Financials.xlsx` and `NVDA_Guidance_Tracker.xlsx`.

2. **ingest-annual** if the reported quarter was Q4 (10-K is filed shortly
   after).
   - Populates `data/financials/annual/FY<YY>.yaml`.
   - Cross-checks vs sum of quarterly YAMLs.

3. **Sweep `research/inbox/`.** For each file:
   - Run `ingest-research`.
   - Present proposed deltas to the user in a batch (all files' proposals
     together, numbered, so the user can approve/reject each).

4. **Apply approved deltas** via `update-projection`, producing
   changelog entries.

5. **Rewrite `views/thesis.md`** if any of the per-entry threshold checks
   or the cumulative drift since last rewrite triggers it.

6. **Update `views/open_questions.md`** — remove answered questions,
   add new ones surfaced during the refresh.

7. **Emit refresh summary** to the user:

   ```
   # NVDA Refresh — FY<YY>Q<q>

   ## Quarter in one line
   <revenue, YoY, segment mix headline, vs guide>

   ## Guidance scoring
   - Prior quarter <metric>: guide X, actual Y → <Delivered | Missed by Z%>
   - Management promises: <n Delivered> / <n Partial> / <n Missed> / <n Pending>

   ## New guidance
   <next quarter outlook summary>

   ## Research processed
   - <file>: <impact> — <one-line>
   - ...

   ## Forecast changes
   - <N changelog entries appended>
   - FY<YY>E revenue: $<X>B (was $<Y>B) / <delta>%
   - FY<YY+1>E revenue: $<X>B (was $<Y>B) / <delta>%

   ## Thesis
   <rewritten | unchanged since YYYY-MM-DD>

   ## Open questions
   <top 3-5 unresolved items>
   ```

## Invariants

- Do not skip the research sweep. Even if `research/inbox/` is empty,
  say so explicitly in the summary.
- Never update the projection model without a changelog entry.
- Never rewrite the thesis without running the threshold check first.
- If a step fails (e.g. a filing can't be parsed), stop and surface the
  error rather than continuing with partial data.
