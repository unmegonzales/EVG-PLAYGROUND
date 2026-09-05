# Adobe / self-managed editing

## What to open for edits

| File | Adobe app | Editable text? | Best for |
| --- | --- | --- | --- |
| `exports/Zia-Two-VIP-Beverage-Menu-editable.svg` | **Illustrator** | Yes (live text) | Price / copy / layout changes |
| `exports/Zia-Two-VIP-Beverage-Menu.pdf` | Acrobat / Illustrator | Limited | Print / share / proof |
| `index.html` + `styles.css` | Browser | Yes (code) | Regenerating the look |

## Recommended Adobe workflow

1. Open `exports/Zia-Two-VIP-Beverage-Menu-editable.svg` in **Adobe Illustrator**.
2. Install (or accept substitutes for) **Cinzel**, **Cormorant Garamond**, and **Outfit**.
3. **File → Save As → Adobe Illustrator (*.ai)** — that becomes your native working file.
4. Edit prices/text directly; export PDF/PNG when ready for print.

## Important

- The browser **PDF is print-ready**, not an ideal Adobe master. Illustrator can open it, but text often breaks into fragments.
- Native **`.ai`** cannot be authored here without Illustrator; the **SVG is the Adobe-acceptable editable master** we can ship from this environment.
- After your first Save As `.ai`, use that `.ai` for all future self-managed changes.
