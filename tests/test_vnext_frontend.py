from contextlib import contextmanager
from time import sleep

from playwright.sync_api import Page, expect

PORT = "8701"


@contextmanager
def run_streamlit():
    import subprocess

    p = subprocess.Popen(
        [
            "streamlit",
            "run",
            "examples/vnext_app.py",
            "--server.port",
            PORT,
            "--server.headless",
            "true",
        ]
    )
    sleep(5)
    try:
        yield
    finally:
        p.kill()


def test_vnext_example_renders_and_clicks(page: Page):
    with run_streamlit():
        page.goto(f"http://localhost:{PORT}")
        expect(page.get_by_text("streamlit-folium vnext")).to_be_visible()
        page.get_by_text("streamlit_folium_vnext scaffold").click(force=True)
        expect(page.get_by_text("State")).to_be_visible()
