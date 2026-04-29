from PIL import Image, ImageDraw, ImageFont
import os, sys

print("=== PIL 环境诊断 ===")
print(f"Python: {sys.version}")

from PIL import __version__ as pil_version
print(f"Pillow: {pil_version}")

# 测试基本绘图
img = Image.new('RGB', (1000, 420), '#f5f1e8')
draw = ImageDraw.Draw(img)

# 测试默认字体能不能用
try:
    default_font = ImageFont.load_default()
    draw.text((50, 50), "default font test", fill='black', font=default_font)
    print("✓ Default font works")
except Exception as e:
    print(f"✗ Default font failed: {e}")

# 测试系统字体
font_candidates = [
    '/System/Library/Fonts/Helvetica.ttc',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    '/Library/Fonts/Arial.ttf',
]

found = []
for f in font_candidates:
    if os.path.exists(f):
        try:
            fnt = ImageFont.truetype(f, 100)
            draw.text((50, 150), "BIG TEXT 1,960", fill='#1a1a1a', font=fnt)
            found.append(f)
            print(f"✓ Font works: {f}")
            break
        except Exception as e:
            print(f"✗ Font found but failed: {f} — {e}")
    else:
        print(f"- Not exist: {f}")

if not found:
    print("\n!!! 没有任何系统字体可用,这就是封面废的根本原因 !!!")
    print("立刻安装字体:")
    print("  Mac: 系统自带 Helvetica 应该有,你的环境可能在容器里")
    print("  Linux: apt install fonts-dejavu fonts-liberation -y")
    print("  Termux: pkg install fontconfig")

img.save('/tmp/pil_test.png', 'PNG')
print(f"\n输出: /tmp/pil_test.png  尺寸: {os.path.getsize('/tmp/pil_test.png')} bytes")

# 验证图片确实被画了东西(不是纯空白)
img2 = Image.open('/tmp/pil_test.png')
pixels = list(img2.getdata())
unique_colors = len(set(pixels))
print(f"图中 unique colors: {unique_colors}")
if unique_colors < 3:
    print("!!! 图片几乎全是同色,说明文字根本没画上去 !!!")
else:
    print("✓ 图片有多种颜色,绘图链路是通的")
