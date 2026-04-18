# CLAUDE.md — NVIDIA Investment DD Workspace

This file is required reading at the start of every session in this repo.
It defines **what this workspace is**, the **invariants** you must not violate,
and the **standard workflows** for updating it.

---

## Purpose

Track NVDA as a long-running fundamental research project:
- Reported financials for the last 4 fiscal quarters + prior full fiscal year,
  extended each new quarter and each new fiscal year.
- A projection model (bottom-up customer × chip-SKU and top-down TAM/share) that
  forecasts revenue, margin, and EPS forward, with a supply-side ceiling driven
  by TSMC CoWoS / HBM allocation.
- A tracker of management guidance and qualitative promises, scored for delivery.
- A flow for ingesting broker reports, meeting notes, transcripts, and upstream/
  downstream news, turning them into proposed assumption changes.
- An append-only log of every forecast change so you can always reconstruct
  *why* the current view is the current view.

The user works primarily in Excel. Data workbooks are regenerated from YAML;
the projection model is a hand-built formula workbook where Claude only writes
into pre-defined named input cells.

---

## Invariants (do not violate)

1. **Source of truth is YAML, not Excel.** `data/financials/`, `data/guidance/`,
   and `data/assumptions/base.yaml` are authoritative. Workbooks in `workbooks/`
   are build artifacts — regenerate them, do not hand-edit them. The sole
   exception is `NVDA_Projections.xlsx`, which is hand-built; for that workbook
   only write into cells defined in its named ranges (see
   `.claude/skills/update-projection/SKILL.md`).

2. **Every forecast change requires a changelog entry in the same turn.**
   Any write into `NVDA_Projections.xlsx` input cells, or any edit to
   `data/assumptions/base.yaml`, must be accompanied by an append to
   `views/changelog.md` in the format defined in that skill. No silent changes.

3. **Every research item produces a canonical markdown file + an `INDEX.md`
   row.** Paste, file drop, or URL — all three paths end in the same artifact
   under `research/<type>/` with the YAML front-matter defined in the
   `ingest-research` skill.

4. **Cite sources for every number.** Every YAML entry in `data/financials/`
   or `data/guidance/` carries a `source:` field pointing to the filing + the
   specific section / page / line. Every changelog entry links upward to its
   trigger (research file) and downward to the cells/keys it touched.

5. **Lean ingestion — do not waste tokens on boilerplate.** Before reading a
   filing, consult `.claude/skills/ingest-quarterly/SOURCES.md`. Before reading
   a research doc, consult `.claude/skills/ingest-research/FILTERS.md`. Skip
   risk factors, legal-proceedings language, safe-harbor preambles, analyst
   rating matrices, distribution disclaimers, etc. Never quote low-signal
   sections back in conversation.

6. **Scenarios are Bear / Base / Bull.** Base is the working view. Bear and
   Bull are maintained alongside. Don't casually flip Base without a changelog
   entry that crosses the rewrite threshold (see rule 7).

7. **Rewrite `views/thesis.md`** when cumulative changes since last rewrite
   exceed any of: FY revenue >2%, full-company GM >50 bps, or a qualitative
   stance flip (bull/neutral/bear).

8. **Only NVDA in v1.** Folder layout intentionally hardcodes the ticker. Do
   not introduce multi-ticker abstractions prematurely.

---

## Repo map

```
CLAUDE.md                  — this file
README.md                  — human intro
.claude/skills/            — skill instructions (read these before workflows)
  ingest-quarterly/        — new quarter ingest (+ SOURCES.md whitelist)
  ingest-annual/           — new 10-K ingest
  ingest-research/         — broker / note / news / transcript (+ FILTERS.md)
  update-projection/       — apply an approved assumption change
  quarterly-refresh/       — orchestrator for the full quarterly cycle
data/
  financials/annual/       — FY<YY>.yaml (one per fiscal year)
  financials/quarterly/    — FY<YY>Q<q>.yaml (one per fiscal quarter)
  guidance/                — FY<YY>Q<q>.yaml (guidance issued that quarter)
  assumptions/base.yaml    — projection drivers (demand/supply/margins)
workbooks/
  NVDA_Financials.xlsx     — generated (regenerable)
  NVDA_Guidance_Tracker.xlsx — generated (regenerable)
  NVDA_Projections.xlsx    — hand-built; scripts write named input cells only
scripts/
  build_financials_xlsx.py
  build_guidance_xlsx.py
  write_projection_inputs.py
  lib/excel_utils.py
filings/                   — raw docs by type (10-K, 10-Q, press release, etc.)
research/                  — processed research; inbox/ for user file drops
views/
  thesis.md                — current one-page view
  changelog.md             — append-only log of every forecast change
  open_questions.md
requirements.txt
```

---

## Standard workflows

### A new quarter lands (NVDA reports)
Use skill `ingest-quarterly`. Inputs: the press release, CFO commentary,
10-Q, and earnings call transcript. Output: new `FY<YY>Q<q>.yaml` in both
`data/financials/quarterly/` and `data/guidance/`, filings archived under
`filings/`, guidance-tracker workbook regenerated, and a changelog entry if
actuals shift the Base forecast materially.

### A new fiscal year closes (10-K filed)
Use skill `ingest-annual`. Inputs: the 10-K (whitelist sections only).
Output: new `FY<YY>.yaml` in `data/financials/annual/`, cross-checked
against the sum of that year's quarterly YAMLs.

### User shares a broker report / meeting note / news (any channel)
Use skill `ingest-research`. Works with pasted text, a file dropped in
`research/inbox/`, or a URL. Produces a canonical markdown file under
`research/<type>/`, appends to `research/INDEX.md`, and **proposes**
assumption deltas for user review — does not auto-apply.

### User approves an assumption change
Use skill `update-projection`. Edits `data/assumptions/base.yaml`, runs
`scripts/write_projection_inputs.py` to push values into the named input
cells of `NVDA_Projections.xlsx`, appends to `views/changelog.md`, and
rewrites `views/thesis.md` if the cumulative shift breaches invariant 7.

### User asks "what's your current view?"
Read `views/thesis.md` first. Read the most recent ~10 entries of
`views/changelog.md` for context. Answer based on those, not on from-scratch
reasoning. If the user is asking a question the thesis does not answer,
propose updating the thesis.

---

## Excel conventions

- Python-generated workbooks (`NVDA_Financials.xlsx`,
  `NVDA_Guidance_Tracker.xlsx`) are fully regenerated by their build scripts.
  Do not hand-edit — any edit will be lost on the next build.
- `NVDA_Projections.xlsx` is hand-built with live formulas. Script writes
  are limited to cells reachable by named ranges registered on the
  **Assumptions_BottomUp**, **Assumptions_TopDown**, **Supply_Model**,
  **Margins**, and **Opex_Below** sheets. Never write to formula cells.
- Named-range convention: `nv.<area>.<key>.<period>`. Examples:
  `nv.bu.msft.gb200.units.fy27q1`, `nv.supply.cowos_wafers.fy27`,
  `nv.margin.hbm_cost_per_gb.fy27q1`, `nv.opex.rd_growth.fy27`.
- Periods use NVDA fiscal convention: `fy<YY>q<q>` (e.g. `fy27q1`).

---

## Git

- Work on branch `claude/nvidia-investment-workspace-x3gFr`.
- Commit in logical chunks (scaffolding, skills, build scripts, data ingest,
  projection model, etc.). Never push or open a PR without explicit user
  instruction.
