"""
PIL 封面 — 终端截图风（真人感）
"""
import sys, os, random
from PIL import Image, ImageDraw, ImageFont

def _font(size):
    paths = ['/System/Library/Fonts/Menlo.ttc', '/System/Library/Fonts/Monaco.ttf']
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def render(out):
    W, H = 1000, 420
    img = Image.new('RGB', (W, H), '#1a1a1a')
    draw = ImageDraw.Draw(img)

    # Terminal chrome
    draw.rectangle([(0,0), (W-1,29)], fill='#2d2d2d')
    draw.text((12, 7), "vincentliu@vps:~$ python monad_burst.py | grep TX", fill='#999', font=_font(13))

    # Tx log lines — simulate tail -f
    logs = [
        ("13:42:01", "TX", "0x3f2a...b9e1 SUCCESS", "#4ade80"),
        ("13:42:03", "TX", "0x7d1c...f4a8 SUCCESS", "#4ade80"),
        ("13:42:04", "NONCE", "collision — retrying", "#f59e0b"),
        ("13:42:06", "TX", "0xa83b...c272 SUCCESS", "#4ade80"),
        ("13:42:07", "TX", "0x5c91...ed4f FAILED", "#f87171"),
        ("13:42:09", "TX", "0x2e60...b04d SUCCESS", "#4ade80"),
        ("13:42:10", "TOTAL", "1960 tx · 14 days · 0$ spent", "#fff"),
        ("13:42:11", "", "Ctrl+C → goodbye", "#666"),
    ]

    for i, (time_str, tag, msg, color) in enumerate(logs):
        y = 50 + i * 40
        draw.text((12, y), time_str, fill='#666', font=_font(14))
        if tag:
            draw.text((100, y), f"[{tag}]", fill='#888', font=_font(14))
            draw.text((155 if len(tag) <= 5 else 175, y), msg, fill=color, font=_font(14))
        else:
            draw.text((100, y), msg, fill=color, font=_font(14))

    # Blinking cursor
    draw.text((550, 50 + 7*40), "▊", fill='#fff', font=_font(16))

    img.save(out, 'PNG', optimize=True)
    return out

if __name__ == "__main__":
    render(sys.argv[1])
    print(f"OK: {sys.argv[1]}")
