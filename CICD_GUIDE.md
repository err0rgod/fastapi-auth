# CI/CD Setup Guide for Tokenly

This guide explains how to set up professional automation for your library using GitHub Actions.

## 1. Automated Testing (`tests.yml`)

This pipeline runs every time you push code or open a Pull Request. It ensures that new changes don't break existing features.

**Setup:**
1. Create a folder: `.github/workflows/`
2. Create a file: `.github/workflows/tests.yml`
3. Paste the following configuration:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install . pytest
      
      - name: Run tests
        run: |
          pytest tests/
```

## 2. Automated Publishing (`publish.yml`)

This pipeline automatically uploads your library to PyPI when you create a "Release" on GitHub.

**Setup:**
1. Generate an **API Token** from [pypi.org](https://pypi.org/manage/account/).
2. In your GitHub Repo: Go to **Settings > Secrets and variables > Actions**.
3. Create a **New repository secret**:
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your token (starts with `pypi-`).
4. Create a file: `.github/workflows/publish.yml`
5. Paste the following:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          python -m build
          python -m twine upload dist/*
```

## 3. Local Quality Check

Before pushing, it is good practice to run linting locally.
1. Install Ruff: `pip install ruff`
2. Run Lint Check: `ruff check .`
3. Auto-fix errors: `ruff check . --fix`
4. Format code: `ruff format .`
```
