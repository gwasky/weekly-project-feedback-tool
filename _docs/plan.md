# Weekly Project Feedback Tool — Scope Draft

## 1. Product Purpose

Build a standalone web application for collecting, reviewing, consolidating, and publishing weekly project feedback.

The tool is intended for three audiences:

- **Team members** — submit weekly project updates.
- **Project leads/managers** — review individual submissions and publish a consolidated weekly summary.
- **Stakeholders/executives** — read the latest published project summary.

The core workflow is:

**Individual submissions → Project lead review → AI-generated draft summary → Project lead approval → Published stakeholder summary**

---

## 2. Core Reporting Model

### Submission model

The tool uses a **hybrid model**:

- Individual contributors submit their own weekly updates.
- The project lead reviews the submissions.
- The system generates a consolidated project-level draft.
- The project lead edits and publishes the final weekly summary.

### Individual weekly submission structure

Each contributor submits:

- **Key achievements**
- **Measurable outcomes**
- **Blockers**
- **Risks**
- **Next steps**

The emphasis is on outcomes rather than simple activity reporting.

---

## 3. AI Assistance

The tool is **AI-assisted**, not AI-controlled.

### AI responsibilities

At the weekly deadline, the system automatically generates a draft executive summary from submitted updates.

The AI should:

- Consolidate contributor inputs.
- Remove duplication.
- Produce a concise project-level summary.
- Use only facts contained in contributor submissions.

The AI should **not**:

- Infer unreported conclusions.
- Recommend what the project should do.
- Assess project health.
- Invent missing information.
- Publish anything automatically.

### Final summary structure

Every generated summary follows this fixed structure:

1. **Achievements**
2. **Outcomes**
3. **Blockers / Risks**
4. **Next Steps**

---

## 4. Project Health

The tool will **not use explicit project health indicators** such as:

- Green / Amber / Red
- On Track / At Risk / Off Track
- Confidence scores

The weekly summary itself should communicate the state of the project.

---

## 5. Product Surface

The product will be a **standalone web application**.

It will act as the system of record for weekly feedback.

For the initial scope:

- No Slack/Teams-first workflow.
- No email-first workflow.
- No external subscription mechanism.

---

## 6. Reporting Cadence

All projects follow a **single company-wide weekly reporting cycle**.

The reporting deadline is fixed rather than configurable per project.

### Missed submissions

The system sends **automatic in-app reminders** to contributors who have not submitted.

There is no manager escalation workflow in the initial scope.

---

## 7. Team Visibility

Individual weekly submissions are visible to **all members of the same project team**.

This promotes transparency and helps reduce duplicate reporting.

Published project summaries are visible to **anyone in the organization with access to the tool**.

People outside the project do not subscribe to updates; they must visit the project page to read the latest published summary.

---

## 8. Objectives and Milestones

Weekly updates can optionally be linked to predefined:

- Project objectives
- Project milestones

This linkage is **optional**, not mandatory.

The tool should provide traceability without making weekly reporting cumbersome.

---

## 9. Week-to-Week Continuity

The tool maintains continuity between reporting cycles.

### Next steps

Previous week's next steps are automatically pre-populated into the new week's submission.

The contributor can mark each item as:

- Completed
- Carried forward
- Dropped

### Blockers and risks

Unresolved blockers and risks automatically carry forward into future reporting cycles until resolved.

Each blocker and risk must include:

- **Owner**
- **Target resolution date**

This creates an actionable open-items layer without turning the product into a task-management system.

---

## 10. Project Setup

Project creation should remain lightweight.

Required project fields:

- **Project name**
- **Description**
- **Project lead**
- **Team members**

Objectives, milestones, and other detailed project-management metadata are not required during setup.

---

## 11. Task Management Boundary

The tool is **not a task-management product**.

It will not support:

- General task creation
- Task boards
- Dependencies
- Sprint planning
- Backlogs
- Full project execution tracking

The product remains focused on:

- Weekly feedback
- Outcomes
- Blockers
- Risks
- Next steps
- Summary generation

---

## 12. Submission Ownership and Review

Contributors retain ownership of their individual submissions.

Project leads cannot directly edit contributor submissions.

Instead, the project lead can:

- Review a submission.
- Leave a review comment.
- Request changes.

For the MVP, review comments are **one-way**.

Contributors respond by revising their submission rather than replying in a comment thread.

---

## 13. Late Changes

Contributors may revise submissions after the weekly deadline.

Late changes must be **clearly marked** so there is an audit trail.

---

## 14. Publication Workflow

At the weekly deadline:

1. Contributor submissions close for the normal reporting cycle, though late edits remain possible and are marked.
2. The system automatically generates a draft project summary.
3. The project lead reviews and edits the draft.
4. The project lead manually clicks **Publish**.
5. The published summary becomes the official weekly project update.

There is **no automatic publication**.

---

## 15. Published Summary Immutability

Once a weekly project summary is published, it is **immutable**.

The published version becomes the official record for that reporting cycle.

---

## 16. Stakeholder Experience

Stakeholders see only the **latest published weekly summary** for each project.

The initial product will not expose a browsable historical archive of weekly summaries to stakeholders.

However, the system still retains historical data internally.

---

## 17. Historical Data Retention

The system retains all historical:

- Individual submissions
- Generated drafts
- Review activity
- Carried-forward items
- Published summaries

This history is retained for:

- Auditability
- Week-to-week continuity
- Internal traceability

Historical summaries do not need to be broadly exposed in the stakeholder-facing UI.

---

## 18. Notifications

Notifications are **in-app only** for the initial product.

The system should use them primarily for:

- Weekly submission reminders
- Missing submission reminders
- Project lead review notifications
- Publication-related workflow notifications

Email notifications are outside the current scope.

---

## 19. Current MVP Principles

The product should remain:

- **Lightweight** — weekly reporting should not feel like project administration.
- **Outcome-focused** — emphasize what changed and what was achieved.
- **Human-approved** — AI drafts, humans publish.
- **Transparent** — project members can see one another's submissions.
- **Continuous** — unresolved work carries forward between weeks.
- **Auditable** — late edits and historical records are retained.
- **Focused** — avoid becoming a task-management or project-management suite.

---

## 20. Current End-to-End Flow

```text
Project created
    ↓
Weekly reporting cycle opens
    ↓
Previous next steps, blockers, and risks are carried forward
    ↓
Team members submit:
    - Achievements
    - Outcomes
    - Blockers
    - Risks
    - Next steps
    ↓
Project team can view individual submissions
    ↓
Project lead reviews and can request revisions
    ↓
Weekly deadline reached
    ↓
System automatically generates AI draft
    ↓
Project lead reviews and edits draft
    ↓
Project lead manually publishes
    ↓
Latest executive summary becomes visible organization-wide
    ↓
Historical data retained internally
    ↓
Next weekly cycle begins
```

---

## 21. Open Design Question

The next unresolved question in the scoping discussion is:

**Can a user belong to multiple projects at the same time?**

Options:

- **A. Yes**
- **B. No — one active project per user**

