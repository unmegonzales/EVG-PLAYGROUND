#!/usr/bin/env python3
"""Generate a quiet UNM Lobos F&B menu board base for Canva overlays.

Designed as a calm printed-menu plate: light neutral field, thin brand
edge accents only, wide open space for headers/items. No stadium lights,
heavy motion graphics, or dense pattern fills.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

# Brand colors
CHERRY = (186, 12, 47)
SILVER = (167, 168, 170)
METAL = (74, 79, 85)
TURQUOISE = (0, 168, 181)
WHITE = (255, 255, 255)
LIGHT = (244, 244, 246)
# Slightly softer field than pure #F4F4F6 for print warmth
FIELD = (246, 246, 248)


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def draw_quiet_board(w: int, h: int) -> Image.Image:
    """
    Layout (inspired by prior Stadium Sips core, simplified further):

      [ thin cherry top bar ]
      [ turquoise hairline  ]
      [ soft header reserve — empty for Canva brand/title ]
      [ open 3-column content field ]
      [ thin silver bottom bar + cherry corner ticks ]
    """
    # Flat light field — no playbook/chevron wash (prior year felt too busy in print)
    img = Image.new("RGB", (w, h), FIELD)
    draw = ImageDraw.Draw(img)

    # --- Top brand frame (thin, not a heavy ribbon stack) ---
    top_bar = max(18, h // 48)
    draw.rectangle([0, 0, w, top_bar], fill=CHERRY)

    hair = max(3, h // 220)
    draw.rectangle([0, top_bar, w, top_bar + hair], fill=TURQUOISE)

    # Soft white header reserve (empty — Canva places Lobos / location title here)
    header_bottom = int(h * 0.22)
    # Gentle fade from white into field so header zone reads cleanly
    for i in range(header_bottom - top_bar - hair):
        t = i / max(1, header_bottom - top_bar - hair - 1)
        y = top_bar + hair + i
        # white → field
        c = mix(WHITE, FIELD, t * t)
        draw.line([(0, y), (w, y)], fill=c)

    # Thin silver side rails (edge only — keep content open)
    rail = max(10, w // 280)
    draw.rectangle([0, top_bar + hair, rail, h], fill=mix(SILVER, FIELD, 0.35))
    draw.rectangle([w - rail, top_bar + hair, w, h], fill=mix(SILVER, FIELD, 0.35))

    # Inner content breathing margin markers (corners only, not frames)
    margin_x = int(w * 0.04)
    margin_y_top = int(h * 0.26)
    margin_y_bot = int(h * 0.90)
    tick = max(28, w // 90)
    tick_h = max(4, h // 200)
    # Four corner ticks in cherry — subtle alignment aids, not decoration clutter
    corners = [
        (margin_x, margin_y_top),
        (w - margin_x - tick, margin_y_top),
        (margin_x, margin_y_bot),
        (w - margin_x - tick, margin_y_bot),
    ]
    for cx, cy in corners:
        draw.rectangle([cx, cy, cx + tick, cy + tick_h], fill=mix(CHERRY, FIELD, 0.55))

    # Extremely faint 3-column guides (Canva-friendly; nearly invisible in print)
    # Columns align under a typical concessions triptych: drinks | snacks | beer
    guide = mix(FIELD, SILVER, 0.22)
    col1 = int(w * 0.345)
    col2 = int(w * 0.655)
    guide_top = int(h * 0.30)
    guide_bot = int(h * 0.86)
    draw.line([(col1, guide_top), (col1, guide_bot)], fill=guide, width=1)
    draw.line([(col2, guide_top), (col2, guide_bot)], fill=guide, width=1)

    # Bottom edge: slim silver bar + cherry end caps
    bot = max(12, h // 70)
    draw.rectangle([0, h - bot, w, h], fill=SILVER)
    cap = max(120, w // 18)
    draw.rectangle([0, h - bot, cap, h], fill=CHERRY)
    draw.rectangle([w - cap, h - bot, w, h], fill=CHERRY)
    # Tiny turquoise ticks on bottom bar
    draw.rectangle([cap, h - bot, cap + max(8, w // 200), h], fill=TURQUOISE)
    draw.rectangle([w - cap - max(8, w // 200), h - bot, w - cap, h], fill=TURQUOISE)

    return img.convert("RGB")


def create_svg(out_path: Path, w: int = 3600, h: int = 1200) -> None:
    top_bar = max(18, h // 48)
    hair = max(3, h // 220)
    header_bottom = int(h * 0.22)
    rail = max(10, w // 280)
    bot = max(12, h // 70)
    cap = max(120, w // 18)
    margin_x = int(w * 0.04)
    margin_y_top = int(h * 0.26)
    margin_y_bot = int(h * 0.90)
    tick = max(28, w // 90)
    tick_h = max(4, h // 200)
    col1 = int(w * 0.345)
    col2 = int(w * 0.655)
    guide_top = int(h * 0.30)
    guide_bot = int(h * 0.86)
    turquoise_tick = max(8, w // 200)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  <title>UNM Lobos F&amp;B Menu Background — Quiet Core</title>
  <desc>Calm Canva-ready board plate. Light field, thin brand accents, open columns for overlay text.</desc>

  <!-- Field (flat — no pattern wash for print clarity) -->
  <rect width="{w}" height="{h}" fill="#F6F6F8"/>

  <!-- Top brand frame -->
  <rect x="0" y="0" width="{w}" height="{top_bar}" fill="#BA0C2F"/>
  <rect x="0" y="{top_bar}" width="{w}" height="{hair}" fill="#00A8B5"/>

  <!-- Soft header reserve -->
  <defs>
    <linearGradient id="headerFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F6F6F8"/>
    </linearGradient>
  </defs>
  <rect x="0" y="{top_bar + hair}" width="{w}" height="{header_bottom - top_bar - hair}" fill="url(#headerFade)"/>

  <!-- Side rails -->
  <rect x="0" y="{top_bar + hair}" width="{rail}" height="{h - top_bar - hair}" fill="#D6D7D9"/>
  <rect x="{w - rail}" y="{top_bar + hair}" width="{rail}" height="{h - top_bar - hair}" fill="#D6D7D9"/>

  <!-- Corner ticks (alignment aids) -->
  <rect x="{margin_x}" y="{margin_y_top}" width="{tick}" height="{tick_h}" fill="#D98898"/>
  <rect x="{w - margin_x - tick}" y="{margin_y_top}" width="{tick}" height="{tick_h}" fill="#D98898"/>
  <rect x="{margin_x}" y="{margin_y_bot}" width="{tick}" height="{tick_h}" fill="#D98898"/>
  <rect x="{w - margin_x - tick}" y="{margin_y_bot}" width="{tick}" height="{tick_h}" fill="#D98898"/>

  <!-- Faint 3-column guides -->
  <line x1="{col1}" y1="{guide_top}" x2="{col1}" y2="{guide_bot}" stroke="#A7A8AA" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="{col2}" y1="{guide_top}" x2="{col2}" y2="{guide_bot}" stroke="#A7A8AA" stroke-opacity="0.18" stroke-width="1"/>

  <!-- Bottom edge -->
  <rect x="0" y="{h - bot}" width="{w}" height="{bot}" fill="#A7A8AA"/>
  <rect x="0" y="{h - bot}" width="{cap}" height="{bot}" fill="#BA0C2F"/>
  <rect x="{w - cap}" y="{h - bot}" width="{cap}" height="{bot}" fill="#BA0C2F"/>
  <rect x="{cap}" y="{h - bot}" width="{turquoise_tick}" height="{bot}" fill="#00A8B5"/>
  <rect x="{w - cap - turquoise_tick}" y="{h - bot}" width="{turquoise_tick}" height="{bot}" fill="#00A8B5"/>
</svg>
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg)
    print(f"Wrote {out_path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    # Primary quiet cores
    board_3x1 = draw_quiet_board(3600, 1200)
    board_3x1.save(assets / "unm-menu-bg-quiet-core.png", "PNG", optimize=True)
    print("Wrote", assets / "unm-menu-bg-quiet-core.png", "(3600x1200)")

    board_16x3 = draw_quiet_board(4800, 900)
    board_16x3.save(assets / "unm-menu-bg-quiet-core-16x3.png", "PNG", optimize=True)
    print("Wrote", assets / "unm-menu-bg-quiet-core-16x3.png", "(4800x900)")

    create_svg(assets / "unm-menu-bg-quiet-core.svg", 3600, 1200)
    create_svg(assets / "unm-menu-bg-quiet-core-16x3.svg", 4800, 900)

    # Also overwrite "primary" athletic filenames with quiet core so Canva import path is obvious
    # Keep prior athletic renders as *-athletic-* for optional high-energy use.
    board_3x1.save(assets / "unm-menu-bg-canva-base.png", "PNG", optimize=True)
    print("Wrote", assets / "unm-menu-bg-canva-base.png", "(primary Canva import)")


if __name__ == "__main__":
    main()
