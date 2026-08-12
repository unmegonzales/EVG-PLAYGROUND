#!/usr/bin/env python3
"""Generate UNM Lobos F&B menu background — Athletic Motion (Idea 1)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# Brand colors
CHERRY = (186, 12, 47)
SILVER = (167, 168, 170)
METAL = (74, 79, 85)
TURQUOISE = (0, 168, 181)
WHITE = (255, 255, 255)
LIGHT = (244, 244, 246)
DARK = (18, 20, 24)
DARK_SOFT = (32, 36, 42)
NIGHT = (10, 12, 16)

W, H = 3600, 1200  # 3:1 ultra-wide


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )


def vertical_gradient(draw: ImageDraw.ImageDraw, box, top, bottom, steps=120):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        y_a = int(lerp(y0, y1, t))
        y_b = int(lerp(y0, y1, (i + 1) / (steps - 1))) + 1
        draw.rectangle([x0, y_a, x1, y_b], fill=mix(top, bottom, t))


def horizontal_gradient(draw: ImageDraw.ImageDraw, box, left, right, steps=160):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        x_a = int(lerp(x0, x1, t))
        x_b = int(lerp(x0, x1, (i + 1) / (steps - 1))) + 1
        draw.rectangle([x_a, y0, x_b, y1], fill=mix(left, right, t))


def soft_ellipse(base: Image.Image, cx: int, cy: int, rx: int, ry: int, color, alpha: int):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(*color, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=max(rx, ry) // 5))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def draw_angled_band(draw: ImageDraw.ImageDraw, x, y, w, h, skew, fill):
    """Parallelogram band: skew is horizontal offset of top vs bottom."""
    pts = [
        (x + skew, y),
        (x + w + skew, y),
        (x + w, y + h),
        (x, y + h),
    ]
    draw.polygon(pts, fill=fill)


def create_png(out_path: Path) -> None:
    img = Image.new("RGBA", (W, H), (*DARK, 255))
    draw = ImageDraw.Draw(img)

    # Base stadium night field
    vertical_gradient(draw, (0, 0, W, H), NIGHT, DARK_SOFT, steps=180)

    # Upper stadium atmosphere with cherry wash
    for i in range(100):
        t = i / 99
        y0 = int(lerp(0, 380, t))
        y1 = int(lerp(0, 380, (i + 1) / 99)) + 1
        c = mix(NIGHT, mix(CHERRY, DARK, 0.55), t * 0.85)
        draw.rectangle([0, y0, W, y1], fill=c)

    # Left cherry power block
    draw.polygon(
        [
            (0, 0),
            (620, 0),
            (420, H),
            (0, H),
        ],
        fill=CHERRY,
    )

    # Nested cherry motion bars
    draw.polygon([(80, 0), (280, 0), (120, H), (-80, H)], fill=mix(CHERRY, (120, 8, 30), 0.35))
    draw.polygon([(200, 0), (340, 0), (180, H), (40, H)], fill=mix(CHERRY, WHITE, 0.08))

    # Silver angled motion graphics (left)
    for i, ox in enumerate([380, 460, 540]):
        shade = mix(SILVER, METAL, i * 0.25)
        draw.polygon(
            [
                (ox, -40),
                (ox + 90, -40),
                (ox - 160, H + 40),
                (ox - 250, H + 40),
            ],
            fill=shade,
        )

    # Turquoise electric accent line (left)
    draw.polygon(
        [
            (500, -20),
            (512, -20),
            (300, H + 20),
            (288, H + 20),
        ],
        fill=TURQUOISE,
    )

    # Right metallic panel with fade
    for i in range(120):
        t = i / 119
        x0 = int(lerp(W - 520, W, t))
        x1 = int(lerp(W - 520, W, (i + 1) / 119)) + 1
        a = int(lerp(0, 255, t**1.4))
        # approximate with metal blend toward dark
        fill = mix(DARK_SOFT, METAL, t)
        draw.rectangle([x0, 0, x1, H], fill=fill)

    # Right silver motion bars
    draw.polygon(
        [
            (W - 280, 0),
            (W - 160, 0),
            (W - 40, H),
            (W - 160, H),
        ],
        fill=mix(SILVER, METAL, 0.35),
    )
    draw.polygon(
        [
            (W - 420, 80),
            (W - 360, 80),
            (W - 220, H - 40),
            (W - 280, H - 40),
        ],
        fill=mix(SILVER, WHITE, 0.15),
    )

    # Right turquoise accent
    draw.polygon(
        [
            (W - 340, 0),
            (W - 328, 0),
            (W - 180, H),
            (W - 192, H),
        ],
        fill=TURQUOISE,
    )

    # Top geometric color block strip (dynamic stadium graphic)
    draw.polygon([(900, 0), (1280, 0), (1180, 160), (820, 160)], fill=CHERRY)
    draw.polygon([(1280, 0), (1480, 0), (1380, 160), (1180, 160)], fill=METAL)
    draw.polygon([(1480, 0), (1580, 0), (1500, 160), (1380, 160)], fill=SILVER)
    draw.polygon([(820, 148), (1500, 148), (1490, 160), (810, 160)], fill=TURQUOISE)

    # Soft stadium light blooms (composited)
    for cx, cy, rx, ry, a in [
        (980, 40, 140, 70, 90),
        (1400, 30, 160, 80, 110),
        (1850, 35, 150, 75, 100),
        (2300, 40, 140, 70, 90),
        (2750, 45, 130, 65, 80),
        (3200, 50, 120, 60, 70),
    ]:
        img = soft_ellipse(img, cx, cy, rx, ry, WHITE, a)
        img = soft_ellipse(img, cx, cy + 10, rx // 2, ry // 2, (255, 240, 210), a + 20)

    draw = ImageDraw.Draw(img)

    # Central / lower light menu panel — wide open negative space
    panel = (560, 320, 3040, 1120)
    # shadow layer
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([panel[0] + 8, panel[1] + 16, panel[2] + 8, panel[3] + 16], radius=14, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(panel, radius=12, fill=LIGHT)
    # white header band for optional title area
    draw.rounded_rectangle((560, 320, 3040, 420), radius=12, fill=WHITE)
    draw.rectangle((560, 400, 3040, 420), fill=WHITE)

    # subtle column guides (very faint, for layout hint — almost invisible)
    for x in (1387, 2213):
        draw.line([(x, 460), (x, 1080)], fill=mix(LIGHT, SILVER, 0.35), width=1)

    # Bottom cherry accent bar under panel edge energy
    draw.polygon(
        [
            (560, 1110),
            (3040, 1110),
            (3040, 1120),
            (560, 1120),
        ],
        fill=CHERRY,
    )
    draw.polygon(
        [
            (560, 1104),
            (900, 1104),
            (900, 1110),
            (560, 1110),
        ],
        fill=TURQUOISE,
    )

    # Upper turquoise hairline across atmosphere
    draw.rectangle([620, 188, 3100, 194], fill=TURQUOISE)

    # Angled silver chevrons (subtle motion, top-left of panel)
    for i in range(3):
        ox = 620 + i * 48
        draw.polygon(
            [
                (ox, 250),
                (ox + 28, 250),
                (ox + 10, 290),
                (ox - 18, 290),
            ],
            fill=mix(SILVER, METAL, 0.2),
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)
    print(f"Wrote {out_path} ({W}x{H})")


def create_svg(out_path: Path) -> None:
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0A0C10"/>
      <stop offset="55%" stop-color="#20242A"/>
      <stop offset="100%" stop-color="#24282E"/>
    </linearGradient>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0A0C10"/>
      <stop offset="70%" stop-color="#281218"/>
      <stop offset="100%" stop-color="#BA0C2F" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="rightFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4A4F55" stop-opacity="0"/>
      <stop offset="40%" stop-color="#4A4F55" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#4A4F55"/>
    </linearGradient>
    <filter id="panelShadow" x="-5%" y="-5%" width="110%" height="120%">
      <feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#000" flood-opacity="0.28"/>
    </filter>
    <filter id="glow">
      <feGaussianBlur stdDeviation="28" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base -->
  <rect width="{W}" height="{H}" fill="url(#base)"/>
  <rect width="{W}" height="420" fill="url(#sky)"/>

  <!-- Left cherry power block + motion -->
  <polygon points="0,0 620,0 420,{H} 0,{H}" fill="#BA0C2F"/>
  <polygon points="80,0 280,0 120,{H} -80,{H}" fill="#78081E"/>
  <polygon points="200,0 340,0 180,{H} 40,{H}" fill="#C52845"/>

  <!-- Silver angled motion -->
  <polygon points="380,-40 470,-40 220,{H + 40} 130,{H + 40}" fill="#A7A8AA" opacity="0.55"/>
  <polygon points="460,-40 550,-40 300,{H + 40} 210,{H + 40}" fill="#A7A8AA" opacity="0.35"/>
  <polygon points="540,-40 630,-40 380,{H + 40} 290,{H + 40}" fill="#4A4F55" opacity="0.55"/>

  <!-- Turquoise electric accents -->
  <polygon points="500,-20 512,-20 300,{H + 20} 288,{H + 20}" fill="#00A8B5"/>
  <rect x="620" y="188" width="2480" height="6" fill="#00A8B5"/>

  <!-- Right metal panel -->
  <rect x="{W - 520}" y="0" width="520" height="{H}" fill="url(#rightFade)"/>
  <polygon points="{W - 280},0 {W - 160},0 {W - 40},{H} {W - 160},{H}" fill="#8C9094"/>
  <polygon points="{W - 420},80 {W - 360},80 {W - 220},{H - 40} {W - 280},{H - 40}" fill="#B8B9BB"/>
  <polygon points="{W - 340},0 {W - 328},0 {W - 180},{H} {W - 192},{H}" fill="#00A8B5"/>

  <!-- Top stadium graphic blocks -->
  <polygon points="900,0 1280,0 1180,160 820,160" fill="#BA0C2F"/>
  <polygon points="1280,0 1480,0 1380,160 1180,160" fill="#4A4F55"/>
  <polygon points="1480,0 1580,0 1500,160 1380,160" fill="#A7A8AA"/>
  <polygon points="820,148 1500,148 1490,160 810,160" fill="#00A8B5"/>

  <!-- Stadium light blooms -->
  <g filter="url(#glow)" opacity="0.85">
    <ellipse cx="980" cy="40" rx="70" ry="28" fill="#FFFFFF"/>
    <ellipse cx="1400" cy="30" rx="80" ry="32" fill="#FFFFFF"/>
    <ellipse cx="1850" cy="35" rx="75" ry="30" fill="#FFFFFF"/>
    <ellipse cx="2300" cy="40" rx="70" ry="28" fill="#FFFFFF"/>
    <ellipse cx="2750" cy="45" rx="65" ry="26" fill="#FFFFFF"/>
    <ellipse cx="3200" cy="50" rx="60" ry="24" fill="#FFFFFF"/>
  </g>

  <!-- Motion chevrons -->
  <polygon points="620,250 648,250 630,290 602,290" fill="#A7A8AA"/>
  <polygon points="668,250 696,250 678,290 650,290" fill="#A7A8AA" opacity="0.75"/>
  <polygon points="716,250 744,250 726,290 698,290" fill="#A7A8AA" opacity="0.5"/>

  <!-- Menu text panel — open negative space -->
  <rect x="560" y="320" width="2480" height="800" rx="12" fill="#F4F4F6" filter="url(#panelShadow)"/>
  <path d="M560 320 H3040 V420 H560 Z" fill="#FFFFFF"/>
  <rect x="560" y="320" width="2480" height="12" rx="12" fill="#FFFFFF"/>
  <rect x="560" y="1110" width="2480" height="10" fill="#BA0C2F"/>
  <rect x="560" y="1104" width="340" height="6" fill="#00A8B5"/>

  <!-- Faint column guides for multi-column menus -->
  <line x1="1387" y1="460" x2="1387" y2="1080" stroke="#A7A8AA" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="2213" y1="460" x2="2213" y2="1080" stroke="#A7A8AA" stroke-opacity="0.28" stroke-width="1"/>
</svg>
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg)
    print(f"Wrote {out_path}")


def create_png_16x3(out_path: Path) -> None:
    """Purpose-built 16:3 ultra banner (4800×900) preserving stadium lights + text panel."""
    global W, H
    old = (W, H)
    W, H = 4800, 900
    try:
        img = Image.new("RGBA", (W, H), (*DARK, 255))
        draw = ImageDraw.Draw(img)
        vertical_gradient(draw, (0, 0, W, H), NIGHT, DARK_SOFT, steps=140)

        for i in range(80):
            t = i / 79
            y0 = int(lerp(0, 260, t))
            y1 = int(lerp(0, 260, (i + 1) / 79)) + 1
            c = mix(NIGHT, mix(CHERRY, DARK, 0.55), t * 0.8)
            draw.rectangle([0, y0, W, y1], fill=c)

        draw.polygon([(0, 0), (720, 0), (520, H), (0, H)], fill=CHERRY)
        draw.polygon([(100, 0), (320, 0), (160, H), (-60, H)], fill=mix(CHERRY, (120, 8, 30), 0.35))
        draw.polygon([(460, -30), (540, -30), (300, H + 30), (220, H + 30)], fill=SILVER)
        draw.polygon([(560, -30), (640, -30), (400, H + 30), (320, H + 30)], fill=mix(SILVER, METAL, 0.3))
        draw.polygon([(600, -20), (612, -20), (380, H + 20), (368, H + 20)], fill=TURQUOISE)

        for i in range(100):
            t = i / 99
            x0 = int(lerp(W - 600, W, t))
            x1 = int(lerp(W - 600, W, (i + 1) / 99)) + 1
            draw.rectangle([x0, 0, x1, H], fill=mix(DARK_SOFT, METAL, t))
        draw.polygon(
            [(W - 320, 0), (W - 180, 0), (W - 40, H), (W - 180, H)],
            fill=mix(SILVER, METAL, 0.35),
        )
        draw.polygon(
            [(W - 380, 0), (W - 368, 0), (W - 200, H), (W - 212, H)],
            fill=TURQUOISE,
        )

        draw.polygon([(1100, 0), (1550, 0), (1450, 120), (1020, 120)], fill=CHERRY)
        draw.polygon([(1550, 0), (1780, 0), (1680, 120), (1450, 120)], fill=METAL)
        draw.polygon([(1780, 0), (1900, 0), (1820, 120), (1680, 120)], fill=SILVER)
        draw.rectangle([1020, 112, 1820, 120], fill=TURQUOISE)
        draw.rectangle([780, 140, 4000, 146], fill=TURQUOISE)

        for cx, cy, rx, ry, a in [
            (1200, 36, 120, 55, 100),
            (1700, 28, 130, 60, 115),
            (2250, 32, 125, 58, 110),
            (2800, 36, 120, 55, 100),
            (3350, 40, 110, 50, 90),
            (3900, 44, 100, 48, 80),
        ]:
            img = soft_ellipse(img, cx, cy, rx, ry, WHITE, a)
            img = soft_ellipse(img, cx, cy + 8, rx // 2, ry // 2, (255, 240, 210), a + 20)

        draw = ImageDraw.Draw(img)
        panel = (700, 200, 4100, 840)
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle(
            [panel[0] + 8, panel[1] + 14, panel[2] + 8, panel[3] + 14],
            radius=12,
            fill=(0, 0, 0, 70),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(24))
        img = Image.alpha_composite(img, shadow)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(panel, radius=10, fill=LIGHT)
        draw.rounded_rectangle((700, 200, 4100, 280), radius=10, fill=WHITE)
        draw.rectangle((700, 260, 4100, 280), fill=WHITE)
        for x in (1833, 2967):
            draw.line([(x, 310), (x, 800)], fill=mix(LIGHT, SILVER, 0.35), width=1)
        draw.rectangle([700, 830, 4100, 840], fill=CHERRY)
        draw.rectangle([700, 824, 1050, 830], fill=TURQUOISE)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(out_path, "PNG", optimize=True)
        print(f"Wrote {out_path} ({W}x{H})")
    finally:
        W, H = old


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    create_png(assets / "unm-menu-bg-athletic-motion.png")
    create_svg(assets / "unm-menu-bg-athletic-motion.svg")
    create_png_16x3(assets / "unm-menu-bg-athletic-motion-16x3.png")


if __name__ == "__main__":
    main()
