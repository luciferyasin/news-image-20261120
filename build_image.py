#!/usr/bin/env python3
"""BBC-style front page for 20 Nov 2026 — REAL PHOTOS version (v2).

v2: Riyadh strip photo cropped tight on the bent PIF Tower facade so the
damage reads; Riyadh headline reworded to the verified AP wording
("fire more missiles") after the "decisive response" quote could not be
tied to 20 November reporting.

Layout approach: masthead + date + red rule; hero photo ~55% of the page
with a dark scrim and the headline overlaid at the bottom; three-column
photo strip underneath; single-line footer with photo credits and sources.

All four pictures are REAL news photographs, all from 20 Nov 2026 coverage:
  hero  = Kyiv bridge wreckage after the overnight missile/drone attack
          (sfg.media share photo of the Podilsko-Voskresenskyi Bridge);
  strip = PIF Tower damage in Riyadh (Saudi Press Agency photo, via ABS-CBN);
          GTA VI launch-night crowd in Miami (AFP photo, via Bangkok Post);
          CGIL general-strike protest in Italy (Reuters photo).

Palette: pure white, near-black #202224, BBC red #BB1919, hairline rules.
No gradients on the chrome, no shadows, no AI-generated imagery.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
DIR = "/home/hatch/workspace/makefun/entries/news-image-20261120"
PHOTOS = f"{DIR}/real_photos"

NOTO_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
NOTO = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

WHITE = (255, 255, 255)
INK = (32, 34, 36)        # near-black #202224
RED = (187, 25, 25)       # BBC red #BB1919
RULE = (230, 230, 230)    # hairline #E6E6E6
MUTED = (90, 90, 90)      # footer grey
BLACK = (0, 0, 0)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines=2):
    """Shrink the font until the text wraps to at most max_lines lines."""
    while size > 12:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    return font(path, 12), wrap(draw, text, font(path, 12), max_w)


def cover(path, w, h, cy=0.5, cx=0.5, box=None):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:
        nw = int(ih * target)
        x0 = int((iw - nw) * cx)
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target)
        y0 = int((ih - nh) * cy)
        y0 = max(0, min(ih - nh, y0))
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def pill(d, x, y, text, fnt, fill, fg):
    tw = int(d.textlength(text, font=fnt)) + 24
    d.rounded_rectangle([x, y, x + tw, y + 26], radius=13, fill=fill)
    d.text((x + tw // 2, y + 13), text, font=fnt, fill=fg, anchor="mm")
    return tw


# ---- stories (all verified as 20 November 2026) ----
hero = ("kyiv_sfg.jpg",
        "KYIV  ·  UKRAINE",
        "Russia strikes Kyiv\u2019s bridges in biggest attack yet",
        "Three killed and 15 injured as missiles and drones hit three "
        "crossings over the Dnipro.")

strip = [
    # (photo, tag, headline, source crop box or None)
    # PIF Tower: crop tight on the bent, blown-out facade (right face,
    # upper half of the frame) so the damage, not just a tower, is visible.
    ("houthi_pif.jpg",
     "RIYADH  ·  MIDDLE EAST",
     "Houthis fire more missiles at Saudi Arabia",
     (600, 120, 1200, 620)),
    ("gta_miami.jpg",
     "GAMES  ·  TECH",
     "GTA VI \u2018sold $2.36bn on day one\u2019, estimate says",
     None),
    ("italy_protest.jpg",
     "EUROPE  ·  PROTEST",
     "Youth strike sweeps 25 countries in Europe",
     None),
]

# ---- canvas: pure white ----
img = Image.new("RGBA", (W, H), WHITE + (255,))
d = ImageDraw.Draw(img)

# ---- masthead + date + red rule ----
d.text((W // 2, 40), "T H E   W O R L D   T O D A Y",
       font=font(NOTO_B, 26), fill=RED, anchor="mm")
d.text((W // 2, 86), "FRIDAY,  20  NOVEMBER  2026",
       font=font(NOTO_B, 38), fill=INK, anchor="mm")
d.line([36, 118, W - 36, 118], fill=RED, width=3)

# ---- HERO: 952 x 560 = 55% of the page ----
HX, HY, HW, HH = 36, 136, 952, 560
hero_im = cover(f"{PHOTOS}/{hero[0]}", HW, HH, cy=0.42, cx=0.45).convert("RGBA")
grad_h = 170
grad = Image.new("RGBA", (HW, grad_h), (0, 0, 0, 0))
gd = ImageDraw.Draw(grad)
for i in range(grad_h):
    a = int(220 * (i / grad_h) ** 1.4)
    gd.line([(0, i), (HW, i)], fill=BLACK + (a,))
hero_im.alpha_composite(grad, (0, HH - grad_h))
img.paste(hero_im, (HX, HY))

# hero text, anchored from the bottom of the image
dek_y = HY + HH - 42
d.text((HX + 28, dek_y), hero[3], font=font(NOTO, 17), fill=(235, 235, 235))
head_fnt, head_lines = fit_lines(d, hero[2], NOTO_B, 30, HW - 56, max_lines=2)
hy = dek_y - 14 - 34 * len(head_lines)
for ln in head_lines:
    d.text((HX + 28, hy), ln, font=head_fnt, fill=WHITE)
    hy += 34
pill(d, HX + 28, hy - 34 - 40, hero[1], font(NOTO_B, 15), RED, WHITE)

# ---- BOTTOM STRIP: 3 columns, hairline dividers ----
CELL_W, GAP, STRIP_Y = 306, 17, 726
IMG_H = 150
f_tag = font(NOTO_B, 12)
for b in (350, 673):
    d.line([(b, STRIP_Y), (b, STRIP_Y + IMG_H + 84)], fill=RULE, width=1)
for idx, (pic, tag, head, box) in enumerate(strip):
    cx = 36 + idx * (CELL_W + GAP)
    pic_im = cover(f"{PHOTOS}/{pic}", CELL_W, IMG_H, cy=0.5, box=box)
    img.paste(pic_im, (cx, STRIP_Y))
    d.text((cx, STRIP_Y + IMG_H + 14), tag, font=f_tag, fill=RED)
    f_head, lines = fit_lines(d, head, NOTO_B, 17, CELL_W, max_lines=2)
    hy = STRIP_Y + IMG_H + 36
    for ln in lines[:2]:
        d.text((cx, hy), ln, font=f_head, fill=INK)
        hy += 22

# ---- footer ----
d.text((W // 2, 990),
       "Photos: sfg.media  \u00b7  Reuters  \u00b7  AFP  \u00b7  Saudi Press Agency"
       "   \u2014   Sources: Reuters  \u00b7  AP  \u00b7  AFP  \u00b7  Sensor Tower",
       font=font(NOTO, 13), fill=MUTED, anchor="mm")

out = img.convert("RGB")
# JPEG (rules allow PNG or JPEG by first bytes, name stays entry.png).
out.save(f"{DIR}/entry.png", "JPEG", quality=90, optimize=True)
print("saved", f"{DIR}/entry.png")
print("bytes:", os.path.getsize(f"{DIR}/entry.png"))
print("size:", out.size)
print("hero share: 560/1024 = %.1f%%" % (560 / 1024 * 100))
