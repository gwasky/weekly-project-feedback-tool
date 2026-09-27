# Design System

How the UI looks and behaves. Read this before building or changing any page.

The app is server-rendered Django templates with HTMX. Styling is plain CSS in `static/css/app.css`, driven by the design tokens below. There is no CSS framework or JavaScript build step.

---

## 1. Principles

- **Quiet and fast.** Weekly reporting should take minutes. Few colours, no decoration, no animation beyond small transitions.
- **Content first.** Submissions and summaries are text; give them readable line lengths and generous spacing.
- **No health signals.** The product deliberately has no project health indicators. Never colour projects, summaries or submissions red, amber or green to suggest how a project is doing. Colour is only for interface state (errors, focus, links, late markers).
- **Humans decide.** Anything the AI produced is labelled as a draft and shows where each point came from. Publishing always needs an explicit, confirmed action.
- **Works without JavaScript tricks.** Every form works as a normal POST; HTMX makes it nicer, not possible.

---

## 2. Design tokens

Defined once as CSS custom properties on `:root` in `app.css`. Use the tokens; never hard-code colours, sizes or spacing in templates or other CSS.

### Colour

| Token | Light | Dark | Use |
|---|---|---|---|
| `--color-bg` | `#f7f7f5` | `#161616` | Page background |
| `--color-surface` | `#ffffff` | `#1f1f1f` | Cards, forms, dropdowns |
| `--color-border` | `#e2e2de` | `#333333` | Dividers, input borders |
| `--color-text` | `#1b1b1b` | `#ececec` | Body text |
| `--color-text-muted` | `#5f5f5a` | `#a3a3a3` | Secondary text, timestamps |
| `--color-accent` | `#2f5bd3` | `#7d9cf0` | Links, primary buttons, focus ring |
| `--color-accent-contrast` | `#ffffff` | `#111111` | Text on accent |
| `--color-danger` | `#b3261e` | `#f08b84` | Form errors, destructive actions |
| `--color-late` | `#8a5a00` | `#e0b45c` | "Late" badge only |
| `--color-draft` | `#6b4fbb` | `#b7a3f0` | "AI draft" label only |

Dark values apply under `@media (prefers-color-scheme: dark)`. Text on any background must meet WCAG AA contrast (4.5:1 for body text).

### Typography

- Font: system stack — `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.
- Sizes: `--text-sm` 0.875rem · `--text-base` 1rem · `--text-lg` 1.125rem · `--text-xl` 1.375rem · `--text-2xl` 1.75rem.
- Line height 1.5 for body, 1.25 for headings.
- Weights: 400 for text, 600 for headings, labels and buttons. No other weights.
- Reading width: long text blocks max `68ch`.

### Spacing, radius, shadow

- Spacing scale: `--space-1` 0.25rem · `--space-2` 0.5rem · `--space-3` 0.75rem · `--space-4` 1rem · `--space-6` 1.5rem · `--space-8` 2rem · `--space-12` 3rem.
- Radius: `--radius` 6px for inputs, buttons and cards; `--radius-pill` 999px for badges.
- Shadow: `--shadow` for dropdowns only. Cards use a border, not a shadow.

---

## 3. Layout

- **Page shell** (`base.html`): header, then a centred main column, max width `72rem`, with side padding of at least `--space-4`.
- **Header**: app name (links home), main navigation (My projects, All projects), notifications bell, user menu with logout.
- **Page title**: one `<h1>` per page, with the project name and week where relevant (e.g. "Payments revamp — week of 22 Sep").
- **Two-column pages** (review view, draft editor): main content left, context right (submissions, sources). Below `48rem` wide, columns stack.
- All pages work at 400px width. Only tables may scroll horizontally, inside their own container.

---

## 4. Components

Each reusable component is a template in `templates/components/` used with `{% include %}`. Add a new component there before copying markup between pages.

### Buttons

| Variant | Use |
|---|---|
| Primary (accent fill) | The main action on a page: Submit, Publish. At most one per view. |
| Secondary (border) | Save draft, Regenerate, Cancel. |
| Danger (danger text/border) | Remove, Drop. Never used for Publish. |
| Link-style | Minor actions inside rows: Edit, Remove entry. |

Buttons use verbs ("Submit update", "Request changes"), never "OK" or "Yes".

### Forms

- Every field has a visible `<label>`; no placeholder-only fields.
- Required fields are marked "(required)" in the label; optional ones need no marker.
- Errors appear under the field in `--color-danger`, plus a summary at the top of the form listing each error.
- Help text sits under the label in `--color-text-muted`.

### Entry lists

Used for achievements, outcomes, next steps and open items in the submission form.

- Each row: text field, optional objective/milestone selector, and a remove link.
- "Add achievement" / "Add outcome" / etc. appends a new row via HTMX.
- Reorder with Move up / Move down buttons (keyboard accessible), not drag-only.

### Carried-forward items

- Last week's next steps appear at the top of the next-steps section, each with a three-way choice: Completed · Carried forward · Dropped, shown as a radio group.
- Open blockers and risks show owner, target date and "raised in week of …", with actions: Add note · Change date · Mark resolved.
- A target date in the past is shown in `--color-text-muted` with "(past target date)" in text — not red.

### Badges

Small pill labels, text always included (never colour alone).

| Badge | Style |
|---|---|
| Not started · Draft · Submitted | Neutral (border + muted text) |
| Changes requested | Neutral border, `--color-text` |
| Late | `--color-late` |
| AI draft | `--color-draft` |
| Published | Accent outline |

### Cards

Surface background, 1px border, `--radius`, padding `--space-6`. Used for a submission, a summary section or a project in a list.

### Summary

Always the four sections in this order and with these headings: **Achievements · Outcomes · Blockers / Risks · Next Steps**. Empty sections say "Nothing reported this week." rather than disappearing.

In the draft editor each bullet shows its sources as small chips (e.g. "Amina · achievement") linking to the submission. Bullets removed during source checking are listed in a collapsible "Removed — no valid source" panel.

The published summary shows the week, the publisher and the publish date, with no edit controls.

### Review comments

Shown above the submission content, newest first, with reviewer, date and a "Changes requested" badge when relevant. No reply box (comments are one-way).

### Notifications

- Bell in the header with an unread count badge (hidden when zero).
- Dropdown lists the 10 most recent: message, relative time, link. Unread items have a left accent border.
- "Mark all read" at the bottom.

### Empty states

Every list has one: a short sentence saying what will appear and, if the user can act, one action. E.g. "No submissions yet this week." · "You're not on any projects yet."

### Confirmation step

Irreversible actions (Publish) use an in-page confirmation, not a browser dialog: the button reveals a panel stating what will happen ("This becomes the official summary for the week of 22 Sep and can't be changed.") with **Publish summary** and **Cancel**.

### Messages

Success and error messages after an action use Django's messages framework, shown at the top of the main column and dismissible.

---

## 5. HTMX patterns

- Fragments live in `templates/partials/`, named after what they render (`partials/entry_row.html`, `partials/notification_count.html`).
- A view returns the fragment when the request has `HX-Request`, and the full page otherwise.
- Prefer `hx-target` + `hx-swap="outerHTML"` on the smallest element that changes.
- Show a loading state for anything slower than a click: `hx-indicator` with a small "Saving…" text, and disable the triggering button while in flight.
- On a failed request, show the error inline where the action happened; never fail silently.
- Polling (notification count) is every 60 seconds; nothing else polls.

---

## 6. Accessibility

- All interactive elements are reachable and usable by keyboard, in a logical order.
- Visible focus ring on everything focusable: 2px `--color-accent` outline with offset.
- Colour is never the only signal; badges and states always include text.
- Use semantic HTML first: `<button>` for actions, `<a>` for navigation, `<fieldset>`/`<legend>` for grouped choices such as the Completed / Carried forward / Dropped radios.
- HTMX-updated regions that report results (save status, notification count) use `aria-live="polite"`.

---

## 7. Writing

- Plain, short, active sentences. Sentence case for headings and buttons.
- Say "week of 22 Sep", not cycle IDs or ISO dates.
- Say "project lead", "team member" and "summary" consistently; don't mix in "manager", "report" or "digest".
- Don't describe how a project is doing in interface text (no "on track", "at risk", "healthy").
