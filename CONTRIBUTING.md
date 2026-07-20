# Contributing to Disaster Missing Persons

Thanks for your interest in improving this project. It exists to help disaster response teams reconnect missing people with their families, so clarity, reliability, and low-bandwidth performance matter more than cleverness.

## Getting Started

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/disaster-missing-persons.git
   cd disaster-missing-persons
   ```
2. Create a virtual environment and install with dev dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\Activate.ps1 on Windows
   pip install -e ".[dev]"
   ```
3. Copy the environment template and point it at a local MongoDB instance:
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   python -m disaster_missing_persons
   ```

## Making Changes

- Create a branch off `main` named `fix/...`, `feat/...`, or `docs/...` depending on the change.
- Keep pull requests focused on a single change; smaller PRs are reviewed faster.
- Add or update tests in `tests/` for any behavior change.
- Update `README.md` or `docs/USERMANUAL.md` if your change affects setup, configuration, or user-facing behavior.

## Code Style

This project uses `black` for formatting, `ruff` for linting, and `mypy` for type checking. Please run all three before opening a PR:

```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

`black` and `ruff` must pass cleanly and are enforced in CI. `mypy` currently has pre-existing errors in the codebase and is run as informational-only in CI (it won't block your PR) — please don't introduce *new* mypy errors, but you don't need to fix unrelated existing ones unless your PR is specifically about type-safety cleanup.

## Running Tests

```bash
pytest
```

Please add tests for new endpoints, permission rules, or bug fixes so regressions are caught automatically.

## Commit Messages

Use short, descriptive commit messages in the imperative mood, e.g. `Fix path traversal in photo upload` rather than `Fixed bug`.

## Reporting Bugs / Requesting Features

Please use the issue templates under `.github/ISSUE_TEMPLATE/` so reports include the information needed to reproduce or evaluate them.

## Security Issues

Because this project may be deployed in real disaster-response scenarios, please report security vulnerabilities privately (e.g. via a private security advisory or direct message to a maintainer) rather than opening a public issue, until a fix is available.

## Code of Conduct

Be respectful and constructive. This project supports people working in high-stress, high-stakes situations — keep discussion professional and focused on the work.
