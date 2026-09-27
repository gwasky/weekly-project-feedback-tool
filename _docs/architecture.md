# Weekly Project Feedback Tool — Architecture

Companion to `plan.md`. Records the chosen tech stack, data model, project layout and build order.

Status: **draft for review** — no code written yet.

---

## 1. Decision

**Option 1 — Django monolith, server-rendered with HTMX.**

The product is mostly forms, records and permissions, plus one scheduled AI job. Django covers login, permissions, admin and migrations out of the box and keeps the project in Python. If the lead's draft-editing screen later outgrows HTMX, that single page can become a React component without changing the rest.

### Stack

| Layer | Choice | Notes |
|---|---|---|
| Language / packaging | Python 3.13, `uv` | `pyproject.toml` + `uv.lock` |
| Web framework | Django 5.2 LTS | Custom `User` model from day one |
| Database | PostgreSQL 17 | Local via `docker compose` |
| Frontend | Django templates + HTMX 2 (+ Alpine.js where needed) | No JS build step |
| Styling | Plain CSS with design tokens | See `design-system.md` |
| Background jobs | Procrastinate (Postgres-backed queue with periodic tasks) | Avoids running Redis |
| AI | Anthropic Python SDK, `claude-sonnet-5` | Structured output with source citations |
| Auth | Company SSO over OIDC (`mozilla-django-oidc`) | Username/password login in dev only |
| Config | `django-environ` | Settings split: `base`, `dev`, `prod` |
| Quality | `ruff`, `pytest-django`, `factory-boy` | |

---

## 2. Assumption on the open question (plan §21)

**A user can belong to several projects at once.** Membership is its own table, so this costs nothing now. If the answer turns out to be "one project per user", a single constraint enforces it.

---

## 3. Django apps

| App | Responsibility |
|---|---|
| `accounts` | Custom user, SSO login |
| `projects` | Projects, memberships, objectives, milestones, access rules |
| `cycles` | The company-wide weekly reporting cycle and its deadline |
| `submissions` | Contributor submissions, revisions, next steps, blockers and risks, review comments |
| `summaries` | AI draft generation, draft editing, publication |
| `notifications` | In-app notifications |

---

## 4. Data model

### accounts

**User** (extends `AbstractUser`): email is the login identifier; stores display name.

### projects

**Project**: `name`, `description`, `created_at`, `archived_at` (nullable).

**ProjectMembership**: `project`, `user`, `role` (`lead` | `member`), `joined_at`, `left_at` (nullable).
- Unique active `(project, user)`.
- Partial unique index: exactly one active `lead` per project.

**Objective**: `project`, `title`, `description`, `is_active`.
**Milestone**: `project`, `title`, `target_date`, `is_active`.
Both are optional and can be added after setup (plan §8, §10).

### cycles

**ReportingCycle**: `week_start` (date, unique), `deadline` (datetime), `status` (`open` | `closed`).
- One row per week for the whole company (plan §6).
- The deadline comes from a single setting, e.g. `REPORTING_DEADLINE = "FRI 17:00 Africa/Nairobi"`.

### submissions

**Submission**: `project`, `cycle`, `author`, `status` (`draft` | `submitted` | `changes_requested`), `first_submitted_at`, `updated_at`.
- Unique `(project, cycle, author)`.
- Holds the *current* editable content through its child rows below.

**SubmissionEntry**: `submission`, `kind` (`achievement` | `outcome`), `text`, `objective` (nullable FK), `milestone` (nullable FK), `position`.
Achievements and outcomes are lists of entries rather than one text blob. That lets each entry link to an objective or milestone (plan §8) and lets the AI cite individual entries.

**NextStep**: `submission`, `text`, `carried_from` (nullable self-FK), `position`.

**NextStepDisposition**: `next_step` (from the previous week), `submission` (this week's), `disposition` (`completed` | `carried_forward` | `dropped`).
- When a new submission is opened, last week's next steps are shown pre-filled (plan §9).
- Choosing *carried forward* also creates a new `NextStep` with `carried_from` set, so each item's history can be followed across weeks.

**OpenItem** (blockers and risks): `project`, `kind` (`blocker` | `risk`), `description`, `owner` (FK User, must be a project member), `target_resolution_date`, `raised_in` (FK Submission), `status` (`open` | `resolved`), `resolved_at`, `resolved_in` (nullable FK Submission).
- Belongs to the project, not to one week. Open items appear in every submission until resolved, so "carrying forward" requires no copying (plan §9).

**OpenItemUpdate**: `open_item`, `submission`, `note`, `new_status`, `new_target_date`, `created_at`. Records what was said about an item each week.

**SubmissionRevision**: `submission`, `number`, `snapshot` (JSON of the full submission content), `created_at`, `is_late`.
- A new, never-modified row is written on every submit or resubmit.
- `is_late = created_at > cycle.deadline` (plan §13).
- This is the audit trail. Live rows can change; revisions cannot.

**ReviewComment**: `submission`, `revision` (the revision being reviewed), `reviewer`, `body`, `requests_changes` (bool), `created_at`.
- One-way (plan §12). If `requests_changes` is true, the submission status becomes `changes_requested` and the author is notified.

### summaries

**SummaryDraft**: `project`, `cycle`, `status` (`pending` | `generating` | `ready` | `failed`), `generated_content` (JSON), `edited_content` (JSON), `input_snapshot` (JSON of the revisions fed to the model), `model`, `prompt_version`, `raw_response`, `error`, `created_at`, `edited_by`, `updated_at`.
- A project and cycle can have several drafts, because the lead can regenerate one.
- Everything needed to reproduce or audit a draft is stored on it.

**PublishedSummary**: `project`, `cycle`, `content` (JSON: the four sections), `source_draft`, `published_by`, `published_at`.
- Unique `(project, cycle)`.
- **Immutable** (plan §15): a Postgres trigger rejects `UPDATE` and `DELETE`, and the model's `save()` refuses to update an existing row.
- The stakeholder view reads the newest row per project (plan §16).

### notifications

**Notification**: `recipient`, `kind`, `project`, `cycle`, `message`, `url`, `created_at`, `read_at`.
Kinds: `submission_reminder`, `submission_missing`, `changes_requested`, `submission_revised`, `draft_ready`, `summary_published`.

### Relationship sketch

```text
User ──< ProjectMembership >── Project ──< Objective / Milestone
                                  │
ReportingCycle ──< Submission >───┤ (author = User)
                     │            │
                     ├──< SubmissionEntry
                     ├──< NextStep ──< NextStepDisposition
                     ├──< SubmissionRevision
                     ├──< ReviewComment
                     │
                  OpenItem (project-level) ──< OpenItemUpdate

Project + ReportingCycle ──< SummaryDraft ──1 PublishedSummary
```

---

## 5. Access rules

All checks live in `projects/permissions.py`, and every view calls them.

| Action | Who |
|---|---|
| View a project's submissions | Active members of that project |
| Create or edit a submission | Its author only |
| Comment or request changes | The project lead |
| View or edit drafts | The project lead |
| Publish | The project lead |
| View the latest published summary | Any signed-in user |
| Create projects, manage membership | Staff (Django Admin), to start with |

---

## 6. Scheduled jobs (Procrastinate periodic tasks)

| Job | When | What it does |
|---|---|---|
| `open_cycle` | Monday 00:00 | Creates the week's `ReportingCycle`. Submissions are created on first open, with next steps and open items pre-filled. |
| `send_reminders` | Deadline minus 24h, and minus 2h | Notifies active members with no submitted `Submission`. |
| `close_cycle` | At the deadline | Marks the cycle closed and enqueues one `generate_draft` per active project. |
| `generate_draft(project, cycle)` | Enqueued | Builds the input, calls Claude, stores the draft and notifies the lead. Retries on failure. |

Edge cases:
- **No submissions for a project**: store a draft saying so, without calling the model.
- **Late revision after a draft exists**: notify the lead, mark the draft "inputs changed", and offer **Regenerate**. The draft is never rewritten automatically.

---

## 7. AI summary generation

Lives in `summaries/services/summarizer.py`.

1. **Input**: the latest `SubmissionRevision` for each contributor, with every entry, next step and open item given a stable ID (e.g. `E12`, `N4`, `B7`).
2. **Prompt**: stored in a versioned file, `summaries/prompts/v1.md`. It states the plan §3 rules: only use given facts; remove duplicates; no recommendations, health assessment or inference.
3. **Output**: forced through a tool/JSON schema:
   ```text
   { achievements: [{text, sources: [ids]}],
     outcomes:     [...],
     blockers_risks: [...],
     next_steps:   [...] }
   ```
4. **Validation**: every `sources` ID must exist in the input. Bullets without a valid source are dropped and reported to the lead.
5. **Review UI**: each bullet links to the submissions it came from, so the lead can check it before publishing.
6. **Settings**: low temperature. `model` and `prompt_version` are stored on the draft.

---

## 8. Main screens

| Screen | Users |
|---|---|
| My projects / this week's status | Everyone |
| Submission form (entries, pre-filled next steps with dispositions, open items) | Contributor |
| Project week view (all submissions for the cycle) | Project members |
| Review view (submission, revision history, comment / request changes) | Lead |
| Draft editor (sections with source links, regenerate, publish) | Lead |
| Project summary page (latest published summary) | Everyone |
| Notifications dropdown (polled via HTMX) | Everyone |
| Django Admin (projects, memberships, objectives, milestones) | Staff |

---

## 9. Repository layout

```text
ai-native/
├── pyproject.toml
├── uv.lock
├── manage.py
├── docker-compose.yml          # postgres
├── .env.example
├── config/
│   ├── settings/{base,dev,prod}.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── apps/
│   ├── accounts/
│   ├── projects/
│   ├── cycles/
│   ├── submissions/
│   ├── summaries/
│   │   ├── services/summarizer.py
│   │   └── prompts/v1.md
│   └── notifications/
├── templates/                  # base.html, partials/ for HTMX fragments
├── static/
├── tests/
└── _docs/
```

---

## 10. Build order

1. **Skeleton**: uv project, Django settings, Postgres in Docker, custom User, dev login, ruff and pytest.
2. **Projects**: models, membership rules, Django Admin, access helpers.
3. **Cycles and submissions**: cycle model, submission form, revisions with late flag.
4. **Continuity**: next-step dispositions, open items and their updates.
5. **Review**: project week view, review comments, request changes.
6. **Notifications and scheduling**: Procrastinate, reminders, cycle open and close.
7. **AI drafts**: summarizer, draft editor with source links, regenerate.
8. **Publishing**: immutable published summaries, stakeholder page.
9. **SSO and deployment**: OIDC, production settings, container image.

---

## 11. To confirm

- Reporting deadline day, time and timezone.
- SSO provider (Okta, Entra ID, Google Workspace, …).
- ~~Tailwind or plain CSS~~ — plain CSS (see `design-system.md`).
- Hosting target (a cloud container service, or inside the company network).
- Multi-project membership (assumed **yes**, §2).
