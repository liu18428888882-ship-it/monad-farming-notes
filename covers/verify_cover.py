"""封面自检 — 终端截图风"""
import sys, os
from PIL import Image

def verify(path):
    img = Image.open(path)
    fsize = os.path.getsize(path) / 1024

    assert img.size == (1000, 420), f"FAIL: {img.size}"
    px = img.getpixel((50, 50))
    # Terminal style: dark background
    assert all(c < 50 for c in px[:3]), f"FAIL: bg too bright {px}"
    assert 3 < fsize < 500, f"FAIL: {fsize}KB"

    print(f"PASS: {path} {img.size} {fsize:.1f}KB terminal-style")

if __name__ == "__main__":
    verify(sys.argv[1])
