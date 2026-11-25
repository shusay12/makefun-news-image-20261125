#!/usr/bin/env python3
"""Render the news-image-20261125 front page (1024x1024 PNG).

Draws a newspaper front page, "THE WORLD IN ONE DAY", summing up
Wednesday 25 November 2026 from stories verified by web search in the
build session (early edition, ~02:00 UTC):

  1. LEAD: a new analysis finds more than 700,000 Russian soldiers
     killed in the war in Ukraine (RFE/RL, first reported 25 Nov 2026).
  2. Trump meets NATO chief Mark Rutte in Palm Beach, Florida, late
     this afternoon (White House, announced 23 Nov; meeting on 25 Nov).
  3. World Chess Championship, Geneva: Game 2 today, 15:00 CET,
     Gukesh (White) vs Sindarov; Game 1 drawn in 38 moves, 0.5-0.5.

Deterministic: fixed fonts, fixed colours, no timestamps, no random
numbers, so re-running this script reproduces the same bytes.
Standard library + Pillow only. Run: python3 build_image.py [out.png]
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (18, 33, 61)
NAVY_DARK = (10, 20, 40)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
GREY = (90, 90, 90)
PANEL = (255, 255, 255)
RULE = (180, 175, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_cross(draw, cx, cy, s, fill):
    """A small memorial cross centred at (cx, cy), size s."""
    w = max(2, s // 5)
    draw.rectangle([cx - w // 2, cy - s // 2, cx + w // 2, cy + s // 2], fill=fill)
    draw.rectangle([cx - s // 2, cy - s // 4, cx + s // 2, cy + s // 4], fill=fill)


def draw_chessboard(draw, x0, y0, sq):
    """8x8 board with a few pieces (white king, black queen, pawns)."""
    light, dark = (240, 217, 181), (181, 136, 99)
    for r in range(8):
        for c in range(8):
            col = light if (r + c) % 2 == 0 else dark
            draw.rectangle([x0 + c * sq, y0 + r * sq,
                            x0 + (c + 1) * sq, y0 + (r + 1) * sq], fill=col)
    # pieces: simple discs with a letter
    pieces = {(3, 7): ("K", (255, 255, 255)), (3, 0): ("Q", (30, 30, 30)),
              (4, 6): ("P", (255, 255, 255)), (4, 1): ("P", (30, 30, 30))}
    pf = font(SANS_B, int(sq * 0.62))
    for (c, r), (ch, col) in pieces.items():
        cx, cy = x0 + c * sq + sq // 2, y0 + r * sq + sq // 2
        rad = int(sq * 0.36)
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                     fill=col, outline=(60, 60, 60), width=2)
        tw = draw.textlength(ch, font=pf)
        th = pf.size
        tcol = (20, 20, 20) if col == (255, 255, 255) else (240, 240, 240)
        draw.text((cx - tw / 2, cy - th / 2 - 1), ch, font=pf, fill=tcol)


def draw_us_flag(draw, x0, y0, w, h):
    """Simplified US flag: 13 stripes + blue canton with star dots."""
    stripe = h / 13
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x0, y0 + i * stripe, x0 + w, y0 + (i + 1) * stripe],
                       fill=col)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x0, y0, x0 + cw, y0 + ch], fill=(60, 59, 110))
    sf = font(SANS_B, 10)
    for r in range(4):
        for c in range(5):
            sx = x0 + 8 + c * (cw - 14) / 4
            sy = y0 + 7 + r * (ch - 14) / 3
            draw.text((sx, sy), "*", font=sf, fill=(255, 255, 255))


def draw_nato_star(draw, cx, cy, r, fill):
    """NATO compass rose: four-point star."""
    pts = []
    for i in range(8):
        ang = -90 + i * 45
        rr = r if i % 2 == 0 else r * 0.28
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    draw.polygon(pts, fill=fill)
    draw.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16],
                 fill=fill)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.rectangle([0, 132, W, 138], fill=GOLD)
    f_mast = font(SERIF_B, 58)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 14), t,
           font=f_mast, fill=(255, 255, 255))
    f_date = font(SANS_B, 26)
    t = "WEDNESDAY  25  NOVEMBER  2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 72), t,
           font=f_date, fill=GOLD)
    f_ed = font(SANS, 15)
    t = "EARLY EDITION  —  VERIFIED 02:00 UTC"
    d.text(((W - d.textlength(t, font=f_ed)) / 2, 104), t,
           font=f_ed, fill=(200, 205, 220))

    # ---- lead story ----------------------------------------------
    lx, ly, lw, lh = 24, 156, 976, 420
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=NAVY_DARK)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=GOLD, width=3)
    # memorial crosses along the bottom of the lead panel
    horizon = ly + lh - 78
    d.rectangle([lx, horizon, lx + lw, ly + lh], fill=(8, 16, 34))
    d.line([lx, horizon, lx + lw, horizon], fill=(70, 80, 110), width=2)
    for i, cx in enumerate(range(lx + 60, lx + lw - 40, 64)):
        s = 30 if i % 3 else 40
        draw_cross(d, cx, horizon + 50, s, (150, 155, 175))
    # lead kicker + headline
    f_kick = font(SANS_B, 20)
    d.text((lx + 28, ly + 22), "UKRAINE  •  THE WAR'S TOLL",
           font=f_kick, fill=GOLD)
    f_head = font(SERIF_B, 56)
    y = draw_wrapped(d, lx + 28, ly + 56,
                     "MORE THAN 700,000",
                     f_head, lw - 56, (255, 255, 255), leading=60)
    y = draw_wrapped(d, lx + 28, y + 2,
                     "RUSSIAN SOLDIERS KILLED",
                     f_head, lw - 56, (255, 255, 255), leading=60)
    f_sub = font(SERIF, 25)
    y = draw_wrapped(d, lx + 28, y + 14,
                     "A new analysis puts Moscow's military dead past "
                     "700,000 in the nearly five-year war in Ukraine — a "
                     "staggering toll, first reported today.",
                     f_sub, lw - 56, (225, 228, 238), leading=33)
    f_src = font(SANS, 15)
    d.text((lx + 28, y + 8),
           "Source: RFE/RL analysis, 25 Nov 2026, 01:00 UTC",
           font=f_src, fill=(170, 175, 195))
    f_day = font(SANS_B, 17)
    t = "DAY 1,735 OF THE WAR  —  SINCE 24 FEBRUARY 2022"
    d.text((lx + lw - 28 - d.textlength(t, font=f_day), y + 6), t,
           font=f_day, fill=GOLD)

    # ---- two lower panels -----------------------------------------
    py, ph = 594, 346
    pw = 478
    # --- left: Trump / Rutte
    x0 = 24
    d.rectangle([x0, py, x0 + pw, py + ph], fill=PANEL, outline=RULE, width=2)
    d.rectangle([x0, py, x0 + pw, py + 8], fill=RED)
    draw_us_flag(d, x0 + 24, py + 30, 150, 78)
    # NATO blue circle with compass star
    cx, cy, r = x0 + 250, py + 69, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 51, 153))
    draw_nato_star(d, cx, cy, 34, (255, 255, 255))
    d.text((x0 + 330, py + 44), "NATO", font=font(SANS_B, 26),
           fill=(0, 51, 153))
    f_h2 = font(SERIF_B, 29)
    y = draw_wrapped(d, x0 + 24, py + 128,
                     "TRUMP MEETS NATO CHIEF TODAY",
                     f_h2, pw - 48, INK, leading=33)
    f_body = font(SERIF, 20)
    draw_wrapped(d, x0 + 24, y + 8,
                 "Donald Trump meets Mark Rutte in Palm Beach, Florida, "
                 "late this afternoon — days after his trilateral summit "
                 "with Putin and Xi.",
                 f_body, pw - 48, (40, 40, 40), leading=26)
    # --- right: chess
    x1 = 522
    d.rectangle([x1, py, x1 + pw, py + ph], fill=PANEL, outline=RULE, width=2)
    d.rectangle([x1, py, x1 + pw, py + 8], fill=NAVY)
    draw_chessboard(d, x1 + 24, py + 26, 16)
    d.text((x1 + 176, py + 30), "GENEVA", font=font(SANS_B, 24), fill=NAVY)
    d.text((x1 + 176, py + 62), "GAME 2  •  15:00 CET",
           font=font(SANS, 19), fill=GREY)
    d.text((x1 + 176, py + 88), "SCORE  0.5 – 0.5",
           font=font(SANS_B, 19), fill=INK)
    y = draw_wrapped(d, x1 + 24, py + 168,
                     "CHESS: GAME 2 IN GENEVA TODAY",
                     f_h2, pw - 48, INK, leading=33)
    draw_wrapped(d, x1 + 24, y + 8,
                 "Gukesh has White against Sindarov after Game 1 was "
                 "drawn in 38 moves on Tuesday.",
                 f_body, pw - 48, (40, 40, 40), leading=26)

    # ---- footer ----------------------------------------------------
    fy = 956
    d.line([24, fy, W - 24, fy], fill=RULE, width=2)
    f_foot = font(SANS, 17)
    draw_wrapped(d, 24, fy + 10,
                 "Every event above happened, or was first reported, on "
                 "Wednesday 25 November 2026. Early edition: the day is "
                 "only two hours old in UTC — its later news is still to come.",
                 f_foot, W - 48, GREY, leading=22)

    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = render()
    img.save(out, format="PNG", optimize=True)
    print(out, img.size)
