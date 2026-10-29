# Lab 2.1 — Demo and Validation Plan

## Objective

Improve one area of the Gyaanify website—the learning-path cards—without changing the rest of the product or adding infrastructure.

## What changed

- Card styling: more consistent spacing, rounded corners, restrained elevation, and a blue/teal accent.
- Topic thumbnails: distinct but coordinated color treatments using CSS gradients.
- Information hierarchy: clearer topic and level labels, card headings, and lesson/time metadata.
- Usability cue: visible “Explore learning path” cue; the card remains its original link.
- Accessibility and responsive behavior: explicit focus styling, smaller-screen spacing, and reduced-motion handling.

## Rubric mapping (10 points total)

| Criterion | Points | Demonstration evidence |
|---|---:|---|
| Enterprise look and feel | 3 | Show consistent card layouts, typography, colored topic thumbnails, level badges, and subtle elevation. |
| Usefulness of change | 3 | Explain scanability and the visible navigation cue; click a card and show it still opens its lesson path. |
| Smart use of AI prompts | 2 | Open `AI_PROMPT_LOG.md`; explain the design, implementation constraints, and critic/validation prompt. |
| Demo and explanation | 2 | Present the before/after comparison and explain the limited scope and test results honestly. |

These are rubric-aligned deliverables, not a guaranteed score.

## Local test checklist

- [ ] Capture the original homepage before applying the branch.
- [ ] Open the updated homepage and capture the same viewport.
- [ ] Confirm all visible cards open the right destination.
- [ ] Test home-page search.
- [ ] Open `paths.html`; test a topic filter and a level filter.
- [ ] Use Tab/Shift+Tab to confirm the focused card has a visible outline.
- [ ] Check the page in a narrow viewport (e.g. mobile emulation or a narrow browser window).
- [ ] Check light and dark system themes.
- [ ] Enable reduced-motion preferences and confirm card motion is suppressed.
- [ ] Check browser DevTools Console for new errors.

## Suggested 60-second talk track

**0–10 seconds — Problem:** “The learning paths are useful, but the cards can make topic, level, time, and the next action easier to scan.”

**10–30 seconds — Before/after:** “I focused on this one reusable card component. I improved spacing and hierarchy, added topic-specific CSS treatments, and made hover and keyboard focus easier to see.”

**30–45 seconds — Usability:** “The entire card remains the existing link, and the visible ‘Explore learning path’ cue makes that action clearer. Search, filters, routes, and progress behavior were not rewritten.”

**45–60 seconds — AI and reliability:** “I used a design prompt, an implementation prompt with scope constraints, and a critic prompt. I tested the existing workflows and responsive/accessibility checks listed here. These are the checks I completed, and these are any remaining limitations.”

Only say that an individual check passed after actually testing it in the browser.

## Site-wide theme switch checks

- [ ] Toggle from light to dark mode in the header.
- [ ] Navigate to another page and confirm the selected theme persists.
- [ ] Reload and confirm the selection persists.
- [ ] Test first-visit behavior in a fresh/private browser profile with system light mode, then dark mode.
- [ ] Inspect the homepage, catalogue, one lesson page, Azure/certification page, and resources page in both modes.
- [ ] Check text, links, buttons, search suggestions, filter buttons, lesson checkboxes, progress bar, and footer contrast.
- [ ] Confirm the theme button has an accessible label and can be activated with Enter/Space.
- [ ] Confirm no JavaScript errors appear in DevTools Console.

