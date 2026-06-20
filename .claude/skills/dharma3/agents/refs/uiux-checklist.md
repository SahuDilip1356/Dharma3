# UI/UX reference pack  (distilled from Dharma 0.x uiux-* skills)

The **design** operating agent loads this on demand. Standard: **WCAG 2.1 AA** (AAA for
healthcare / compliance-critical). Output findings as `file:line [severity] rule → fix`.

## 1. Accessibility (a11y)
- **Contrast:** normal text ≥ 4.5:1 · large text (≥18px / ≥14px bold) ≥ 3:1 · UI components/focus rings ≥ 3:1.
- **Never color alone:** status = icon + color + text; form errors = message + icon + border; links = underline.
- **Keyboard:** every interactive element reachable + operable by keyboard; visible focus ring; logical tab order; no traps; Esc closes modals.
- **Screen reader:** semantic HTML first (`button`, `nav`, `main`, `h1–h6` in order); labels on every input; `alt` on meaningful images; ARIA only when semantics can't express it.
- **Forms:** label tied to input; errors announced; required state not color-only.

## 2. Responsive
- Verify at **375px (mobile) · 768px (tablet) · 1280px (desktop)**.
- No horizontal scroll; tap targets ≥ 44×44px; content reflows (not just shrinks); test long strings + small screens together.

## 3. Interaction & states (the slop killers)
- Every view handles: **default (realistic content, not Lorem) · loading (skeleton/spinner) · empty · error · success**.
- Broken/empty states are a defect, not a nicety. Disabled vs loading vs error are visually distinct.
- Motion respects `prefers-reduced-motion`.

## 4. Design system consistency
- Reuse tokens (spacing, color, type scale, radius) — no one-off values.
- Match existing component patterns; don't invent a new visual language per screen.

## 5. Final visual QA (last gate before ship)
- Screenshot each breakpoint × each state. **Look at the image** — catch spacing, alignment, overlap, contrast, intent drift.
- Compare to the design intent / established system. Verdict: **ship / hold** with specific issues.
