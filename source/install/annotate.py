# ตัดภาพหน้าจอ Arduino IDE ของครู แล้ววงตำแหน่งที่ต้องกดพร้อมเลขขั้นตอน
from PIL import Image, ImageDraw, ImageFont
UP = '/mnt/user-data/uploads/'
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
AMBER, DARK = (255, 200, 87), (16, 40, 44)

def mark(im, boxes):
    d = ImageDraw.Draw(im)
    for n, (x0, y0, x1, y1), side in boxes:
        for w, col in ((12, (0, 0, 0, 150)), (6, AMBER)):
            d.rounded_rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), radius=14, outline=col, width=w)
        r = 27
        cx = x1 + 8 + r + 6 if side == 'r' else x0 - 8 - r - 6 if side == 'l' else (x0 + x1) // 2
        cy = (y0 + y1) // 2 if side in 'lr' else y1 + 8 + r + 6
        d.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=(0, 0, 0))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=AMBER)
        d.text((cx, cy + 1), str(n), font=FONT, fill=DARK, anchor='mm')
    return im

def shot(src, crop, boxes, out, width=None, pad_bottom=0):
    im = Image.open(UP + src).convert('RGB').crop(crop)
    if pad_bottom:   # เติมแถบสีเดียวกับแถบเครื่องมือ ไว้วางเลขใต้ปุ่ม
        bg = Image.new('RGB', (im.width, im.height + pad_bottom), im.getpixel((im.width - 5, im.height - 5)))
        bg.paste(im, (0, 0)); im = bg
    im = mark(im, [(n, (x0 - crop[0], y0 - crop[1], x1 - crop[0], y1 - crop[1]), s) for n, (x0, y0, x1, y1), s in boxes])
    if width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save('img/' + out, 'WEBP', quality=84, method=6)
    print(out, im.size)

# 1 เปิดตัวจัดการบอร์ด: ไอคอนบอร์ดแถบซ้าย + ช่องค้นหา
shot('a27981c5-image.png', (0, 0, 1060, 620), [(1, (12, 222, 60, 268), 'b'), (2, (95, 180, 474, 216), 'r')], 'install-boards-manager.webp')
# 2 ค้น arduino r4 แล้วกด INSTALL ที่ Arduino UNO R4 Boards
shot('b146dbb0-image.png', (0, 0, 1060, 560), [(1, (95, 180, 474, 217), 'r'), (2, (210, 471, 344, 508), 'r')], 'install-uno-r4-boards.webp')
# 3 ตัวจัดการไลบรารี: ไอคอนหนังสือ + ค้น MatrixMiniR4 + INSTALL (ตัดแผง Output ออก)
shot('95d63e92-image.png', (0, 0, 1060, 580), [(1, (12, 300, 60, 350), 'b'), (2, (95, 180, 474, 217), 'r'), (3, (210, 483, 344, 520), 'r')], 'install-matrixminir4.webp')
# 4 แถบเครื่องมือ: เลือกบอร์ด ตรวจโค้ด อัปโหลด
shot('a27981c5-image.png', (0, 30, 820, 134), [(1, (186, 80, 533, 124), 'r'), (2, (18, 82, 60, 123), 'b'), (3, (72, 82, 114, 123), 'b')], 'install-toolbar.webp', pad_bottom=78)
