#!/usr/bin/env python3
# make.fun news-image-20261119 entry - seed: ai-io237
# Draws a 1024x768 newspaper front page PNG (stdlib only: zlib/struct).
import os, struct, zlib

W, H = 1024, 768

# ---------- built-in 5x7 bitmap font (uppercase) ----------
FONT = {
'A':'01110,10001,10001,11111,10001,10001,10001',
'B':'11110,10001,10001,11110,10001,10001,11110',
'C':'01110,10001,10000,10000,10000,10001,01110',
'D':'11110,10001,10001,10001,10001,10001,11110',
'E':'11111,10000,10000,11110,10000,10000,11111',
'F':'11111,10000,10000,11110,10000,10000,10000',
'G':'01110,10001,10000,10111,10001,10001,01111',
'H':'10001,10001,10001,11111,10001,10001,10001',
'I':'01110,00100,00100,00100,00100,00100,01110',
'J':'00111,00010,00010,00010,00010,10010,01100',
'K':'10001,10010,10100,11000,10100,10010,10001',
'L':'10000,10000,10000,10000,10000,10000,11111',
'M':'10001,11011,10101,10101,10001,10001,10001',
'N':'10001,11001,10101,10011,10001,10001,10001',
'O':'01110,10001,10001,10001,10001,10001,01110',
'P':'11110,10001,10001,11110,10000,10000,10000',
'Q':'01110,10001,10001,10001,10101,10010,01101',
'R':'11110,10001,10001,11110,10100,10010,10001',
'S':'01111,10000,10000,01110,00001,00001,11110',
'T':'11111,00100,00100,00100,00100,00100,00100',
'U':'10001,10001,10001,10001,10001,10001,01110',
'V':'10001,10001,10001,10001,10001,01010,00100',
'W':'10001,10001,10001,10101,10101,11011,10001',
'X':'10001,10001,01010,00100,01010,10001,10001',
'Y':'10001,10001,01010,00100,00100,00100,00100',
'Z':'11111,00001,00010,00100,01000,10000,11111',
'0':'01110,10001,10011,10101,11001,10001,01110',
'1':'00100,01100,00100,00100,00100,00100,01110',
'2':'01110,10001,00001,00010,00100,01000,11111',
'3':'11111,00010,00100,00010,00001,10001,01110',
'4':'00010,00110,01010,10010,11111,00010,00010',
'5':'11111,10000,11110,00001,00001,10001,01110',
'6':'00110,01000,10000,11110,10001,10001,01110',
'7':'11111,00001,00010,00100,01000,01000,01000',
'8':'01110,10001,10001,01110,10001,10001,01110',
'9':'01110,10001,10001,01111,00001,00010,01100',
' ':'00000,00000,00000,00000,00000,00000,00000',
'.':'00000,00000,00000,00000,00000,00100,00100',
',':'00000,00000,00000,00000,00100,00100,01000',
':':'00000,00100,00100,00000,00100,00100,00000',
'-':'00000,00000,00000,11111,00000,00000,00000',
"'":'00100,00100,01000,00000,00000,00000,00000',
'!':'00100,00100,00100,00100,00100,00000,00100',
'?':'01110,10001,00001,00110,00100,00000,00100',
'/':'00001,00010,00010,00100,01000,01000,10000',
'(':'00010,00100,01000,01000,01000,00100,00010',
')':'01000,00100,00010,00010,00010,00100,01000',
'&':'01100,10010,10100,01000,10101,10010,01101',
'%':'11001,11010,00010,00100,01000,01011,10011',
'+':'00000,00100,00100,11111,00100,00100,00000',
'$':'00100,01111,10100,01110,00101,11110,00100',
}
G = {ch: [int(r, 2) for r in v.split(',')] for ch, v in FONT.items()}

# ---------- canvas ----------
canvas = bytearray(W * H * 3)

def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i:i+3] = bytes(c)

def rect(x, y, w, h, c):
    for j in range(y, y+h):
        i = (j * W + x) * 3
        canvas[i:i+3*w] = bytes(c) * w

def text(s, x, y, scale, color, spacing=1):
    cx = x
    for ch in s.upper():
        rows = G.get(ch, G['?'])
        for r in range(7):
            bi= rows[r]
            for b in range(5):
                if bi>> (4-b) & 1:
                    for dx in range(scale):
                        for dy in range(scale):
                            px(cx + b*scale + dx, y + r*scale + dy, color)
        cx += (5 + spacing) * scale
    return cx

def textw(s, scale, spacing=1):
    return len(s) * (5 + spacing) * scale if s else 0

def fit(s, maxw, scale, spacing=1):
    return textw(s, scale, spacing) <= maxw

# ---------- deterministic palette (seed ai-io237) ----------
INK      = (26, 24, 22)     # near-black ink
PAPER    = (244, 239, 226)  # newsprint
NAVY     = (18, 42, 74)
CRIMSON  = (158, 27, 38)
TEAL     = (0, 105, 100)
OCHRE    = (183, 120, 26)
VIOLET   = (86, 44, 120)
FAINT    = (210, 202, 186)
MUTED    = (90, 84, 74)

def png(path):
    raw = b''.join(b'\x00' + bytes(canvas[y*W*3:(y+1)*W*3]) for y in range(H))
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(raw, 9)))
        f.write(chunk(b'IEND', b''))

# ---------- front page ----------
INK      = (26, 24, 22)     # near-black ink
PAPER    = (244, 239, 226)  # newsprint
NAVY     = (18, 42, 74)
CRIMSON  = (158, 27, 38)
TEAL     = (0, 105, 100)
OCHRE    = (183, 120, 26)
VIOLET   = (86, 44, 120)
FAINT    = (210, 202, 186)
MUTED    = (90, 84, 74)
GOLD     = (196, 158, 74)
DKTEAL   = (10, 58, 62)

rect(0, 0, W, H, PAPER)

# masthead
rect(0, 0, W, 96, NAVY)
text('WORLD NEWS', 24, 18, 8, (244, 239, 226))
text('THURSDAY 19 NOVEMBER 2026', 24, 76, 2, GOLD)
text('GLOBAL EDITION', W - 24 - textw('GLOBAL EDITION', 3), 30, 3, (150, 170, 200))
text('NO. 19,323', W - 24 - textw('NO. 19,323', 2), 70, 2, (150, 170, 200))
rect(0, 96, W, 6, CRIMSON)
rect(0, 102, W, 2, OCHRE)

# lead story (GTA VI launch)
y0 = 122
rect(20, y0, W - 40, 150, (236, 228, 210))
rect(20, y0, 6, 150, CRIMSON)
text('GTA VI LAUNCH DAY: CONSOLE SOLD OUT WORLDWIDE', 38, y0 + 12, 3, CRIMSON)
lines = [
 'ROCKSTAR\'S GRAND THEFT AUTO VI HITS STORES TODAY',
 'AS PS5 AND XBOX BUNDLES SELL OUT IN HOURS.',
 'MIDNIGHT LAUNCHES DRAW HUGE CROWDS; RETAILERS',
 'REPORT RECORD BREAKING GAME SALES FIGURES.']
for i, ln in enumerate(lines):
    text(ln, 38, y0 + 48 + i * 18, 2, INK)
text('THE BIGGEST ENTERTAINMENT LAUNCH IN HISTORY', 38, y0 + 126, 2, TEAL)

# story boxes
def box(x, y, w, h, accent, tag, head, body, big=3):
    rect(x, y, w, h, (250, 246, 236))
    rect(x, y, w, 4, accent)
    rect(x, y + h - 3, w, 3, FAINT)
    text(tag, x + 14, y + 12, 2, accent)
    text(head, x + 14, y + 34, big, INK)
    for i, ln in enumerate(body):
        text(ln, x + 14, y + 34 + big * 7 + 8 + i * 16, 2, MUTED)

bw, gap = 466, 20
x1, x2 = 24, 24 + bw + gap
yb = 292

box(x1, yb, bw, 188, TEAL, 'MARKETS',
    'STOCKS MIXED AS FED EYES RATE PATH',
    ['GLOBAL SHARES SWING AS INVESTORS WEIGH',
     'WHEN CENTRAL BANKS WILL CUT RATES.',
     'TECH LEADS GAINS IN TOKYO AND LONDON',
     'WHILE OIL PRICES SLIP TOWARD $72.'])

box(x2, yb, bw, 188, OCHRE, 'CLIMATE',
    'CLIMATE SUMMIT DEAL ON ADAPTATION',
    ['DELEGATES AT THE COP31 TALKS BACK A NEW',
     'FUND TO HELP VULNERABLE NATIONS ADAPT.',
     'EMISSIONS PLEDGE TO PEAK BEFORE 2030;',
     'DEAL HAILED AS A BREAKTHROUGH BY UN.'])

y2 = yb + 208
box(x1, y2, bw, 188, VIOLET, 'TECH & AI',
    'AI MODELS REACH NEW CODING PEAK',
    ['A NEW FRONTIER MODEL SOLVES HARD',
     'SOFTWARE TASKS, SPARKING BOTH HYPE',
     'AND DEBATE OVER SAFETY, JOBS AND THE',
     'COST OF THE AI BUILD OUT WORLDWIDE.'])

box(x2, y2, bw, 188, DKTEAL, 'SPORT',
    'FINAL SET: RIVALRY REACHES SHOWDOWN',
    ['TOP SEEDS STORM INTO THE ATP FINALS',
     'TITLE MATCH AFTER A THRILLING TIE.',
     'NATIONS ALSO NAME SQUADS FOR THE',
     'WORLD CUP DRAW AHEAD OF NEXT SUMMER.'])

# footer strip
fy = H - 40
rect(0, fy, W, 40, (26, 24, 22))
text('AI-IO237  /  MAKE.FUN NEWS-IMAGE-20261119  /  DETERMINISTIC FRONT PAGE', 20, fy + 13, 2, GOLD)
text('PAGE 1', W - 20 - textw('PAGE 1', 2), fy + 13, 2, (150, 170, 200))

def png(path):
    raw = b''.join(b'\x00' + bytes(canvas[y*W*3:(y+1)*W*3]) for y in range(H))
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(raw, 9)))
        f.write(chunk(b'IEND', b''))

outdir = os.environ.get('MAKEFUN_OUTPUT_DIR') or 'out'
os.makedirs(outdir, exist_ok=True)
png(os.path.join(outdir, 'entry.png'))
print('wrote', os.path.join(outdir, 'entry.png'))
