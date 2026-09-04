#!/usr/bin/env python3
"""Generate Canva-ready layered SVGs for the Red Rally digital menu board."""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
LAYERS = ROOT / "layers"
CROPPED = ROOT / "cropped"
PREVIEW = ROOT / "preview"
FONT_DIR = Path("/tmp/fonts")

W, H = 1920, 480
FOOTER_Y = 402
GRID_Y = 128

RED = "#E21B24"
RED_DEEP = "#B0121C"
BLACK = "#070707"
INK = "#111111"
WHITE = "#FFFFFF"
CYAN = "#5CE1E6"
CYAN_HOT = "#7AF6FF"
SLATE = "#1A1A1A"
MUTED = "#D7D7D7"

FONTS = {
    "rally": FONT_DIR / "BarlowCondensed-BlackItalic.ttf",
    "condensed": FONT_DIR / "BarlowCondensed-ExtraBoldItalic.ttf",
    "label": FONT_DIR / "BarlowCondensed-Bold.ttf",
    "anton": FONT_DIR / "Anton-Regular.ttf",
    "bebas": FONT_DIR / "BebasNeue-Regular.ttf",
    "oswald": FONT_DIR / "Oswald-Bold.ttf",
    "inter": Path("/usr/share/fonts/truetype/macos/Inter-Bold.ttf"),
    "inter_italic": Path("/usr/share/fonts/truetype/macos/Inter-BoldItalic.ttf"),
    "script": FONT_DIR / "GreatVibes-Regular.ttf",
    "script2": FONT_DIR / "Pacifico-Regular.ttf",
}


class FontDrawer:
    def __init__(self, path: Path):
        self.font = TTFont(path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]
        os2 = self.font["OS/2"]
        self.cap = getattr(os2, "sCapHeight", None) or 700
        self.asc = os2.sTypoAscender
        self.desc = os2.sTypoDescender

    def _advance(self, ch: str, size: float) -> float:
        gid = self.cmap.get(ord(ch))
        if gid is None:
            return size * 0.33
        return self.hmtx[gid][0] * (size / self.upm)

    def width(self, text: str, size: float, tracking: float = 0) -> float:
        if not text:
            return 0
        total = sum(self._advance(ch, size) for ch in text)
        return total + tracking * max(0, len(text) - 1)

    def path(self, text: str, x: float, y: float, size: float, tracking: float = 0) -> str:
        scale = size / self.upm
        pen_x = 0.0
        chunks: list[str] = []
        for i, ch in enumerate(text):
            gid = self.cmap.get(ord(ch))
            if gid is None:
                pen_x += size * 0.33
                continue
            svg_pen = SVGPathPen(self.glyph_set)
            transform = Transform().translate(x + pen_x, y).scale(scale, -scale)
            self.glyph_set[gid].draw(TransformPen(svg_pen, transform))
            d = compact_path(svg_pen.getCommands())
            if d:
                chunks.append(d)
            pen_x += self.hmtx[gid][0] * scale
            if i < len(text) - 1:
                pen_x += tracking
        return " ".join(chunks)


_FONT_CACHE: dict[str, FontDrawer] = {}


def font(name: str) -> FontDrawer:
    if name not in _FONT_CACHE:
        _FONT_CACHE[name] = FontDrawer(FONTS[name])
    return _FONT_CACHE[name]


def compact_path(d: str) -> str:
    def repl(match: re.Match[str]) -> str:
        value = float(match.group())
        if abs(value - round(value)) < 0.005:
            return str(int(round(value)))
        return f"{value:.2f}"

    return re.sub(r"-?\d+\.\d+", repl, d)


def path_el(d: str, fill: str, extra: str = "") -> str:
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def text_el(name: str, text: str, x: float, y: float, size: float, fill: str, tracking: float = 0, extra: str = "") -> str:
    d = font(name).path(text, x, y, size, tracking)
    if not d:
        return ""
    return path_el(d, fill, extra)


def line(x1: float, y1: float, x2: float, y2: float, color: str, width: float, cap: str = "square") -> str:
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="{cap}"/>'
    )


def rect(x: float, y: float, w: float, h: float, fill: str, extra: str = "") -> str:
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" {extra}/>'


def circle(cx: float, cy: float, r: float, fill: str, extra: str = "") -> str:
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" {extra}/>'


def svg_doc(body: str, width: int = W, height: int = H, view: str | None = None) -> str:
    view_box = view or f"0 0 {width} {height}"
    vw, vh = width, height
    if view:
        parts = view.split()
        vw, vh = float(parts[2]), float(parts[3])
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw:.0f}" height="{vh:.0f}" '
        f'viewBox="{view_box}" fill="none">\n{body}\n</svg>\n'
    )


def write_layer(name: str, body: str, crop: tuple[float, float, float, float] | None = None) -> None:
    LAYERS.mkdir(parents=True, exist_ok=True)
    CROPPED.mkdir(parents=True, exist_ok=True)
    (LAYERS / f"{name}.svg").write_text(svg_doc(body), encoding="utf-8")
    if crop:
        x, y, w, h = crop
        pad = 8
        vx, vy, vw, vh = x - pad, y - pad, w + pad * 2, h + pad * 2
        cropped_body = f'<g transform="translate({-vx:.2f} {-vy:.2f})">\n{body}\n</g>'
        (CROPPED / f"{name}.svg").write_text(
            svg_doc(cropped_body, width=int(vw), height=int(vh), view=f"0 0 {vw:.2f} {vh:.2f}"),
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------

def icon_hotdog(cx: float, cy: float, scale: float = 1.0, color: str = RED) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})" fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M-50 10c2 16 98 16 100 0" stroke-width="7"/>
  <path d="M-56 0c2-12 108-12 112 0 0 8-16 14-56 14S-56 8-56 0z" stroke-width="7"/>
  <path d="M-48 -6c4-16 92-16 96 0" stroke-width="7"/>
  <path d="M-30 -4c8 8 14-8 22 0s14-8 22 0 12-6 20 2" stroke-width="4.5"/>
</g>'''


def icon_pretzel(cx: float, cy: float, scale: float = 1.0, color: str = RED) -> str:
    # Pictogrammers Material Design Icons "pretzel", Apache 2.0.
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})">
  <g transform="scale(5.1) translate(-12 -12)">
    <path fill="{color}" fill-rule="evenodd" d="M5.15 15.84C3.81 14.27 3 12.23 3 10V9.97C3 7.22 5.25 5 8 5C9.64 5 11.09 5.79 12 7C12.91 5.79 14.37 5 16 5C18.76 5 21 7.24 21 10C21 12.23 20.19 14.27 18.85 15.84L20.21 17.2L18.79 18.61L17.39 17.21C15.89 18.33 14 19 12 19C10 19 8.11 18.33 6.61 17.21L5.21 18.61L3.79 17.2L5.15 15.84M15.96 15.77L12 11.82L8.04 15.77C9.17 16.55 10.53 17 12 17C13.47 17 14.83 16.55 15.96 15.77M11 10C11 8.34 9.65 7 8 7C6.34 7 5 8.34 5 10C5 11.68 5.59 13.21 6.57 14.42L11 10M17.43 14.42C18.41 13.21 19 11.68 19 10V10C19 8.33 17.65 7 16 7C14.35 7 13 8.34 13 10L17.43 14.42Z"/>
  </g>
</g>'''


def icon_nachos(cx: float, cy: float, scale: float = 1.0, color: str = RED) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})" fill="none" stroke="{color}" stroke-width="6.2" stroke-linejoin="round" stroke-linecap="round">
  <path d="M-40 30 L-6 -38 L26 30z"/>
  <path d="M-6 32 L28 -34 L58 32z"/>
  <path d="M-58 34 L-30 -16 L4 34z"/>
  <path d="M-24 10c8 10 20 12 30 3"/>
  <path d="M10 12c8 8 18 10 26 1"/>
  <circle cx="-18" cy="18" r="3.1" fill="{color}" stroke="none"/>
  <circle cx="8" cy="20" r="3.1" fill="{color}" stroke="none"/>
  <circle cx="30" cy="18" r="3.1" fill="{color}" stroke="none"/>
</g>'''


def icon_drinks(cx: float, cy: float, scale: float = 1.0, color: str = RED) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})" fill="none" stroke="{color}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">
  <ellipse cx="-24" cy="-16" rx="18" ry="6"/>
  <path d="M-40 -16l6 54c1 8 8 12 10 12h8c2 0 9-4 10-12l6-54"/>
  <path d="M-12 -16l8 -20"/>
  <ellipse cx="22" cy="-10" rx="18" ry="6"/>
  <path d="M6 -10l6 50c1 8 8 12 10 12h8c2 0 9-4 10-12l6-50"/>
  <path d="M34 -10l8 -18"/>
  <path d="M-32 8h16M14 14h16"/>
</g>'''


def food_soda(cx: float, cy: float, scale: float = 1.0) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})">
  <path d="M-16 -8h32l-4 46c-1 8-6 10-12 10s-11-2-12-10z" fill="#1E6BFF"/>
  <path d="M-16 -8h32l-1.2 12h-29.6z" fill="#0B4AD6"/>
  <rect x="-18" y="-16" width="36" height="10" rx="3" fill="#EEF3FF"/>
  <rect x="-12" y="-14" width="24" height="4" rx="2" fill="#C9D7F5"/>
  <path d="M8 -16l10 -18" stroke="#E21B24" stroke-width="4" stroke-linecap="round"/>
  <circle cx="18" cy="-36" r="3.2" fill="#E21B24"/>
  <path d="M-6 8c4-6 8 6 12 0" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity="0.7"/>
  <circle cx="-8" cy="22" r="2.2" fill="#7AF6FF" opacity="0.8"/>
</g>'''


def food_dog(cx: float, cy: float, scale: float = 1.0) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})">
  <path d="M-30 6c2 12 58 12 60 0 1-7-8-12-30-12s-31 5-30 12z" fill="#F2C56D"/>
  <path d="M-32 -2c2-11 62-11 64 0 1 6-10 10-32 10s-33-4-32-10z" fill="#E7B45A"/>
  <path d="M-34 -1c1-8 68-8 70 2-2 7-12 9-35 9s-36-3-35-11z" fill="#C24532"/>
  <path d="M-22 -6c8 8 12-7 20 1s11-7 18 1 10-6 16 2" fill="none" stroke="#F5D447" stroke-width="3.2" stroke-linecap="round"/>
</g>'''


def food_popcorn(cx: float, cy: float, scale: float = 1.0) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})">
  <path d="M-18 6h36l-4 28h-28z" fill="#F2C400"/>
  <path d="M-14 6h6l-4 28h-6z" fill="#FFFFFF"/>
  <path d="M-2 6h6l-4 28h-6z" fill="#FFFFFF"/>
  <path d="M10 6h6l-4 28h-6z" fill="#FFFFFF"/>
  <circle cx="-12" cy="-2" r="8" fill="#FFF4C2"/>
  <circle cx="-2" cy="-10" r="9" fill="#FFE680"/>
  <circle cx="10" cy="-4" r="8.5" fill="#FFF1A8"/>
  <circle cx="2" cy="2" r="7" fill="#FFE07A"/>
  <circle cx="-14" cy="8" r="6" fill="#FFF7D1"/>
  <circle cx="14" cy="6" r="6.5" fill="#FFE38F"/>
</g>'''


def food_water(cx: float, cy: float, scale: float = 1.0) -> str:
    return f'''<g transform="translate({cx:.2f} {cy:.2f}) scale({scale:.3f})">
  <rect x="-7" y="-28" width="14" height="8" rx="2" fill="#3AA0E8"/>
  <rect x="-5" y="-22" width="10" height="6" fill="#9ED6F5"/>
  <path d="M-11 -16c-2 4-3 10-3 18 0 16 4 28 14 28s14-12 14-28c0-8-1-14-3-18z" fill="#D7F2FF"/>
  <path d="M-10 -8c-1 4-2 10-2 16 0 14 3.2 24 12 24 1.4 0 2.7-.2 3.8-.6C-2 26-6 16-6 4c0-6 1-10 2-14z" fill="#8FD4F8" opacity="0.85"/>
  <rect x="-9" y="2" width="18" height="10" rx="1.5" fill="#1A7FBF"/>
</g>'''


def payment_badge(cx: float, cy: float, kind: str) -> str:
    r = 18
    body = [circle(cx, cy, r, WHITE), circle(cx, cy, r - 1.1, "#0E0E0E")]
    if kind == "apple":
        body.append(f'''<g transform="translate({cx:.2f} {cy:.2f})">
          <path d="M4.2-8.6c1.1 0 2.4.7 3.1 1.7-2.7 1.6-2.3 5.7.4 6.9-.7 1.5-1.7 3-3 3-1.1 0-1.5-.7-2.9-.7s-1.8.7-2.9.7c-1.4 0-2.5-1.7-3.3-3.2-1.6-3.1-1.3-7.1.7-9.2 1.1-1.1 2.6-1.8 3.9-1.8 1.2 0 2.4.6 3 1.6z" fill="#fff"/>
          <path d="M3.6-9.4c.7-1.1 1.9-1.8 2.9-1.8.1 1.3-.5 2.6-1.4 3.4-1 .9-2.2 1.4-3.1 1.3 0-1.1.5-2.1 1.6-2.9z" fill="#fff"/>
        </g>''')
    elif kind == "gpay":
        body.append(text_el("inter", "G", cx - 6.2, cy + 6.2, 16.5, WHITE))
    elif kind == "venmo":
        body.append(text_el("inter_italic", "V", cx - 6.6, cy + 6.6, 17.5, "#2C9BEA"))
    elif kind == "mc":
        body.append(circle(cx - 5.2, cy, 7.4, "#EB5A3C"))
        body.append(circle(cx + 5.2, cy, 7.4, "#F5C145"))
        body.append(f'<path d="M{cx-1:.2f},{cy-7.2:.2f} a7.4,7.4 0 0 1 0,14.8 a7.4,7.4 0 0 1 0,-14.8" fill="#F0893D"/>')
    elif kind == "visa":
        body.append(text_el("condensed", "VISA", cx - 12.2, cy + 5.2, 12, "#1A6CFF", tracking=0.4))
    elif kind == "amex":
        body.append(rect(cx - 13, cy - 7.5, 26, 15, "#2E77BC"))
        body.append(text_el("label", "AMEX", cx - 11.4, cy + 4.4, 10.5, WHITE, tracking=0.2))
    return f'<g id="pay-{kind}">' + "".join(body) + "</g>"


# ---------------------------------------------------------------------------
# Layers
# ---------------------------------------------------------------------------

def layer_background() -> str:
    return f'<g id="background">{rect(0, 0, W, H, BLACK)}</g>'


def layer_grid() -> str:
    parts = ['<g id="grid-lines">']
    parts.append(line(0, GRID_Y, W, GRID_Y, CYAN, 2))
    for x in (480, 960, 1440):
        parts.append(line(x, GRID_Y, x, FOOTER_Y, WHITE, 1.25))
    parts.append("</g>")
    return "\n".join(parts)


def layer_header() -> str:
    fnt = font("rally")
    size = 72
    label = "RED RALLY"
    tw = fnt.width(label, size, tracking=1.6)
    x = 48
    baseline = 86
    rule_w = tw
    return f'''<g id="header-red-rally">
  {line(x, 34, x + rule_w, 34, CYAN, 2.5)}
  {text_el("rally", label, x, baseline, size, RED, tracking=1.6)}
  {line(x, 102, x + rule_w, 102, CYAN, 2.5)}
</g>'''


def layer_promo_classic() -> str:
    # Parallelogram promo, faithful to the original energy.
    x0, y0, w, h = 1010, 10, 898, 112
    skew = 28
    pts = f"{x0+skew},{y0} {x0+w},{y0} {x0+w-10},{y0+h} {x0},{y0+h}"
    stripe = f"{x0+skew},{y0} {x0+skew+18},{y0} {x0+18},{y0+h} {x0},{y0+h}"
    items = [("16 OZ SODA", food_soda), ("LONG DOG", food_dog), ("POPCORN", food_popcorn), ("16 OZ WATER", food_water)]
    item_block = []
    for i, (label, draw) in enumerate(items):
        iy = 38 + i * 18
        item_block.append(text_el("label", label, 1248, iy, 13, WHITE, tracking=1.1))
    foods = [
        food_soda(1588, 64, 0.92),
        food_dog(1668, 70, 1.05),
        food_popcorn(1752, 62, 0.95),
        food_water(1832, 62, 0.95),
    ]
    return f'''<g id="promo-4for4-classic">
  <polygon points="{pts}" fill="#121212"/>
  <polygon points="{stripe}" fill="{RED}"/>
  {text_el("anton", "4", 1058, 104, 118, WHITE)}
  {text_el("rally", "FOR $4", 1146, 58, 34, WHITE, tracking=1.2)}
  {"".join(item_block)}
  {"".join(foods)}
  {rect(1010, 122, 910, 4, RED)}
</g>'''


def layer_promo_redesign() -> str:
    x, y, w, h = 992, 8, 916, 116
    cols = 4
    rail_x = x + 236
    rail_w = w - 248
    col_w = rail_w / cols
    labels = [
        ("16 OZ", "SODA"),
        ("LONG", "DOG"),
        ("FRESH", "POPCORN"),
        ("16 OZ", "WATER"),
    ]
    icons = [food_soda, food_dog, food_popcorn, food_water]
    cells = []
    for i, ((top, bot), draw) in enumerate(zip(labels, icons)):
        cx = rail_x + col_w * i + col_w / 2
        if i:
            cells.append(
                f'<line x1="{rail_x + col_w * i:.2f}" y1="{y + 18:.2f}" x2="{rail_x + col_w * i:.2f}" y2="{y + h - 16:.2f}" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>'
            )
        cells.append(draw(cx, y + 44, 0.92 if i != 1 else 1.02))
        tw = font("label").width(top, 11, tracking=1.2)
        cells.append(text_el("label", top, cx - tw / 2, y + 84, 11, CYAN, tracking=1.2))
        tw2 = font("label").width(bot, 14, tracking=0.8)
        cells.append(text_el("label", bot, cx - tw2 / 2, y + 102, 14, WHITE, tracking=0.8))

    combo_w = font("label").width("COMBO", 11, tracking=2.4)
    return f'''<g id="promo-4for4-redesign">
  {rect(x, y, w, h, SLATE)}
  {rect(x, y, 8, h, RED)}
  {rect(x, y, w, 2, CYAN)}
  {rect(x, y + h - 3, w, 3, RED)}
  {text_el("label", "COMBO", x + 28, y + 24, 11, CYAN, tracking=2.4)}
  {line(x + 28, y + 30, x + 28 + combo_w, y + 30, CYAN, 1)}
  {text_el("anton", "4", x + 22, y + 108, 92, WHITE)}
  {text_el("rally", "FOR", x + 108, y + 64, 22, MUTED, tracking=1.8)}
  {rect(x + 108, y + 74, 86, 28, RED)}
  {text_el("rally", "$4", x + 124, y + 97, 26, WHITE, tracking=0.6)}
  {line(x + 214, y + 18, x + 214, y + h - 14, CYAN, 1.5)}
  {"".join(cells)}
</g>'''


def layer_icon(name: str, drawer, col: int) -> str:
    cx = 240 + col * 480
    cy = 208
    return f'<g id="icon-{name}">{drawer(cx, cy, 1.18)}</g>'


def layer_icon_grid() -> str:
    return f'''<g id="icon-grid">
  {icon_hotdog(240, 208, 1.18)}
  {icon_pretzel(720, 208, 1.18)}
  {icon_nachos(1200, 208, 1.18)}
  {icon_drinks(1680, 208, 1.18)}
</g>'''


def layer_footer_bar() -> str:
    return f'<g id="footer-bar">{rect(0, FOOTER_Y, W, H - FOOTER_Y, RED)}</g>'


def layer_footer_cashless() -> str:
    return f'''<g id="footer-cashless">
  {text_el("rally", "CASHLESS VENUE", 36, 456, 36, WHITE, tracking=1.4)}
</g>'''


def layer_footer_payments() -> str:
    start = 412
    kinds = ["apple", "gpay", "venmo", "mc", "visa", "amex"]
    badges = []
    for i, kind in enumerate(kinds):
        badges.append(payment_badge(start + i * 48, 441, kind))
    return f'<g id="footer-payments">{"".join(badges)}</g>'


def layer_footer_sponsors() -> str:
    # Wordmark wells — swap with official brand files in Canva for production.
    cy = 441
    parts = ['<g id="footer-sponsors">']
    parts.append(line(1396, 418, 1396, 464, WHITE, 1.4))
    parts.append(text_el("script2", "Lobos", 1420, 458, 40, WHITE))
    for cx, top, bot in ((1638, "BUD", "LIGHT"), (1748, "MICHELOB", "ULTRA")):
        parts.append(circle(cx, cy, 26, WHITE))
        parts.append(circle(cx, cy, 23.6, RED))
        tw = font("label").width(top, 9.5, tracking=0.7)
        parts.append(text_el("label", top, cx - tw / 2, cy - 1, 9.5, WHITE, tracking=0.7))
        tw = font("label").width(bot, 9.5, tracking=0.7)
        parts.append(text_el("label", bot, cx - tw / 2, cy + 12, 9.5, WHITE, tracking=0.7))
    parts.append(text_el("script", "Levy", 1810, 458, 42, WHITE))
    parts.append("</g>")
    return "".join(parts)


def layer_price_slots() -> str:
    # Editable SVG text (not outlined) so Canva can convert these to type.
    labels = ["ITEM / PRICE", "ITEM / PRICE", "ITEM / PRICE", "ITEM / PRICE"]
    parts = [
        '<g id="price-slots">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-weight:800;letter-spacing:.12em;text-anchor:middle;fill:#ffffff;}</style>",
    ]
    for i, label in enumerate(labels):
        cx = 240 + i * 480
        parts.append(f'<text x="{cx}" y="318" font-size="15" opacity="0.42">{label}</text>')
        parts.append(f'<text x="{cx}" y="358" font-size="28">$ --</text>')
    parts.append("</g>")
    return "\n".join(parts)


def preview_html(files: list[str]) -> str:
    checks = []
    images = []
    for i, name in enumerate(files):
        checked = "checked"
        checks.append(
            f'<label><input type="checkbox" data-layer="{name}" {checked}> {name}</label>'
        )
        images.append(
            f'<img src="../layers/{name}.svg" data-layer="{name}" alt="{name}">'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Red Rally — layered SVG preview</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; font-family: Arial, sans-serif; background: #111; color: #eee; }}
    header {{ padding: 20px 24px 8px; }}
    h1 {{ margin: 0 0 8px; font-size: 22px; letter-spacing: .04em; text-transform: uppercase; }}
    p {{ margin: 0 0 16px; color: #bbb; max-width: 820px; line-height: 1.5; }}
    .board-wrap {{ margin: 0 24px 24px; background: #000; outline: 1px solid #333; }}
    .board {{ position: relative; width: min(1920px, 100%); aspect-ratio: 1920 / 480; }}
    .board img {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .toggles {{ display: flex; flex-wrap: wrap; gap: 10px 16px; padding: 0 24px 24px; }}
    label {{ font-size: 13px; }}
  </style>
</head>
<body>
  <header>
    <h1>Red Rally layer stack</h1>
    <p>Toggle layers to preview the Canva inlay order. Import every file from <code>layers/</code> onto a 1920×480 Canva design at position 0,0. Use the redesign promo instead of the classic promo unless you want the original lockup.</p>
  </header>
  <div class="board-wrap"><div class="board" id="board">
    {"".join(images)}
  </div></div>
  <div class="toggles">{"".join(checks)}</div>
  <script>
    document.querySelectorAll("input[type=checkbox]").forEach((box) => {{
      box.addEventListener("change", () => {{
        document.querySelectorAll("img[data-layer='" + box.dataset.layer + "']").forEach((img) => {{
          img.style.display = box.checked ? "block" : "none";
        }});
      }});
    }});
  </script>
</body>
</html>
"""


def readme() -> str:
    return """# Red Rally — Canva layer pack

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
"""


def assemble(bodies: list[str]) -> str:
    return svg_doc("\n".join(bodies))


def main() -> None:
    LAYERS.mkdir(parents=True, exist_ok=True)
    CROPPED.mkdir(parents=True, exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)

    bg = layer_background()
    grid = layer_grid()
    header = layer_header()
    promo_classic = layer_promo_classic()
    promo_redesign = layer_promo_redesign()
    hotdog = layer_icon("hot-dog", icon_hotdog, 0)
    pretzel = layer_icon("pretzel", icon_pretzel, 1)
    nachos = layer_icon("nachos", icon_nachos, 2)
    drinks = layer_icon("drinks", icon_drinks, 3)
    icons = layer_icon_grid()
    footer = layer_footer_bar()
    cashless = layer_footer_cashless()
    payments = layer_footer_payments()
    sponsors = layer_footer_sponsors()
    prices = layer_price_slots()

    write_layer("01-background", bg, crop=None)
    write_layer("02-grid-lines", grid, crop=(0, GRID_Y, W, FOOTER_Y - GRID_Y))
    write_layer("03-header-red-rally", header, crop=(40, 22, 420, 92))
    write_layer("04-promo-4for4-classic", promo_classic, crop=(1000, 8, 920, 122))
    write_layer("04-promo-4for4-redesign", promo_redesign, crop=(992, 8, 916, 116))
    write_layer("05-icon-hot-dog", hotdog, crop=(120, 140, 240, 140))
    write_layer("06-icon-pretzel", pretzel, crop=(600, 140, 240, 140))
    write_layer("07-icon-nachos", nachos, crop=(1080, 140, 240, 140))
    write_layer("08-icon-drinks", drinks, crop=(1560, 140, 240, 140))
    write_layer("05-08-icon-grid", icons, crop=(0, 140, W, 160))
    write_layer("09-footer-bar", footer, crop=(0, FOOTER_Y, W, H - FOOTER_Y))
    write_layer("10-footer-cashless", cashless, crop=(28, 414, 400, 54))
    write_layer("11-footer-payments", payments, crop=(400, 416, 300, 52))
    write_layer("12-footer-sponsors", sponsors, crop=(1388, 408, 520, 68))
    write_layer("13-price-slots-editable-text", prices, crop=(0, 290, W, 90))

    assembled = assemble(
        [bg, grid, header, promo_redesign, icons, footer, cashless, payments, sponsors, prices]
    )
    (PREVIEW / "assembled.svg").write_text(assembled, encoding="utf-8")
    classic_assembled = assemble(
        [bg, grid, header, promo_classic, icons, footer, cashless, payments, sponsors]
    )
    (PREVIEW / "assembled-classic.svg").write_text(classic_assembled, encoding="utf-8")

    stack = [
        "01-background",
        "02-grid-lines",
        "03-header-red-rally",
        "04-promo-4for4-redesign",
        "05-icon-hot-dog",
        "06-icon-pretzel",
        "07-icon-nachos",
        "08-icon-drinks",
        "09-footer-bar",
        "10-footer-cashless",
        "11-footer-payments",
        "12-footer-sponsors",
        "13-price-slots-editable-text",
    ]
    (PREVIEW / "preview.html").write_text(preview_html(stack), encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")

    for name in ("assembled.svg", "assembled-classic.svg"):
        src = PREVIEW / name
        dest = PREVIEW / name.replace(".svg", ".png")
        try:
            subprocess.run(
                ["rsvg-convert", "-w", "1920", "-h", "480", str(src), "-o", str(dest)],
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    zip_path = ROOT / "red-rally-canva-layers.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for folder in (LAYERS, CROPPED, PREVIEW):
            for path in sorted(folder.rglob("*")):
                if path.is_file() and path.suffix.lower() in {".svg", ".html", ".md", ".png", ".txt"}:
                    if path.parent.name == "png":
                        continue
                    zf.write(path, path.relative_to(ROOT.parent))
        zf.write(ROOT / "README.md", "red-rally-layers/README.md")
        zf.write(ROOT / "generate.py", "red-rally-layers/generate.py")

    print(f"Wrote layers to {LAYERS}")
    print(f"Zip: {zip_path} ({zip_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
