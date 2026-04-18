# NVIDIA Investment DD Workspace

A personal equity-research workspace for NVDA. Historical financials, management
guidance tracking, and a bottom-up/top-down projection model — all driven from
structured YAML source data into Excel workbooks, with an append-only changelog
of every forecast change.

Read `CLAUDE.md` first — it defines the invariants and workflows that Claude
must follow in every session.

## Quick map

| Folder | What lives here |
| --- | --- |
| `data/financials/` | YAML source of truth for reported P&L, BS, CF (quarterly + annual) |
| `data/guidance/` | YAML source of truth for management guidance issued each quarter |
| `data/assumptions/` | Projection drivers (`base.yaml`) — customer × chip units, ASPs, supply caps |
| `workbooks/` | Generated Excel workbooks + hand-built projection model |
| `filings/` | Raw source documents (10-Q, 10-K, press releases, CFO commentary, transcripts) |
| `research/` | Ingested broker reports, meeting notes, news — canonical markdown |
| `views/` | Current thesis + append-only changelog + open questions |
| `scripts/` | Build scripts (`build_financials_xlsx.py`, etc.) |
| `.claude/skills/` | Skill instructions Claude loads for each workflow |

## Workflows

- **New quarter lands** → `ingest-quarterly` skill
- **New 10-K lands** → `ingest-annual` skill
- **Broker report / meeting note / news** → `ingest-research` skill (paste, drop in `research/inbox/`, or share URL)
- **Assumption change approved** → `update-projection` skill
- **Full quarterly refresh** → `quarterly-refresh` skill

## Setup

```bash
pip install -r requirements.txt
```

## Branch

All development on `claude/nvidia-investment-workspace-x3gFr`.
