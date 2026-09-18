#!/usr/bin/env python3
"""
Convert the ARVC settlement worksheet into a single reusable Vendor Payout
template controlled by Event Date + Payee/NPO.

Architecture (one-directional only):
  SOURCE (MSR RAW, EVENT ASSIGNMENT, TIPS DATA, CATEGORY MAP, SET-UP)
    → CALCULATION (MSR DATA, CONTRACT CALC)
    → OUTPUT (VENDOR PAYOUT)

The output sheet never feeds data back into source/calculation tabs.
Location detail rows are filtered from CONTRACT CALC / EVENT ASSIGNMENT by
the selected Event Date + Payee, so the same template can show 2, 5, 20+
locations without per-NPO worksheets.
"""

from __future__ import annotations

from copy import copy
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SRC = Path(__file__).with_name("NPO_Payout_Prototype_V10.xlsx")
OUT = Path(__file__).with_name("NPO_Payout_Vendor_Template.xlsx")

# Enough slots for large multi-location assignments; unused rows stay blank.
MAX_LOCATIONS = 25
DETAIL_START = 18  # first location detail row
DETAIL_END = DETAIL_START + MAX_LOCATIONS - 1  # 42
TOTAL_ROW = DETAIL_END + 1  # 43
NOTE_ROW = TOTAL_ROW + 1  # 44
SUPP_HEADER = NOTE_ROW + 1  # 45
SUPP_START = SUPP_HEADER + 1  # 46
SUPP_END = SUPP_START + 5  # 51
SUPP_SUM = SUPP_END + 1  # 52
AUTH_HEADER = SUPP_SUM + 3  # 55
AUTH_END = AUTH_HEADER + 6  # 61

MONEY = '\\$#,##0.00;[Red]\\($#,##0.00\\);\\-'
MONEY_TOTAL = '\\$#,##0.00;[Red]\\($#,##0.00\\);\\-'
PAYABLE_FMT = '\\$#,##0.00;\\($#,##0.00\\);\\-'
GL_MONEY = '_($* #,##0.00_);_($* (#,##0.00);_($* -??_);_(@_)'

THIN = Border(
    left=Side(style="thin", color="FFB0B7C3"),
    right=Side(style="thin", color="FFB0B7C3"),
    top=Side(style="thin", color="FFB0B7C3"),
    bottom=Side(style="thin", color="FFB0B7C3"),
)

HEADER_FILL = PatternFill("solid", fgColor="FF17365D")
HEADER_FONT = Font(name="Aptos", size=7.5, bold=True, color="FFFFFFFF")
SECTION_FILL = PatternFill("solid", fgColor="FFF3F5F7")
SECTION_FONT = Font(name="Aptos", size=12, bold=True, color="FF17365D")
TITLE_FONT = Font(name="Aptos", size=24, bold=True, color="FF17365D")
SUBTITLE_FONT = Font(name="Aptos", size=11, bold=True, color="FF17365D")
PAYEE_FONT = Font(name="Aptos", size=16, bold=True, color="FF17365D")
BODY_FONT = Font(name="Aptos", size=8, bold=False)
BODY_NUM_FONT = Font(name="Aptos", size=12, bold=False)
TOTAL_LABEL_FONT = Font(name="Aptos", size=8.5, bold=True)
TOTAL_NUM_FONT = Font(name="Aptos", size=12, bold=True)
NOTE_FONT = Font(name="Aptos", size=8, italic=True, color="FF666666")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFFFF")
PAYABLE_FILL = PatternFill("solid", fgColor="FFF7F8FA")


def copy_cell_style(src, dst):
    if src.has_style:
        dst.font = copy(src.font)
        dst.border = copy(src.border)
        dst.fill = copy(src.fill)
        dst.number_format = src.number_format
        dst.protection = copy(src.protection)
        dst.alignment = copy(src.alignment)


def clear_range(ws, min_row, max_row, min_col=1, max_col=12):
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            ws.cell(r, c).value = None


def unmerge_overlapping(ws, min_row, max_row):
    to_remove = []
    for merged in ws.merged_cells.ranges:
        if merged.max_row >= min_row and merged.min_row <= max_row:
            to_remove.append(str(merged))
    for ref in to_remove:
        ws.unmerge_cells(ref)


def location_formulas(row: int, k: int) -> dict[str, str]:
    """Validated commission math for the k-th matching assignment.

    Uses plain INDEX/MATCH against EVENT ASSIGNMENT helper key column K
    (yyyymmdd|PAYEE|seq). No FILTER, no AGGREGATE arrays — formulas openpyxl
    writes that Excel will not repair away.
    CONTRACT CALC row = EVENT ASSIGNMENT data index + 12
    (MATCH position 1 = EA row 2 = CC row 13).
    """
    # Absolute key for this detail slot: date|payee|k
    key = f'TEXT($B$10,"yyyymmdd")&"|"&$E$10&"|{k}"'
    # Relative position within EA!$2:$101 (1 = first data row)
    pos = (
        f'IFERROR(MATCH({key},\'EVENT ASSIGNMENT\'!$K$2:$K$101,0),"")'
    )
    return {
        "A": f"={pos}",
        "B": (
            f'=IF({pos}="","",'
            f"IFERROR(INDEX('EVENT ASSIGNMENT'!$D$2:$D$101,{pos}),\"\"))"
        ),
        "C": (
            f'=IF(OR({pos}="",B{row}=""),"",'
            f"IFERROR(INDEX('CONTRACT CALC'!$G$13:$G$112,{pos})"
            f"*INDEX('CONTRACT CALC'!$F$13:$F$112,{pos}),\"\"))"
        ),
        "D": (
            f'=IF(OR({pos}="",B{row}=""),"",'
            f"IFERROR(INDEX('CONTRACT CALC'!$I$13:$I$112,{pos})"
            f"*INDEX('CONTRACT CALC'!$F$13:$F$112,{pos}),\"\"))"
        ),
        "E": f'=IF(D{row}="","",D{row}*\'CONTRACT CALC\'!$B$4)',
        "F": (
            f'=IF(OR({pos}="",B{row}=""),"",'
            f"IFERROR(INDEX('CONTRACT CALC'!$H$13:$H$112,{pos})"
            f"*INDEX('CONTRACT CALC'!$F$13:$F$112,{pos}),\"\"))"
        ),
        "G": f'=IF(F{row}="","",F{row}*\'CONTRACT CALC\'!$B$5)',
        "H": f'=IF(B{row}="","",N(E{row})+N(G{row}))',
        "I": (
            f'=IF(OR({pos}="",B{row}=""),"",'
            f'IF(COUNTIFS(\'TIPS DATA\'!$A$2:$A$101,$B$10,'
            f"'TIPS DATA'!$C$2:$C$101,$E$10,"
            f"'TIPS DATA'!$D$2:$D$101,"
            f"INDEX('EVENT ASSIGNMENT'!$C$2:$C$101,{pos}))>0,"
            f"SUMIFS('TIPS DATA'!$H$2:$H$101,"
            f"'TIPS DATA'!$A$2:$A$101,$B$10,"
            f"'TIPS DATA'!$C$2:$C$101,$E$10,"
            f"'TIPS DATA'!$D$2:$D$101,"
            f"INDEX('EVENT ASSIGNMENT'!$C$2:$C$101,{pos})),"
            f"SUMIFS('TIPS DATA'!$H$2:$H$101,"
            f"'TIPS DATA'!$A$2:$A$101,$B$10,"
            f"'TIPS DATA'!$C$2:$C$101,$E$10,"
            f"'TIPS DATA'!$E$2:$E$101,"
            f"INDEX('EVENT ASSIGNMENT'!$D$2:$D$101,{pos}))))"
        ),
    }


def style_detail_row(ws, row: int, template_row: int = 18):
    for col in range(1, 10):
        src = ws.cell(template_row, col)
        dst = ws.cell(row, col)
        # Apply known styles rather than copying potentially empty template after rewrite
        dst.font = BODY_FONT if col == 2 else BODY_NUM_FONT
        if col == 1:
            dst.font = Font(name="Aptos", size=8, color="FFAAAAAA")
        dst.border = THIN if col >= 2 else Border()
        dst.number_format = MONEY if col >= 3 else "General"
        dst.alignment = Alignment(vertical="center")


def build():
    wb = load_workbook(SRC)

    # --- EVENT ASSIGNMENT lookup keys (source helpers; not a new calc sheet) ---
    # J = running seq for Event+Payee; K = yyyymmdd|PAYEE|seq for INDEX/MATCH.
    ea = wb["EVENT ASSIGNMENT"]
    ea["J1"] = "Payee Seq"
    ea["K1"] = "Payout Lookup Key"
    ea["J1"].font = Font(name="Aptos", size=10, bold=True)
    ea["K1"].font = Font(name="Aptos", size=10, bold=True)
    for r in range(2, 102):
        # Seq restarts per Event Date + NPO within the assignment list
        ea.cell(r, 10).value = (
            f'=IF(OR(A{r}="",F{r}=""),"",'
            f'COUNTIFS($A$2:A{r},A{r},$F$2:F{r},F{r}))'
        )
        ea.cell(r, 11).value = (
            f'=IF(OR(A{r}="",F{r}="",J{r}=""),"",'
            f'TEXT(A{r},"yyyymmdd")&"|"&F{r}&"|"&J{r})'
        )

    # --- SUPPLEMENTAL DATA (source): Event + Payee keyed adjustments ---
    # Keeps Bonus / fees / incentives off the output sheet so switching Payee
    # cannot carry a prior vendor's manual adjustments into the next statement.
    if "SUPPLEMENTAL DATA" in wb.sheetnames:
        wb.remove(wb["SUPPLEMENTAL DATA"])
    supp = wb.create_sheet("SUPPLEMENTAL DATA")
    # Place after TIPS DATA for source-tab grouping
    try:
        wb.move_sheet(supp, offset=len(wb.sheetnames) - 1 - wb.sheetnames.index("TIPS DATA"))
    except Exception:
        pass
    headers = [
        "Event Date",
        "NPO",
        "Sales Incentive",
        "Culinary - Cook Fee",
        "Minimum Donation",
        "Bonus (Other)",
        "Deductible POS Shortages",
        "Uniform / Staffing / Cleaning Fees",
        "Notes",
    ]
    for c, h in enumerate(headers, start=1):
        cell = supp.cell(1, c, h)
        cell.fill = PatternFill("solid", fgColor="FF17365D")
        cell.font = Font(name="Aptos", size=10, bold=True, color="FFFFFFFF")
    # Seed zero rows for the proof event; enter non-zero adjustments per Event + Payee here.
    setup_date = wb["SET-UP & SUMMARY"]["B4"].value
    for r, npo in enumerate(
        ["ARVC", "AIRFORCE", "UNITED FIT", "DCVA", "DEL N CHEER", "RIO GRANDE RGHS", "VICTORY OUTREACH"],
        start=2,
    ):
        supp.cell(r, 1).value = setup_date
        supp.cell(r, 1).number_format = "mmmm d, yyyy"
        supp.cell(r, 2).value = npo
        for c in range(3, 9):
            supp.cell(r, c).value = 0
            supp.cell(r, c).number_format = MONEY
    supp.cell(2, 9).value = (
        "Enter vendor-specific adjustments by Event + Payee. "
        "VENDOR PAYOUT reads these; it does not store them."
    )
    for col, width in enumerate([14, 18, 14, 16, 14, 14, 18, 22, 40], start=1):
        supp.column_dimensions[get_column_letter(col)].width = width
    # NPO validation
    dv_supp = DataValidation(
        type="list",
        formula1="='SET-UP & SUMMARY'!$A$12:$A$18",
        allow_blank=True,
    )
    dv_supp.add("B2:B101")
    supp.add_data_validation(dv_supp)

    # --- Rename ARVC → VENDOR PAYOUT (single reusable output template) ---
    ws = wb["ARVC"]
    ws.title = "VENDOR PAYOUT"

    # Capture supplemental / auth content before restructuring
    old = {
        "supp_labels": [ws.cell(r, 7).value for r in range(26, 32)],
        "supp_values": [ws.cell(r, 9).value for r in range(26, 32)],
        "auth_left": {
            35: [ws.cell(35, c).value for c in range(2, 5)],
            36: [ws.cell(36, c).value for c in range(2, 5)],
            37: [ws.cell(37, c).value for c in range(2, 5)],
            38: [ws.cell(38, c).value for c in range(2, 5)],
            39: [ws.cell(39, c).value for c in range(2, 5)],
            40: [ws.cell(40, c).value for c in range(2, 5)],
            41: [ws.cell(41, c).value for c in range(2, 5)],
        },
        "auth_right": {
            35: [ws.cell(35, c).value for c in range(5, 9)],
            36: [ws.cell(36, c).value for c in range(5, 9)],
            37: [ws.cell(37, c).value for c in range(5, 9)],
            38: [ws.cell(38, c).value for c in range(5, 9)],
            39: [ws.cell(39, c).value for c in range(5, 9)],
        },
        "settlement_notes_header": ws["B26"].value,
        "note_line": ws["B24"].value,
        "b6": ws["B6"].value,
        "g5": ws["G5"].value,
    }

    # Unmerge regions that will move
    unmerge_overlapping(ws, 18, 80)

    # Clear old detail through end of sheet content
    clear_range(ws, 18, 80, 1, 12)

    # --- Header controls: Event Date (from SET-UP) + Payee selector ---
    # B5 shows selected payee (was hardcoded to SET-UP!A12 / ARVC)
    ws["B5"] = '=$E$10'
    ws["B5"].font = PAYEE_FONT

    # E9 label clarifies this is the Payee/NPO control
    ws["E9"] = "PAYEE / NPO"
    ws["E9"].font = Font(name="Aptos", size=12, bold=True)
    ws["E9"].fill = SECTION_FILL

    # E10 = Payee selector (starts at ARVC to preserve validated proof case)
    ws["E10"] = "ARVC"
    ws["E10"].font = Font(name="Aptos", size=12, bold=True)
    ws["E10"].number_format = "General"
    ws["E10"].fill = PatternFill("solid", fgColor="FFFFF2CC")  # control highlight

    # B10 Event Date = template control (seeded from SET-UP; not a back-write)
    setup_date = wb["SET-UP & SUMMARY"]["B4"].value
    ws["B10"] = setup_date
    ws["B10"].number_format = "mmmm d, yyyy"
    ws["B10"].font = Font(name="Aptos", size=12, bold=True)
    ws["B10"].fill = PatternFill("solid", fgColor="FFFFF2CC")

    # Invoice still derives from Event Date + Payee
    ws["C10"] = '=CONCATENATE("UNM-",TEXT(B10,"MMDDYY-"),E10)'

    # Soft guide under controls (does not change layout hierarchy)
    ws["B11"] = (
        "Controls: Event Date (B10) + Payee/NPO (E10). "
        "Location rows filter from EVENT ASSIGNMENT via CONTRACT CALC. "
        "Flow: SOURCE → CALCULATION → OUTPUT (never reverse)."
    )
    ws["B11"].font = NOTE_FONT

    # Re-apply header merges that were removed if needed
    for ref in [
        "C2:G2",
        "C3:G3",
        "B5:F5",
        "G5:H5",
        "B6:F6",
        "G6:H7",
        "C9:D9",
        "E9:F9",
        "E10:F10",
        "E12:F12",
        "B16:I16",
    ]:
        try:
            ws.merge_cells(ref)
        except ValueError:
            pass

    ws["G5"] = old["g5"]
    ws["G5"].font = Font(name="Aptos", size=12, bold=True)
    ws["G5"].fill = PAYABLE_FILL

    # TOTAL PAYABLE references new total / supplemental rows
    ws["G6"] = (
        f"=SUM(H{TOTAL_ROW},I{TOTAL_ROW},"
        f"I{SUPP_START},I{SUPP_START+1},I{SUPP_START+2},"
        f"I{SUPP_START+3},I{SUPP_START+4},I{SUPP_START+5})"
    )
    ws["G6"].font = Font(name="Aptos", size=20, bold=True)
    ws["G6"].fill = PAYABLE_FILL
    ws["G6"].number_format = PAYABLE_FMT

    # Sales summary boxes → point at new TOTAL row (preserve mapping)
    ws["B14"] = f"=D{TOTAL_ROW}"
    ws["C14"] = f"=F{TOTAL_ROW}"
    ws["D14"] = f"=C{TOTAL_ROW}"
    ws["E14"] = f"=D{TOTAL_ROW}"
    ws["F14"] = f"=E{TOTAL_ROW}"
    for col in "BCDEF":
        ws[f"{col}14"].number_format = "\\$#,##0.00"
        ws[f"{col}14"].font = Font(name="Aptos", size=14, bold=True)

    # --- Location detail header (row 17 preserved) ---
    # Ensure header labels remain
    headers = {
        "B17": "SERVICE AREA",
        "C17": "NET SALES",
        "D17": "FOOD / NON-ALC\nNET SALES",
        "E17": "10% FOOD / NON-ALC\nCOMMISSION",
        "F17": "ALCOHOL\nNET SALES",
        "G17": "8% ALCOHOL\nCOMMISSION",
        "H17": "TOTAL\nCOMMISSION",
        "I17": "GRATUITIES",
    }
    for addr, val in headers.items():
        ws[addr] = val
        ws[addr].font = HEADER_FONT
        ws[addr].fill = HEADER_FILL
        ws[addr].alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws[addr].border = THIN

    ws["A17"] = "#"
    ws["A17"].font = HEADER_FONT
    ws["A17"].fill = HEADER_FILL

    # --- Detail rows driven by Event + Payee match into CONTRACT CALC ---
    for i, row in enumerate(range(DETAIL_START, DETAIL_END + 1), start=1):
        formulas = location_formulas(row, i)
        for col, formula in formulas.items():
            cell = ws[f"{col}{row}"]
            cell.value = formula
        style_detail_row(ws, row)
        ws[f"A{row}"].number_format = "General"

    # --- TOTAL row ---
    ws[f"B{TOTAL_ROW}"] = "TOTAL"
    ws[f"B{TOTAL_ROW}"].font = TOTAL_LABEL_FONT
    for col, letter in enumerate(["C", "D", "E", "F", "G", "H", "I"], start=3):
        # SUM over detail block; blanks ignored
        ws.cell(TOTAL_ROW, col).value = f"=SUM({letter}{DETAIL_START}:{letter}{DETAIL_END})"
        ws.cell(TOTAL_ROW, col).font = TOTAL_NUM_FONT
        ws.cell(TOTAL_ROW, col).number_format = MONEY_TOTAL
        ws.cell(TOTAL_ROW, col).border = THIN
    ws[f"B{TOTAL_ROW}"].border = THIN
    for col in range(2, 10):
        ws.cell(TOTAL_ROW, col).fill = SECTION_FILL

    # Note
    ws[f"B{NOTE_ROW}"] = (
        "Location rows are filtered from EVENT ASSIGNMENT / CONTRACT CALC by Event Date + Payee. "
        "Location Total = Contractual Donation + Gratuities; commission rates are shown explicitly by sales category above."
    )
    ws[f"B{NOTE_ROW}"].font = NOTE_FONT
    try:
        ws.merge_cells(start_row=NOTE_ROW, start_column=2, end_row=NOTE_ROW, end_column=8)
    except ValueError:
        pass

    # --- Supplemental payout (preserve labels/values) ---
    ws[f"G{SUPP_HEADER}"] = "SUPPLEMENTAL PAYOUT:"
    ws[f"G{SUPP_HEADER}"].font = SECTION_FONT
    ws[f"G{SUPP_HEADER}"].fill = SECTION_FILL
    try:
        ws.merge_cells(
            start_row=SUPP_HEADER, start_column=7, end_row=SUPP_HEADER, end_column=9
        )
    except ValueError:
        pass

    ws[f"B{SUPP_START}"] = old["settlement_notes_header"]
    ws[f"B{SUPP_START}"].font = Font(name="Aptos", size=10, bold=True)
    try:
        ws.merge_cells(
            start_row=SUPP_START, start_column=2, end_row=SUPP_START, end_column=5
        )
    except ValueError:
        pass

    # Supplemental amounts come from SUPPLEMENTAL DATA by Event Date + Payee
    # (SOURCE → OUTPUT). Switching Payee cannot carry over another vendor's bonus.
    supp_cols = [
        # (label, column letter on SUPPLEMENTAL DATA)
        ("Sales Incentive", "C"),
        ("Culinary - Cook Fee", "D"),
        ("Minimum Donation", "E"),
        ("Bonus (Other)", "F"),
        ("Deductible POS Shortages", "G"),
        ("Uniform / Staffing / Cleaning Fees", "H"),
    ]
    for offset, (label, col_letter) in enumerate(supp_cols):
        r = SUPP_START + offset
        ws.cell(r, 7).value = label
        ws.cell(r, 7).font = Font(name="Aptos", size=10, bold=True)
        ws.cell(r, 9).value = (
            f"=IFERROR(SUMIFS('SUPPLEMENTAL DATA'!${col_letter}$2:${col_letter}$101,"
            f"'SUPPLEMENTAL DATA'!$A$2:$A$101,$B$10,"
            f"'SUPPLEMENTAL DATA'!$B$2:$B$101,$E$10),0)"
        )
        ws.cell(r, 9).number_format = MONEY
        ws.cell(r, 9).font = BODY_NUM_FONT
        ws.cell(r, 9).border = THIN

    try:
        ws.merge_cells(
            start_row=SUPP_START + 1, start_column=2, end_row=SUPP_END, end_column=5
        )
    except ValueError:
        pass

    ws[f"I{SUPP_SUM}"] = f"=SUM(I{SUPP_START}:I{SUPP_END})"
    ws[f"I{SUPP_SUM}"].font = TOTAL_NUM_FONT
    ws[f"I{SUPP_SUM}"].number_format = '"$"#,##0.00_);[Red]\\("$"#,##0.00\\)'

    # --- Internal authorization / GL (preserve layout, retarget formulas) ---
    ws.cell(AUTH_HEADER, 2).value = "INTERNAL AUTHORIZATION CHECK REQUEST"
    ws.cell(AUTH_HEADER, 2).font = Font(name="Aptos", size=9, bold=True, color="FFFFFFFF")
    ws.cell(AUTH_HEADER, 2).fill = HEADER_FILL
    try:
        ws.merge_cells(
            start_row=AUTH_HEADER, start_column=2, end_row=AUTH_HEADER, end_column=3
        )
    except ValueError:
        pass

    ws.cell(AUTH_HEADER, 5).value = "INTERNAL - ACCOUNTING GL ENTRY - SUMMARY"
    ws.cell(AUTH_HEADER, 5).font = Font(name="Arial", size=9, bold=True, color="FFFFFFFF")
    ws.cell(AUTH_HEADER, 5).fill = HEADER_FILL
    try:
        ws.merge_cells(
            start_row=AUTH_HEADER, start_column=5, end_row=AUTH_HEADER, end_column=7
        )
    except ValueError:
        pass

    # Left signatures (from captured rows 36-41)
    left_rows = [
        (1, "Abigail Tenorio", "Concessions Manager"),
        (3, "Ray Velasquez", "Director of Operations"),
        (5, "Evan E. Gonzales", "Finance Manager"),
    ]
    # Recreate from original captured values
    ws.cell(AUTH_HEADER + 1, 2).value = old["auth_left"][36][0]
    ws.cell(AUTH_HEADER + 1, 3).value = "=TODAY()"
    ws.cell(AUTH_HEADER + 2, 2).value = old["auth_left"][37][0]
    ws.cell(AUTH_HEADER + 3, 2).value = old["auth_left"][38][0]
    ws.cell(AUTH_HEADER + 3, 3).value = "=TODAY()"
    ws.cell(AUTH_HEADER + 4, 2).value = old["auth_left"][39][0]
    ws.cell(AUTH_HEADER + 5, 2).value = old["auth_left"][40][0]
    ws.cell(AUTH_HEADER + 5, 3).value = "=TODAY()"
    ws.cell(AUTH_HEADER + 6, 2).value = old["auth_left"][41][0]

    for r in range(AUTH_HEADER + 1, AUTH_HEADER + 7):
        ws.cell(r, 2).font = Font(name="Aptos", size=10, bold=True)

    # Right GL summary — preserve validated mappings to commission / tips / misc
    gl_rows = [
        (1, "Group Commission", "241 | 36127 | GL:611225", f"=H{TOTAL_ROW}"),
        (2, "Gratuities", "241 | 36127 | GL:212113", f"=I{TOTAL_ROW}"),
        (
            3,
            "Misc. (to be reclassed)",
            "241 | 36127 | GL:673000",
            f"=SUM(I{SUPP_START}:I{SUPP_START+4})",
        ),
        (
            4,
            "Cleaning Fee - Expense",
            "241 | 36127 | GL:674102",
            f"=I{SUPP_END}",
        ),
    ]
    for offset, label, acct, formula in gl_rows:
        r = AUTH_HEADER + offset
        ws.cell(r, 5).value = label
        ws.cell(r, 5).font = Font(name="Arial", size=9, bold=True)
        ws.cell(r, 6).value = acct
        ws.cell(r, 6).font = Font(name="Arial", size=9)
        ws.cell(r, 7).value = formula
        ws.cell(r, 7).font = Font(name="Arial", size=10, bold=True)
        ws.cell(r, 7).number_format = GL_MONEY

    # Data validation for Payee/NPO from SET-UP summary NPO list
    dv_payee = DataValidation(
        type="list",
        formula1="='SET-UP & SUMMARY'!$A$12:$A$18",
        allow_blank=False,
        showDropDown=False,
        showErrorMessage=True,
        errorTitle="Payee / NPO",
        error="Select a Payee/NPO from the SET-UP & SUMMARY list.",
        promptTitle="Payee / NPO",
        prompt="Select the vendor / NPO for this settlement statement.",
    )
    dv_payee.add("E10")
    ws.add_data_validation(dv_payee)

    # Event Date choices come from EVENT ASSIGNMENT (source), not from this output sheet
    dv_event = DataValidation(
        type="list",
        formula1="='EVENT ASSIGNMENT'!$A$2:$A$101",
        allow_blank=False,
        showDropDown=False,
        showErrorMessage=True,
        errorTitle="Event Date",
        error="Select an Event Date that exists on EVENT ASSIGNMENT.",
        promptTitle="Event Date",
        prompt="Select the event date for this settlement statement.",
    )
    dv_event.add("B10")
    ws.add_data_validation(dv_event)

    # Print / PDF area covers full template including expanded locations
    ws.print_area = f"$B$2:$I${AUTH_END}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.print_options.horizontalCentered = True
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # Column A helper width (not in print area)
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["A"].hidden = False

    # --- Guardrail note on SET-UP (non-invasive) ---
    setup = wb["SET-UP & SUMMARY"]
    setup["A21"] = (
        "VENDOR PAYOUT is the reusable settlement OUTPUT controlled by Event Date + Payee/NPO. "
        "Update source data, select Event + Payee on VENDOR PAYOUT, review, export PDF. "
        "One-way only: SOURCE → CALCULATION → OUTPUT."
    )
    setup["A21"].font = Font(name="Aptos", size=8, italic=True, color="FF666666")

    # Verify no source/calc FORMULAS reference the output sheet (one-way only)
    banned = []
    for name in wb.sheetnames:
        if name == "VENDOR PAYOUT":
            continue
        sheet = wb[name]
        for row in sheet.iter_rows():
            for cell in row:
                val = cell.value
                if not isinstance(val, str) or not val.startswith("="):
                    continue
                upper = val.upper()
                if "VENDOR PAYOUT" in upper or "'ARVC'!" in upper or "ARVC!" in upper:
                    banned.append(f"{name}!{cell.coordinate}: {val}")

    if banned:
        raise RuntimeError(
            "Circular / reverse references detected:\n" + "\n".join(banned)
        )

    wb.save(OUT)
    print(f"Wrote {OUT}")
    print(f"Detail rows: {DETAIL_START}-{DETAIL_END} ({MAX_LOCATIONS} slots)")
    print(f"TOTAL row: {TOTAL_ROW}")
    print(f"Supplemental: {SUPP_START}-{SUPP_END}, Auth: {AUTH_HEADER}-{AUTH_END}")
    print("No reverse references from source/calc → output.")


if __name__ == "__main__":
    build()
