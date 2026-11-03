import base64, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
from story_template import LOGO, OUT
FEST = "Diwali"; MSG = "May your work shine bright and your ideas glow. Light up one idea at a time."
DATE = "08 Nov 2026"; BG = "festival_bg.png"
im = Image.open(BG).convert("RGB"); w = 1080; h = round(im.height * w / im.width)
im = im.resize((w, h)); top = max(0, (h - 1920) // 2); im = im.crop((0, top, 1080, top + 1920)) if h >= 1920 else im
im.save(pathlib.Path(OUT, "festival_bg.jpg"), quality=90)
bg = base64.b64encode(open(pathlib.Path(OUT, "festival_bg.jpg"), "rb").read()).decode()
html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=Instrument+Sans:wght@400;700&display=swap">
<style>*{{box-sizing:border-box;margin:0}}body{{background:#0E0D0C}}
.s{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#F5F1EC;font-family:'Instrument Sans',Arial,sans-serif;background:#0E0D0C url(data:image/jpeg;base64,{bg}) center/cover}}
.s:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,13,12,.92) 0%,rgba(14,13,12,.75) 30%,rgba(14,13,12,.15) 52%,rgba(14,13,12,0) 70%,rgba(14,13,12,.85) 100%)}}
.in{{position:relative;height:100%;padding:150px 90px 120px;display:flex;flex-direction:column}}
.logo{{position:absolute;top:150px;right:90px;width:92px}}
.kick{{font:700 30px/1.2 'Instrument Sans';letter-spacing:.16em;text-transform:uppercase;color:#C9C2BA}}
.dash{{width:150px;height:6px;background:#F04D23;margin-top:18px}}
h1{{font:800 200px/.88 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:56px}}
h1 .o{{color:#F04D23}}
.msg{{font:700 40px/1.35 'Instrument Sans';margin-top:44px;max-width:820px}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;font:400 26px/1.3 'Instrument Sans';color:#C9C2BA}}
.foot span:first-child{{font-weight:700;color:#F5F1EC}}</style></head><body><div class="s" id="s"><div class="in">
<img class="logo" src="data:image/png;base64,{LOGO}" alt="">
<div class="kick">The Kerning Times · Festival</div><div class="dash"></div>
<h1>Happy<br><span class="o">{FEST}</span></h1>
<p class="msg">{MSG}</p>
<div class="foot"><span>@designeryogesh</span><span>From The Kerning Times · {DATE}</span></div>
</div></div></body></html>"""
f = pathlib.Path(OUT, "story-festival.html"); f.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file://" + str(f), wait_until="networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    over = pg.evaluate("(()=>{const s=document.getElementById('s');return s.scrollHeight>s.clientHeight})()")
    pg.locator("#s").screenshot(path=str(pathlib.Path(OUT, "story-festival.png"))); b.close()
Image.open(pathlib.Path(OUT, "story-festival.png")).convert("RGB").save(pathlib.Path(OUT, "story-festival.jpg"), quality=92)
print("story-festival", "overflow" if over else "fits")
