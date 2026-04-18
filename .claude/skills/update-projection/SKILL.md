---
name: update-projection
description: Apply an approved set of assumption changes — edit base.yaml, push values into named input cells of NVDA_Projections.xlsx, append to views/changelog.md, and rewrite views/thesis.md if thresholds are breached.
---

# update-projection

Trigger: user approves one or more assumption deltas proposed by
`ingest-research`, `ingest-quarterly`, or an ad-hoc user request.

## Invariants (from CLAUDE.md)

- Write ONLY into named input cells on the allowed sheets:
  `Assumptions_BottomUp`, `Assumptions_TopDown`, `Supply_Model`,
  `Margins`, `Opex_Below`. Never touch formula cells or layout.
- Every change must produce a `views/changelog.md` entry in the same
  turn. No silent changes.
- If cumulative change since last thesis rewrite exceeds FY rev >2%,
  GM >50 bps, or flips qualitative stance → rewrite `views/thesis.md`.

## Steps

1. **Load the current state.** Read `data/assumptions/base.yaml`. Read the
   last 5 entries of `views/changelog.md` to understand recent drift.

2. **Edit `data/assumptions/base.yaml`** with the approved deltas. Keep
   YAML keys stable — they map 1:1 to named ranges in the projection
   workbook. See the key convention below.

3. **Run the projection writer:**
   ```bash
   python scripts/write_projection_inputs.py
   ```
   This opens `workbooks/NVDA_Projections.xlsx`, writes each value in
   `base.yaml` to its corresponding named cell, saves, and exits. The
   script refuses to write anywhere other than the registered named
   ranges — this is the guard against corrupting the model.

4. **Read the recalculated output** from the Dashboard sheet (FY revenue,
   GM%, EPS for each forward year). These are the numbers to cite in the
   changelog entry.

5. **Append to `views/changelog.md`** using the template from that file.
   One entry per logical change (usually 1 per `update-projection` call
   is fine, even if multiple keys were edited, as long as they share a
   trigger).

6. **Check thesis threshold.** Compare the new Dashboard numbers to the
   numbers currently recorded in `views/thesis.md`. If any of the
   following is true since the last thesis rewrite:
   - |ΔFY revenue| / FY revenue > 2% for any projected FY
   - |ΔFY GM%| > 50 bps for any projected FY
   - Qualitative stance flip (bull ↔ neutral ↔ bear)

   then rewrite `views/thesis.md` in full, using the current Dashboard
   numbers and the latest thinking from the changelog. Note the rewrite
   date at the top.

7. **Output summary** to the user: which keys changed, the Dashboard
   delta, whether thesis was rewritten, and confidence level.

## `base.yaml` key convention

Flat, dotted keys that mirror named ranges:

```yaml
# Bottom-up demand (units × ASP by customer × SKU × period)
bu:
  msft:
    gb200:
      units:
        fy27q1: 120000
        fy27q2: 130000
      asp:
        fy27q1: 38000
        fy27q2: 38000

# Top-down
td:
  accelerator_tam:
    fy27: 450000       # $m
  nvda_share:
    fy27: 0.82

# Supply
supply:
  cowos_wafers:
    fy27: 600000       # wafer equivalents
  hbm_allocation_gb:
    fy27: 90000000     # GB
  packaging_yield_pct:
    fy27: 0.92

# Margins
margin:
  hbm_cost_per_gb:
    fy27q1: 20
  yield_uplift_pct:
    fy27q1: 0.02

# Opex and below-the-line
opex:
  rd_growth_yoy_pct:
    fy27: 0.25
  sga_growth_yoy_pct:
    fy27: 0.15
  tax_rate_pct:
    fy27: 0.165
  buyback_usd:
    fy27: 50000        # $m
```

The named range for `bu.msft.gb200.units.fy27q1` is `nv.bu.msft.gb200.units.fy27q1`.
`write_projection_inputs.py` flattens the YAML, prefixes keys with `nv.`,
and looks up each name in the workbook. Missing names are warnings, not
errors.

## Changelog entry (strict format)

```markdown
## YYYY-MM-DD — <short title>
- **Trigger:** <research file path or filing>
- **Prior view:** <specific metric and value>
- **New view:** <specific metric and value>
- **Cells / keys touched:** `bu.msft.gb200.units.fy27q1`, `supply.cowos_wafers.fy27`
- **Thesis delta:** FY27 rev <X>% (was $<Y>B, now $<Z>B); GM% <+/-> <bps>; EPS <+/-><$>
- **Confidence:** Low | Medium | High — <one-sentence rationale>
```

## Thesis rewrite format

Overwrite `views/thesis.md` in full with the structure already present —
don't drift from the template. Update the `_Last updated:_` line, fill in
all revenue / margin / EPS cells from the Dashboard, and refresh the Key
drivers / Key risks bullets based on the latest changelog entries.
