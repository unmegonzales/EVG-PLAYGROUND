#!/usr/bin/env python3
"""Build Visitor File Submissions deck matching FY2026 ABR look & feel."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "presentation"
ARTIFACTS = Path("/opt/cursor/artifacts")
IMG_SRC = ROOT / "assets" / "culinary-review.png"
IMG_HERO = OUT_DIR / "hero-widescreen.jpg"
IMG_PANEL = OUT_DIR / "hero-panel.jpg"
LOGO_WHITE = OUT_DIR / "levy-logo-white.png"
LOGO_NAVY = OUT_DIR / "levy-logo-navy.png"
PPTX_PATH = OUT_DIR / "Visitor-File-Submissions.pptx"

# FY2026 ABR design tokens
NAVY = RGBColor(0x0F, 0x1E, 0x35)
NAVY_DEEP = RGBColor(0x08, 0x13, 0x24)
RED = RGBColor(0xE4, 0x00, 0x2B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF5, 0xF6, 0xF7)
GRAY_LINE = RGBColor(0xD7, 0xDA, 0xDD)
GRAY_BODY = RGBColor(0x58, 0x5B, 0x5E)
GRAY_MUTED = RGBColor(0x75, 0x78, 0x7B)
GRAY_FOOT = RGBColor(0x99, 0x99, 0x99)
GRAY_PAGE = RGBColor(0xBC, 0xC0, 0xC4)
INK = RGBColor(0x3F, 0x42, 0x44)

# Same canvas as ABR: 20" × 11.25" (16:9)
SLIDE_W = Inches(20)
SLIDE_H = Inches(11.25)

FONT_DISPLAY = "Bebas Neue"
FONT_BODY = "Calibri"
FONT_SERIF = "Georgia"


def prepare_images() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(IMG_SRC).convert("RGB")
    w, h = img.size
    target_ratio = 16 / 9
    crop_h = int(w / target_ratio)
    top = max(0, min(h - crop_h, int(h * 0.34)))
    hero = img.crop((0, top, w, top + crop_h)).resize((1920, 1080), Image.Resampling.LANCZOS)
    hero.save(IMG_HERO, "JPEG", quality=88, optimize=True)

    panel_w = int(w * 0.78)
    left = max(0, w - panel_w)
    panel = img.crop((left, int(h * 0.05), w, int(h * 0.78))).resize((900, 1200), Image.Resampling.LANCZOS)
    panel.save(IMG_PANEL, "JPEG", quality=88, optimize=True)


def set_run(run, *, size: float, bold: bool = False, color: RGBColor = WHITE, font: str = FONT_BODY, italic: bool = False) -> None:
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text,
    *,
    size=14,
    bold=False,
    color=WHITE,
    align=PP_ALIGN.LEFT,
    font=FONT_BODY,
    italic=False,
    anchor=MSO_ANCHOR.TOP,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf._txBody.bodyPr.set(
            "anchor",
            {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor],
        )
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color, font=font, italic=italic)
    return box


def add_rich_lines(slide, left, top, width, height, lines, *, space_after=6):
    """lines: list of dicts with text/size/bold/color/font/italic."""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = line.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(line.get("space_after", space_after))
        run = p.add_run()
        run.text = line["text"]
        set_run(
            run,
            size=line.get("size", 14),
            bold=line.get("bold", False),
            color=line.get("color", WHITE),
            font=line.get("font", FONT_BODY),
            italic=line.get("italic", False),
        )
    return box


def add_rect(slide, left, top, width, height, fill: RGBColor, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    return shape


def add_hairline(slide, left, top, width, color=GRAY_LINE):
    return add_rect(slide, left, top, width, Pt(1.25), color)


def add_red_rule(slide, left, top, width=Inches(0.55)):
    return add_rect(slide, left, top, width, Pt(3.5), RED)


def blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def dark_bg(slide):
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, NAVY)


def light_bg(slide):
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, WHITE)


def add_logo(slide, dark: bool = True, left=Inches(1.08), top=Inches(10.35), width=Inches(1.15)):
    path = LOGO_WHITE if dark else LOGO_NAVY
    if path.exists():
        slide.shapes.add_picture(str(path), left, top, width=width)


def light_chrome(slide, section_num: str, section_name: str, title: str, helper: str, page: str, footer_right: str):
    """ABR light-content slide chrome."""
    light_bg(slide)
    add_textbox(slide, Inches(1.08), Inches(1.08), Inches(0.55), Inches(0.45), section_num, size=22.5, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(1.62), Inches(1.24), Inches(6), Inches(0.33), section_name, size=12.75, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(1.08), Inches(1.81), Inches(12), Inches(0.8), title, size=58.5, color=NAVY, font=FONT_DISPLAY)
    add_textbox(slide, Inches(14.2), Inches(1.9), Inches(4.7), Inches(0.7), helper, size=14.5, color=GRAY_BODY, font=FONT_SERIF, italic=True)
    add_textbox(slide, Inches(18.55), Inches(0.55), Inches(0.7), Inches(0.45), page, size=19.5, color=GRAY_PAGE, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_hairline(slide, Inches(1.08), Inches(2.7), Inches(17.84))
    add_logo(slide, dark=False, left=Inches(1.08), top=Inches(10.4), width=Inches(1.05))
    add_textbox(slide, Inches(14.5), Inches(10.48), Inches(4.5), Inches(0.3), footer_right, size=10, color=GRAY_FOOT, font=FONT_BODY, align=PP_ALIGN.RIGHT)


def slide_title(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    add_logo(slide, dark=True, left=Inches(1.08), top=Inches(0.85), width=Inches(1.25))
    add_textbox(slide, Inches(14.0), Inches(1.15), Inches(5.1), Inches(0.4), "GROUP SALES · VISITOR INTAKE", size=20, color=WHITE, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(1.08), Inches(2.02), Inches(8), Inches(0.33), "FISCAL YEAR 2026", size=12.75, color=WHITE, font=FONT_BODY)
    add_red_rule(slide, Inches(1.08), Inches(2.42), width=Inches(0.7))

    add_rich_lines(
        slide,
        Inches(1.08),
        Inches(3.1),
        Inches(14),
        Inches(4.4),
        [
            {"text": "VISITOR", "size": 112, "font": FONT_DISPLAY, "color": WHITE, "space_after": 0},
            {"text": "FILE", "size": 112, "font": FONT_DISPLAY, "color": RED, "space_after": 0},
            {"text": "SUBMISSIONS", "size": 112, "font": FONT_DISPLAY, "color": WHITE, "space_after": 0},
        ],
    )

    add_hairline(slide, Inches(1.08), Inches(8.55), Inches(17.84), color=RGBColor(0x3A, 0x4A, 0x5F))
    add_textbox(slide, Inches(1.08), Inches(9.0), Inches(9), Inches(0.7), "SECURE INTAKE BRIEF", size=36, color=WHITE, font=FONT_DISPLAY)
    add_textbox(slide, Inches(16.1), Inches(9.15), Inches(2.9), Inches(0.22), "PREPARED BY", size=9, color=WHITE, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(16.1), Inches(9.4), Inches(2.9), Inches(0.35), "Group Sales", size=15, bold=True, color=WHITE, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(16.1), Inches(9.8), Inches(2.9), Inches(0.3), "Submitted 2026", size=13.5, color=GRAY_LINE, font=FONT_SERIF, italic=True, align=PP_ALIGN.RIGHT)


def slide_howto(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    add_textbox(slide, Inches(0.75), Inches(0.5), Inches(18.5), Inches(1.0), "HOW TO USE THIS VISITOR INTAKE BRIEF", size=66, color=WHITE, font=FONT_DISPLAY)
    add_textbox(
        slide,
        Inches(0.75),
        Inches(1.55),
        Inches(18.5),
        Inches(0.4),
        "A section-by-section guide for submitting venue documents, event files, and review materials.",
        size=15,
        color=GRAY_LINE,
        font=FONT_SERIF,
        italic=True,
    )
    add_hairline(slide, Inches(0.75), Inches(2.15), Inches(18.5), color=RED)

    items = [
        (0.75, 2.45, "01", "THE PROBLEM", "Why scattered visitor files slow reviews and sales handoffs."),
        (0.75, 4.35, "02", "THE FLOW", "Profile, packet, and receipt — one path for every submission."),
        (0.75, 6.35, "03", "TEAMS & TYPES", "Who receives the packet and which submission types are supported."),
        (10.42, 2.45, "04", "PACKET STANDARDS", "File formats, size limits, notes, and approval requirements."),
        (10.42, 4.35, "05", "THE WORKSPACE", "How the visitor profile and live status panel work together."),
        (10.42, 6.35, "06", "OUTCOMES", "Faster handoffs, less rework, clear ownership, audit-ready receipts."),
    ]
    for x, y, num, title, copy in items:
        add_textbox(slide, Inches(x), Inches(y), Inches(0.7), Inches(0.55), num, size=27, bold=True, color=RED, font=FONT_BODY)
        add_textbox(slide, Inches(x + 0.75), Inches(y), Inches(7.8), Inches(0.4), title, size=16, bold=True, color=WHITE, font=FONT_BODY)
        add_textbox(slide, Inches(x + 0.75), Inches(y + 0.45), Inches(7.8), Inches(1.1), copy, size=14, color=GRAY_LINE, font=FONT_BODY)

    add_logo(slide, dark=True, left=Inches(0.75), top=Inches(10.25), width=Inches(1.1))
    add_textbox(slide, Inches(2.2), Inches(10.55), Inches(14), Inches(0.3), "ANNUAL GROUP SALES REVIEW · VISITOR INTAKE · FY2026", size=10, color=GRAY_MUTED, font=FONT_BODY)


def slide_problem(prs):
    light_chrome(
        slide := blank_slide(prs),
        "01",
        "THE PROBLEM",
        "SCATTERED FILES. STALLED REVIEWS.",
        "What slows visitor intake today.",
        "03",
        "THE PROBLEM · 01",
    )
    pains = [
        ("EMAIL CHAINS", "Documents land in inboxes without context, owner, or due date."),
        ("MISSING PACKETS", "Photos, contracts, menus, and reviews arrive in pieces."),
        ("WRONG DESTINATION", "Culinary, Finance, and Ops receive work meant for someone else."),
        ("NO RECEIPT TRAIL", "Teams cannot prove what was submitted or when it arrived."),
    ]
    for i, (title, copy) in enumerate(pains):
        col, row = i % 2, i // 2
        x = Inches(1.08) + Inches(col * 9.2)
        y = Inches(3.2) + Inches(row * 3.0)
        add_rect(slide, x, y, Inches(8.7), Inches(2.55), LIGHT)
        add_rect(slide, x, y, Inches(0.12), Inches(2.55), RED)
        add_textbox(slide, x + Inches(0.5), y + Inches(0.45), Inches(7.7), Inches(0.45), title, size=22, bold=True, color=NAVY, font=FONT_BODY)
        add_textbox(slide, x + Inches(0.5), y + Inches(1.15), Inches(7.7), Inches(1.0), copy, size=16, color=GRAY_BODY, font=FONT_SERIF, italic=True)


def slide_flow(prs):
    light_chrome(
        slide := blank_slide(prs),
        "02",
        "THE FLOW",
        "THREE STEPS. ONE PACKET.",
        "Every visitor submission follows the same path.",
        "04",
        "THE FLOW · 02",
    )
    steps = [
        ("01", "VISITOR DETAILS", "Name, organization, email, destination team, submission type, and due date."),
        ("02", "FILES ATTACHED", "Drop PDF, PPTX, DOCX, XLSX, images, or ZIP packets — up to 25 MB each."),
        ("03", "RECEIPT ISSUED", "Confirm approval for review and generate a submission receipt for the trail."),
    ]
    for i, (num, title, copy) in enumerate(steps):
        x = Inches(1.08) + Inches(i * 6.15)
        add_red_rule(slide, x, Inches(3.3), width=Inches(0.7))
        add_textbox(slide, x, Inches(3.7), Inches(5.6), Inches(0.9), num, size=72, color=RED, font=FONT_DISPLAY)
        add_textbox(slide, x, Inches(4.8), Inches(5.6), Inches(0.45), title, size=22, bold=True, color=NAVY, font=FONT_BODY)
        add_textbox(slide, x, Inches(5.5), Inches(5.5), Inches(1.5), copy, size=16, color=GRAY_BODY, font=FONT_SERIF, italic=True)
        if i < 2:
            add_rect(slide, x + Inches(5.85), Inches(3.4), Pt(1.25), Inches(4.2), GRAY_LINE)


def slide_teams(prs):
    light_chrome(
        slide := blank_slide(prs),
        "03",
        "DESTINATION TEAMS",
        "ROUTE ONCE. REACH THE RIGHT DESK.",
        "Choose the team before you submit.",
        "05",
        "TEAMS · 03",
    )
    teams = [
        ("GROUP SALES", "Business reviews, proposals, and visitor kits"),
        ("EVENT OPERATIONS", "Run-of-show files, photos, and logistics packets"),
        ("FINANCE", "Contracts, invoices, and commercial paperwork"),
        ("CULINARY", "Menus, tasting notes, and sales kits"),
        ("VENUE LEADERSHIP", "Executive summaries and decision packets"),
    ]
    for i, (name, desc) in enumerate(teams):
        y = Inches(3.15) + Inches(i * 1.25)
        add_hairline(slide, Inches(1.08), y, Inches(17.84))
        add_textbox(slide, Inches(1.08), y + Inches(0.25), Inches(0.7), Inches(0.5), f"{i+1:02d}", size=24, bold=True, color=RED, font=FONT_BODY)
        add_textbox(slide, Inches(2.0), y + Inches(0.3), Inches(6), Inches(0.45), name, size=20, bold=True, color=NAVY, font=FONT_BODY)
        add_textbox(slide, Inches(8.5), y + Inches(0.35), Inches(10), Inches(0.45), desc, size=16, color=GRAY_BODY, font=FONT_SERIF, italic=True)


def slide_types(prs):
    light_chrome(
        slide := blank_slide(prs),
        "03",
        "SUBMISSION TYPES",
        "BUILT FOR THE FILES WE USE",
        "Select the type that matches the packet.",
        "06",
        "TYPES · 03",
    )
    types = [
        ("01", "ANNUAL BUSINESS REVIEW", "Structured visitor and account review materials."),
        ("02", "VENUE ANALYSIS", "Performance notes, walkthroughs, and opportunity packs."),
        ("03", "EVENT PHOTOS", "Visual proof and atmosphere for sales storytelling."),
        ("04", "CONTRACT OR INVOICE", "Commercial documents ready for Finance review."),
        ("05", "MENU OR SALES KIT", "Culinary and offering assets for pitching."),
        ("06", "NOTES FOR THE TEAM", "Context, event names, and review requests that travel with the packet."),
    ]
    for i, (num, title, copy) in enumerate(types):
        col, row = i % 3, i // 3
        x = Inches(1.08) + Inches(col * 6.15)
        y = Inches(3.2) + Inches(row * 3.2)
        add_textbox(slide, x, y, Inches(5.5), Inches(0.45), num, size=24, bold=True, color=RED, font=FONT_BODY)
        add_textbox(slide, x, y + Inches(0.6), Inches(5.5), Inches(0.5), title, size=20, bold=True, color=NAVY, font=FONT_BODY)
        add_textbox(slide, x, y + Inches(1.3), Inches(5.5), Inches(1.0), copy, size=15, color=GRAY_BODY, font=FONT_SERIF, italic=True)


def slide_standards(prs):
    slide = blank_slide(prs)
    light_bg(slide)
    add_textbox(slide, Inches(1.08), Inches(1.08), Inches(0.55), Inches(0.45), "04", size=22.5, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(1.62), Inches(1.24), Inches(6), Inches(0.33), "PACKET STANDARDS", size=12.75, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(1.08), Inches(1.81), Inches(10), Inches(0.8), "CLEAN PACKETS. FASTER REVIEWS.", size=52, color=NAVY, font=FONT_DISPLAY)
    add_textbox(slide, Inches(14.2), Inches(1.9), Inches(4.7), Inches(0.7), "What every submission must include.", size=14.5, color=GRAY_BODY, font=FONT_SERIF, italic=True)
    add_textbox(slide, Inches(18.55), Inches(0.55), Inches(0.7), Inches(0.45), "07", size=19.5, color=GRAY_PAGE, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_hairline(slide, Inches(1.08), Inches(2.7), Inches(17.84))

    # Left image panel like ABR venue slide
    slide.shapes.add_picture(str(IMG_PANEL), Inches(1.08), Inches(3.1), width=Inches(7.4), height=Inches(6.4))
    add_rect(slide, Inches(1.08), Inches(8.2), Inches(7.4), Inches(1.3), NAVY_DEEP)
    add_textbox(slide, Inches(1.35), Inches(8.4), Inches(6.8), Inches(0.45), "VISITOR FILE PACKET", size=28, color=WHITE, font=FONT_DISPLAY)
    add_textbox(slide, Inches(1.35), Inches(8.95), Inches(6.8), Inches(0.3), "Group Sales · Secure Intake", size=14, color=GRAY_LINE, font=FONT_BODY)

    rules = [
        ("ACCEPTED FORMATS", "PDF, PPTX, DOCX, XLSX, PNG, JPG, ZIP"),
        ("SIZE LIMIT", "Up to 25 MB per file"),
        ("PROFILE REQUIRED", "Visitor details + destination team"),
        ("CONTEXT NOTES", "Event names and review asks"),
        ("APPROVAL", "Confirm files are approved before submit"),
        ("ONE PACKET", "Keep one packet per review request"),
    ]
    for i, (label, copy) in enumerate(rules):
        y = Inches(3.15) + Inches(i * 0.95)
        add_textbox(slide, Inches(9.0), y, Inches(9.8), Inches(0.3), label, size=13, bold=True, color=RED, font=FONT_BODY)
        add_textbox(slide, Inches(9.0), y + Inches(0.32), Inches(9.8), Inches(0.4), copy, size=16, color=INK, font=FONT_SERIF, italic=True)

    add_logo(slide, dark=False, left=Inches(1.08), top=Inches(10.4), width=Inches(1.05))
    add_textbox(slide, Inches(14.5), Inches(10.48), Inches(4.5), Inches(0.3), "STANDARDS · 04", size=10, color=GRAY_FOOT, font=FONT_BODY, align=PP_ALIGN.RIGHT)


def slide_workspace(prs):
    light_chrome(
        slide := blank_slide(prs),
        "05",
        "THE WORKSPACE",
        "PROFILE. PACKET. LIVE STATUS.",
        "How the submission portal is organized.",
        "08",
        "WORKSPACE · 05",
    )

    # Form panel
    add_rect(slide, Inches(1.08), Inches(3.15), Inches(11.4), Inches(6.5), LIGHT)
    add_textbox(slide, Inches(1.45), Inches(3.45), Inches(1.0), Inches(0.55), "01", size=36, color=NAVY, font=FONT_DISPLAY)
    add_textbox(slide, Inches(2.55), Inches(3.5), Inches(5), Inches(0.3), "VISITOR PROFILE", size=12.75, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(2.55), Inches(3.9), Inches(8), Inches(0.4), "TELL US WHO IS SUBMITTING", size=28, color=NAVY, font=FONT_DISPLAY)

    fields = ["FULL NAME", "ORGANIZATION", "EMAIL", "DESTINATION TEAM", "SUBMISSION TYPE", "DUE DATE"]
    for i, field in enumerate(fields):
        col, row = i % 2, i // 2
        x = Inches(1.55) + Inches(col * 5.3)
        y = Inches(4.7) + Inches(row * 1.35)
        add_textbox(slide, x, y, Inches(4.8), Inches(0.28), field, size=11, bold=True, color=GRAY_MUTED, font=FONT_BODY)
        add_rect(slide, x, y + Inches(0.35), Inches(4.8), Inches(0.55), WHITE, line=GRAY_LINE)

    # Status panel
    add_rect(slide, Inches(12.85), Inches(3.15), Inches(6.05), Inches(6.5), NAVY)
    add_textbox(slide, Inches(13.25), Inches(3.5), Inches(5.2), Inches(0.3), "SUBMISSION STATUS", size=12, bold=True, color=RED, font=FONT_BODY)
    add_textbox(slide, Inches(13.25), Inches(4.1), Inches(5.2), Inches(1.0), "03", size=84, color=RED, font=FONT_DISPLAY)
    add_textbox(slide, Inches(13.25), Inches(5.3), Inches(5.2), Inches(0.45), "READY FOR FILES", size=24, color=WHITE, font=FONT_DISPLAY)
    add_textbox(
        slide,
        Inches(13.25),
        Inches(5.95),
        Inches(5.2),
        Inches(1.2),
        "Complete the visitor profile and attach at least one file to generate a submission receipt.",
        size=15,
        color=GRAY_LINE,
        font=FONT_SERIF,
        italic=True,
    )
    add_textbox(slide, Inches(13.25), Inches(7.7), Inches(3.5), Inches(0.28), "PACKET COMPLETION", size=11, bold=True, color=GRAY_MUTED, font=FONT_BODY)
    add_textbox(slide, Inches(16.5), Inches(7.65), Inches(1.9), Inches(0.35), "100%", size=18, bold=True, color=RED, font=FONT_BODY, align=PP_ALIGN.RIGHT)
    add_rect(slide, Inches(13.25), Inches(8.15), Inches(5.2), Inches(0.14), RGBColor(0x2A, 0x3B, 0x52))
    add_rect(slide, Inches(13.25), Inches(8.15), Inches(5.2), Inches(0.14), RED)


def slide_outcomes(prs):
    light_chrome(
        slide := blank_slide(prs),
        "06",
        "OUTCOMES",
        "WHAT CHANGES WHEN INTAKE IS SHARP",
        "Operating results of a clean visitor packet.",
        "09",
        "OUTCOMES · 06",
    )
    outcomes = [
        ("01", "FASTER HANDOFFS", "Sales, Ops, Culinary, and Finance start from one complete packet."),
        ("02", "LESS REWORK", "Required context travels with the files — fewer follow-up emails."),
        ("03", "CLEAR OWNERSHIP", "Destination team selection removes ambiguity on day one."),
        ("04", "AUDIT-READY TRAIL", "Receipts create a lightweight history of what was submitted."),
    ]
    for i, (num, title, copy) in enumerate(outcomes):
        x = Inches(1.08) + Inches(i * 4.65)
        add_rect(slide, x, Inches(3.25), Inches(4.35), Inches(5.9), LIGHT)
        add_textbox(slide, x + Inches(0.35), Inches(3.7), Inches(3.6), Inches(0.7), num, size=42, color=RED, font=FONT_DISPLAY)
        add_textbox(slide, x + Inches(0.35), Inches(4.8), Inches(3.6), Inches(1.1), title, size=26, color=NAVY, font=FONT_DISPLAY)
        add_textbox(slide, x + Inches(0.35), Inches(6.3), Inches(3.6), Inches(2.0), copy, size=16, color=GRAY_BODY, font=FONT_SERIF, italic=True)


def slide_close(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    slide.shapes.add_picture(str(IMG_HERO), Inches(8.5), 0, height=SLIDE_H)
    add_rect(slide, 0, 0, Inches(10.2), SLIDE_H, NAVY)
    add_rect(slide, Inches(9.4), 0, Inches(1.4), SLIDE_H, NAVY_DEEP)

    add_textbox(slide, Inches(1.08), Inches(2.0), Inches(8), Inches(0.33), "FISCAL YEAR 2026", size=12.75, color=WHITE, font=FONT_BODY)
    add_red_rule(slide, Inches(1.08), Inches(2.4), width=Inches(0.7))
    add_rich_lines(
        slide,
        Inches(1.08),
        Inches(3.0),
        Inches(8.5),
        Inches(4.5),
        [
            {"text": "SUBMIT THE PACKET.", "size": 72, "font": FONT_DISPLAY, "color": WHITE, "space_after": 2},
            {"text": "OWN THE REVIEW.", "size": 72, "font": FONT_DISPLAY, "color": WHITE, "space_after": 2},
            {"text": "MOVE THE", "size": 72, "font": FONT_DISPLAY, "color": WHITE, "space_after": 2},
            {"text": "BUSINESS.", "size": 72, "font": FONT_DISPLAY, "color": RED, "space_after": 2},
        ],
    )
    add_logo(slide, dark=True, left=Inches(1.08), top=Inches(10.2), width=Inches(1.2))
    add_textbox(slide, Inches(12.5), Inches(10.4), Inches(6.5), Inches(0.35), "GROUP SALES · VISITOR INTAKE · FY2026", size=12, color=GRAY_LINE, font=FONT_BODY, align=PP_ALIGN.RIGHT)


def build() -> Path:
    prepare_images()
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_title(prs)
    slide_howto(prs)
    slide_problem(prs)
    slide_flow(prs)
    slide_teams(prs)
    slide_types(prs)
    slide_standards(prs)
    slide_workspace(prs)
    slide_outcomes(prs)
    slide_close(prs)

    PPTX_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(PPTX_PATH))
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / PPTX_PATH.name).write_bytes(PPTX_PATH.read_bytes())
    return PPTX_PATH


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")
