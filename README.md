# Gyaanify

Clear, practical lessons on security, cloud, AI and careers.

- Live site (Firebase): https://gyaanify-web.web.app
- Live site (GitHub Pages): https://shierenk.github.io/gyaanify/

Gyaanify is a **static website**: plain HTML, CSS and JavaScript. There is no database and no framework, so it runs anywhere.

---

## Run it on your computer

### Option 1: just open it (no setup)

1. Download or clone this repository.
2. Double-click `index.html` to open it in your browser.

Everything works this way, including search and lesson progress.

### Option 2: run a local web server (recommended)

A local server behaves exactly like the live site. Use **one** of these from inside the project folder.

**Python** (already installed on most Mac/Linux machines):

```bash
python -m http.server 8000
```

**Node.js:**

```bash
npx serve .
```

**Firebase CLI:**

```bash
firebase serve --only hosting
```

Then open http://localhost:8000 (or the address the command prints).

> **Windows tip:** if PowerShell says "running scripts is disabled", add `.cmd` to the command, for example `npx.cmd serve .` or `firebase.cmd serve --only hosting`.

---

## Project structure

```
gyaanify-website/
├── index.html              Home page
├── paths.html              All learning paths (with filters)
├── path-*.html             One page per learning path (lessons)
├── azure.html              Azure certification roadmap
├── cert-*.html             Study material for each certification
├── resources.html          Free learning resources
├── 404.html                Page-not-found page
├── assets/
│   ├── style.css           All styles (light and dark mode)
│   └── app.js              Search, filters, progress tracking, insight of the day
├── favicon.svg             Browser-tab icon
├── src/                    Source used to generate the pages (not published)
│   ├── content.py          All lesson, certification and resource text
│   ├── build.py            Generates the HTML pages from content.py
│   ├── style.css           Source stylesheet
│   └── app_src.js          Source JavaScript
├── firebase.json           Firebase Hosting settings
└── .nojekyll               Tells GitHub Pages to publish files as they are
```

---

## Edit content

All text lives in `src/content.py`:

- `PATHS`: learning paths and their lessons
- `CERTS`: Azure certifications and their study material
- `RESOURCES`: links on the Resources page

After editing, rebuild the pages (needs Python 3) from the project folder:

```bash
python src/build.py .
```

Then check the result locally (see above) before publishing.

---

## Publish changes

**Firebase Hosting:**

```bash
firebase deploy --only hosting
```

**GitHub (also updates GitHub Pages):**

```bash
git add .
git commit -m "Describe your change"
git push
```

---

## Contributing

Found a mistake or want to suggest a topic? Open an issue or a pull request on GitHub.

---

## Lab 2.1 — AI Website Makeover

This branch contains a focused makeover of the reusable learning-path cards. It improves visual hierarchy, topic thumbnails, hover and keyboard-focus feedback, and the visible learning-path action cue while keeping the site static and preserving its existing navigation and JavaScript behavior.

- [AI prompt log](AI_PROMPT_LOG.md): design brief, implementation constraints, and review prompt.
- [Demo and validation checklist](LAB-2.1-DEMO.md): rubric mapping, browser tests, and a one-minute talk track.

### Test locally

Run from the repository root:

```bash
python -m http.server 8000
```

Then open http://localhost:8000/ and http://localhost:8000/paths.html. Complete the browser checklist before presenting the result; see [LAB-2.1-DEMO.md](LAB-2.1-DEMO.md). This is a CSS-only makeover and does not require an API key or cloud resources.

### Site-wide design and day/night themes

The makeover now applies across the shared site stylesheet and shared header, including the home page, learning catalogue, lesson pages, Azure/certification pages, resources, and the 404 page.

- Use the **Dark mode / Light mode** button in the header to switch themes.
- Your choice is saved in browser local storage and persists across pages.
- On first visit, the site follows your operating-system color preference.
- The theme is implemented with CSS variables and a small vanilla JavaScript toggle; no framework, API key, or cloud service is needed.

Before presenting, test both theme modes on the homepage, catalogue, a lesson page, and a certification/resource page. Confirm text, cards, buttons, search, filters, and progress UI remain readable and functional.

## Contributing and quality checks

See [CONTRIBUTING.md](CONTRIBUTING.md) for the source-of-truth files, build instructions, and local checks. GitHub Actions checks local links and anchors, JavaScript syntax, and whether generated assets match their source files.

