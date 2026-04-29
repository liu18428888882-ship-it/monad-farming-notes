"""封面自检 — 每次渲染完封面后必须跑"""
import sys, os
from PIL import Image

def verify_terminal_style(path):
    img = Image.open(path)
    assert img.size == (1000, 420), f"FAIL: size {img.size}"
    bg_pixel = img.getpixel((10, 10))
    assert all(c < 50 for c in bg_pixel[:3]), f"FAIL: bg too bright {bg_pixel}"
    pixels = list(img.getdata())
    unique_colors = len(set(pixels))
    assert unique_colors > 100, f"FAIL: only {unique_colors} colors, looks blank"
    bottom_pixel = img.getpixel((500, 300))
    assert bottom_pixel != bg_pixel, f"FAIL: bottom is empty, content only at top"
    fsize = os.path.getsize(path) / 1024
    assert 5 < fsize < 500, f"FAIL: file size {fsize}KB suspicious"
    print(f"PASS: terminal-style verified {img.size} {fsize:.1f}KB {unique_colors} colors")

if __name__ == "__main__":
    verify_terminal_style(sys.argv[1])
