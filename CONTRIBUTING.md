# Contributing to streamlit-folium

All of the necessary commands to get the project running are in the
[Taskfile](https://taskfile.dev/). You can install task with Homebrew:
`brew install go-task`. See [Installation](https://taskfile.dev/installation/)
for more details.

### Linting and formatting

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, and
[mypy](https://github.com/python/mypy) for type checking.

To run ruff and mypy, you can use the following command:

```bash
task lint
```

### Running tests

To run the tests, you can use the following command:

```bash
task test
```

### Adding tests

If you add a new feature, or fix a bug, please add a test to ensure that the feature works as expected.

The pattern for creating tests is to use the example streamlit app, and use
[playwright](https://playwright.dev/python/docs/intro) to create and
run tests on the app.

These tests are primarily located in the `tests/frontend.py` file.

If you are making a change that only affects the python code, you can
run the playwright [codegen](https://playwright.dev/python/docs/codegen) tool to
help generate the tests by running `task generate-tests`.

If you are making a change that affects the javascript code, you need to set up
folium to use your local frontend code. This can be done by:

1. Edit `streamlit_folium/__init__.py` to set `_RELEASE = False`
2. Run `task generate-tests-frontend`
3. Add tests as appropriate in `tests/frontend.py`
4. Run `task test-frontend` to run the tests
    * Note that `test_release` will fail while `_RELEASE = False` -- this is expected
5. Set `_RELEASE = True` in `streamlit_folium/__init__.py` before opening a PR
