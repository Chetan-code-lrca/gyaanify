# AI Prompt Log — Lab 2.1: Gyaanify Website Makeover

**Target component:** Learning-path cards on the home page and learning-path catalogue  
**Constraint:** Keep the scope to one component; preserve the site's existing HTML structure and JavaScript behavior.  
**Implementation:** CSS-only card styling in `assets/style.css`, plus this documentation.

## Prompt 1 — Design plan

> Act as a senior product designer and front-end engineer. Review the Gyaanify learning-path cards and propose a focused enterprise-quality makeover for this one component only. Prioritize clear information hierarchy, scanability, purposeful color, consistent spacing, responsive layouts, accessible keyboard focus, reduced-motion support, and an obvious next action. Keep the existing static HTML/CSS/JavaScript architecture. Do not add dependencies, API calls, new services, or features that require a backend. Preserve existing link targets, search, filters, lesson progress, and theme behavior. Explain the intended change before implementation.

**Decision:** Improve the existing card component rather than redesigning the full website. The same `.pcard` component is reused on both the homepage and catalogue, so shared CSS gives consistent treatment in both places.

## Prompt 2 — Implement with constraints

> Implement the approved learning-card makeover as a small, maintainable CSS enhancement appended to the existing stylesheet. Use the current design tokens and existing classes wherever possible. Add a restrained blue/teal accent, stronger card elevation and hover/focus states, improved topic thumbnails and difficulty badges, readable metadata, and a visible “Explore learning path” cue. Include responsive spacing and honor `prefers-reduced-motion`. Do not modify content, routes, application JavaScript, filters, or progress-tracking logic. Avoid external assets, frameworks, libraries, and paid services. Scope every rule to the learning-card component unless a shared grid alignment rule is essential.

**Decision:** Keep the whole card as its existing anchor. The “Explore learning path” text is a visual cue inside the card, not a separate nested control.

## Prompt 3 — Critique and validation plan

> Review the CSS change as a strict code reviewer. Check that it is limited to the learning-card area; existing selectors still work; light and dark theme values remain legible; focus is visible; reduced-motion is respected; narrow screens do not overflow; and no JavaScript or links have been changed. Identify checks that require a real browser and do not claim they passed unless they were actually run. Provide a concise before/after demonstration plan mapped to the workshop rubric: enterprise look and feel (3), usefulness (3), smart AI prompt use (2), demo/explanation (2).

**Review outcome:** The patch only modifies `assets/style.css`; no HTML or JavaScript files are changed. The browser behavior and visual result still need to be verified locally using the checklist in `LAB-2.1-DEMO.md`.

## Evidence to capture

- Before: homepage with the original learning cards.
- After: the same viewport with the enhanced cards.
- Show hover and keyboard focus on a card.
- Open the learning-path catalogue and test one topic/level filter.
- Resize the browser to a narrow viewport.
- Confirm no new errors in the browser console.

Do not report the work as fully validated until these browser checks are complete.

## Prompt 4 — Extend the design system and theme control site-wide

> Extend the approved makeover beyond the homepage cards to the shared site experience. Keep the static HTML/CSS/vanilla-JavaScript architecture and preserve all current links, search, filters, lesson progress, and mobile navigation. Add a user-visible day/night toggle to the shared header on every page using the shared app script. Use the existing CSS variables so backgrounds, text, borders, surfaces, and controls switch together. Respect the operating-system preference on first visit, persist an explicit choice in localStorage, and make the toggle keyboard accessible with an accessible label. Refine shared buttons, focus states, search, cards, lesson surfaces, and footer with restrained styling. Do not add dependencies, remote APIs, or backend requirements. Test syntax and check every page that loads the shared app script; clearly distinguish code inspection from browser validation.

**Implementation decision:** The theme control is injected into the common header by `assets/app.js`, so the repeated page templates do not each need a separate button. The CSS uses `data-theme="light"` and `data-theme="dark"` on the document root; a saved choice wins, otherwise the first load follows the OS preference. The selection is stored under `gy-theme`.

**Validation status:** The shared HTML pages were checked for the shared script/header, and CSS brace balance was checked after editing. Real browser checks for visual contrast, theme persistence, mobile layout, and feature regressions remain to be completed locally.

## Prompt 5 — Make the change maintainable for upstream review

> Review the repository's source/generated-file workflow. Ensure styling and behavior edits live in the source files consumed by the build rather than only in generated assets. Add a tiny early theme bootstrap so saved light/dark preference is applied before stylesheets load. Add dependency-free automated checks for local links/anchors and shared asset inclusion, and a GitHub Actions workflow that checks JavaScript syntax and source/generated asset parity. Document how contributors reproduce the build and test changes. Keep the project dependency-free and do not claim browser tests were completed unless they were actually run.

**Outcome:** `src/style.css` and `src/app_src.js` are aligned with `assets/style.css` and the generated `assets/app.js`. `src/build.py` emits the theme bootstrap before stylesheets and copies the generated bootstrap asset. CI checks local navigation, script syntax, generated output, and source/asset consistency. The link checker understands the existing category-chip convention where URL fragments correspond to `data-v` filter values rather than HTML IDs.

