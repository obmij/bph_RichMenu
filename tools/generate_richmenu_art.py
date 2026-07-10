from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 2500, 1686
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'richmenu' / 'bph-rich-menu-main-2500x1686.png'

COLORS = {
    'stretch_limo': '#2B2C2F',
    'cloud_dancer': '#F1F0EB',
    'scarlet_smile': '#AE2038',
    'bordeaux': '#9D637E',
    'dragonfly': '#2D6C75',
    'graphite': '#56573D',
    'satin_slipper': '#9A907C',
    'micron': '#666A69',
    'logo_green': '#617A29',
    'paper': '#FBFAF4',
}

def rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgba(name, alpha=255):
    return rgb(COLORS[name]) + (alpha,)

def pick_font(size, bold=False):
    candidates = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT_TITLE = pick_font(90, True)
FONT_SUB = pick_font(32, False)
FONT_EN = pick_font(28, True)
FONT_FOOT = pick_font(25, False)
FONT_NUM = pick_font(20, True)

LABELS = [
    ('旅店據點', 'LOCATIONS', '西門｜長春', 'dragonfly'),
    ('客房介紹', 'ROOMS', '背包床位・雙人房', 'scarlet_smile'),
    ('設施服務', 'FACILITIES', 'Wi‑Fi・洗衣・交誼', 'graphite'),
    ('在地景點', 'LOCAL GUIDE', '台北探索', 'bordeaux'),
    ('聯絡我們', 'CONTACT', 'LINE・Email・電話', 'satin_slipper'),
    ('線上訂房', 'BOOK NOW', '官網直訂更優惠', 'stretch_limo'),
]

def shadow(base, box, radius=52):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), radius=radius, fill=(0, 0, 0, 78))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))

def route_background(d):
    d.rectangle((0, 0, W, H), fill=rgba('paper'))
    for i, color in enumerate(['dragonfly', 'scarlet_smile', 'graphite', 'bordeaux', 'satin_slipper', 'stretch_limo']):
        cx = int((i % 3 + 0.5) * W / 3)
        cy = int((i // 3 + 0.55) * H / 2)
        r = 520
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(color, 36))
    for offset, color in [(0, 'dragonfly'), (100, 'scarlet_smile'), (200, 'logo_green')]:
        pts = []
        for x in range(-120, W + 160, 70):
            y = 250 + offset * 3 + math.sin((x + offset) / 240) * 55
            pts.append((x, y))
        d.line(pts, fill=rgba(color, 90), width=8, joint='curve')

def logo_mark(d, cx, cy):
    d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=(255, 255, 255, 225))
    d.pieslice((cx - 33, cy - 33, cx + 33, cy + 33), 85, 280, fill=rgba('logo_green'))
    d.ellipse((cx - 11, cy - 27, cx + 9, cy - 7), fill=(255, 255, 255, 255))
    d.polygon([(cx - 8, cy - 5), (cx + 8, cy - 5), (cx + 18, cy + 29), (cx - 15, cy + 29)], fill=(255, 255, 255, 255))
    d.line((cx + 10, cy + 10, cx + 38, cy + 32), fill=rgba('logo_green'), width=6)

def pin(d, x, y, s, fill):
    d.ellipse((x - s * .36, y - s * .72, x + s * .36, y), fill=fill, outline=(255, 255, 255, 255), width=7)
    d.polygon([(x, y + s * .45), (x - s * .22, y - s * .06), (x + s * .22, y - s * .06)], fill=fill)
    d.ellipse((x - s * .12, y - s * .48, x + s * .12, y - s * .24), fill=(255, 255, 255, 255))

def scene_locations(d, box, accent):
    x0, y0, x1, y1 = box
    for i in range(6):
        y = y0 + 92 + i * 58
        d.line((x0 + 45, y, x1 - 45, y), fill=(255, 255, 255, 190), width=4)
    for i in range(6):
        x = x0 + 70 + i * 95
        d.line((x, y0 + 65, x, y1 - 155), fill=(255, 255, 255, 150), width=4)
    d.line((x0 + 70, y0 + 190, x0 + 260, y0 + 115, x0 + 430, y0 + 178, x1 - 90, y0 + 92), fill=rgba('scarlet_smile'), width=10, joint='curve')
    d.line((x0 + 90, y1 - 245, x0 + 260, y1 - 330, x0 + 520, y1 - 292), fill=rgba('dragonfly'), width=10, joint='curve')
    pin(d, x0 + 260, y0 + 250, 150, rgba('dragonfly', 235))
    pin(d, x0 + 500, y0 + 390, 125, rgba('logo_green', 235))
    for label, bx, by in [('西門', x0 + 130, y1 - 220), ('長春', x0 + 410, y1 - 190)]:
        d.rounded_rectangle((bx, by, bx + 145, by + 54), radius=27, fill=rgba('cloud_dancer', 235))
        d.text((bx + 30, by + 8), label, font=FONT_SUB, fill=rgba('stretch_limo'))

def scene_rooms(d, box, accent):
    x0, y0, x1, y1 = box
    for row in range(2):
        y = y0 + 135 + row * 205
        d.rounded_rectangle((x0 + 120, y, x1 - 105, y + 112), radius=28, fill=rgba('cloud_dancer', 245))
        d.rounded_rectangle((x0 + 150, y + 28, x0 + 340, y + 88), radius=18, fill=rgba('scarlet_smile', 220))
        d.rounded_rectangle((x0 + 365, y + 28, x1 - 145, y + 88), radius=18, fill=(255, 255, 255, 230))
    d.line((x1 - 165, y0 + 105, x1 - 165, y1 - 150), fill=rgba('cloud_dancer'), width=12)
    for y in [y0 + 185, y0 + 280, y0 + 390, y0 + 480]:
        d.line((x1 - 230, y, x1 - 105, y), fill=rgba('cloud_dancer'), width=8)
    d.rounded_rectangle((x0 + 110, y1 - 250, x0 + 250, y1 - 90), radius=34, fill=rgba('graphite', 240))
    d.rectangle((x0 + 165, y1 - 215, x0 + 198, y1 - 90), fill=rgba('cloud_dancer', 225))

def scene_facilities(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = x0 + 190, y0 + 170
    for r in [45, 80, 118]:
        d.arc((cx - r, cy - r, cx + r, cy + r), 205, 335, fill=rgba('cloud_dancer'), width=13)
    d.ellipse((cx - 15, cy + 42, cx + 15, cy + 72), fill=rgba('cloud_dancer'))
    d.rounded_rectangle((x0 + 115, y0 + 320, x1 - 115, y0 + 465), radius=44, fill=rgba('cloud_dancer', 238))
    d.rounded_rectangle((x0 + 170, y0 + 250, x0 + 410, y0 + 385), radius=36, fill=rgba('bordeaux', 220))
    d.rounded_rectangle((x0 + 470, y0 + 250, x1 - 170, y0 + 385), radius=36, fill=rgba('dragonfly', 220))
    d.rounded_rectangle((x1 - 250, y0 + 105, x1 - 120, y0 + 275), radius=26, fill=rgba('cloud_dancer'))
    d.ellipse((x1 - 218, y0 + 165, x1 - 150, y0 + 235), outline=rgba('graphite'), width=9)
    d.rounded_rectangle((x0 + 500, y1 - 230, x0 + 620, y1 - 150), radius=24, fill=(255, 255, 255, 230), outline=rgba('cloud_dancer'), width=4)
    d.arc((x0 + 595, y1 - 216, x0 + 670, y1 - 155), -80, 90, fill=rgba('cloud_dancer'), width=8)

def scene_guide(d, box, accent):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 40, y1 - 230), (x0 + 260, y0 + 250), (x0 + 475, y1 - 230)], fill=rgba('graphite', 165))
    d.polygon([(x0 + 300, y1 - 230), (x0 + 570, y0 + 165), (x1 - 55, y1 - 230)], fill=rgba('dragonfly', 150))
    cx = x0 + 470
    base = y1 - 220
    for i in range(6):
        y = base - i * 58
        d.polygon([(cx - 56 + i * 5, y), (cx + 56 - i * 5, y), (cx + 46 - i * 5, y - 48), (cx - 46 + i * 5, y - 48)], fill=rgba('cloud_dancer', 240))
    d.polygon([(cx - 18, base - 6 * 58 - 40), (cx + 18, base - 6 * 58 - 40), (cx, base - 6 * 58 - 105)], fill=rgba('cloud_dancer'))
    for lx, ly, color in [(x0 + 155, y0 + 150, 'scarlet_smile'), (x0 + 290, y0 + 210, 'bordeaux'), (x1 - 170, y0 + 170, 'scarlet_smile')]:
        d.line((lx, ly - 80, lx, ly - 30), fill=rgba('cloud_dancer', 200), width=4)
        d.ellipse((lx - 45, ly - 35, lx + 45, ly + 45), fill=rgba(color, 235), outline=rgba('cloud_dancer'), width=5)

def scene_contact(d, box, accent):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 110, y0 + 120, x0 + 390, y0 + 240), radius=45, fill=rgba('cloud_dancer', 245))
    d.rounded_rectangle((x0 + 420, y0 + 185, x1 - 120, y0 + 335), radius=55, fill=rgba('satin_slipper', 235))
    for i in range(3):
        d.ellipse((x0 + 190 + i * 70, y0 + 165, x0 + 225 + i * 70, y0 + 200), fill=rgba('stretch_limo', 220))
    for i in range(3):
        d.ellipse((x0 + 505 + i * 86, y0 + 240, x0 + 545 + i * 86, y0 + 280), fill=rgba('cloud_dancer'))
    d.rounded_rectangle((x0 + 120, y1 - 300, x1 - 120, y1 - 160), radius=35, fill=rgba('cloud_dancer', 240))
    ex, ey = x0 + 180, y0 + 440
    d.rectangle((ex, ey, ex + 235, ey + 140), fill=(255, 255, 255, 230), outline=rgba('cloud_dancer'), width=5)
    d.line((ex, ey, ex + 118, ey + 82, ex + 235, ey), fill=rgba('satin_slipper'), width=6, joint='curve')
    px, py = x1 - 260, y0 + 420
    d.rounded_rectangle((px, py, px + 120, py + 190), radius=24, fill=rgba('cloud_dancer'))
    d.rectangle((px + 20, py + 34, px + 100, py + 150), fill=rgba('stretch_limo', 210))

def scene_booking(d, box, accent):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 120, y0 + 110, x0 + 430, y0 + 360), radius=38, fill=rgba('cloud_dancer'))
    d.rounded_rectangle((x0 + 120, y0 + 110, x0 + 430, y0 + 188), radius=38, fill=rgba('scarlet_smile'))
    d.rectangle((x0 + 120, y0 + 155, x0 + 430, y0 + 188), fill=rgba('scarlet_smile'))
    for i in range(3):
        for j in range(3):
            d.rounded_rectangle((x0 + 175 + i * 82, y0 + 225 + j * 46, x0 + 220 + i * 82, y0 + 253 + j * 46), radius=8, fill=rgba('stretch_limo', 160))
    d.ellipse((x1 - 305, y0 + 170, x1 - 210, y0 + 265), outline=rgba('cloud_dancer'), width=14)
    d.line((x1 - 218, y0 + 218, x1 - 55, y0 + 218), fill=rgba('cloud_dancer'), width=14)
    d.rounded_rectangle((x0 + 230, y1 - 390, x1 - 220, y1 - 145), radius=52, fill=rgba('dragonfly', 225), outline=rgba('cloud_dancer'), width=8)
    d.arc((x0 + 520, y1 - 460, x0 + 700, y1 - 330), 180, 360, fill=rgba('cloud_dancer'), width=14)
    d.line((x1 - 360, y1 - 110, x1 - 180, y1 - 110), fill=rgba('cloud_dancer'), width=16)
    d.polygon([(x1 - 180, y1 - 110), (x1 - 235, y1 - 155), (x1 - 235, y1 - 65)], fill=rgba('cloud_dancer'))

SCENES = [scene_locations, scene_rooms, scene_facilities, scene_guide, scene_contact, scene_booking]

def draw():
    img = Image.new('RGBA', (W, H), rgba('paper'))
    d = ImageDraw.Draw(img)
    route_background(d)

    cell_w = [833, 833, 834]
    cell_h = 843
    for idx, (title, en, sub, color) in enumerate(LABELS):
        col = idx % 3
        row = idx // 3
        x0 = sum(cell_w[:col])
        y0 = row * cell_h
        x1 = x0 + cell_w[col]
        y1 = y0 + cell_h
        pad = 42
        card = (x0 + pad, y0 + pad, x1 - pad, y1 - pad)
        shadow(img, card)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle(card, radius=52, fill=rgba(color, 240))
        d.rounded_rectangle((card[0] + 16, card[1] + 16, card[2] - 16, card[3] - 16), radius=42, outline=(255, 255, 255, 190), width=4)
        d.ellipse((card[2] - 230, card[1] - 210, card[2] + 120, card[1] + 140), fill=(255, 255, 255, 38))
        d.ellipse((card[0] - 160, card[3] - 120, card[0] + 150, card[3] + 190), fill=(255, 255, 255, 26))
        scene_box = (card[0] + 10, card[1] + 50, card[2] - 10, card[3] - 120)
        SCENES[idx](d, scene_box, rgba(color))
        logo_mark(d, card[2] - 90, card[1] + 78)

        dark = color == 'satin_slipper'
        text_fill = rgba('stretch_limo') if dark else (255, 255, 255, 255)
        sub_fill = rgba('stretch_limo', 225) if dark else (255, 255, 255, 225)
        tx = card[0] + 58
        ty = card[3] - 260
        d.text((tx, ty), title, font=FONT_TITLE, fill=text_fill)
        d.text((tx + 4, ty + 105), en, font=FONT_EN, fill=sub_fill)
        d.text((tx + 4, ty + 148), sub, font=FONT_SUB, fill=sub_fill)
        d.rounded_rectangle((tx, card[3] - 62, tx + 350, card[3] - 20), radius=21, fill=(255, 255, 255, 45 if not dark else 80))
        d.text((tx + 20, card[3] - 57), 'Backpackers Hostel', font=FONT_FOOT, fill=sub_fill)
        d.text((card[2] - 82, card[3] - 61), f'{idx + 1:02}', font=FONT_NUM, fill=sub_fill)

    img = img.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Quantized PNG keeps the LINE rich-menu file under 1 MB.
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(OUT, optimize=True)
    print(f'Generated {OUT} ({OUT.stat().st_size} bytes)')

if __name__ == '__main__':
    draw()