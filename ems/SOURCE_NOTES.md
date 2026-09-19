# Source notes

These notes record what was taken from live UNM files versus Copilot chat. The Access generator should treat live files as truth.

Copilot’s **Developer Build Binder v4.0 Volume A** (pasted 2026-09-19) is the chapter map for this package. Field-level truth is still the live workbooks. Full diff: `COPILOT_V4_CROSSWALK.md`.

## Files ingested

| File | Role |
|---|---|
| Copilot EMS Developer Build Binder v4.0 Volume A | Chapter 1–7 outline: FE/BE, lookups, core tables, category map, contracts, forms, build sequence |
| EMS Project Manager Action Plan | Construction order, FE/BE split, alpha definition, earlier Copilot Volume A sketch |
| NPO Payout Vendor Template final-V4 | Live NPO engine: assignment, category map, tips, donation formula, vendor aliases |
| MyVenue Location List All UNM 09-14-26 | 81-location master |
| MSR Location Payout CSV 09-05-26 | Nested MyVenue export shape and product codes |
| SUB AP UNM REMIT NAME 12-01-25.xlsx | SUB engine, LAG/SUG identity, rates, expenses, invoice numbers |
| SUB Sugar Shivers PDF 12-01-25 | Print layout + GL split for SUB |
| NPO ARVC PDF 12-01-25 | Older NPO print layout; filled ARVC SAP/BSS |

## Copilot vs live

| Topic | Copilot said | Live files show |
|---|---|---|
| Volume A shape | 7 chapters: architecture, lookups, core, category, contract, forms, build sequence | Kept as the binder chapter map (v6.0) |
| $200 NPO minimum | Copilot A: per location auto. Copilot B: calc $125 → pay $200 | Excel: manual yellow statement line. Store `MinimumDonation`; do **not** auto-apply until Finance confirms |
| Location key | LocationCode indexed; examples `FB106` `PIT104` | Official spaced codes (`FB 106`). PIT 101 is two MyVenue rows. Compact codes are not unique aliases |
| Mini Melts | FB 113 / FB 113B in NPO template | Official FB 114 / FB 115 as of 9/14/26 |
| Invoice | PDF name `MM-DD-YY - TYPE - AP UNM - InvoiceNumber.pdf` | Invoice number `UNM-MMDDYY-SHORTCODE` is what AP uses |
| SUB | “vendor-specific contract rates” (correct) | Four buckets + tax strip + card fee 3% max + ice $3/bag |
| Event types | Six types | Add Baseball (`BB 101` exists) |
| Category class | Free-text `FOOD_NONALC` / `ALCOHOL` on tblCategoryMap | FK to `tblContractClass` (FOOD / NA_BEV / BEER / LIQUOR) |
| Import Center | Volume A form: Import MyVenue, Import Tips, status/count/exceptions | Alpha shell only; parsers are Volume B |
| Vendor form name | `frmVendorMaster` | Object `frmVendor`, caption Vendor Master |
| NPO math | Copilot B: Gross × one % | **Net** × 10% food/non-alc + 8% alcohol × AllocationPct |
| Assignments | Copilot B: vendor + location only | Posted `tblEventAssignment` with AllocationPct; staging `tblAssignmentImport` |
| ARVC SAP/BSS | Blank in NPO MASTER | 1013051 / 5487 on 12/01/25 PDF |

## NPO 9/5/26 proof totals (do not seed as settlements)

Assignment sales $54,718.50, donation $5,129.94, tips $3,421.74, payout $8,551.68. ARVC statement also had a $25 cook-fee bonus.

## SUB 12/01/25 proof totals (do not seed as settlements)

LAG check $1,639.33 invoice `UNM-120125-LAG`. SUG check $1,293.64 invoice `UNM-120125-SUG`. Event: MBB - NM HIGHLANDS.
