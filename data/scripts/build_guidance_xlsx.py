"""Build workbooks/NVDA_Guidance_Tracker.xlsx from data/guidance/*.yaml.

Emits two sheets:
  - "Guide vs Actual" — quantitative guide issued each quarter, plus the
    actual delivered in the following quarter and variance.
  - "Management Promises" — qualitative commitments, status, evidence.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml
from openpyxl.styles import Font

from lib.excel_utils import (
    DATA_DIR,
    WORKBOOKS_DIR,
    add_sheet,
    autosize,
    discover_yaml,
    ensure_workbooks_dir,
    flatten_periods,
    muted,
    new_workbook,
    style_header,
    write_value,
)

OUTPUT = WORKBOOKS_DIR / "NVDA_Guidance_Tracker.xlsx"


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_cover(wb, n_quarters):
    ws = add_sheet(wb, "Cover")
    ws["A1"] = "NVDA Guidance Tracker — generated workbook"
    ws["A1"].font = Font(name="Calibri", bold=True, size=16, color="111827")
    ws["A3"] = f"Last build: {dt.datetime.now():%Y-%m-%d %H:%M}"
    ws["A4"] = f"Quarters tracked: {n_quarters}"
    ws["A6"] = "Source of truth: data/guidance/*.yaml — do NOT hand-edit this workbook."
    ws.column_dimensions["A"].width = 100


def build_guide_vs_actual(wb, quarters, docs):
    ws = add_sheet(wb, "Guide vs Actual")
    ws["A1"] = "Quarterly guide vs actual"
    ws["A1"].font = Font(name="Calibri", bold=True, size=14, color="111827")

    headers = [
        "Issued in",
        "Guides for",
        "Metric",
        "Midpoint",
        "Range (± %)",
        "Range (± bps)",
        "Actual",
        "Variance %",
        "Variance bps",
    ]
    for c, h in enumerate(headers, start=1):
        ws.cell(row=3, column=c, value=h)
    style_header(ws, 3, len(headers))

    row = 4
    for p, path in quarters:
        doc = docs[path]
        issued = doc.get("period", p.label)
        guides_for = doc.get("guides_for", "")
        quant = doc.get("quantitative", {}) or {}
        for metric_key, metric in quant.items():
            if not isinstance(metric, dict):
                continue
            write_value(ws, row, 1, issued)
            write_value(ws, row, 2, guides_for)
            write_value(ws, row, 3, metric_key)
            write_value(ws, row, 4, metric.get("midpoint"))
            write_value(ws, row, 5, metric.get("range_pct"))
            write_value(ws, row, 6, metric.get("range_bps"))
            write_value(ws, row, 7, metric.get("actual"))
            write_value(ws, row, 8, metric.get("variance_pct"))
            write_value(ws, row, 9, metric.get("variance_bps"))
            row += 1
    autosize(ws, min_width=12, max_width=24)


def build_promises(wb, quarters, docs):
    ws = add_sheet(wb, "Management Promises")
    ws["A1"] = "Qualitative management commitments"
    ws["A1"].font = Font(name="Calibri", bold=True, size=14, color="111827")

    headers = [
        "Issued in",
        "ID",
        "Speaker",
        "Quote",
        "Timeframe",
        "Status",
        "Evidence",
    ]
    for c, h in enumerate(headers, start=1):
        ws.cell(row=3, column=c, value=h)
    style_header(ws, 3, len(headers))

    row = 4
    for p, path in quarters:
        doc = docs[path]
        issued = doc.get("period", p.label)
        for prom in doc.get("management_promises", []) or []:
            write_value(ws, row, 1, issued)
            write_value(ws, row, 2, prom.get("id", ""))
            write_value(ws, row, 3, prom.get("speaker", ""))
            muted(ws, row, 4, prom.get("quote", ""))
            write_value(ws, row, 5, prom.get("timeframe", ""))
            write_value(ws, row, 6, prom.get("status", "Pending"))
            muted(ws, row, 7, prom.get("evidence", ""))
            row += 1
    autosize(ws, min_width=12, max_width=60)


def main() -> None:
    ensure_workbooks_dir()
    files = discover_yaml(DATA_DIR / "guidance")
    quarters = flatten_periods(files)
    docs = {p: load_yaml(p) for p in files}

    wb = new_workbook()
    build_cover(wb, len(quarters))
    build_guide_vs_actual(wb, quarters, docs)
    build_promises(wb, quarters, docs)

    wb.save(OUTPUT)
    print(f"wrote {OUTPUT}  ({len(quarters)} quarter(s) of guidance)")


if __name__ == "__main__":
    main()
