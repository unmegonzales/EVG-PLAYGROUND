# Red Rally — Canva layer pack

Vector layers for the Red Rally digital menu board. Canva's Magic Layers often fails on large photographic boards; these SVGs are small, outlined, and meant to be dropped in one section at a time.

## Board size

- **1920 × 480 px** (4:1 ribbon / menu board)
- Every file in `layers/` uses that same artboard with a **transparent background**
- Place each imported SVG at **X 0, Y 0** and they will stack

## Import order in Canva

Bottom → top:

1. `01-background.svg`
2. `02-grid-lines.svg`
3. `03-header-red-rally.svg`
4. `04-promo-4for4-redesign.svg` *(recommended)* **or** `04-promo-4for4-classic.svg`
5. `05-icon-hot-dog.svg`
6. `06-icon-pretzel.svg`
7. `07-icon-nachos.svg`
8. `08-icon-drinks.svg`
9. `09-footer-bar.svg`
10. `10-footer-cashless.svg`
11. `11-footer-payments.svg`
12. `12-footer-sponsors.svg`
13. `13-price-slots-editable-text.svg` *(optional; uses live text Canva can edit)*

`05–08` together are the same artwork as `05-08-icon-grid.svg` if you prefer one chunk instead of four.

## Cropped files

`cropped/` contains the same artwork with a tight viewBox. Use these when you want to place or scale a section freely instead of stacking full-board layers.

## 4 for $4 redesign

The original top-right block was a parallelogram with a giant 4, a stacked item list, and product photos. The redesign keeps the red / black / cyan system but:

- Drops the slanted photo dump
- Locks **4** + a red **$4** chip as the price hierarchy
- Puts the four combo items in a clean product rail
- Uses vector food instead of photos so the file stays tiny for Canva

If you want the older energy, import `04-promo-4for4-classic.svg` instead and hide the redesign.

## Production notes

- Headings are **converted to outlines**, so Canva will not require those fonts.
- Payment marks and sponsor wordmarks are **placeholders**. Swap in official Apple Pay, Google Pay, Venmo, Mastercard, Visa, American Express, Lobos, Bud Light, Michelob Ultra, and Levy brand files before this goes on a board.
- Leave the black field under each icon open for item names and prices. The optional price-slot layer is only a starting point.
- Do not import both promo files at once unless you are comparing them.

## Preview

Open `preview/preview.html` locally, or look at `preview/assembled.svg` / `preview/assembled.png`.

Headlines are outlined from Barlow Condensed, Anton, Great Vibes, and Pacifico (SIL Open Font License). The pretzel mark is adapted from Pictogrammers Material Design Icons (Apache 2.0).

Regenerate everything with:

```bash
python3 red-rally-layers/generate.py
```
