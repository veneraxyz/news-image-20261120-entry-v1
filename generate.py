#!/usr/bin/env python3
"""Render the news-image-20261120 entry: one 1024x1024 front page summing up
world news of Friday 20 November 2026.

Deterministic: fixed geometry, fixed palette, fixed fonts, no randomness,
no timestamps, no network. Run it, then main.ts copies the committed
entry.png to the output directory.

Layout (1024 x 1024):
  - top band (~14%): the date, large, alone
  - lead card (~33%): Cyclone Akvan landfall in Odisha, with a restrained
    coastal map marking Gopalpur
  - four briefs in a 2x2 grid (~48%): Trump/Iran, Voyager 1, Hayabusa2,
    Han Duck-soo
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 244, 236)
INK = (27, 36, 48)
MUTED = (92, 102, 114)
CARD = (255, 255, 255)
BORDER = (217, 210, 194)
BAND = (20, 32, 46)
GOLD = (201, 162, 39)
RED = (179, 55, 44)
RUST = (168, 91, 42)
SEA = (216, 233, 241)
SEA_LINE = (185, 203, 214)
LAND = (239, 229, 204)
COAST = (138, 123, 92)
LAND_LABEL = (122, 106, 74)
SEA_LABEL = (91, 122, 140)
SPACE_BLUE = (46, 95, 138)
ROCK = (138, 141, 145)
ROCK_DARK = (104, 107, 111)
GREEN = (47, 107, 79)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit(text, name, start, max_width, min_size=18):
    """Largest font size (down from start) at which text fits max_width."""
    size = start
    while size > min_size:
        f = font(name, size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(name, min_size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def tracked_text(draw, cx, y, text, f, fill, tracking):
    """Draw text centred on cx with extra tracking between characters."""
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += w + tracking


def card(draw, x0, y0, x1, y1, radius=12):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=CARD,
                           outline=BORDER, width=2)


def hairline(draw, x0, x1, y, fill=BORDER, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- top band

def draw_band(draw):
    draw.rectangle([0, 0, W, 140], fill=BAND)
    draw.rectangle([0, 137, W, 140], fill=GOLD)
    f = fit("20 NOVEMBER 2026", "NotoSans-Black.ttf", 66, 900)
    tracked_text(draw, W / 2, 34, "20 NOVEMBER 2026", f, (255, 255, 255), 6)


# ------------------------------------------------------------- coastal map

def draw_map(draw, x0, y0, x1, y1):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=SEA,
                           outline=SEA_LINE, width=2)
    # Land west of a gently curving coastline; sea to the east.
    coast = [(x0 + 76, y0), (x0 + 106, y0 + 62), (x0 + 146, y0 + 122),
             (x0 + 174, y0 + 192), (x0 + 194, y1)]
    land = [(x0, y0)] + coast + [(x0, y1)]
    draw.polygon(land, fill=LAND)
    draw.line(coast, fill=COAST, width=3, joint="curve")
    # Restrained cyclone swirl in the sea, off the coast.
    cx, cy = x0 + 228, y0 + 74
    for r, start in ((12, 200), (22, 140), (32, 80)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start,
                 end=start + 300, fill=SPACE_BLUE, width=3)
    # Labels.
    f_land = font("NotoSans-Bold.ttf", 20)
    draw.text((x0 + 16, y0 + 42), "ODISHA", font=f_land, fill=LAND_LABEL)
    f_sea = font("NotoSans-Regular.ttf", 17)
    draw.text((x0 + 168, y1 - 34), "BAY OF BENGAL", font=f_sea, fill=SEA_LABEL)
    # Gopalpur marker on the coastline.
    gx, gy = x0 + 146, y0 + 122
    draw.ellipse([gx - 10, gy - 10, gx + 10, gy + 10], fill=(255, 255, 255),
                 outline=RED, width=2)
    draw.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED)
    f_pin = font("NotoSans-Bold.ttf", 20)
    label = "GOPALPUR"
    lw = text_w(draw, label, f_pin)
    draw.text((gx - lw / 2, gy + 16), label, font=f_pin, fill=INK,
              stroke_width=3, stroke_fill=(247, 244, 236))
    # North arrow, top right.
    nx, ny = x1 - 26, y0 + 18
    draw.text((nx - 6, ny), "N", font=font("NotoSans-Bold.ttf", 16), fill=MUTED)
    draw.polygon([(nx, ny + 24), (nx - 6, ny + 38), (nx + 6, ny + 38)],
                 fill=MUTED)


# ------------------------------------------------------------- lead card

def draw_lead(draw):
    x0, y0, x1, y1 = 28, 154, 996, 494
    card(draw, x0, y0, x1, y1)
    tx = 56
    f_head = font("NotoSans-Black.ttf", 52)
    draw.text((tx, 178), "CYCLONE AKVAN", font=f_head, fill=INK)
    draw.text((tx, 234), "LANDFALL IN ODISHA", font=f_head, fill=INK)
    f_sub = font("NotoSans-Regular.ttf", 27)
    draw.text((tx, 300), "Near Gopalpur \u2022 20 November",
              font=f_sub, fill=MUTED)
    hairline(draw, tx, 660, 340)
    f_stat = font("NotoSans-Black.ttf", 42)
    draw.text((tx, 354), "300,000+ EVACUATED", font=f_stat, fill=RED)
    f_wind = font("NotoSans-SemiBold.ttf", 27)
    draw.text((tx, 406), "Winds 70\u201380 km/h \u2022 Gusts to 90",
              font=f_wind, fill=INK)
    f_note = font("NotoSans-Regular.ttf", 25)
    draw.text((tx, 442), "No major damage or loss of life reported",
              font=f_note, fill=(61, 71, 83))
    draw_map(draw, 684, 178, 972, 470)


# ------------------------------------------------------------- brief motifs

def motif_iran(draw, x0, y0, x1, y1):
    """A calendar page for 1 January, with an arrow pointing towards it:
    the decision comes after that date. No small text: the motif is a
    graphic, the headline carries the words."""
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    # Arrow shaft and head, left of the calendar.
    draw.line([(cx - 118, cy + 2), (cx - 52, cy + 2)], fill=RUST, width=4)
    draw.polygon([(cx - 52, cy + 2), (cx - 66, cy - 8), (cx - 66, cy + 12)],
                 fill=RUST)
    bx0, by0, bx1, by1 = cx - 40, y0 + 2, cx + 118, y1 - 2
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=6, fill=CARD,
                           outline=RUST, width=3)
    draw.rounded_rectangle([bx0, by0, bx1, by0 + 20], radius=6, fill=RUST)
    draw.rectangle([bx0, by0 + 12, bx1, by0 + 20], fill=RUST)
    # Big "1" for the first day, plus a small grid of day cells.
    f_day = font("NotoSans-Black.ttf", 32)
    draw.text((bx0 + 12, by0 + 20), "1", font=f_day, fill=INK)
    for r in range(2):
        for c in range(4):
            gx = bx0 + 52 + c * 22
            gy = by0 + 28 + r * 16
            draw.rectangle([gx, gy, gx + 14, gy + 10], outline=MUTED,
                           width=2)


def motif_voyager(draw, x0, y0, x1, y1):
    """A dish antenna sending radio waves outwards: one-way signal travel.
    The wavefronts are flat ellipses so they stay inside the strip and
    never touch the text above."""
    cy = (y0 + y1) / 2
    fx = x0 + 70  # feed point of the dish
    # Dish: a shallow bowl opening to the right, with a body behind it.
    draw.arc([fx - 44, cy - 26, fx + 8, cy + 26], start=270, end=90,
             fill=SPACE_BLUE, width=5)
    draw.line([(fx - 8, cy - 20), (fx, cy)], fill=SPACE_BLUE, width=3)
    draw.line([(fx - 8, cy + 20), (fx, cy)], fill=SPACE_BLUE, width=3)
    draw.ellipse([fx - 4, cy - 4, fx + 4, cy + 4], fill=SPACE_BLUE)
    draw.rectangle([fx - 58, cy - 8, fx - 44, cy + 8], fill=INK)
    draw.line([(fx - 44, cy), (fx - 26, cy)], fill=INK, width=3)
    # Expanding wavefronts, fading with distance: flat ellipses, only the
    # right-hand cap, so the tallest stays inside the strip.
    for r, col in ((60, (46, 95, 138)), (120, (84, 130, 168)),
                   (180, (122, 163, 194)), (235, (160, 192, 214))):
        ry = int(r * 0.30)
        draw.arc([fx - r, cy - ry, fx + r, cy + ry], start=335, end=25,
                 fill=col, width=4)
    # A few distant stars.
    for sx, sy in ((x1 - 60, y0 + 12), (x1 - 110, y1 - 14), (x1 - 30, y1 - 26)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=MUTED)


def motif_hayabusa(draw, x0, y0, x1, y1):
    """A boxy probe on a dashed approach line that TERMINATES (red X) short
    of the asteroid: the landing plan was dropped, the probe is intact."""
    cy = (y0 + y1) / 2
    px = x0 + 30
    # Probe body with two solar panels: deliberately boxy, not a dish.
    draw.rectangle([px, cy - 12, px + 26, cy + 12], fill=INK)
    draw.rectangle([px - 26, cy - 18, px - 2, cy + 18], fill=SPACE_BLUE,
                   outline=INK, width=2)
    draw.rectangle([px + 28, cy - 18, px + 52, cy + 18], fill=SPACE_BLUE,
                   outline=INK, width=2)
    # Asteroid: fixed irregular rock, right side.
    ax, ay = x1 - 66, cy
    rock = [(ax - 34, ay - 18), (ax - 10, ay - 30), (ax + 18, ay - 26),
            (ax + 36, ay - 8), (ax + 30, ay + 16), (ax + 6, ay + 30),
            (ax - 22, ay + 26), (ax - 38, ay + 6)]
    # Dashed approach line from the probe towards the asteroid, stopping
    # well short of it.
    lx0, lx1 = px + 58, ax - 62
    step, dash = 14, 8
    x = lx0
    while x < lx1:
        draw.line([(x, cy), (min(x + dash, lx1), cy)], fill=MUTED, width=3)
        x += step
    draw.polygon(rock, fill=ROCK, outline=ROCK_DARK)
    for cxr, cyr, rr in ((ax - 12, ay - 6, 6), (ax + 12, ay + 8, 5),
                         (ax + 2, ay - 16, 4)):
        draw.ellipse([cxr - rr, cyr - rr, cxr + rr, cyr + rr],
                     fill=ROCK_DARK)
    # Termination mark: a red X where the approach line ends.
    tx, ty = lx1 + 6, cy
    draw.line([(tx - 9, ty - 9), (tx + 9, ty + 9)], fill=RED, width=5)
    draw.line([(tx - 9, ty + 9), (tx + 9, ty - 9)], fill=RED, width=5)


def motif_korea(draw, x0, y0, x1, y1):
    """A courthouse pediment over columns: the Supreme Court."""
    cx = (x0 + x1) / 2
    top, base = y0 + 6, y1 - 6
    # Pediment.
    draw.polygon([(cx - 84, top + 22), (cx, top), (cx + 84, top + 22)],
                 fill=GREEN)
    draw.rectangle([cx - 84, top + 22, cx + 84, top + 28], fill=GREEN)
    # Columns.
    for i in range(4):
        col_x = cx - 66 + i * 44
        draw.rectangle([col_x, top + 32, col_x + 12, base - 8], fill=GREEN)
    # Base.
    draw.rectangle([cx - 84, base - 8, cx + 84, base - 2], fill=GREEN)


# ------------------------------------------------------------- brief cards

def draw_brief(draw, x0, y0, accent, subject, headlines, subline, motif,
               head_size=40, sub_size=24):
    x1, y1 = x0 + 476, y0 + 238
    card(draw, x0, y0, x1, y1)
    tx = x0 + 24
    # Accent chip + subject line.
    draw.rounded_rectangle([tx, y0 + 28, tx + 12, y0 + 40], radius=2,
                           fill=accent)
    f_subj = font("NotoSans-Bold.ttf", 28)
    draw.text((tx + 22, y0 + 18), subject, font=f_subj, fill=INK)
    # Headline lines, fitted to the card width.
    max_w = 428
    head_y = y0 + 56
    head_gap = head_size + 6
    for i, (line, color) in enumerate(headlines):
        f = fit(line, "NotoSans-Black.ttf", head_size, max_w)
        draw.text((tx, head_y + i * head_gap), line, font=f, fill=color)
    # Subline sits right under the last headline; the motif strip starts
    # below it (or at the default offset when there is no subline).
    motif_top = y0 + 158
    if subline:
        sub_y = head_y + len(headlines) * head_gap + 4
        f_sub = font("NotoSans-Regular.ttf", sub_size)
        draw.text((tx, sub_y), subline, font=f_sub, fill=MUTED)
        motif_top = max(motif_top, sub_y + sub_size + 12)
    motif(draw, x0 + 24, motif_top, x1 - 24, y1 - 14)


def draw_briefs(draw):
    cols = (28, 520)
    rows = (508, 758)
    draw_brief(draw, cols[0], rows[0], RUST, "TRUMP / IRAN",
               [("STRIKE DECISION", INK), ("AFTER JAN 1, 2027", RUST)],
               None, motif_iran)
    draw_brief(draw, cols[1], rows[0], SPACE_BLUE, "VOYAGER 1",
               [("24 HOURS ONE WAY", INK)],
               "Radio signals now take one day", motif_voyager)
    draw_brief(draw, cols[0], rows[1], ROCK_DARK, "HAYABUSA2",
               [("DROPS ASTEROID", INK), ("LANDING PLAN", INK)],
               "Engine trouble", motif_hayabusa, head_size=34, sub_size=22)
    draw_brief(draw, cols[1], rows[1], GREEN, "HAN DUCK-SOO",
               [("CONVICTION OVERTURNED", INK)],
               "South Korea's Supreme Court", motif_korea)


# ------------------------------------------------------------------ main

def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_band(draw)
    draw_lead(draw)
    draw_briefs(draw)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
