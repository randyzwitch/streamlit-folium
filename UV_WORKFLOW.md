# UV Workflow Quick Reference

## Initial Setup
```bash
# Install package in development mode with all dependencies
uv sync --editable .
uv sync --groups dev,test,examples --editable .

# Install pre-commit hooks
uv add pre-commit --dev
pre-commit install
```

## Managing Dependencies
```bash
# Add a new dependency to the main package
uv add package_name

# Add a new development dependency
uv add package_name --dev

# Add a new test dependency
uv add package_name --group test

# Add a new example dependency
uv add package_name --group examples

# Install dependencies from pyproject.toml
uv sync

# Update all dependencies
uv sync --upgrade

# Using native interface for uv
uv add streamlit-folium              # For users installing the package
uv add streamlit-folium[examples]    # For users installing with optional dependencies
```

## Development Workflow
```bash
# Run linting
pre-commit run --all-files

# Run tests
pytest

# Run a specific test
pytest tests/test_frontend.py::test_name

# Run examples
streamlit run examples/streamlit_app.py
```