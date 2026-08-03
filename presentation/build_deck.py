#!/usr/bin/env python3
"""Build an editable PowerPoint deck for Visitor File Submissions."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "presentation"
ARTIFACTS = Path("/opt/cursor/artifacts")
IMG_SRC = ROOT / "assets" / "culinary-review.png"
IMG_HERO = OUT_DIR / "hero-widescreen.jpg"
IMG_PANEL = OUT_DIR / "hero-panel.jpg"
PPTX_PATH = OUT_DIR / "Visitor-File-Submissions.pptx"

# Brand system from the portal
NAVY = RGBColor(0x07, 0x15, 0x28)
NAVY_2 = RGBColor(0x0D, 0x22, 0x3C)
PINK = RGBColor(0xF4, 0x34, 0x73)
AMBER = RGBColor(0xD4, 0x89, 0x33)
GREEN = RGBColor(0x6F, 0xAE, 0x7D)
PAPER = RGBColor(0xF7, 0xF5, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0x6B, 0x72, 0x80)
INK = RGBColor(0x17, 0x20, 0x33)
LINE = RGBColor(0x2A, 0x3B, 0x52)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def prepare_images() -> None:
    """Crop the vertical kitchen photo into widescreen assets."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(IMG_SRC).convert("RGB")
    w, h = img.size

    # Widescreen hero: bias toward the plating action (lower-middle of the frame)
    target_ratio = 16 / 9
    crop_h = int(w / target_ratio)
    top = max(0, min(h - crop_h, int(h * 0.34)))
    hero = img.crop((0, top, w, top + crop_h)).resize((1600, 900), Image.Resampling.LANCZOS)
    hero.save(IMG_HERO, "JPEG", quality=85, optimize=True)

    # Side panel: chef focus for split layouts
    panel_w = int(w * 0.78)
    left = max(0, w - panel_w)
    panel = img.crop((left, int(h * 0.05), w, int(h * 0.78))).resize((720, 960), Image.Resampling.LANCZOS)
    panel.save(IMG_PANEL, "JPEG", quality=85, optimize=True)


def set_run(run, *, size: int, bold: bool = False, color: RGBColor = WHITE, font: str = "Arial") -> None:
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_textbox(slide, left, top, width, height, text, *, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font="Arial", anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color, font=font)
    return box


def add_multiline(slide, left, top, width, height, lines, *, size=16, bold=False, color=WHITE, space_after=8, font="Arial"):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = line
        set_run(run, size=size, bold=bold, color=color, font=font)
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


def add_accent_bar(slide, left, top, width=Inches(0.55), height=Inches(0.08), color=PINK):
    return add_rect(slide, left, top, width, height, color)


def blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def dark_bg(slide):
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, NAVY)


def light_bg(slide):
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, PAPER)


def footer(slide, label: str, page: str, dark: bool = True):
    color = RGBColor(0xA8, 0xB2, 0xC0) if dark else MUTED
    add_textbox(slide, Inches(0.55), Inches(7.05), Inches(8), Inches(0.3), label, size=11, color=color, font="Arial")
    add_textbox(slide, Inches(11.4), Inches(7.05), Inches(1.4), Inches(0.3), page, size=11, color=color, align=PP_ALIGN.RIGHT, font="Arial")


def slide_title(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    # Full-bleed culinary hero on the right half
    slide.shapes.add_picture(str(IMG_HERO), Inches(5.4), 0, height=SLIDE_H)
    add_rect(slide, 0, 0, Inches(7.15), SLIDE_H, NAVY)
    add_rect(slide, Inches(6.55), 0, Inches(0.9), SLIDE_H, NAVY_2)

    add_textbox(slide, Inches(0.7), Inches(0.55), Inches(5.8), Inches(0.35), "GROUP SALES  ·  VISITOR INTAKE  ·  FY2026", size=12, bold=True, color=PINK)
    add_accent_bar(slide, Inches(0.7), Inches(1.05), width=Inches(0.7))
    add_textbox(slide, Inches(0.7), Inches(1.4), Inches(6.2), Inches(2.5), "VISITOR\nFILE\nSUBMISSIONS", size=58, bold=True, color=WHITE, font="Arial Black")
    add_textbox(
        slide,
        Inches(0.7),
        Inches(4.35),
        Inches(5.6),
        Inches(1.1),
        "One secure packet for venue documents, event files, and review materials — routed to the right team with a clear receipt.",
        size=17,
        color=RGBColor(0xD7, 0xDE, 0xE7),
    )
    add_rect(slide, Inches(0.7), Inches(5.75), Inches(2.35), Inches(0.55), PINK)
    add_textbox(slide, Inches(0.7), Inches(5.82), Inches(2.35), Inches(0.4), "SECURE PORTAL", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(3.25), Inches(5.85), Inches(3.2), Inches(0.4), "Editable PowerPoint brief", size=14, color=RGBColor(0xC8, 0xD0, 0xDB))
    footer(slide, "Levy Group Sales  |  Visitor Intake", "01", dark=True)


def slide_agenda(prs):
    slide = blank_slide(prs)
    light_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.45), Inches(8), Inches(0.35), "AGENDA", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.85), Inches(10), Inches(0.7), "What this brief covers", size=36, bold=True, color=NAVY, font="Arial Black")
    add_accent_bar(slide, Inches(0.7), Inches(1.65))

    items = [
        ("01", "The intake problem", "Why scattered visitor files slow reviews and sales handoffs."),
        ("02", "The three-step flow", "Profile, packet, receipt — a single path for every submission."),
        ("03", "What routes where", "Teams, file types, and packet standards that keep work moving."),
        ("04", "Operating outcome", "Faster reviews, cleaner handoffs, and a repeatable visitor process."),
    ]
    for i, (num, title, copy) in enumerate(items):
        y = Inches(2.1) + Inches(i * 1.1)
        add_textbox(slide, Inches(0.7), y, Inches(1.1), Inches(0.6), num, size=28, bold=True, color=PINK, font="Arial Black")
        add_textbox(slide, Inches(2.0), y, Inches(9), Inches(0.4), title, size=22, bold=True, color=NAVY)
        add_textbox(slide, Inches(2.0), y + Inches(0.4), Inches(9.5), Inches(0.45), copy, size=15, color=MUTED)
    footer(slide, "Visitor File Submissions  |  Agenda", "02", dark=False)


def slide_problem(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.45), Inches(8), Inches(0.35), "THE PROBLEM", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.9), Inches(11), Inches(1.0), "Visitor files arrive\nscattered. Reviews stall.", size=40, bold=True, color=WHITE, font="Arial Black")
    add_accent_bar(slide, Inches(0.7), Inches(3.05), width=Inches(0.8))

    pains = [
        ("Email chains", "Documents land in inboxes without context, owner, or due date."),
        ("Missing packets", "Photos, contracts, menus, and reviews arrive in pieces."),
        ("Wrong destination", "Culinary, Finance, and Ops get work meant for someone else."),
        ("No receipt trail", "Teams cannot prove what was submitted or when."),
    ]
    for i, (title, copy) in enumerate(pains):
        col = i % 2
        row = i // 2
        x = Inches(0.7) + Inches(col * 6.2)
        y = Inches(3.5) + Inches(row * 1.45)
        add_rect(slide, x, y, Inches(5.8), Inches(1.25), NAVY_2)
        add_rect(slide, x, y, Inches(0.12), Inches(1.25), PINK)
        add_textbox(slide, x + Inches(0.35), y + Inches(0.22), Inches(5.1), Inches(0.35), title, size=18, bold=True, color=WHITE)
        add_textbox(slide, x + Inches(0.35), y + Inches(0.6), Inches(5.1), Inches(0.5), copy, size=14, color=RGBColor(0xB8, 0xC2, 0xCF))
    footer(slide, "Visitor File Submissions  |  Problem", "03", dark=True)


def slide_flow(prs):
    slide = blank_slide(prs)
    light_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.4), Inches(8), Inches(0.3), "THE FLOW", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.8), Inches(11), Inches(0.6), "Three steps. One packet.", size=36, bold=True, color=NAVY, font="Arial Black")
    add_textbox(slide, Inches(0.7), Inches(1.45), Inches(11), Inches(0.4), "Every visitor submission follows the same path — clear for guests, actionable for teams.", size=16, color=MUTED)

    steps = [
        ("01", "Visitor details", "Name, organization, email, destination team, submission type, and due date."),
        ("02", "Files attached", "Drop PDFs, PPTX, DOCX, XLSX, images, or ZIP packets up to 25 MB each."),
        ("03", "Receipt issued", "Confirm approval for review and generate a submission receipt for the trail."),
    ]
    for i, (num, title, copy) in enumerate(steps):
        x = Inches(0.7) + Inches(i * 4.15)
        add_accent_bar(slide, x, Inches(2.35), width=Inches(0.7))
        add_textbox(slide, x, Inches(2.7), Inches(3.7), Inches(0.7), num, size=48, bold=True, color=PINK, font="Arial Black")
        add_textbox(slide, x, Inches(3.6), Inches(3.7), Inches(0.5), title.upper(), size=18, bold=True, color=NAVY)
        add_textbox(slide, x, Inches(4.25), Inches(3.7), Inches(1.5), copy, size=15, color=MUTED)
        if i < 2:
            add_rect(slide, x + Inches(3.85), Inches(2.5), Inches(0.015), Inches(3.2), RGBColor(0xD9, 0xD4, 0xCA))
    footer(slide, "Visitor File Submissions  |  Flow", "04", dark=False)


def slide_teams(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.45), Inches(8), Inches(0.3), "DESTINATION TEAMS", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.9), Inches(11), Inches(0.7), "Route once. Reach the right desk.", size=34, bold=True, color=WHITE, font="Arial Black")
    add_accent_bar(slide, Inches(0.7), Inches(1.75), width=Inches(0.75))

    teams = [
        ("Group Sales", "Business reviews, proposals, and visitor kits"),
        ("Event Operations", "Run-of-show files, photos, and logistics packets"),
        ("Finance", "Contracts, invoices, and commercial paperwork"),
        ("Culinary", "Menus, tasting notes, and sales kits"),
        ("Venue Leadership", "Executive summaries and decision packets"),
    ]
    for i, (name, desc) in enumerate(teams):
        y = Inches(2.2) + Inches(i * 0.85)
        add_rect(slide, Inches(0.7), y, Inches(11.9), Inches(0.72), NAVY_2)
        add_rect(slide, Inches(0.7), y, Inches(0.14), Inches(0.72), AMBER if i % 2 else PINK)
        add_textbox(slide, Inches(1.1), y + Inches(0.15), Inches(3.5), Inches(0.4), name, size=18, bold=True, color=WHITE)
        add_textbox(slide, Inches(4.9), y + Inches(0.18), Inches(7.3), Inches(0.4), desc, size=15, color=RGBColor(0xB8, 0xC2, 0xCF))
    footer(slide, "Visitor File Submissions  |  Teams", "05", dark=True)


def slide_types(prs):
    slide = blank_slide(prs)
    light_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.4), Inches(8), Inches(0.3), "SUBMISSION TYPES", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.8), Inches(11), Inches(0.6), "Built for the files we actually use", size=34, bold=True, color=NAVY, font="Arial Black")

    types = [
        ("Annual business review", "Structured visitor and account review materials."),
        ("Venue analysis", "Performance notes, walkthroughs, and opportunity packs."),
        ("Event photos", "Visual proof and atmosphere for sales storytelling."),
        ("Contract or invoice", "Commercial documents ready for Finance review."),
        ("Menu or sales kit", "Culinary and offering assets for pitching."),
        ("Notes for the team", "Context, event names, and review requests that travel with the packet."),
    ]
    for i, (title, copy) in enumerate(types):
        col = i % 3
        row = i // 3
        x = Inches(0.7) + Inches(col * 4.15)
        y = Inches(1.95) + Inches(row * 2.2)
        add_accent_bar(slide, x, y, width=Inches(0.55))
        add_textbox(slide, x, y + Inches(0.25), Inches(3.7), Inches(0.4), f"{i+1:02d}", size=22, bold=True, color=PINK, font="Arial Black")
        add_textbox(slide, x, y + Inches(0.75), Inches(3.7), Inches(0.45), title, size=17, bold=True, color=NAVY)
        add_textbox(slide, x, y + Inches(1.25), Inches(3.7), Inches(0.7), copy, size=14, color=MUTED)
    footer(slide, "Visitor File Submissions  |  Types", "06", dark=False)


def slide_standards(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    slide.shapes.add_picture(str(IMG_PANEL), Inches(8.6), 0, height=SLIDE_H)
    add_rect(slide, Inches(8.2), 0, Inches(0.55), SLIDE_H, NAVY)

    add_textbox(slide, Inches(0.7), Inches(0.45), Inches(7), Inches(0.3), "PACKET STANDARDS", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.9), Inches(7.2), Inches(1.1), "Clean packets.\nFaster reviews.", size=36, bold=True, color=WHITE, font="Arial Black")
    add_accent_bar(slide, Inches(0.7), Inches(2.25), width=Inches(0.7))

    rules = [
        "Accepted: PDF, PPTX, DOCX, XLSX, PNG, JPG, ZIP",
        "Size limit: up to 25 MB per file",
        "Include visitor profile + destination team",
        "Add notes with event names and review asks",
        "Confirm files are approved before submit",
        "Keep one packet per review request",
    ]
    for i, rule in enumerate(rules):
        y = Inches(2.7) + Inches(i * 0.6)
        add_rect(slide, Inches(0.7), y, Inches(0.18), Inches(0.18), PINK)
        add_textbox(slide, Inches(1.15), y - Inches(0.05), Inches(6.8), Inches(0.4), rule, size=15, color=RGBColor(0xD7, 0xDE, 0xE7))
    footer(slide, "Visitor File Submissions  |  Standards", "07", dark=True)


def slide_workspace(prs):
    slide = blank_slide(prs)
    light_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.4), Inches(8), Inches(0.3), "THE WORKSPACE", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.8), Inches(11), Inches(0.55), "Profile. Packet. Live status.", size=34, bold=True, color=NAVY, font="Arial Black")

    # Left panel - form
    add_rect(slide, Inches(0.7), Inches(1.7), Inches(7.5), Inches(4.7), WHITE)
    add_textbox(slide, Inches(1.0), Inches(1.95), Inches(1), Inches(0.4), "01", size=28, bold=True, color=NAVY, font="Arial Black")
    add_textbox(slide, Inches(2.0), Inches(2.0), Inches(5.5), Inches(0.3), "VISITOR PROFILE", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(2.0), Inches(2.3), Inches(5.5), Inches(0.4), "Tell us who is submitting", size=20, bold=True, color=NAVY)

    fields = ["Full name", "Organization", "Email", "Destination team", "Submission type", "Due date"]
    for i, field in enumerate(fields):
        col = i % 2
        row = i // 2
        x = Inches(1.0) + Inches(col * 3.4)
        y = Inches(3.0) + Inches(row * 0.95)
        add_textbox(slide, x, y, Inches(3.0), Inches(0.25), field.upper(), size=10, bold=True, color=MUTED)
        add_rect(slide, x, y + Inches(0.3), Inches(3.1), Inches(0.42), PAPER, line=RGBColor(0xD5, 0xD0, 0xC6))

    # Right panel - status
    add_rect(slide, Inches(8.5), Inches(1.7), Inches(4.1), Inches(4.7), NAVY)
    add_textbox(slide, Inches(8.85), Inches(2.0), Inches(3.5), Inches(0.3), "SUBMISSION STATUS", size=11, bold=True, color=PINK)
    add_textbox(slide, Inches(8.85), Inches(2.5), Inches(3.5), Inches(0.7), "03", size=48, bold=True, color=PINK, font="Arial Black")
    add_textbox(slide, Inches(8.85), Inches(3.3), Inches(3.5), Inches(0.4), "READY FOR FILES", size=16, bold=True, color=WHITE)
    add_textbox(
        slide,
        Inches(8.85),
        Inches(3.8),
        Inches(3.5),
        Inches(1.0),
        "Complete the visitor profile and attach at least one file to generate a submission receipt.",
        size=13,
        color=RGBColor(0xB8, 0xC2, 0xCF),
    )
    add_textbox(slide, Inches(8.85), Inches(5.1), Inches(2.2), Inches(0.25), "PACKET COMPLETION", size=10, bold=True, color=MUTED)
    add_textbox(slide, Inches(11.2), Inches(5.05), Inches(1.0), Inches(0.3), "100%", size=14, bold=True, color=PINK, align=PP_ALIGN.RIGHT)
    add_rect(slide, Inches(8.85), Inches(5.45), Inches(3.4), Inches(0.12), RGBColor(0x2A, 0x3B, 0x52))
    add_rect(slide, Inches(8.85), Inches(5.45), Inches(3.4), Inches(0.12), PINK)
    footer(slide, "Visitor File Submissions  |  Workspace", "08", dark=False)


def slide_outcomes(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    add_textbox(slide, Inches(0.7), Inches(0.45), Inches(8), Inches(0.3), "OUTCOMES", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(0.9), Inches(11), Inches(0.7), "What changes when intake is sharp", size=34, bold=True, color=WHITE, font="Arial Black")
    add_accent_bar(slide, Inches(0.7), Inches(1.75), width=Inches(0.75))

    outcomes = [
        ("Faster handoffs", "Sales, Ops, Culinary, and Finance start from one complete packet."),
        ("Less rework", "Required context travels with the files — fewer follow-up emails."),
        ("Clear ownership", "Destination team selection removes ambiguity on day one."),
        ("Audit-ready trail", "Receipts create a lightweight history of what was submitted."),
    ]
    for i, (title, copy) in enumerate(outcomes):
        x = Inches(0.7) + Inches((i % 4) * 3.1)
        y = Inches(2.4)
        add_rect(slide, x, y, Inches(2.95), Inches(3.6), NAVY_2)
        add_textbox(slide, x + Inches(0.25), y + Inches(0.4), Inches(2.4), Inches(0.5), f"{i+1:02d}", size=28, bold=True, color=PINK, font="Arial Black")
        add_textbox(slide, x + Inches(0.25), y + Inches(1.3), Inches(2.4), Inches(0.8), title, size=18, bold=True, color=WHITE)
        add_textbox(slide, x + Inches(0.25), y + Inches(2.2), Inches(2.4), Inches(1.1), copy, size=13, color=RGBColor(0xB8, 0xC2, 0xCF))
    footer(slide, "Visitor File Submissions  |  Outcomes", "09", dark=True)


def slide_close(prs):
    slide = blank_slide(prs)
    dark_bg(slide)
    slide.shapes.add_picture(str(IMG_HERO), 0, 0, width=SLIDE_W, height=SLIDE_H)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    # Keep image visible on right with navy overlay on left
    # Re-add image and overlay properly
    for shape in list(slide.shapes):
        sp = shape._element
        sp.getparent().remove(sp)
    dark_bg(slide)
    slide.shapes.add_picture(str(IMG_HERO), Inches(5.8), 0, height=SLIDE_H)
    add_rect(slide, 0, 0, Inches(7.4), SLIDE_H, NAVY)
    add_rect(slide, Inches(6.8), 0, Inches(1.0), SLIDE_H, NAVY_2)

    add_textbox(slide, Inches(0.7), Inches(1.3), Inches(6), Inches(0.3), "NEXT STEP", size=12, bold=True, color=PINK)
    add_textbox(slide, Inches(0.7), Inches(1.8), Inches(6.2), Inches(1.8), "Submit the packet.\nOwn the review.", size=40, bold=True, color=WHITE, font="Arial Black")
    add_textbox(
        slide,
        Inches(0.7),
        Inches(4.0),
        Inches(5.8),
        Inches(1.0),
        "Use the visitor portal to send venue documents, event files, and review materials in one organized submission.",
        size=16,
        color=RGBColor(0xD7, 0xDE, 0xE7),
    )
    add_rect(slide, Inches(0.7), Inches(5.4), Inches(3.1), Inches(0.6), PINK)
    add_textbox(slide, Inches(0.7), Inches(5.5), Inches(3.1), Inches(0.4), "OPEN SUBMISSION PORTAL", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    footer(slide, "Group Sales  ·  Visitor Intake  ·  FY2026", "10", dark=True)


def build() -> Path:
    prepare_images()
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_title(prs)
    slide_agenda(prs)
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
    artifact = ARTIFACTS / PPTX_PATH.name
    artifact.write_bytes(PPTX_PATH.read_bytes())
    return PPTX_PATH


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
    print(f"Copied to /opt/cursor/artifacts/{path.name}")
