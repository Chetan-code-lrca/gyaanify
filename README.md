# Gyaanify

**Practical, beginner-friendly learning paths for security, cloud, AI, DevOps, and tech careers.**

Gyaanify is a static learning website built with HTML, CSS, and vanilla JavaScript. It has no application server, database, package installation, or runtime API dependency.

- **Repository:** [Chetan-code-lrca/gyaanify](https://github.com/Chetan-code-lrca/gyaanify)
- **Expected GitHub Pages URL:** [https://chetan-code-lrca.github.io/gyaanify/](https://chetan-code-lrca.github.io/gyaanify/)
- **Deployment status:** The deployment workflow is committed. GitHub Pages must be enabled in repository settings before the first deployment can succeed.
- **Quality checks:** [GitHub Actions](https://github.com/Chetan-code-lrca/gyaanify/actions)

## Contents

- [Features](#features)
- [Design and themes](#design-and-themes)
- [Technology](#technology)
- [Run locally](#run-locally)
- [Build and validate](#build-and-validate)
- [Project structure](#project-structure)
- [GitHub Pages deployment](#github-pages-deployment)
- [Troubleshooting deployment](#troubleshooting-deployment)
- [Contributing](#contributing)
- [Project documentation](#project-documentation)

## Features

- Learning paths covering cyber safety, cloud fundamentals, DevOps, AI, careers, and hackathons.
- Search across learning paths, lessons, and Azure certification material.
- Catalogue filters for topic and experience level.
- Lesson completion and progress tracking stored in the browser.
- Azure certification roadmap and study resources.
- Responsive navigation and page layouts.
- Shared light/dark appearance with a user-selectable theme.
- A custom 404 page and a legacy `shorts.html` redirect.

## Design and themes

The site-wide design update is implemented in the common stylesheet and JavaScript, rather than only on the homepage.

### Visual system

- Consistent surfaces, borders, spacing, typography, buttons, and focus states across the homepage, catalogue, lesson pages, Azure/certification pages, resources, and 404 page.
- Refined learning-path cards with topic-specific thumbnails, clearer level badges, hover/focus feedback, and an explicit learning-path action cue.
- Responsive layouts and reduced-motion support.

### Light and dark mode

A theme control is added to the shared header by `assets/app.js`.

- On first visit, the site follows the operating system's light/dark preference.
- A saved preference takes precedence on later visits.
- The selection is stored in browser `localStorage` using the key `gy-theme`.
- `assets/theme-init.js` applies the saved preference before the main stylesheet loads to reduce a flash of the wrong theme.
- The theme toggle uses CSS variables and vanilla JavaScript; it does not require a library, API key, or backend.

Theme preference is local to each browser profile. It is not synced between devices.

## Technology

| Area | Implementation |
|---|---|
| Pages | Static HTML |
| Styling | CSS custom properties and responsive CSS |
| Client-side behavior | Vanilla JavaScript |
| Content and page generation | Python 3, using the standard library |
| Local validation | Python standard library and Node.js syntax checks |
| Continuous integration | GitHub Actions |
| Hosting target | GitHub Pages |

No `npm install` is needed for the site or its validation workflow.

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Chetan-code-lrca/gyaanify.git
cd gyaanify
```

To work on the current theme and quality contribution instead of the default branch:

```bash
git fetch origin contrib/site-wide-theme-quality
git switch --track -c contrib/site-wide-theme-quality origin/contrib/site-wide-theme-quality
```

If you already have the branch locally, run `git switch contrib/site-wide-theme-quality` instead.

### 2. Start the static site server

With Python 3 installed:

```bash
python -m http.server 8000
```

Open [http://localhost:8000/](http://localhost:8000/) in your browser. Keep the terminal running while testing; press `Ctrl+C` to stop the server.

For WSL, run the command inside the Linux project directory. Windows browsers can normally open `http://localhost:8000/`.

## Build and validate

The checked-in HTML and `assets/` directory are the generated site. The canonical source files are in `src/`. When changing content, shared styles, or behavior, update the source and regenerate the output.

### Rebuild the checked-in website

From the repository root:

```bash
python src/build.py .
```

Review the generated diff before committing. The build outputs generated HTML and JavaScript/CSS assets; it does not replace repository configuration, documentation, or workflow files.

### Run the static-site checker

```bash
python scripts/check_site.py .
```

The checker validates local file links, in-site anchors, duplicate HTML IDs, and required shared assets/theme bootstrap on content pages. It understands the catalogue's category chips, whose URL fragments select existing `data-v` filter values.

### Check JavaScript syntax and generated-file consistency

If Node.js is installed:

```bash
node --check assets/app.js
node --check src/app_src.js
node --check assets/theme-init.js
node --check src/theme_init.js

cmp src/style.css assets/style.css
cmp src/theme_init.js assets/theme-init.js

python -c 'from pathlib import Path; built = Path("assets/app.js").read_text(encoding="utf-8").split("\\n", 1)[1]; source = Path("src/app_src.js").read_text(encoding="utf-8"); assert built == source, "assets/app.js is out of sync with src/app_src.js"'
```

### Rebuild into a separate preview directory

To test generated output without replacing the checked-in files:

```bash
rm -rf _site
python src/build.py _site
cp favicon.svg .nojekyll shorts.html _site/
python scripts/check_site.py _site
python -m http.server 8000 --directory _site
```

Then open [http://localhost:8000/](http://localhost:8000/). Delete the temporary `_site/` directory after testing if you do not need it.

### Browser regression checklist

Before opening or updating a pull request, verify manually:

- [ ] Light and dark modes both render legibly.
- [ ] Theme selection persists after reload and navigation.
- [ ] Homepage and catalogue cards link to the correct paths.
- [ ] Search and topic/level filters work.
- [ ] Lesson checkboxes and progress tracking work.
- [ ] Mobile navigation works at narrow viewport widths.
- [ ] Keyboard focus is visible and reduced-motion preferences are respected.
- [ ] No new JavaScript errors appear in DevTools Console.

## Project structure

```text
.
├── index.html                   Homepage
├── paths.html                   Filterable learning-path catalogue
├── path-*.html                  Learning-path lesson pages
├── azure.html                   Azure certification roadmap
├── cert-*.html                  Certification study pages
├── resources.html               Learning resources
├── 404.html                     Not-found page
├── shorts.html                  Legacy redirect to the homepage
├── assets/
│   ├── style.css                Generated shared stylesheet
│   ├── app.js                   Generated search and site behavior
│   └── theme-init.js            Early theme preference bootstrap
├── src/
│   ├── content.py               Learning paths, lessons, resources, certifications
│   ├── build.py                 Generates HTML and runtime assets
│   ├── style.css                Canonical stylesheet source
│   ├── app_src.js               Canonical application JavaScript source
│   └── theme_init.js            Canonical early theme bootstrap source
├── scripts/
│   └── check_site.py            Dependency-free link/anchor and asset checker
├── .github/workflows/
│   ├── site-check.yml           CI checks
│   └── deploy-pages.yml         Build, validate, and deploy to GitHub Pages
├── CONTRIBUTING.md              Contributor workflow and review expectations
├── AI_PROMPT_LOG.md             Design and implementation prompt record
├── LAB-2.1-DEMO.md              Challenge rubric and demo checklist
├── firebase.json                Firebase Hosting configuration
└── .nojekyll                    Disables Jekyll processing on Pages
```

### Editing guidance

- Content: edit `src/content.py`.
- Shared visual styles: edit `src/style.css`.
- Client behavior: edit `src/app_src.js`.
- Early theme selection: edit `src/theme_init.js`.
- Page templates/build process: edit `src/build.py`.
- Static-site validation: edit `scripts/check_site.py`.

Regenerate and test the site after source changes. Commit relevant source files and generated output together. Avoid editing generated assets alone, because a rebuild would overwrite the change.

## GitHub Pages deployment

Deployment is handled by [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml). It builds the website from the source, checks JavaScript syntax and local links, validates generated/source asset parity, uploads the static `_site/` artifact, and deploys it to GitHub Pages.

### One-time setup required

A repository administrator must enable Pages for this fork:

1. Open [Settings → Pages](https://github.com/Chetan-code-lrca/gyaanify/settings/pages).
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Save if GitHub shows a Save button.

The workflow first builds and validates the site, then invokes GitHub's Pages deployment API. If Pages has not been enabled, the deploy step fails with an HTTP `404 Not Found` / “Ensure GitHub Pages has been enabled” message. This is a repository setup prerequisite rather than a build failure: the build and `Site quality checks` can pass while Pages is disabled. After enabling Pages and selecting **GitHub Actions** as the source, rerun the deployment workflow.

### Trigger deployment

The Pages workflow runs on pushes to `main` and `contrib/site-wide-theme-quality`, and supports manual execution:

1. Open the [deployment workflow](https://github.com/Chetan-code-lrca/gyaanify/actions/workflows/deploy-pages.yml).
2. Choose **Run workflow**.
3. Select `contrib/site-wide-theme-quality` to deploy the reviewed contribution branch, or `main` after the change has been merged.
4. Inspect the workflow run. The build must pass before the deploy job can run.

Expected project-site URL after a successful deployment:

**https://chetan-code-lrca.github.io/gyaanify/**

GitHub Pages is public. Review the repository contents and remove secrets or private material before enabling public hosting. After the first successful deployment, confirm the published URL in **Settings → Pages** and test it in a real browser.

### Deployment troubleshooting

| Symptom | Cause / action |
|---|---|
| `Configure GitHub Pages` reports `Get Pages site failed` or HTTP 404 | Enable Pages and set the source to **GitHub Actions** in repository Settings → Pages, then rerun the workflow. |
| Build or site-check job fails | Open the failed step in Actions; fix its specific log output before retrying. |
| CSS/JavaScript does not reflect source edits | Run `python src/build.py .`, check generated diffs, and commit source plus generated assets. |
| Theme flashes or the theme control is missing | Confirm the page loads `assets/theme-init.js` before `assets/style.css` and loads `assets/app.js` at the end of the body. |
| Page loads but assets return 404 | Check that paths are relative (for example `assets/style.css`, not an absolute `/assets/style.css`) so the project-site `/gyaanify/` prefix is preserved. |
| A workflow succeeds but the URL is not available yet | Check Settings → Pages for the published URL and wait for GitHub Pages to finish publishing; inspect the latest Actions run. |

## Contributing

Contributions for content accuracy, accessibility, responsive behavior, performance, and learning experience are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before making a substantial change.

For pull requests, include:

1. The problem being addressed and who it helps.
2. The implementation summary and relevant trade-offs.
3. Automated check results and manual checks actually completed.
4. Before/after screenshots for visual changes.
5. Known limitations or follow-up work.

Automated tests do not replace manual checks for color contrast, keyboard use, responsive behavior, or learning workflows.

## Project documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) — source of truth, build process, validation, and PR expectations.
- [AI_PROMPT_LOG.md](AI_PROMPT_LOG.md) — prompts and design decisions recorded for the makeover.
- [LAB-2.1-DEMO.md](LAB-2.1-DEMO.md) — judging-criteria mapping and demo checklist.
- [Site quality workflow](.github/workflows/site-check.yml) — automated quality checks.
- [GitHub Pages workflow](.github/workflows/deploy-pages.yml) — deployment pipeline.
