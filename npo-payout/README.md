# NPO Vendor Payout Workbook

One-directional settlement model:

**SOURCE → CALCULATION → OUTPUT**

| Layer | Sheets |
| --- | --- |
| SOURCE | `MSR RAW`, `EVENT ASSIGNMENT`, `TIPS DATA`, `CATEGORY MAP`, `SET-UP & SUMMARY` |
| CALCULATION | `MSR DATA`, `CONTRACT CALC` |
| OUTPUT | `VENDOR PAYOUT` (single reusable template) |

The output sheet never feeds values back into source or calculation tabs.

## Workflow

1. **Update source data** — MSR export, event assignments, tips, category map.
2. **Select Event + Payee** on `VENDOR PAYOUT` (`B10` Event Date, `E10` Payee/NPO).
3. **Review payout** — location rows filter from `EVENT ASSIGNMENT` via `CONTRACT CALC` (2, 5, 20+ locations as assigned).
4. **Export PDF** — print area is set on `VENDOR PAYOUT`.

Do **not** create a worksheet per NPO. Change Payee on the same template.

## Preserved commission logic

Per location (allocated):

- Food / Non-Alcoholic net × **10%** (`CONTRACT CALC!$B$4`)
- Alcohol net × **8%** (`CONTRACT CALC!$B$5`)
- Gratuities from `TIPS DATA`
- Final payable = total commission + gratuities + supplemental lines

## Rebuild

```bash
python3 build_vendor_payout_template.py
```

Reads `NPO_Payout_Prototype_V10.xlsx` and writes `NPO_Payout_Vendor_Template.xlsx`.
