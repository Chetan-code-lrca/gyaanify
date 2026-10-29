import json, math, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import PATHS, RESOURCES, SHORTS, CERTS

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
E = html.escape

ICONS = {
 "shield": '<path d="M12 2.5l8 3v6c0 5-3.4 9.2-8 10.5-4.6-1.3-8-5.5-8-10.5v-6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "cloud": '<path d="M7 18a5 5 0 1 1 1-9.9A6 6 0 0 1 19 10a4 4 0 0 1-1 8z"/>',
 "pipeline": '<circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M7.5 12h4l5-6M11.5 12l5 6"/>',
 "chip": '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9zM9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
 "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
 "bar": '<path d="M5 20V10M12 20V4M19 20v-7"/>',
 "check": '<path d="M5 12l4.5 4.5L19 7"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "play": '<path d="M8 5v14l11-7z"/>',
 "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
}
def icon(n, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>'

def words(l): return sum(len(p.split()) for p in l["body"]) + sum(len(t.split()) for t in l["takeaways"])
for p in PATHS:
    for l in p["lessons"]:
        l["mins"] = max(2, math.ceil(words(l) / 120))
    p["mins"] = sum(l["mins"] for l in p["lessons"])
PATTERNS = ["p-grid", "p-dots", "p-diag", "p-rings", "p-lines", "p-cross"]

LOGO = '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect x=".5" y=".5" width="31" height="31" rx="8" fill="currentColor"/><path d="M22.5 11.2A8 8 0 1 0 24 16h-8" fill="none" stroke="var(--logo-cut)" stroke-width="3" stroke-linecap="square"/><rect x="21" y="21" width="3" height="3" fill="var(--logo-cut)"/></svg>'

NAV = [("index.html", "Home"), ("paths.html", "Learning paths"), ("azure.html", "Azure"), ("resources.html", "Resources")]

def page(fname, title, body, active="", desc="Gyaanify: clear, practical lessons on security, cloud, AI and careers."):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap nav">
  <a class="logo" href="index.html" aria-label="Gyaanify home">{LOGO}<span>Gyaanify</span></a>
  <nav class="menu" aria-label="Main">{nav}</nav>
  <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" id="burger"><span></span><span></span></button>
</div>
<nav class="mobile" id="mobileNav" aria-label="Main" hidden>{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div><a class="logo" href="index.html">{LOGO}<span>Gyaanify</span></a><p>Clear, practical lessons on security, cloud, AI and careers. Free to learn.</p></div>
    <div><h4>Learn</h4><ul>{"".join(f'<li><a href="path-{p["slug"]}.html">{E(p["title"])}</a></li>' for p in PATHS[:3])}</ul></div>
    <div><h4>More paths</h4><ul>{"".join(f'<li><a href="path-{p["slug"]}.html">{E(p["title"])}</a></li>' for p in PATHS[3:])}</ul></div>
    <div><h4>Explore</h4><ul><li><a href="paths.html">All learning paths</a></li><li><a href="azure.html">Azure certifications</a></li><li><a href="resources.html">Free resources</a></li></ul></div>
  </div>
  <div class="legal"><span>© 2026 Gyaanify</span><span>Cyber fraud in India? Call 1930 or visit cybercrime.gov.in</span></div>
</div></footer>
<script src="assets/app.js"></script>
</body>
</html>
'''
    open(os.path.join(OUT, fname), "w").write(doc)

def card(p, i):
    return f'''<a class="pcard" href="path-{p["slug"]}.html" data-topic="{E(p["topic"])}" data-level="{E(p["level"])}">
  <div class="thumb {PATTERNS[i % len(PATTERNS)]}"><span class="thumb-topic">{E(p["topic"])}</span>{icon(p["icon"], "thumb-i")}</div>
  <div class="pbody">
    <span class="level">{E(p["level"])}</span>
    <h3>{E(p["title"])}</h3>
    <p>{E(p["summary"])}</p>
    <div class="meta">{icon("book")}<span>{len(p["lessons"])} lessons</span>{icon("clock")}<span>{p["mins"]} min</span></div>
  </div>
</a>'''

def search_box(idp, ph="Search lessons, e.g. phishing, CI/CD, prompts"):
    return f'''<div class="search" role="search">
  {icon("search")}
  <input id="{idp}" type="search" placeholder="{E(ph)}" autocomplete="off" aria-label="Search lessons">
  <div class="results" id="{idp}-results" hidden></div>
</div>'''

# ---------------- HOME ----------------
topics = []
for p in PATHS:
    if p["topic"] not in topics: topics.append(p["topic"])
total_lessons = sum(len(p["lessons"]) for p in PATHS)
home = f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Free learning, made simple</span>
    <h1>Learn the skills that matter, one short lesson at a time.</h1>
    <p class="lede">Practical learning paths on security, cloud, AI and careers. Plain language, real examples, and every lesson takes about five minutes.</p>
    {search_box("homeSearch")}
    <div class="chips">{"".join(f'<a class="chip" href="paths.html#{E(t)}">{E(t)}</a>' for t in topics)}</div>
  </div>
  <aside class="insight" aria-label="Insight of the day">
    <div class="insight-top"><span class="eyebrow">Insight of the day</span><span class="count" id="tipCount">01 / 07</span></div>
    <span class="tag" id="tipTopic">Security</span>
    <p class="insight-text" id="tipText">Your UPI PIN is only for sending money. Never for receiving it.</p>
    <p class="insight-why" id="tipWhy">If anyone asks you to scan a QR code or enter your PIN to receive money, it is a scam.</p>
    <div class="insight-nav"><button type="button" id="tipPrev" aria-label="Previous insight">←</button><button type="button" id="tipNext" aria-label="Next insight">→</button></div>
  </aside>
</div></section>

<section class="stats"><div class="wrap stat-row">
  <div><b>{len(PATHS)}</b><span>learning paths</span></div>
  <div><b>{total_lessons}</b><span>short lessons</span></div>
  <div><b>~5 min</b><span>per lesson</span></div>
  <div><b>Free</b><span>no sign-up needed</span></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Start here</span><h2>Popular learning paths</h2></div><a class="more" href="paths.html">View all paths {icon("arrow")}</a></div>
  <div class="cards">{"".join(card(p, i) for i, p in enumerate(PATHS[:3]))}</div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">How it works</span><h2>Learn in three simple steps</h2></div></div>
  <ol class="steps">
    <li><span class="n">1</span><h3>Pick a path</h3><p>Choose a topic that fits your goal, from staying safe online to starting a tech career.</p></li>
    <li><span class="n">2</span><h3>Take short lessons</h3><p>Each lesson explains one idea in plain words and ends with three key takeaways.</p></li>
    <li><span class="n">3</span><h3>Practise and keep going</h3><p>Mark lessons complete, track your progress and practise with hand-picked free resources.</p></li>
  </ol>
</div></section>

__AZHOME__
<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Keep learning</span><h2>More paths to explore</h2></div><a class="more" href="paths.html">View all paths {icon("arrow")}</a></div>
  <div class="cards">{"".join(card(p, i + 3) for i, p in enumerate(PATHS[3:]))}</div>
</div></section>

<section class="band"><div class="wrap band-in">
  <div><h2>Start your first lesson today.</h2><p>No account, no cost. Just pick a path and begin.</p></div>
  <div class="band-cta"><a class="btn light" href="path-cyber-safety.html">Start with Cyber Safety</a><a class="btn ghost-light" href="paths.html">Browse all paths</a></div>
</div></section>
'''
azhome = f"""<section class="sec azband"><div class="wrap az-grid">
  <div><span class="eyebrow">Certification path</span><h2>Get Azure certified, step by step</h2><p class="lede">Free study material for {', '.join(c['code'] for c in CERTS)}: what each exam covers, key concepts explained simply, study plans and exam tips.</p><a class="btn dark" href="azure.html" style="margin-top:22px">Explore Azure certifications</a></div>
  <div class="az-steps">{''.join(f'<a href="cert-{c["slug"]}.html"><span class="ccode">{E(c["code"])}</span><span><b>{E(c["name"])}</b><em>{E(c["tier"])}</em></span>{icon("arrow")}</a>' for c in CERTS)}</div>
</div></section>"""
home = home.replace("__AZHOME__", azhome)
page("index.html", "Gyaanify", home, "index.html")

# ---------------- PATHS CATALOG ----------------
levels = []
for p in PATHS:
    if p["level"] not in levels: levels.append(p["level"])
catalog = f'''
<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Learning paths</span></nav>
  <h1>Learning paths</h1>
  <p class="lede">Structured, bite-sized paths. Each one builds from the basics, with key takeaways at the end of every lesson.</p>
  {search_box("pathSearch")}
</div></section>
<section class="sec tight"><div class="wrap catalog">
  <aside class="filters" aria-label="Filters">
    <h4>Topic</h4>
    <div class="fgroup" id="fTopic"><button type="button" class="f on" data-v="all">All topics</button>{"".join(f'<button type="button" class="f" data-v="{E(t)}">{E(t)}</button>' for t in topics)}</div>
    <h4>Level</h4>
    <div class="fgroup" id="fLevel"><button type="button" class="f on" data-v="all">All levels</button>{"".join(f'<button type="button" class="f" data-v="{E(l)}">{E(l)}</button>' for l in levels)}</div>
  </aside>
  <div>
    <p class="resultcount" id="pathCount">{len(PATHS)} paths</p>
    <div class="cards two" id="pathGrid">{"".join(card(p, i) for i, p in enumerate(PATHS))}</div>
    <p class="empty" id="pathEmpty" hidden>No paths match these filters yet. Try another topic or level.</p>
  </div>
</div></section>
'''
page("paths.html", "Learning paths · Gyaanify", catalog, "paths.html")

# ---------------- PATH PAGES ----------------
for i, p in enumerate(PATHS):
    nxt = PATHS[(i + 1) % len(PATHS)]
    side = "".join(f'<li><a href="#lesson-{k+1}" data-lesson="{k+1}"><span class="tick">{icon("check")}</span><span class="ln">{k+1}</span><span class="lt">{E(l["title"])}</span></a></li>' for k, l in enumerate(p["lessons"]))
    lessons = ""
    for k, l in enumerate(p["lessons"]):
        paras = "".join(f"<p>{E(x)}</p>" for x in l["body"])
        tks = "".join(f"<li>{icon('check')}<span>{E(t)}</span></li>" for t in l["takeaways"])
        lessons += f'''<article class="lesson" id="lesson-{k+1}">
  <div class="lesson-head"><span class="lesson-n">Lesson {k+1} of {len(p["lessons"])}</span><span class="lesson-t">{icon("clock")}{l["mins"]} min read</span></div>
  <h2>{E(l["title"])}</h2>
  {paras}
  <div class="takeaways"><h3>Key takeaways</h3><ul>{tks}</ul></div>
  <label class="done"><input type="checkbox" id="done-{p["slug"]}-{k+1}" data-path="{p["slug"]}" data-lesson="{k+1}"><span>Mark as complete</span></label>
</article>'''
    outcomes = "".join(f"<li>{icon('check')}<span>{E(o)}</span></li>" for o in p["outcomes"])
    body = f'''
<section class="path-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="paths.html">Learning paths</a><span>/</span><span>{E(p["title"])}</span></nav>
  <div class="path-hero-grid">
    <div>
      <span class="eyebrow">{E(p["topic"])}</span>
      <h1>{E(p["title"])}</h1>
      <p class="lede">{E(p["summary"])}</p>
      <div class="facts">
        <span>{icon("bar")}{E(p["level"])}</span><span>{icon("book")}{len(p["lessons"])} lessons</span><span>{icon("clock")}{p["mins"]} min</span>
      </div>
      <a class="btn dark" href="#lesson-1">Start learning</a>
    </div>
    <div class="learn-box"><h3>What you'll learn</h3><ul>{outcomes}</ul></div>
  </div>
</div></section>
<section class="sec tight"><div class="wrap path-layout" data-path="{p["slug"]}" data-total="{len(p["lessons"])}">
  <aside class="toc" aria-label="Lessons in this path">
    <div class="progress"><div class="progress-top"><span>Your progress</span><b id="progText">0 / {len(p["lessons"])}</b></div><div class="bar"><i id="progBar"></i></div></div>
    <ol>{side}</ol>
  </aside>
  <div class="lessons">{lessons}
    <a class="nextpath" href="path-{nxt["slug"]}.html"><span class="eyebrow">Next path</span><b>{E(nxt["title"])}</b><span>{E(nxt["summary"])}</span>{icon("arrow")}</a>
  </div>
</div></section>
'''
    page(f'path-{p["slug"]}.html', f'{p["title"]} · Gyaanify', body, "paths.html", p["summary"])

# ---------------- RESOURCES ----------------
rcats = []
for r in RESOURCES:
    if r[0] not in rcats: rcats.append(r[0])
rows = "".join(f'<a class="row" href="{E(u)}" target="_blank" rel="noopener" data-cat="{E(c)}"><span class="cat">{E(c)}</span><span class="rt"><b>{E(t)}</b><span>{E(d)}</span></span>{icon("ext")}</a>' for c, t, d, u in RESOURCES)
res = f'''
<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Resources</span></nav>
  <h1>Free resources</h1>
  <p class="lede">Hand-picked, free and from trusted sources. Use them to practise what you learn in each path. Every link opens on its original site.</p>
</div></section>
<section class="sec tight"><div class="wrap">
  <div class="tabs" id="resTabs"><button type="button" class="f on" data-v="all">All</button>{"".join(f'<button type="button" class="f" data-v="{E(c)}">{E(c)}</button>' for c in rcats)}</div>
  <div class="list" id="resList">{rows}</div>
</div></section>
'''
page("resources.html", "Free resources · Gyaanify", res, "resources.html")


# ---------------- 404 ----------------
page("404.html", "Page not found · Gyaanify", f'''<section class="page-head center"><div class="wrap"><h1>Page not found</h1><p class="lede">The page you're looking for doesn't exist or has moved.</p><div class="band-cta" style="justify-content:center;margin-top:24px"><a class="btn dark" href="index.html">Go to home</a><a class="btn outline" href="paths.html">Browse learning paths</a></div></div></section>''')


# ---------------- AZURE ----------------
def cert_card(c):
    return f"""<a class="ccard" href="cert-{c['slug']}.html"><span class="ccode">{E(c['code'])}</span><span class="ctier">{E(c['tier'])}</span><h3>{E(c['name'])}</h3><p>{E(c['summary'])}</p><span class="cgo">Study material {icon('arrow')}</span></a>"""
tiers = ["Fundamentals", "Associate", "Expert"]
roadmap = "".join(f"""<div class="tier"><div class="tier-head"><span class="tier-n">{k+1}</span><div><b>{t}</b><span>{['Start here. No experience needed.','Hands-on skills to run Azure.','Advanced, role-based mastery.'][k]}</span></div></div><div class="tier-cards">{''.join(cert_card(c) for c in CERTS if c['tier']==t)}</div></div>""" for k,t in enumerate(tiers))
az = f"""
<section class="page-head az-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Azure</span></nav>
  <span class="eyebrow" style="display:block;margin-top:14px">Learning path</span>
  <h1>Azure certifications</h1>
  <p class="lede">A clear route from your first cloud exam to expert level. Each certification has its own study material: what the exam covers, key concepts explained simply, a week-by-week plan and exam tips.</p>
  <div class="facts"><span>{icon('book')}{len(CERTS)} certifications</span><span>{icon('bar')}Fundamentals to Expert</span><span>{icon('check')}Based on official Microsoft study guides</span></div>
</div></section>
<section class="sec tight"><div class="wrap">
  <div class="roadmap">{roadmap}</div>
  <div class="note-box"><b>Before you start:</b> start with the Azure path in <a href="path-cloud-basics.html">Cloud Computing Basics</a>, then pick AZ-900. Exams are booked through Microsoft Learn, prices vary by country, and Microsoft offers a free practice assessment for each exam. Associate and Expert certifications must be renewed every year with a free online assessment; Fundamentals don't expire.</div>
</div></section>
"""
page("azure.html", "Azure certifications · Gyaanify", az, "azure.html", "Free study material for Azure certifications: AZ-900, AI-901, AZ-104 and AZ-400.")

for idx_c, c in enumerate(CERTS):
    doms = ""
    for name, w, subs in c["domains"]:
        pct = w.split("–")
        width = int(pct[1].rstrip("%")) if len(pct) == 2 else 0
        bar = f'<div class="wbar"><i style="width:{min(width*1.6,100)}%"></i></div>' if width else ""
        doms += f"""<div class="dom"><div class="dom-top"><b>{E(name)}</b><span class="w">{E(w)}</span></div>{bar}<ul>{''.join(f'<li>{E(x)}</li>' for x in subs)}</ul></div>"""
    notes = "".join(f"""<details class="note"{' open' if k==0 else ''}><summary>{E(t)}</summary><p>{E(b)}</p></details>""" for k,(t,b) in enumerate(c["notes"]))
    plan = "".join(f"""<li><span class="wk">{E(a)}</span><span>{E(b)}</span></li>""" for a,b in c["plan"])
    nxt = CERTS[(idx_c+1) % len(CERTS)]
    tips = ["Read every question twice. Many answers are “which service fits this scenario”.", "Use the free practice assessment on Microsoft Learn until you score 80% or more.", "Hands-on practice beats memorising: build what you read about in a free account.", "Skip hard questions and come back. Unanswered questions score zero, so answer everything.", "Check the official study guide a week before your exam in case the skills changed."]
    body = f"""
<section class="path-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="azure.html">Azure</a><span>/</span><span>{E(c['code'])}</span></nav>
  <div class="path-hero-grid">
    <div>
      <span class="eyebrow">{E(c['tier'])} certification</span>
      <h1>{E(c['code'])}: {E(c['name'])}</h1>
      <p class="lede">{E(c['summary'])}</p>
      <div class="facts"><span>{icon('bar')}{E(c['tier'])}</span><span>{icon('check')}Pass mark 700 / 1000</span><span>{icon('book')}{len(c['domains'])} skill areas</span></div>
      <div class="band-cta"><a class="btn dark" href="#notes">Start studying</a><a class="btn outline" href="{E(c['guide'])}" target="_blank" rel="noopener">Official study guide {icon('ext')}</a></div>
    </div>
    <div class="learn-box"><h3>About this exam</h3><ul>
      <li>{icon('check')}<span><b>Earns:</b> {E(c['credential'])}</span></li>
      <li>{icon('check')}<span><b>For:</b> {E(c['for'])}</span></li>
      <li>{icon('check')}<span>{E(c['updated'])}</span></li>
    </ul></div>
  </div>
</div></section>
<section class="sec tight"><div class="wrap cert-layout">
  <aside class="toc"><ol>
    <li><a href="#skills"><span class="ln">1</span><span class="lt">What the exam covers</span></a></li>
    <li><a href="#notes"><span class="ln">2</span><span class="lt">Key concepts</span></a></li>
    <li><a href="#plan"><span class="ln">3</span><span class="lt">Study plan</span></a></li>
    <li><a href="#tips"><span class="ln">4</span><span class="lt">Exam tips</span></a></li>
    <li><a href="#links"><span class="ln">5</span><span class="lt">Official resources</span></a></li>
  </ol></aside>
  <div class="lessons">
    <article class="lesson" id="skills"><span class="lesson-n">Section 1</span><h2>What the exam covers</h2><p>The exam is split into skill areas. The percentage shows roughly how much of the exam each area makes up, so spend your time to match.</p><div class="doms">{doms}</div></article>
    <article class="lesson" id="notes"><span class="lesson-n">Section 2</span><h2>Key concepts, explained simply</h2><p>These are the ideas that come up again and again. Open each one and make sure you could explain it to a friend.</p><div class="notes">{notes}</div></article>
    <article class="lesson" id="plan"><span class="lesson-n">Section 3</span><h2>Study plan</h2><p>About an hour a day is enough. Adjust the pace to your experience.</p><ol class="plan">{plan}</ol></article>
    <article class="lesson" id="tips"><span class="lesson-n">Section 4</span><h2>Exam tips</h2><div class="takeaways"><ul>{''.join(f'<li>{icon("check")}<span>{E(t)}</span></li>' for t in tips)}</ul></div></article>
    <article class="lesson" id="links"><span class="lesson-n">Section 5</span><h2>Official resources</h2>
      <div class="list">
        <a class="row" href="{E(c['guide'])}" target="_blank" rel="noopener"><span class="cat">Study guide</span><span class="rt"><b>{E(c['code'])} official study guide</b><span>Full list of skills measured, updated by Microsoft</span></span>{icon('ext')}</a>
        <a class="row" href="https://learn.microsoft.com/training/" target="_blank" rel="noopener"><span class="cat">Training</span><span class="rt"><b>Microsoft Learn training</b><span>Free modules and learning paths with sandboxes</span></span>{icon('ext')}</a>
        <a class="row" href="https://learn.microsoft.com/credentials/" target="_blank" rel="noopener"><span class="cat">Practice</span><span class="rt"><b>Free practice assessment</b><span>Find {E(c['code'])} on Microsoft Learn Credentials and open its practice assessment</span></span>{icon('ext')}</a>
      </div>
    </article>
    <a class="nextpath" href="cert-{nxt['slug']}.html"><span class="eyebrow">Next certification</span><b>{E(nxt['code'])}: {E(nxt['name'])}</b><span>{E(nxt['summary'])}</span>{icon('arrow')}</a>
  </div>
</div></section>
"""
    page(f"cert-{c['slug']}.html", f"{c['code']} {c['name']} · Gyaanify", body, "azure.html", c["summary"])

# ---------------- search index ----------------
idx = []
for p in PATHS:
    idx.append({"t": p["title"], "s": p["topic"] + " · learning path", "u": f'path-{p["slug"]}.html', "k": (p["summary"] + " " + p["topic"]).lower()})
    for k, l in enumerate(p["lessons"]):
        idx.append({"t": l["title"], "s": p["title"] + f" · lesson {k+1}", "u": f'path-{p["slug"]}.html#lesson-{k+1}', "k": (" ".join(l["body"]) + " " + " ".join(l["takeaways"])).lower()})
here = os.path.dirname(os.path.abspath(__file__))
for c in CERTS:
    idx.append({"t": c["code"] + ": " + c["name"], "s": "Azure certification · " + c["tier"], "u": f'cert-{c["slug"]}.html', "k": (c["summary"] + " " + " ".join(n[0] + " " + n[1] for n in c["notes"]) + " azure certification exam").lower()})
open(os.path.join(OUT, "assets", "app.js"), "w").write("window.GY_INDEX=" + json.dumps(idx) + ";\n" + open(os.path.join(here, "app_src.js")).read())
open(os.path.join(OUT, "assets", "style.css"), "w").write(open(os.path.join(here, "style.css")).read())
print("built", len(os.listdir(OUT)))
