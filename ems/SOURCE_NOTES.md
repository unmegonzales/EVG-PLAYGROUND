# Source notes

These notes record what was taken from live UNM files versus Copilot chat. The Access generator should treat live files as truth.

## Files ingested

| File | Role |
|---|---|
| EMS Project Manager Action Plan | Construction order, FE/BE split, alpha definition, Copilot Volume A sketch |
| NPO Payout Vendor Template final-V4 | Live NPO engine: assignment, category map, tips, donation formula, vendor aliases |
| MyVenue Location List All UNM 09-14-26 | 81-location master |
| MSR Location Payout CSV 09-05-26 | Nested MyVenue export shape and product codes |
| SUB AP UNM REMIT NAME 12-01-25.xlsx | SUB engine, LAG/SUG identity, rates, expenses, invoice numbers |
| SUB Sugar Shivers PDF 12-01-25 | Print layout + GL split for SUB |
| NPO ARVC PDF 12-01-25 | Older NPO print layout; filled ARVC SAP/BSS |

## Copilot vs live

| Topic | Copilot said | Live files show |
|---|---|---|
| $200 NPO minimum | Automatic per assigned location | Manual statement line; Excel donation formula does not use it |
| Location key | LocationCode unique | PIT 101 is two MyVenue rows |
| Mini Melts | FB 113 / FB 113B in NPO template | Official FB 114 / FB 115 as of 9/14/26 |
| Invoice | PDF name `MM-DD-YY - TYPE - AP UNM - InvoiceNumber.pdf` | Invoice number `UNM-MMDDYY-SHORTCODE` is what AP uses |
| SUB | “vendor-specific contract rates” (correct) | Four buckets + tax strip + card fee 3% max + ice $3/bag |
| Event types | Six types | Add Baseball (`BB 101` exists) |
| ARVC SAP/BSS | Blank in NPO MASTER | 1013051 / 5487 on 12/01/25 PDF |

## NPO 9/5/26 proof totals (do not seed as settlements)

Assignment sales $54,718.50, donation $5,129.94, tips $3,421.74, payout $8,551.68. ARVC statement also had a $25 cook-fee bonus.

## SUB 12/01/25 proof totals (do not seed as settlements)

LAG check $1,639.33 invoice `UNM-120125-LAG`. SUG check $1,293.64 invoice `UNM-120125-SUG`. Event: MBB - NM HIGHLANDS.
