# NPO Vendor Payout Workbook

One-directional settlement model:

**SOURCE → CALCULATION → OUTPUT**

| Layer | Sheets |
| --- | --- |
| SOURCE | `MSR RAW`, `EVENT ASSIGNMENT`, `TIPS DATA`, `SUPPLEMENTAL DATA`, `NPO MASTER`, `CATEGORY MAP`, `SET-UP & SUMMARY` |
| CALCULATION | `MSR DATA`, `CONTRACT CALC` |
| OUTPUT | `VENDOR PAYOUT` (single reusable template) |

## NPO MASTER (vendor identity)

One row per group:

- **Alias (Payee Key)** — must match `EVENT ASSIGNMENT` NPO and `VENDOR PAYOUT` Payee
- Legal / Full Name, **SAP ID**, **BSS ID**
- Contact, phone, email, check payable-to, standing notes

`VENDOR PAYOUT` pulls SAP / BSS / legal name when you select Payee. Fill SAP/BSS here once — not on each statement.

## Review flow (personal factor kept)

1. Update source data (MSR, assignments, tips).
2. On `VENDOR PAYOUT`, select **Event Date** + **Payee**.
3. Review locations / 10% / 8% / tips (from calc — don’t type those).
4. Edit **yellow** cells: supplemental (H36:H41) + settlement notes — this document only.
5. **Export PDF** (the personalized record).
6. Before next vendor: **zero H36:H41** (and clear notes). Optional: copy those amounts into `SUPPLEMENTAL DATA` if you want them to show again later as grey SAVED REF.

Location detail on `VENDOR PAYOUT` is capped at **10 rows** (ultimate max per payee).

Do **not** create a worksheet per NPO.

## Is CATEGORY MAP necessary?

**Yes.** `MSR DATA` uses it to classify MyVenue product codes as FOOD/NON-ALC vs ALCOHOL so `CONTRACT CALC` can apply 10% vs 8%. Keep the sheet; hide the tab if you want less clutter. Add new product codes when MSR exports change.

## Rebuild from your V2 formatting

```bash
python3 enhance_vendor_payout_v3.py
```

Reads `NPO_Payout_Vendor_Template_final-V2.xlsx` → writes `NPO_Payout_Vendor_Template.xlsx`.
