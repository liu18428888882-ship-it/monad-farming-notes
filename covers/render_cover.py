"""
PIL 封面渲染器 — 稳如老狗。
用法:python render_cover.py B out.png "KICKER" "HERO" "SUBTITLE" "FOOTER"
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

FONT_PATHS = {
    'mono': [
        '/System/Library/Fonts/Menlo.ttc',
        '/System/Library/Fonts/Monaco.ttf',
    ],
    'sans': [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
    ],
    'sans_bold': [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
    ],
}

def _font(family, size):
    for path in FONT_PATHS[family]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def template_b(out, kicker, hero, subtitle, footer):
    W, H = 1000, 420
    img = Image.new('RGB', (W, H), '#0d0d0d')
    draw = ImageDraw.Draw(img)

    draw.text((48, 60), kicker, fill='#f59e0b', font=_font('mono', 14))
    draw.text((48, 105), hero, fill='#4ade80', font=_font('mono', 130))
    draw.text((48, 265), subtitle, fill='#cccccc', font=_font('sans', 26))
    
    fw = draw.textlength(footer, font=_font('mono', 11))
    draw.text((W - fw - 48, H - 32), footer, fill='#555555', font=_font('mono', 11))

    img.save(out, 'PNG', optimize=True)
    return out

def template_a(out, kicker, title, m1, m2, m3):
    W, H = 1000, 420
    img = Image.new('RGB', (W, H), '#0a0e27')
    draw = ImageDraw.Draw(img)
    P = 48

    draw.text((P, P), kicker, fill='#7f77dd', font=_font('mono', 16))
    
    font_t = _font('sans_bold', 34)
    words = title.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font_t) > W - 2*P:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    for i, line in enumerate(lines[:3]):
        draw.text((P, P + 40 + i*42), line, fill='white', font=font_t)

    metrics = f"{m1}    {m2}    {m3}"
    draw.text((P, H - P - 16), metrics, fill='#888888', font=_font('mono', 14))
    img.save(out, 'PNG', optimize=True)

def template_c(out, kicker, title_main, title_hl, subtitle):
    W, H = 1000, 420
    img = Image.new('RGB', (W, H), '#1a1a1a')
    draw = ImageDraw.Draw(img)
    P = 48

    draw.text((P, 130), f"— {kicker}", fill='#E24B4A', font=_font('mono', 15))
    draw.text((P, 165), title_main, fill='white', font=_font('sans_bold', 40))
    draw.text((P, 220), title_hl, fill='#E24B4A', font=_font('sans_bold', 40))
    draw.text((P, 290), subtitle, fill='#999999', font=_font('sans', 18))
    img.save(out, 'PNG', optimize=True)

if __name__ == "__main__":
    t = sys.argv[1]
    out = sys.argv[2]
    if t == 'B':
        template_b(out, sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif t == 'A':
        template_a(out, sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    elif t == 'C':
        template_c(out, sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    print(f"OK: {out}")
