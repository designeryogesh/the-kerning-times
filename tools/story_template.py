import os, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
LOGO = "iVBORw0KGgoAAAANSUhEUgAAAKsAAAC/CAYAAACBryyUAAAE7klEQVR4nO3dXXbTQBBE4QqHnbAe9r8NdgAPwsQx1s9opJmu7vu9czCjm0J24vjj188fAhx8m/0AgKOIFTaIFTaIFTaIFTaIFTaIFTaIFTaIFTaIFTaIFTaIFTaIFTa+d/zZ35c9ivt9zH4A8jovKcaZfdETq5OtUEZdlMff4xLtu8c5NeAqsW55XJTR0b57DNGNPqsviPXTzAvhvLrDzosnWP/7rXnRfCjgveKOYWdFrOtmrpxjsLefF7FuI9g2t54Xse6bfVvg5razItb4XIO9PFpiPY5bgsmItQ3Btrn0vIi1nctroVFcdl7E6sVxXaWLgiXWc1jXdt1nRqx+XNe1G7Gex7q26zozYoUNYsVop9eVWPtwKzAQsXoq+SSLWDHDqf+RiBU2iBU2iNVThid2zf8GYoUNYoUNYoUNYvWT4X71FGKFDWKFDWL1UvYWQCJWGCFWH6VXVSJWGCFWD+VXVSJWzNP8M7nEGh+r+hexwgaxxsaqPiFWzHDqPWTEGher+oJYMdrpd+YSa0ys6hvOn4Pl/OFnVXX9vgPnWN95PQzHeB0f8xDZbwMcPwQtq+7rkD3WB4JNoEqskkewWW8BLjn7SrFKHsFiRbVYpbjBsqo7KsYqxQ0WG6rGKsUKllU9oHKsMEOs87GqB1WPNdKtAHZUj3U2VrUBscIGsc7DqjYiVtgg1jlPsljVE4gVNoh1vKyrejtixVVuv50i1j6tF4hV7UCsuMKQJ6nEeh6rOhixotewl/6I9RxWdQJiRY+h31Ah1nas6iTEirOGf5uaWNuwqhMRK86Y8g4LYj2OVZ2MWNFq2vvWiPUYVjUAYkWLqe8GJtZ9rGoQxIqjpv+OBWLdxqoGQqw4YvqqSsS6hlUNiFixJcyqSsT6DqsaFLFiTahVlYj1FasaGLHinXCrKhHrM1Y1OGLFq5CrKhHrA6tqgFjxLOyqSsQKI8TaLustQOhVlYgVRoi1Das6EbHCBrEex6pORqywQazHsKoBECtsEOs+VjUIYoUNYt3GqgZCrLBBrOuyrqotYq3H8hZAItY1rGpAxFqL7apKxPoOqxoUsdZhvaqSd6x3LCCrGphzrDjOflUlYn3GqgbnHiuB7UuxqpJ/rNI1wRK9ge+zH8BFnmNLsyQXSHUWGZa1F6tqgljzSrWqUr5Y+QVriWWLFYt0qyrlipVVTS5TrFikXFUpT6ysagFZYsUi7apKOWJlVYvIECsWqVdV8o+VVS3EPVYs0q+q5B0rq1qMc6xYlFhVyTdWVrUg11ixKLOqkmesrGpRjrFiUWpVJb9YWdXC3GLFotyqSl6xsqrFOcWKRclVlXxiLXuB8Mkl1lZZbwFKf9E6xFr6AuGTQ6ytWNWkosda/gLhU0+sEUNiVROLvqzAP5Fj5ZsAC1b1r95YOUgME3VZWdUFY/Dkilg5UAwRcVlZ1QUj8OKqWDlY3C7asrKqC77437gyVg4Yt7p6WXuCZVUXfNGvuOM2gMM+j7PbcNc9a+uhs6qEuuvOJ1gc/nGc1QF3vxpw5CJUX1VCPWjES1dcjHWcTYNRr7OuXZTKq0qojUZ+0PDj4mQK7gwiPWnGp2KfvVjukRNppywf4R4ZkV7EJVanVSXOm7jESgAI91NXwCpihQ1ihQ1ihQ1ihQ1ihQ1ihQ1ihQ1ihQ1ihQ1ihQ1ihY0/4Pt1H9FhX6sAAAAASUVORK5CYII="

STORIES = [  # FILL: two dicts, e.g.
  # {"slug": "story-graphic-design", "desk": "Graphic Design", "head": ["Brands bet", "on simple"],
  #  "items": [("Title one", "One-sentence summary."), ("Title two", "..."), ("Title three", "...")],
  #  "take": "One-line designer takeaway."},
  # {"slug": "story-ui-ux", "desk": "UI / UX", ...}
]
DATE = "DD Mon YYYY"  # FILL: today, e.g. 19 Oct 2026

CSS = """
*{box-sizing:border-box;margin:0}
body{background:#0E0D0C}
.s{width:1080px;height:1920px;background:#0E0D0C;color:#F5F1EC;position:relative;overflow:hidden;
   padding:150px 90px 160px;display:flex;flex-direction:column;font-family:'Instrument Sans',Arial,sans-serif}
.logo{position:absolute;top:150px;right:90px;width:92px}
.kick{font:700 30px/1.2 'Instrument Sans';letter-spacing:.16em;text-transform:uppercase;color:#C9C2BA}
.dash{flex:none;width:150px;height:6px;background:#F04D23;margin-top:18px}
h1{font:800 168px/.9 'Big Shoulders Display','Big Shoulders',Impact,sans-serif;text-transform:uppercase;letter-spacing:-.005em;margin-top:56px}
h1 .o{color:#F04D23}
.list{margin-top:80px;display:flex;flex-direction:column;gap:46px}
.it{display:grid;grid-template-columns:120px 1fr;gap:28px;align-items:start}
.n{font:800 92px/.82 'Big Shoulders Display',Impact,sans-serif;color:#F04D23}
.it h2{font:800 54px/1 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;color:#F5F1EC}
.it p{font:400 32px/1.42 'Instrument Sans';color:#C9C2BA;margin-top:12px}
.take{flex:none;margin-top:auto;background:#1A1816;padding:38px 42px;border-radius:6px}
.take b{display:block;font:700 26px/1.2 'Instrument Sans';letter-spacing:.16em;text-transform:uppercase;color:#F04D23;margin-bottom:12px}
.take p{font:700 38px/1.32 'Instrument Sans';color:#F5F1EC}
.foot{margin-top:40px;display:flex;justify-content:space-between;font:400 26px/1.3 'Instrument Sans';color:#8F877E}
.foot span:first-child{color:#C9C2BA;font-weight:700}
"""

def html(s):
    head = "<br>".join(s["head"][:-1]) + f'<br><span class="o">{s["head"][-1]}</span>'
    items = "".join(f'<div class="it"><div class="n">0{i+1}</div><div><h2>{t}</h2><p>{d}</p></div></div>' for i,(t,d) in enumerate(s["items"]))
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=Instrument+Sans:wght@400;700&display=swap">
<style>{CSS}</style></head><body><div class="s" id="s">
<img class="logo" src="data:image/png;base64,{LOGO}" alt="">
<div class="kick">The Kerning Times · {s['desk']}</div><div class="dash"></div>
<h1>{head}</h1>
<div class="list">{items}</div>
<div class="take"><b>Designer takeaway</b><p>{s['take']}</p></div>
<div class="foot"><span>@designeryogesh</span><span>Daily design news · {DATE}</span></div>
</div></body></html>"""

if __name__ == "__main__":
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    for s in STORIES:
        f = pathlib.Path(OUT, s["slug"] + ".html"); f.write_text(html(s))
        pg.goto("file://" + str(f), wait_until="networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        over = pg.evaluate("(()=>{const s=document.getElementById('s');return s.scrollHeight>s.clientHeight})()")
        png = pathlib.Path(OUT, s["slug"] + ".png"); pg.locator("#s").screenshot(path=str(png))
        Image.open(png).convert("RGB").save(pathlib.Path(OUT, s["slug"] + ".jpg"), quality=92)
        print(s["slug"], "overflow" if over else "fits", os.path.getsize(pathlib.Path(OUT, s["slug"] + ".jpg"))//1024, "KB")
    b.close()
