"""封面自检 — 验证尺寸/颜色/大小"""
import sys, os
from PIL import Image

def verify(path, template):
    img = Image.open(path)
    fsize = os.path.getsize(path) / 1024

    assert img.size == (1000, 420), f"FAIL: {img.size}"
    px = img.getpixel((50, 50))

    checks = {
        'B': lambda: all(c < 40 for c in px[:3]),
        'A': lambda: px[0] < 30 and px[1] < 30 and px[2] < 60,
        'C': lambda: all(c < 40 for c in px[:3]),
    }
    assert checks[template](), f"FAIL: bg color {px}"
    assert 3 < fsize < 500, f"FAIL: {fsize}KB"

    print(f"PASS: {path} {img.size} {fsize:.1f}KB template={template}")

if __name__ == "__main__":
    verify(sys.argv[1], sys.argv[2])
