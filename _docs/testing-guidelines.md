# Testing Guidelines

## Basics

- Tests use pytest and pytest-django. Write plain test functions, not `unittest.TestCase` classes.
- Tests live in `tests/`, one file per feature: `tests/test_<feature>.py` (e.g. `test_health.py`, `test_home.py`).
- Shared fixtures go in `tests/conftest.py`.
- Run the whole suite with `uv run pytest`, or one file with `uv run pytest tests/test_<feature>.py`.
- The suite must pass before a commit.

## What to test

- **Acceptance criteria first.** Each criterion on the issue should be covered by at least one test. Read them before writing tests.
- **Behaviour, not implementation.** Test what a user or caller sees: responses, saved rows, notifications created. Don't test Django or library internals.
- **Both sides of every permission.** For each protected page or action, test that an allowed user succeeds *and* that a disallowed user is refused (non-member, member who isn't the lead, user who has left the project, anonymous user).
- **Database constraints.** For uniqueness and other constraints, assert that the invalid write raises `IntegrityError`, wrapped in `transaction.atomic()` so the test can continue.
- **Things that must never change.** For submission revisions and published summaries, test that updates and deletes fail both through the ORM and through raw SQL.
- **Edge cases the plan names.** First week with no history, no submissions at the deadline, late revisions, items carried forward and resolved.

## How to write them

- Name tests after the behaviour: `test_non_member_cannot_view_submissions`, not `test_view_2`.
- Arrange, act, assert, separated by blank lines:

  ```python
  def test_health_returns_ok(client):
      response = client.get(reverse("health"))

      assert response.status_code == 200
  ```

- Use `reverse("<url-name>")` rather than hard-coded paths.
- Mark tests that touch the database with `@pytest.mark.django_db` (or use the `db` fixture).
- Build test data with small fixtures or helper functions in `conftest.py` (e.g. `make_user`, `make_project(lead=..., members=[...])`), keeping each test's setup short and visible. Adding a factory library needs approval like any other dependency.
- One behaviour per test. If a test needs several unrelated asserts, split it.

## Time and deadlines

- Never depend on the real clock. Functions that care about "now" (current cycle, lateness, reminders) take a `now` argument so tests can pass a fixed time.
- Change settings such as `REPORTING_DEADLINE` with pytest-django's `settings` fixture, not by editing settings files.
- Test around boundaries: just before and just after the deadline, week start, and timezone changes.

## External services

- Tests never call the Claude API or any other network service. Replace the Anthropic client at the service boundary (`summaries/services/summarizer.py`) with a fake that returns a fixed response.
- Include tests for bad model output: missing sections, unknown source IDs, API errors.
- Background tasks run in-process in tests; assert which tasks were deferred and run the task function directly to test its effect.

## HTMX views

- Send the `HX-Request: true` header when testing HTMX endpoints, and assert on the returned fragment (status code and the key content), not on the full page.
- Also test the same view without the header if it is expected to render a full page.

## Keep the suite fast and reliable

- No `sleep`, no real network, no dependence on test order.
- Each test creates the data it needs; don't rely on data left by another test.
- A flaky test is a bug: fix it or remove it, don't retry it.
