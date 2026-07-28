#!/usr/bin/env python3
"""Render all Dominate Solutions social graphics (1080x1350, 4:5) from templates.

Outputs branded single images and carousels into graphics/<post>/...
Run:  python3 build_posts.py
"""
import os, glob, html, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
ASSETS = "../brand-assets/assets"  # shared fonts + logo, relative to graphics/posts.html

# ----------------------------------------------------------------------------- CSS
CSS = f"""
@font-face{{font-family:'Montserrat';font-weight:400;src:url('{ASSETS}/fonts/ttf/montserrat-latin-400-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:600;src:url('{ASSETS}/fonts/ttf/montserrat-latin-600-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:700;src:url('{ASSETS}/fonts/ttf/montserrat-latin-700-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:800;src:url('{ASSETS}/fonts/ttf/montserrat-latin-800-normal.woff2')}}
@font-face{{font-family:'Oswald';font-weight:500;src:url('{ASSETS}/fonts/ttf/oswald-latin-500-normal.woff2')}}
@font-face{{font-family:'Oswald';font-weight:700;src:url('{ASSETS}/fonts/ttf/oswald-latin-700-normal.woff2')}}
:root{{--cream:#F7F5F1;--gold:#D4A94F;--goldlt:#E0B45E;--warm:#A8A49C;--brown:#767269;
  --dark:#0D0C0B;--dark2:#1A1204;--coral:#E0625E;--green:#5EC07A;}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
body{{font-family:'Montserrat',Arial,sans-serif;}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;}}
.cream{{background:var(--cream);color:#111;}}
.dark{{background:var(--dark);color:var(--cream);}}
.inner{{position:absolute;inset:0;padding:96px 88px 200px;display:flex;flex-direction:column;justify-content:center;}}
.eyebrow{{font-family:'Oswald';font-weight:700;letter-spacing:.26em;text-transform:uppercase;
  font-size:27px;color:var(--gold);}}
.rule{{height:6px;width:96px;background:var(--gold);border-radius:3px;margin:26px 0;}}
h1.head{{font-weight:800;line-height:1.03;letter-spacing:-.015em;}}
.dark .head .g,.cream .head .g{{color:var(--gold);}}
.sub{{font-weight:400;line-height:1.5;}}
.cream .sub{{color:var(--brown);}} .dark .sub{{color:#cdc8be;}}
/* glow for dark slides */
.glow{{position:absolute;right:-260px;top:-220px;width:720px;height:720px;border-radius:50%;
  background:radial-gradient(circle,rgba(212,169,79,.18),transparent 62%);}}
/* corner watermark pin */
.wm{{position:absolute;right:-70px;bottom:-70px;width:360px;opacity:.06;}}
.dark .wm{{opacity:.09;}}
/* ---------- brand footer ---------- */
.bfoot{{position:absolute;left:88px;right:88px;bottom:78px;display:flex;
  justify-content:space-between;align-items:center;}}
.lock{{display:flex;align-items:center;}}
.lock img{{height:44px;display:block;}}
.cream .lock{{background:var(--dark);padding:16px 26px;border-radius:14px;}}
.cream .lock img{{height:36px;}}
.handle{{font-family:'Oswald';font-weight:500;letter-spacing:.12em;text-transform:uppercase;
  font-size:22px;}}
.cream .handle{{color:var(--brown);}} .dark .handle{{color:var(--warm);}}
.swipe{{display:flex;align-items:center;gap:14px;font-family:'Oswald';font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;font-size:22px;color:var(--gold);}}
.swipe .arrows{{font-size:30px;}}
.pill{{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:var(--dark);
  font-family:'Oswald';font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  font-size:26px;padding:20px 34px;border-radius:60px;}}
.tag{{display:inline-block;font-family:'Oswald';font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;font-size:26px;color:var(--dark);background:var(--gold);
  padding:16px 30px;border-radius:60px;}}
/* stat */
.stat{{font-family:'Oswald';font-weight:700;line-height:.9;color:var(--gold);letter-spacing:-.02em;}}
/* numbered tip */
.tipno{{font-family:'Oswald';font-weight:700;color:var(--gold);line-height:1;}}
/* checklist */
.check{{display:flex;align-items:flex-start;gap:22px;margin-top:26px;}}
.check .bx{{min-width:52px;height:52px;border-radius:14px;background:rgba(212,169,79,.18);
  display:flex;align-items:center;justify-content:center;}}
.check .bx svg{{width:30px;height:30px;stroke:var(--gold);fill:none;stroke-width:3;
  stroke-linecap:round;stroke-linejoin:round;}}
.check .tx{{font-size:33px;font-weight:700;line-height:1.3;padding-top:6px;}}
.cream .check .tx small,.dark .check .tx small{{display:block;font-weight:400;font-size:26px;
  color:var(--brown);margin-top:4px;}}
.dark .check .tx small{{color:#b7b2a8;}}
/* browser mock */
.frame{{border-radius:22px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.18);}}
.bar{{height:64px;background:#e9e4d9;display:flex;align-items:center;gap:12px;padding:0 26px;}}
.dot{{width:16px;height:16px;border-radius:50%;background:#c9c3b6;}}
.badge2{{display:inline-flex;align-items:center;gap:12px;border:2px solid var(--gold);
  color:var(--gold);border-radius:60px;padding:14px 30px;font-family:'Oswald';font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;font-size:24px;}}
.chips{{display:flex;gap:20px;margin-top:20px;flex-wrap:wrap;}}
.chip2{{background:#fff;border:1px solid #e7e2d8;border-left:6px solid var(--gold);border-radius:14px;
  padding:24px 28px;flex:1;min-width:360px;}}
.dark .chip2{{background:var(--dark2);border-color:rgba(212,169,79,.3);border-left-color:var(--gold);}}
.chip2 .k{{font-family:'Oswald';font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  font-size:28px;}} .chip2 .v{{font-size:24px;color:var(--brown);margin-top:8px;line-height:1.4;font-weight:400;}}
.dark .chip2 .v{{color:#b7b2a8;}}
.pins{{margin-top:16px;}}
.pinrow{{display:flex;align-items:center;gap:20px;font-size:34px;font-weight:700;margin-top:22px;}}
.pinrow .p{{color:var(--gold);font-size:40px;}}
"""

# ----------------------------------------------------------------------------- components
def foot_cream(right=''):
    r = right or f'<span class="handle">dominatesolutions.com</span>'
    return f'<div class="bfoot"><div class="lock"><img src="{ASSETS}/logo-trans.png"></div>{r}</div>'
def foot_dark(right=''):
    r = right or f'<span class="handle">dominatesolutions.com</span>'
    return f'<div class="bfoot"><div class="lock"><img src="{ASSETS}/logo-trans.png"></div>{r}</div>'
def swipe():   return '<span class="swipe">Swipe <span class="arrows">→→</span></span>'
def foot(theme, right=''):
    return foot_cream(right) if theme=='cream' else foot_dark(right)
def wm(theme):
    return f'<img class="wm" src="{ASSETS}/mark.png">'
def glow(theme):
    return '<div class="glow"></div>' if theme=='dark' else ''

CHECKSVG='<svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg>'

# ----------------------------------------------------------------------------- slide templates
def statement(theme, eyebrow, head_html, sub, right_foot='', head_size=96):
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">{eyebrow}</div><div class="rule"></div>
      <h1 class="head" style="font-size:{head_size}px">{head_html}</h1>
      <p class="sub" style="font-size:38px;margin-top:34px">{sub}</p>
      </div>{foot(theme,right_foot)}</div>'''

def stat_slide(theme, eyebrow, big, big_size, head_html, sub, right_foot=''):
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">{eyebrow}</div>
      <div class="stat" style="font-size:{big_size}px;margin-top:30px">{big}</div>
      <h1 class="head" style="font-size:64px;margin-top:20px">{head_html}</h1>
      <p class="sub" style="font-size:36px;margin-top:28px">{sub}</p>
      </div>{foot(theme,right_foot)}</div>'''

def carousel_cover(theme, eyebrow, head_html, sub, head_size=100):
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">{eyebrow}</div><div class="rule"></div>
      <h1 class="head" style="font-size:{head_size}px">{head_html}</h1>
      <p class="sub" style="font-size:38px;margin-top:34px">{sub}</p>
      </div>{foot(theme,swipe())}</div>'''

def tip_slide(theme, no, total, title, body, last_swipe=True):
    right = swipe() if last_swipe else f'<span class="handle">dominatesolutions.com</span>'
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">Tip {no} / {total}</div>
      <div class="tipno" style="font-size:200px;margin-top:20px">{no:02d}</div>
      <h1 class="head" style="font-size:82px;margin-top:6px">{title}</h1>
      <p class="sub" style="font-size:38px;margin-top:26px">{body}</p>
      </div>{foot(theme,right)}</div>'''

def checklist_slide(theme, no, total, title, items):
    rows=''.join(f'<div class="check"><div class="bx">{CHECKSVG}</div><div class="tx">{i}</div></div>' for i in items)
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">Tip {no} / {total}</div>
      <h1 class="head" style="font-size:74px;margin-top:18px">{title}</h1>
      <div style="margin-top:20px">{rows}</div>
      </div>{foot(theme,swipe())}</div>'''

def cta_slide(theme, eyebrow, head_html, sub, tag, head_size=88):
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">{eyebrow}</div><div class="rule"></div>
      <h1 class="head" style="font-size:{head_size}px">{head_html}</h1>
      <p class="sub" style="font-size:38px;margin-top:30px">{sub}</p>
      <div style="margin-top:44px"><span class="tag">{tag}</span></div>
      </div>{foot(theme)}</div>'''

def testimonial(theme, quote, result, name, biz):
    return f'''<div class="slide {theme}">{glow(theme)}{wm(theme)}<div class="inner">
      <div class="eyebrow">Client Win</div>
      <div style="font-family:Oswald;font-weight:700;color:var(--gold);font-size:150px;line-height:.6;margin-top:26px">&ldquo;</div>
      <h1 class="head" style="font-size:60px;margin-top:6px">{quote}</h1>
      <div class="badge2" style="margin-top:40px">★ {result}</div>
      <p class="sub" style="font-size:34px;margin-top:40px;font-weight:700;color:inherit">{name}<br>
        <span style="font-weight:400;color:var(--brown)">{biz}</span></p>
      </div>{foot(theme)}</div>'''

def before_after(label, theme_after=False):
    """Return a browser-mock slide labelled BEFORE (bad) or AFTER (good)."""
    if label=='BEFORE':
        badge='<div class="badge2" style="border-color:var(--coral);color:var(--coral)">✗ Before</div>'
        mock=f'''<div class="frame" style="margin-top:36px">
          <div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
          <div style="background:#fff;height:640px;padding:40px;position:relative">
            <div style="height:70px;background:#b23b3b;border-radius:6px;width:100%"></div>
            <div style="display:flex;gap:16px;margin-top:20px">
              <div style="height:150px;background:#2f6fb0;flex:1;border-radius:6px"></div>
              <div style="height:150px;background:#3aa03a;flex:1;border-radius:6px"></div>
              <div style="height:150px;background:#c9a11a;flex:1;border-radius:6px"></div></div>
            <div style="height:22px;background:#ddd;width:90%;margin-top:26px;border-radius:4px"></div>
            <div style="height:22px;background:#ddd;width:80%;margin-top:12px;border-radius:4px"></div>
            <div style="height:22px;background:#ddd;width:95%;margin-top:12px;border-radius:4px"></div>
            <div style="height:22px;background:#ddd;width:70%;margin-top:12px;border-radius:4px"></div>
            <div style="position:absolute;bottom:36px;left:40px;font:700 26px Montserrat;color:#b23b3b">Comic Sans vibes • cluttered • slow</div>
          </div></div>'''
        sub='Dated design, no clear message, and nothing telling visitors what to do next.'
    else:
        badge='<div class="badge2" style="border-color:var(--green);color:var(--green)">✓ After</div>'
        mock=f'''<div class="frame" style="margin-top:36px">
          <div class="bar" style="background:var(--dark)"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
          <div style="background:var(--cream);height:640px;padding:46px;position:relative">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <img src="{ASSETS}/mark.png" style="height:56px">
              <div style="height:44px;width:180px;background:var(--gold);border-radius:40px"></div></div>
            <div style="height:60px;background:#111;width:78%;margin-top:44px;border-radius:6px"></div>
            <div style="height:60px;background:var(--gold);width:52%;margin-top:14px;border-radius:6px"></div>
            <div style="height:20px;background:#cfc9bd;width:70%;margin-top:26px;border-radius:4px"></div>
            <div style="height:20px;background:#cfc9bd;width:60%;margin-top:12px;border-radius:4px"></div>
            <div style="height:56px;width:260px;background:var(--dark);border-radius:40px;margin-top:34px"></div>
            <div style="position:absolute;bottom:40px;left:46px;font:700 26px Montserrat;color:var(--gold)">Clear • fast • built to convert</div>
          </div></div>'''
        sub='Clean, mobile-first, one clear call-to-action — built to turn visitors into customers.'
    theme='cream'
    return f'''<div class="slide {theme}"><div class="inner">
      <div class="eyebrow">Website Glow-Up</div>{badge.replace('badge2','badge2" style="margin-top:18px')}
      {mock}
      <p class="sub" style="font-size:34px;margin-top:34px">{sub}</p>
      </div>{foot(theme, swipe())}</div>'''

# ----------------------------------------------------------------------------- content / build list
posts = []   # (folder, [slide_html, ...])

# P1 single
posts.append(("01-website-salesperson", [
    statement("dark","Web Design",
      'Your website is your<br>#1 <span class="g">salesperson.</span>',
      'It works 24/7, never calls in sick — but only if it\'s built to sell. Is yours closing deals, or just sitting there looking pretty?',
      right_foot='<span class="tag">DM &ldquo;WEBSITE&rdquo;</span>', head_size=100),
]))

# P2 carousel - GBP
T=6
posts.append(("02-google-business-profile", [
    carousel_cover("cream","Local SEO",
      'The free tool most<br>Tampa businesses<br>use <span class="g">wrong.</span>',
      'Your Google Business Profile decides if you show up for &ldquo;near me&rdquo; searches. 4 fast wins →', head_size=92),
    tip_slide("cream",1,4,'Add real photos.','Skip the stock. Real photos of your work, team, and location build trust and boost ranking.'),
    tip_slide("dark",2,4,'Post updates<br>weekly.','An active profile signals to Google you\'re open and legit — and keeps you top of mind.'),
    tip_slide("cream",3,4,'Reply to every<br>review.','Good or bad, every reply tells Google (and customers) you care. It\'s a ranking factor.'),
    tip_slide("dark",4,4,'Keep hours &amp;<br>services current.','Nothing kills trust like wrong hours. Accurate info = more calls and directions.'),
    cta_slide("cream","Your Move",
      'Want to out-rank<br>your competition<br>— for <span class="g">free?</span>',
      'We\'ll optimize your Google Business Profile so you show up when it counts.',
      'Comment your city', head_size=84),
]))

# P3 carousel - before/after
posts.append(("03-before-after", [
    before_after("BEFORE"),
    before_after("AFTER", theme_after=True),
    cta_slide("cream","Same Business, Better Results",
      'Ready for your<br>website <span class="g">glow-up?</span>',
      'Same products. Same you. A site that finally pulls its weight. Let\'s build it.',
      'Book a free call', head_size=90),
]))

# P4 single stat
posts.append(("04-site-speed", [
    stat_slide("dark","Website Speed","53%",300,
      'of visitors leave a site that takes<br>over <span class="g">3 seconds</span> to load.',
      'You could be doing everything right and still losing customers to a loading spinner.',
      right_foot='<span class="tag">Comment &ldquo;SPEED&rdquo;</span>'),
]))

# P5 single testimonial (placeholder to swap)
posts.append(("05-client-win", [
    testimonial("cream",
      'We went from a handful of website visits to booking out weeks in advance.',
      '3× more calls in 60 days',
      'Client Name', 'Business Name, Tampa'),
]))

# P6 single - ads
posts.append(("06-google-ads", [
    f'''<div class="slide cream">{wm('cream')}<div class="inner">
      <div class="eyebrow">Google Ads &amp; LSA</div><div class="rule"></div>
      <h1 class="head" style="font-size:92px">Show up the exact<br>moment they\'re<br>ready to <span class="g">buy.</span></h1>
      <div class="chips" style="margin-top:44px">
        <div class="chip2"><div class="k">Google Ads</div><div class="v">Top of the results the second someone searches for what you offer.</div></div>
        <div class="chip2"><div class="k">Local Service Ads</div><div class="v">The &ldquo;Google Guaranteed&rdquo; badge — pay only when a real lead calls.</div></div>
      </div>
      <p class="sub" style="font-size:36px;margin-top:36px">Done right, it\'s the best money you\'ll spend all year.</p>
      </div>{foot('cream','<span class="tag">DM &ldquo;ADS&rdquo;</span>')}</div>'''
]))

# P7 carousel - 5 things that convert
T7=7
posts.append(("07-conversion-checklist", [
    carousel_cover("dark","Web Design",
      '5 things every<br>high-converting<br>website <span class="g">needs.</span>',
      'A pretty site that doesn\'t convert is just an expensive business card. Save this →', head_size=92),
    tip_slide("cream",1,5,'A clear headline.','Visitors should know exactly what you do within 3 seconds of landing.'),
    tip_slide("dark",2,5,'One obvious<br>call-to-action.','&ldquo;Call Now.&rdquo; &ldquo;Get a Quote.&rdquo; Don\'t make people guess their next step.'),
    tip_slide("cream",3,5,'Proof.','Reviews, before/afters, real photos. Trust is what actually closes the deal.'),
    tip_slide("dark",4,5,'Fast &amp; mobile-<br>friendly.','Most of your traffic is on a phone. If it\'s slow or clunky, they\'re gone.'),
    tip_slide("cream",5,5,'Easy contact.','Click-to-call, a short form, no hoops. Make saying yes effortless.'),
    cta_slide("dark","Score Your Site",
      'Missing 2 or more?<br>That\'s leads<br>walking <span class="g">out.</span>',
      'Let\'s fix the leaks and turn your website into a lead machine.',
      'Save &amp; share this', head_size=84),
]))

# P8 single - custom not template
posts.append(("08-custom-not-template", [
    statement("dark","What Makes Us Different",
      'Your business isn\'t<br>a template.<br>Your website<br>shouldn\'t be <span class="g">either.</span>',
      'No $20 themes. No stock-photo soup. Every site built from your story, up.',
      right_foot='<span class="handle">dominatesolutions.com</span>', head_size=84),
]))

# P9 single - tampa local
posts.append(("09-tampa-local", [
    f'''<div class="slide cream">{wm('cream')}<div class="inner">
      <div class="eyebrow">Proudly Local</div><div class="rule"></div>
      <h1 class="head" style="font-size:92px">Helping <span class="g">Tampa Bay</span><br>businesses win<br>online.</h1>
      <p class="sub" style="font-size:36px;margin-top:30px">We\'re right here — we know how this market searches, buys, and competes.</p>
      <div class="pins">
        <div class="pinrow"><span class="p">📍</span> Tampa &amp; Tampa Palms</div>
        <div class="pinrow"><span class="p">📍</span> St. Pete &nbsp;·&nbsp; Brandon</div>
        <div class="pinrow"><span class="p">📍</span> Wesley Chapel &amp; all of Tampa Bay</div>
      </div>
      </div>{foot('cream','<span class="tag">Tag a local biz</span>')}</div>'''
]))

# P10 single - free audit
posts.append(("10-free-audit", [
    f'''<div class="slide dark">{glow('dark')}{wm('dark')}<div class="inner">
      <div class="eyebrow">Limited-Time Offer</div>
      <h1 class="head" style="font-size:118px;margin-top:16px">FREE<br><span class="g">Website Audit</span></h1>
      <div style="margin-top:30px">
        <div class="check"><div class="bx">{CHECKSVG}</div><div class="tx">Design &amp; first-impression review</div></div>
        <div class="check"><div class="bx">{CHECKSVG}</div><div class="tx">Speed + mobile check</div></div>
        <div class="check"><div class="bx">{CHECKSVG}</div><div class="tx">Local SEO / Google visibility</div></div>
        <div class="check"><div class="bx">{CHECKSVG}</div><div class="tx">Where you\'re losing leads</div></div>
      </div>
      <p class="sub" style="font-size:34px;margin-top:34px">No pitch, no pressure — just a clear action plan.</p>
      </div>{foot('dark','<span class="tag">Comment &ldquo;AUDIT&rdquo;</span>')}</div>'''
]))

# ----------------------------------------------------------------------------- assemble + render
def build_html():
    body=[]
    idx=[]
    for folder, slides in posts:
        for i, s in enumerate(slides, 1):
            name = f"{folder}.png" if len(slides)==1 else f"{folder}/{i:02d}.png"
            body.append(f'<div data-file="{name}">{s}</div>')
            idx.append(name)
    doc = f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>{''.join(body)}"
    (HERE/"posts.html").write_text(doc, encoding="utf-8")
    return idx

def find_chromium():
    hits = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
    return hits[-1] if hits else None

def main():
    idx = build_html()
    url = (HERE/"posts.html").resolve().as_uri()
    exe = find_chromium()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=1)
        pg.goto(url, wait_until="networkidle")
        els = pg.query_selector_all("[data-file]")
        for el in els:
            name = el.get_attribute("data-file")
            out = HERE/name
            out.parent.mkdir(parents=True, exist_ok=True)
            el.query_selector(".slide").screenshot(path=str(out))
        b.close()
    print(f"Rendered {len(idx)} slides:")
    for n in idx: print("  ", n)

if __name__ == "__main__":
    main()
