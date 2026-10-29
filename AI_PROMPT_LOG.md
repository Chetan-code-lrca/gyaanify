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
