#!/usr/bin/env python3
"""
Enhance user's V2 Vendor Payout workbook:

1. NPO MASTER — Alias, Legal Name, SAP, BSS, contacts (source of vendor identity)
2. Hybrid supplemental — editable on the statement for personal review/PDF;
   saved reference from SUPPLEMENTAL DATA; no per-NPO worksheets
3. Wire SAP/BSS from NPO MASTER onto VENDOR PAYOUT
4. Fix location seq slots 13–15 (V2 had 23/24/25)
5. Clarify CATEGORY MAP is required for Food vs Alcohol classification

Keeps one-way flow: SOURCE → CALCULATION → OUTPUT
"""

from __future__ import annotations

from copy import copy
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SRC = Path(__file__).with_name("NPO_Payout_Vendor_Template_final-V2.xlsx")
OUT = Path(__file__).with_name("NPO_Payout_Vendor_Template.xlsx")

MONEY = '\\$#,##0.00;[Red]\\($#,##0.00\\);\\-'
INPUT_FILL = PatternFill("solid", fgColor="FFFFF2CC")  # editable control / working cells
REF_FILL = PatternFill("solid", fgColor="FFF3F5F7")
HEADER_FILL = PatternFill("solid", fgColor="FF17365D")
NOTE_FONT = Font(name="Aptos", size=8, italic=True, color="FF666666")
THIN = Border(
    left=Side(style="thin", color="FFB0B7C3"),
    right=Side(style="thin", color="FFB0B7C3"),
    top=Side(style="thin", color="FFB0B7C3"),
    bottom=Side(style="thin", color="FFB0B7C3"),
)

NPO_SEED = [
    # Alias, Legal Name, SAP, BSS, Contact, Phone, Email, Payable To
    ("ARVC", "Albuquerque Rugby Volleyball Club", "", "", "", "", "", "ARVC"),
    ("AIRFORCE", "Air Force Association / Support Group", "", "", "", "", "", "AIRFORCE"),
    ("UNITED FIT", "United Fitness / Booster Group", "", "", "", "", "", "UNITED FIT"),
    ("DCVA", "Duke City Volleyball Association", "", "", "", "", "", "DCVA"),
    ("DEL N CHEER", "Del Norte Cheer", "", "", "", "", "", "DEL N CHEER"),
    ("RIO GRANDE RGHS", "Rio Grande High School", "", "", "", "", "", "RIO GRANDE RGHS"),
    ("VICTORY OUTREACH", "Victory Outreach Albuquerque", "", "", "", "", "", "VICTORY OUTREACH"),
]


def replace_seq_in_row(ws, row: int, old_seq: int, new_seq: int):
    token_old = f"|{old_seq}\""
    token_new = f"|{new_seq}\""
    # also handle |23', etc
    for col in range(1, 10):
        cell = ws.cell(row, col)
        if isinstance(cell.value, str) and f"|{old_seq}" in cell.value:
            cell.value = cell.value.replace(f"|{old_seq}", f"|{new_seq}")


def build_npo_master(wb):
    if "NPO MASTER" in wb.sheetnames:
        del wb["NPO MASTER"]
    # Insert after SET-UP
    ws = wb.create_sheet("NPO MASTER", 1)
    headers = [
        "Alias (Payee Key)",
        "Legal / Full Name",
        "SAP ID",
        "BSS ID",
        "Primary Contact",
        "Phone",
        "Email",
        "Check Payable To",
        "Active",
        "Standing Notes",
    ]
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(1, c, h)
        cell.fill = HEADER_FILL
        cell.font = Font(name="Aptos", size=10, bold=True, color="FFFFFFFF")
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    for r, row in enumerate(NPO_SEED, start=2):
        alias, legal, sap, bss, contact, phone, email, payable = row
        ws.cell(r, 1, alias)
        ws.cell(r, 2, legal)
        ws.cell(r, 3, sap)
        ws.cell(r, 4, bss)
        ws.cell(r, 5, contact)
        ws.cell(r, 6, phone)
        ws.cell(r, 7, email)
        ws.cell(r, 8, payable)
        ws.cell(r, 9, "Y")
        ws.cell(r, 10, "")

    ws.cell(1, 12, "PURPOSE")
    ws.cell(2, 12, (
        "One row per NPO/vendor group. Alias must match EVENT ASSIGNMENT NPO "
        "and VENDOR PAYOUT Payee. SAP/BSS fill the settlement header automatically. "
        "Standing Notes are permanent group info — not event-specific settlement notes."
    ))
    ws.cell(2, 12).font = NOTE_FONT
    ws.cell(2, 12).alignment = Alignment(wrap_text=True)
    ws.merge_cells("L2:O5")

    widths = [18, 36, 12, 12, 18, 14, 24, 22, 8, 28]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    return ws


def enhance_vendor_payout(ws, wb):
    # Fix seq 23/24/25 → 13/14/15 on rows 30–32
    replace_seq_in_row(ws, 30, 23, 13)
    replace_seq_in_row(ws, 31, 24, 14)
    replace_seq_in_row(ws, 32, 25, 15)

    # Legal name under alias (personal / document feel)
    ws["B7"] = '=IFERROR(VLOOKUP($E$10,\'NPO MASTER\'!$A$2:$B$50,2,FALSE),"")'
    ws["B7"].font = Font(name="Aptos", size=10, italic=True, color="FF17365D")

    # SAP / BSS from NPO MASTER
    ws["G10"] = '=IFERROR(VLOOKUP($E$10,\'NPO MASTER\'!$A$2:$D$50,3,FALSE),"")'
    ws["H10"] = '=IFERROR(VLOOKUP($E$10,\'NPO MASTER\'!$A$2:$D$50,4,FALSE),"")'
    for addr in ("G10", "H10"):
        ws[addr].font = Font(name="Aptos", size=11, bold=True)
        ws[addr].fill = REF_FILL

    # Payee remains the control (yellow)
    ws["E10"].fill = INPUT_FILL
    ws["B10"].fill = INPUT_FILL

    # Workflow note
    ws["B11"] = (
        "Review flow: select Event + Payee → confirm locations/commission → "
        "edit yellow THIS STATEMENT bonus/notes → Export PDF → "
        "zero yellow supplemental before next Payee (or copy into SUPPLEMENTAL DATA to remember). "
        "SAP/BSS come from NPO MASTER. Sales always from source/calc — never type those."
    )
    ws["B11"].font = NOTE_FONT
    ws["B11"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[11].height = 36

    # --- Hybrid supplemental ---
    # G = label, H = THIS STATEMENT (editable), I = SAVED REF from SUPPLEMENTAL DATA
    # V2 had G35:I35 merged — split for the two amount columns.
    for merged in list(ws.merged_cells.ranges):
        if str(merged) == "G35:I35":
            ws.unmerge_cells("G35:I35")

    ws["G35"] = "SUPPLEMENTAL PAYOUT"
    ws["H35"] = "THIS STATEMENT\n(edit for PDF)"
    ws["I35"] = "SAVED REF\n(SUPPLEMENTAL DATA)"
    for addr in ("G35", "H35", "I35"):
        ws[addr].font = Font(name="Aptos", size=9, bold=True, color="FFFFFFFF")
        ws[addr].fill = HEADER_FILL
        ws[addr].alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[35].height = 32

    labels = [
        ("Sales Incentive", "C"),
        ("Culinary - Cook Fee", "D"),
        ("Minimum Donation", "E"),
        ("Bonus (Other)", "F"),
        ("Deductible POS Shortages", "G"),
        ("Uniform / Staffing / Cleaning Fees", "H"),
    ]
    for i, (label, col) in enumerate(labels):
        r = 36 + i
        ws.cell(r, 7).value = label
        ws.cell(r, 7).font = Font(name="Aptos", size=10, bold=True)

        # Working / personal amount — editable value (starts at saved ref via formula
        # users may overwrite with a number for this document; that's intentional)
        # Use formula that pulls saved as starting point; overwriting is the "personal" act.
        # To support both load AND edit without VBA: keep H as editable VALUE seeded
        # from current SUPPLEMENTAL DATA snapshot at build time (0), and I as live saved ref.
        ws.cell(r, 8).value = 0
        ws.cell(r, 8).number_format = MONEY
        ws.cell(r, 8).fill = INPUT_FILL
        ws.cell(r, 8).border = THIN
        ws.cell(r, 8).font = Font(name="Aptos", size=12)

        ws.cell(r, 9).value = (
            f"=IFERROR(SUMIFS('SUPPLEMENTAL DATA'!${col}$2:${col}$101,"
            f"'SUPPLEMENTAL DATA'!$A$2:$A$101,$B$10,"
            f"'SUPPLEMENTAL DATA'!$B$2:$B$101,$E$10),0)"
        )
        ws.cell(r, 9).number_format = MONEY
        ws.cell(r, 9).fill = REF_FILL
        ws.cell(r, 9).border = THIN
        ws.cell(r, 9).font = Font(name="Aptos", size=10, color="FF666666")

    # Total payable uses THIS STATEMENT (H), not saved ref
    ws["G6"] = "=SUM(H33,I33,H36,H37,H38,H39,H40,H41)"
    ws["I42"] = "=SUM(H36:H41)"
    ws["I42"].number_format = MONEY
    ws["H42"] = "Statement supplemental total →"
    ws["H42"].font = Font(name="Aptos", size=8, italic=True)

    # GL misc / cleaning use THIS STATEMENT amounts
    ws["G48"] = "=SUM(H36:H40)"
    ws["G49"] = "=H41"

    # Settlement notes — personal, editable (V2 merges B36:E36 header + B37:E41 body)
    ws["B36"] = "SETTLEMENT NOTES (this document — edit freely before PDF)"
    ws["B36"].font = Font(name="Aptos", size=9, bold=True, color="FFFFFFFF")
    ws["B36"].fill = HEADER_FILL
    # Body of notes is merged B37:E41 — write only top-left
    ws["B37"] = ""
    ws["B37"].fill = INPUT_FILL
    ws["B37"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["B43"] = (
        "Tip: yellow H36:H41 + notes = this statement only. Grey I36:I41 = saved for Event+Payee. "
        "After PDF, zero H36:H41 before the next vendor — or copy H into SUPPLEMENTAL DATA to remember."
    )
    ws["B43"].font = NOTE_FONT
    ws["B43"].alignment = Alignment(wrap_text=True)

    # Payee dropdown from NPO MASTER
    # Remove old validations carefully by replacing list
    dvs = DataValidation(
        type="list",
        formula1="='NPO MASTER'!$A$2:$A$50",
        allow_blank=False,
        showErrorMessage=True,
        errorTitle="Payee / NPO",
        error="Select an Alias from NPO MASTER.",
        promptTitle="Payee / NPO",
        prompt="Select vendor Alias. SAP/BSS and legal name fill automatically.",
    )
    dvs.add("E10")
    ws.add_data_validation(dvs)

    # Widen print area to include saved ref column if needed
    if ws.print_area:
        # keep existing style; include I
        ws.print_area = "$B$2:$I$51"


def annotate_category_map(wb):
    ws = wb["CATEGORY MAP"]
    ws["E1"] = "REQUIRED"
    ws["E1"].font = Font(name="Aptos", size=10, bold=True, color="FF990000")
    ws["E2"] = (
        "Maps MyVenue product codes → FOOD/NON-ALC vs ALCOHOL for CONTRACT CALC. "
        "Do not delete this sheet. Add new product codes here when MSR exports change. "
        "You can hide the tab if you want a cleaner workbook; keep the sheet in the file."
    )
    ws["E2"].font = NOTE_FONT
    ws["E2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("E2:H5")
    ws.column_dimensions["E"].width = 18


def annotate_setup(wb):
    setup = wb["SET-UP & SUMMARY"]
    setup["A21"] = (
        "VENDOR PAYOUT = one reusable statement. NPO MASTER = vendor identity (SAP/BSS/Alias). "
        "SUPPLEMENTAL DATA = optional saved bonus/fees by Event+Payee. "
        "Yellow cells on VENDOR PAYOUT are this document’s personal adjustments for review/PDF. "
        "CATEGORY MAP is required for food vs alcohol classification."
    )
    setup["A21"].font = NOTE_FONT
    setup["A21"].alignment = Alignment(wrap_text=True)


def annotate_supplemental(wb):
    if "SUPPLEMENTAL DATA" not in wb.sheetnames:
        return
    ws = wb["SUPPLEMENTAL DATA"]
    ws["J1"] = "HOW TO USE"
    ws["J1"].font = Font(name="Aptos", size=10, bold=True)
    ws["J2"] = (
        "Optional memory for Event + Payee. VENDOR PAYOUT shows these as grey SAVED REF. "
        "Day-of personal bonus/notes are edited in yellow on VENDOR PAYOUT for that PDF. "
        "Copy statement amounts here only when you want them to reload next time."
    )
    ws["J2"].font = NOTE_FONT
    ws["J2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("J2:L5")


def main():
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC}")
    wb = load_workbook(SRC)
    build_npo_master(wb)
    enhance_vendor_payout(wb["VENDOR PAYOUT"], wb)
    annotate_category_map(wb)
    annotate_setup(wb)
    annotate_supplemental(wb)

    # Guard: no reverse refs into VENDOR PAYOUT from source/calc
    banned = []
    for name in wb.sheetnames:
        if name == "VENDOR PAYOUT":
            continue
        sh = wb[name]
        for row in sh.iter_rows():
            for cell in row:
                val = cell.value
                if isinstance(val, str) and val.startswith("=") and "VENDOR PAYOUT" in val.upper():
                    banned.append(f"{name}!{cell.coordinate}")
    if banned:
        raise RuntimeError("Reverse refs: " + ", ".join(banned))

    wb.save(OUT)
    print(f"Wrote {OUT}")
    print("Sheets:", wb.sheetnames)
    print("NPO MASTER aliases:", [r[0] for r in NPO_SEED])
    print("CATEGORY MAP: kept (required for MSR→Food/Alcohol class)")


if __name__ == "__main__":
    main()
