#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: one 1024x1024 front-page summary of
Monday 23 November 2026, drawn from the day's verified headlines.

Stories (all reported on 23 Nov 2026, verified against live news sources):
 1. Democrats win largest House majority since 1992 (258+ seats, NC recount)
 2. COP31 climate talks in Antalya end with no fossil-fuel deal
 3. Delta outage delays 1,600+ flights as Thanksgiving travel begins
 4. Trump signs the Common Cents Act; the penny ends after 232 years
 5. Asian stocks slide on AI-boom fears
 6. Russian cargo ship Sparta II ablaze in the Baltic, drifts to Finland
 7. Alcaraz beats Zverev for his first ATP Finals title

Everything is drawn with PIL primitives (no photos, no stock, no network).
Run: python3 gen_image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (14, 42, 71)
NAVY_LT = (27, 68, 106)
GOLD = (217, 164, 65)
RED = (178, 44, 36)
TEAL = (31, 122, 109)
SKY = (127, 179, 213)
SKY_LT = (214, 233, 244)
CARD = (255, 255, 255)
GREY = (110, 110, 105)
LINE = (200, 192, 175)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def kicker(draw, x, y, label, color):
    f = font(SANS_B, 21)
    tw = draw.textlength(label, font=f) + 18
    draw.rounded_rectangle([x, y, x + tw, y + 30], radius=4, fill=color)
    draw.text((x + 9, y + 4), label, font=f, fill=(255, 255, 255))


def icon_disc(draw, cx, cy, r, bg):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)


def icon_capitol(d, cx, cy, r):
    icon_disc(d, cx, cy, r, SKY_LT)
    d.pieslice([cx - r * 0.52, cy - r * 0.62, cx + r * 0.52, cy + r * 0.28],
               start=180, end=360, fill=NAVY)
    d.rectangle([cx - r * 0.52, cy - r * 0.18, cx + r * 0.52, cy - r * 0.02], fill=NAVY)
    for i in range(-2, 3):
        x0 = cx + i * r * 0.20 - r * 0.055
        d.rectangle([x0, cy - r * 0.02, x0 + r * 0.11, cy + r * 0.42], fill=NAVY)
    d.rectangle([cx - r * 0.62, cy + r * 0.42, cx + r * 0.62, cy + r * 0.54], fill=NAVY)
    d.rectangle([cx - r * 0.70, cy + r * 0.54, cx + r * 0.70, cy + r * 0.62], fill=NAVY)
    d.line([cx, cy - r * 0.92, cx, cy - r * 0.62], fill=RED, width=4)
    d.polygon([(cx, cy - r * 0.92), (cx + r * 0.22, cy - r * 0.86), (cx, cy - r * 0.80)], fill=RED)


def icon_globe(d, cx, cy, r):
    icon_disc(d, cx, cy, r, (46, 134, 193))
    d.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05], fill=(46, 160, 90))
    d.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.60, cy + r * 0.58], fill=(46, 160, 90))
    d.ellipse([cx + r * 0.28, cy - r * 0.62, cx + r * 0.62, cy - r * 0.22], fill=(46, 160, 90))
    d.line([cx - r * 0.55, cy + r * 0.55, cx + r * 0.55, cy - r * 0.55], fill=RED, width=7)


def icon_plane(d, cx, cy, r):
    """Side-view airliner on a sky disc."""
    icon_disc(d, cx, cy, r, SKY_LT)
    # fuselage
    d.rounded_rectangle([cx - r * 0.72, cy - r * 0.18, cx + r * 0.72, cy + r * 0.14],
                        radius=int(r * 0.16), fill=NAVY)
    # nose
    d.polygon([(cx + r * 0.55, cy - r * 0.18), (cx + r * 0.85, cy - r * 0.02),
               (cx + r * 0.55, cy + r * 0.14)], fill=NAVY)
    # tail fin
    d.polygon([(cx - r * 0.62, cy - r * 0.18), (cx - r * 0.78, cy - r * 0.62),
               (cx - r * 0.45, cy - r * 0.18)], fill=NAVY)
    # wing
    d.polygon([(cx - r * 0.05, cy + r * 0.10), (cx + r * 0.18, cy + r * 0.55),
               (cx + r * 0.38, cy + r * 0.55), (cx + r * 0.22, cy + r * 0.10)], fill=NAVY)
    # windows
    for i in range(4):
        wx = cx - r * 0.42 + i * r * 0.22
        d.ellipse([wx, cy - r * 0.10, wx + r * 0.09, cy - r * 0.01], fill=(255, 255, 255))


def icon_penny(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(184, 115, 51))
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82],
              outline=(232, 190, 130), width=4)
    f = font(SANS_B, int(r * 0.72))
    draw_center(d, cx, cy - r * 0.42, "1¢", f, (255, 255, 255))
    f2 = font(SANS_B, int(r * 0.22))
    draw_center(d, cx, cy + r * 0.30, "1793–2026", f2, (255, 240, 210))


def icon_chart(d, cx, cy, r):
    icon_disc(d, cx, cy, r, (252, 228, 228))
    vals = [0.78, 0.60, 0.66, 0.42, 0.48, 0.22]
    bw = r * 1.5 / len(vals)
    for i, v in enumerate(vals):
        x0 = cx - r * 0.75 + i * bw + 2
        d.rectangle([x0, cy + r * 0.55 - v * r * 1.0, x0 + bw - 5, cy + r * 0.55], fill=RED)
    d.line([cx - r * 0.7, cy - r * 0.55, cx + r * 0.7, cy - r * 0.05], fill=NAVY, width=6)
    d.polygon([(cx + r * 0.7, cy - r * 0.05), (cx + r * 0.38, cy - r * 0.10),
               (cx + r * 0.62, cy + r * 0.22)], fill=NAVY)


def icon_ship(d, cx, cy, r):
    icon_disc(d, cx, cy, r, SKY_LT)
    # flame above deck
    d.polygon([(cx + r * 0.05, cy - r * 0.30), (cx + r * 0.28, cy - r * 0.80),
               (cx + r * 0.52, cy - r * 0.30)], fill=(230, 120, 30))
    d.ellipse([cx - r * 0.38, cy - r * 0.72, cx - r * 0.08, cy - r * 0.42], fill=(120, 120, 120))
    # hull
    d.polygon([(cx - r * 0.72, cy + r * 0.05), (cx + r * 0.72, cy + r * 0.05),
               (cx + r * 0.55, cy + r * 0.48), (cx - r * 0.55, cy + r * 0.48)], fill=NAVY)
    # containers
    d.rectangle([cx - r * 0.45, cy - r * 0.22, cx - r * 0.15, cy + r * 0.05], fill=RED)
    d.rectangle([cx - r * 0.10, cy - r * 0.22, cx + r * 0.20, cy + r * 0.05], fill=GOLD)
    # waves
    for yy in (cy + r * 0.62, cy + r * 0.78):
        d.arc([cx - r * 0.8, yy - 12, cx - r * 0.2, yy + 12], 180, 360, fill=NAVY_LT, width=4)
        d.arc([cx - r * 0.1, yy - 12, cx + r * 0.5, yy + 12], 180, 360, fill=NAVY_LT, width=4)


def icon_tennis(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 214, 60))
    # classic )( seams
    d.arc([cx - r, cy - r, cx + r * 0.30, cy + r], 270, 90, fill=(255, 255, 255), width=7)
    d.arc([cx - r * 0.30, cy - r, cx + r, cy + r], 90, 270, fill=(255, 255, 255), width=7)


def story_card(d, x, y, w, h, kicker_label, kicker_color, headline, caption, icon_fn,
               headline_size=28, icon_r=32, caption_size=20):
    """Card with kicker + small icon on the top row, headline and caption
    spanning the full card width below (no text/icon overlap)."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE, width=2)
    pad = 22
    icon_fn(d, x + w - 52, y + 34, icon_r)
    kicker(d, x + pad, y + 16, kicker_label, kicker_color)
    tx = x + pad
    tw = w - 2 * pad
    hf = font(SANS_B, headline_size)
    lines = wrap(d, headline, hf, tw)
    ly = y + 58
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=hf, fill=INK)
        ly += headline_size + 5
    cf = font(SANS, caption_size)
    for ln in wrap(d, caption, cf, tw)[:2]:
        d.text((tx, ly + 4), ln, font=cf, fill=GREY)
        ly += caption_size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 166], fill=GOLD)
    draw_center(d, W // 2, 18, "THE WORLD IN ONE DAY", font(SERIF_B, 58), (255, 255, 255))
    draw_center(d, W // 2, 96, "M O N D A Y   2 3   N O V E M B E R   2 0 2 6",
                font(SANS_B, 28), GOLD)

    # ---- lead story ----
    lx, ly, lw, lh = 28, 182, W - 56, 246
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly + 10, lx + 10, ly + lh - 10], fill=RED)
    kicker(d, lx + 30, ly + 16, "UNITED STATES", RED)
    icon_capitol(d, lx + lw - 108, ly + 122, 80)
    hf = font(SANS_B, 42)
    lines = wrap(d, "DEMOCRATS WIN BIGGEST HOUSE MAJORITY SINCE 1992", hf, lw - 280)
    y = ly + 54
    for ln in lines:
        d.text((lx + 30, y), ln, font=hf, fill=INK)
        y += 50
    cf = font(SANS, 24)
    for ln in wrap(d, "Recount win in North Carolina: at least 258 seats.",
                   cf, lw - 280):
        d.text((lx + 30, y + 4), ln, font=cf, fill=GREY)
        y += 30

    # ---- grid rows ----
    gw = (W - 56 - 20) // 2  # 474
    story_card(d, 28, 444, gw, 192, "CLIMATE", TEAL,
               "COP31 ENDS WITH NO FOSSIL-FUEL DEAL",
               "Two weeks of talks in Antalya close without a finance pact.", icon_globe)
    story_card(d, 28 + gw + 20, 444, gw, 192, "TRAVEL", NAVY_LT,
               "DELTA OUTAGE DELAYS 1,600 FLIGHTS",
               "Weight-and-balance failure hits Atlanta as Thanksgiving travel begins.", icon_plane)
    story_card(d, 28, 652, gw, 192, "ECONOMY", (150, 90, 20),
               "THE PENNY ENDS AFTER 232 YEARS",
               "Trump signs the Common Cents Act into law.", icon_penny)
    story_card(d, 28 + gw + 20, 652, gw, 192, "MARKETS", RED,
               "ASIAN STOCKS SLIDE ON AI FEARS",
               "Indexes fall sharply as doubts grow over the AI boom.", icon_chart)

    # ---- bottom row (slim cards, one-line headlines) ----
    story_card(d, 28, 860, gw, 136, "WAR", NAVY,
               "RUSSIAN SHIP ABLAZE",
               "Sparta II drifts into Finnish waters.", icon_ship,
               headline_size=27, icon_r=30)
    story_card(d, 28 + gw + 20, 860, gw, 136, "SPORT", (90, 130, 40),
               "ALCARAZ WINS ATP FINALS",
               "Beats Zverev in straight sets.", icon_tennis,
               headline_size=27, icon_r=30)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
