# streamlit-folium Development Guide

## Build & Test Commands
- Install with uv (all dependencies): `uv sync --editable . && uv sync --groups dev,test,examples --editable .`
- Install core + test: `uv sync --editable . --groups test`
- Install core only: `uv sync --editable .`
- Add a new dependency: `uv add package_name` or `uv add package_name --group test`
- Install pre-commit: `uv add pre-commit --dev && pre-commit install`
- Run linting: `ruff check --fix` or `pre-commit run --all-files`
- Run formatter: `ruff format`
- Run typechecking: `mypy`
- Run all tests: `pytest`
- Run single test: `pytest tests/test_frontend.py::test_name`
- Run streamlit example: `streamlit run examples/streamlit_app.py`
- Task runner available: `task test`, `task lint`, etc.

## Project Structure
- Package uses pyproject.toml for configuration (PEP 621 compliant)
- Build system: hatchling (defined in pyproject.toml)
- Dependencies managed with uv.lock for reproducible environments
- Optional dependencies defined in pyproject.toml:
  - [dev]: development tools (ruff, mypy, pre-commit)
  - [test]: testing dependencies (pytest, playwright)
  - [examples]: dependencies for example apps

## Code Style Guidelines
- Python 3.9+ compatible
- Line length: 88 characters
- Use type hints and follow MyPy rules
- Follow PEP 8 naming conventions (snake_case for variables/functions)
- Imports: Use absolute imports, standard library first, followed by third-party libraries
- Use contextlib.suppress for exception handling where appropriate
- Use thorough docstrings for all public functions (Google docstring format)
- Frontend development: run `npm install` and `npm run start` in streamlit_folium/frontend/
- Maintain test coverage for all changes