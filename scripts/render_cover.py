import asyncio
import sys
import yaml
from pathlib import Path
from playwright.async_api import async_playwright

TEMPLATES = {
    "A": """
    
      
        {kicker}
        {title}
      
      
        
          {m1}{m2}{m3}
        
        
          
        
      
    """,

    "B": """
    
      
        {kicker}
        {hero}
        {subtitle}
      
      {footer}
    """,

    "C": """
    
      — {kicker}
      {title_main} {title_highlight}
      {subtitle}
    """,
}

STYLE_B = """
body{{background:#0d0d0d;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.kicker{{font-size:14px;color:#f59e0b;text-transform:uppercase;letter-spacing:3px;margin-bottom:20px}}
.hero{{font-size:140px;font-weight:900;color:#4ade80;line-height:1;margin-bottom:12px}}
.subtitle{{font-size:26px;color:#ccc;max-width:700px;text-align:center}}
.footer{{position:absolute;bottom:16px;left:0;right:0;text-align:center;font-size:11px;color:#555;font-family:monospace}}
"""

STYLE_A = """
body{background:linear-gradient(135deg,#0a0a1a 0%,#1a1a3a 100%);color:#fff;display:flex;align-items:center;justify-content:center;font-family:system-ui,sans-serif}
.kicker{font-size:14px;color:#888;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px}
h1{font-size:42px;font-weight:800;line-height:1.15;max-width:800px;margin:0 0 24px 0}
.metrics{display:flex;gap:40px;margin-bottom:24px}
.metric{text-align:center}.metric .val{font-size:36px;font-weight:700;color:#4ade80}.metric .label{font-size:12px;color:#aaa}
.chart-line{margin-top:16px;color:#4ade80;font-size:20px;letter-spacing:2px}
"""

STYLE_B = """
body{background:#0d0d0d;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:system-ui,sans-serif}
.kicker{font-size:14px;color:#f59e0b;text-transform:uppercase;letter-spacing:3px;margin-bottom:20px}
.hero{font-size:140px;font-weight:900;color:#4ade80;line-height:1;margin-bottom:12px}
.subtitle{font-size:26px;color:#ccc;max-width:700px;text-align:center}
.footer{position:absolute;bottom:16px;left:0;right:0;text-align:center;font-size:11px;color:#555;font-family:monospace}
"""

STYLE_C = """
body{background:#0a0a1a;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:system-ui,sans-serif;text-align:center}
.kicker{font-size:13px;color:#f87171;text-transform:uppercase;letter-spacing:3px;margin-bottom:24px}
h1{font-size:38px;font-weight:800;line-height:1.2;max-width:750px;margin:0 0 8px 0}
h1 .hl{color:#f87171}
.subtitle{font-size:22px;color:#aaa;max-width:600px}
"""
STYLES = {"A": STYLE_A, "B": STYLE_B, "C": STYLE_C}

WRAPPER = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1000px;height:420px;overflow:hidden}}
{}
</style></head><body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{}</body></html>"""

async def render(config_path: str):
    cfg = yaml.safe_load(Path(config_path).read_text())
    template = TEMPLATES[cfg["template"]]
    body = template.format(**cfg["vars"])
    style = STYLES[cfg["template"]]
    html = WRAPPER.format(style, body)
    out = Path("covers") / f"{cfg['slug']}.png"
    out.parent.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 420})
        await page.set_content(html)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(out), clip={"x":0,"y":0,"width":1000,"height":420})
        await browser.close()
    print(f"✓ {out}")

if __name__ == "__main__":
    asyncio.run(render(sys.argv[1]))
