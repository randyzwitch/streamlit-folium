from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, expect

LOCAL_TEST = False

PORT = "8599" if LOCAL_TEST else "8503"


@pytest.fixture(scope="module", autouse=True)
def before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")


@contextmanager
def run_streamlit():
    """Run the streamlit app at examples/streamlit_app.py on port 8599"""
    import subprocess

    if LOCAL_TEST:
        try:
            yield 1
        finally:
            pass
    else:
        p = subprocess.Popen(
            [
                "streamlit",
                "run",
                "examples/streamlit_app.py",
                "--server.port",
                "8599",
                "--server.headless",
                "true",
            ]
        )

        sleep(5)

        try:
            yield 1
        finally:
            p.kill()


def test_marker_click(page: Page):
    # Check page title
    expect(page).to_have_title("streamlit-folium documentation")

    expect(page.get_by_text('"last_object_clicked":NULL')).to_be_visible()

    # Click marker
    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("img").click()

    expect(page.get_by_text('"last_object_clicked":NULL')).to_be_hidden()


def test_draw(page: Page):
    # Test draw support
    page.get_by_role("link", name="draw support").click()
    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("link", name="Draw a polygon").click()


def test_limit_data(page: Page):
    # Test limit data support
    page.get_by_role("link", name="limit data return").click()

    expect(page.get_by_text('{"last_object_clicked":NULL}')).to_be_visible()

    # Click marker
    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("img").nth(2).click()

    # Have to click a second time for some reason, maybe because it doesn't load right
    # away
    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("img").nth(2).click()

    expect(page.get_by_text('{"last_object_clicked":{"lat":39.96')).to_be_visible()


def test_dual_map(page: Page):
    page.get_by_role("link", name="misc examples").click()
    page.locator("label").filter(has_text="Dual map").click()

    # Click marker on left map
    page.frame_locator('internal:attr=[title="streamlit_folium.st_folium"i]').locator(
        "#map_div"
    ).get_by_role("img").click()

    # Click marker on right map
    page.frame_locator('internal:attr=[title="streamlit_folium.st_folium"i]').locator(
        "#map_div2"
    ).get_by_role("img").click()