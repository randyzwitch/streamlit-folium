from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, expect

LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@pytest.fixture(scope="module", autouse=True)
def before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")
    page.set_viewport_size({"width": 2000, "height": 2000})


# Take screenshot of each page if there are failures for this session
@pytest.fixture(scope="function", autouse=True)
def after_test(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshot-{request.node.name}.png", full_page=True)


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
                PORT,
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
    try:
        page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').get_by_role(
            "img"
        ).click()
    except Exception as e:
        page.screenshot(path="screenshot-test-marker-click.png", full_page=True)
        raise e

    expect(page.get_by_text('"last_object_clicked":NULL')).to_be_hidden()


def test_draw(page: Page):
    # Test draw support
    page.get_by_role("link", name="draw support").click()
    # Click again to see if it resolves timeout issues
    page.get_by_role("link", name="draw support").click()

    expect(page).to_have_title("streamlit-folium documentation: Draw Support")

    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("link", name="Draw a polygon").click()


def test_limit_data(page: Page):
    # Test limit data support
    page.get_by_role("link", name="limit data return").click()
    # Click again to see if it resolves timeout issues
    page.get_by_role("link", name="limit data return").click()

    expect(page).to_have_title("streamlit-folium documentation: Limit Data Return")

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
    # Click again to see if it resolves timeout issues
    page.get_by_role("link", name="misc examples").click()

    expect(page).to_have_title("streamlit-folium documentation: Misc Examples")

    page.locator("label").filter(has_text="Dual map").click()
    page.locator("label").filter(has_text="Dual map").click()

    # Click marker on left map
    try:
        page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
            "#map_div"
        ).get_by_role("img").click()
        page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
            "#map_div2"
        ).get_by_role("img").click()
    except Exception as e:
        page.screenshot(path="screenshot-dual-map.png", full_page=True)
        raise e


def test_vector_grid(page: Page):
    page.get_by_role("link", name="vector grid").click()
    page.get_by_role("link", name="vector grid").click()

    expect(page).to_have_title("streamlit-folium documentation: Vector Grid")

    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
        ".leaflet-marker-icon"
    ).click()


def test_tooltip_click(page: Page):
    expect(page.get_by_text('"last_object_clicked_tooltip":NULL')).to_be_visible()

    # Click marker on map
    page.frame_locator(
        'internal:attr=[title="streamlit_folium.st_folium"i]'
    ).get_by_role("img").nth(0).click()

    expect(
        page.get_by_text('"last_object_clicked_tooltip":"Liberty Bell"')
    ).to_be_visible()


def test_popup_text(page: Page):
    page.get_by_role("link", name="simple popup").click()
    page.get_by_role("link", name="simple popup").click()

    expect(page.get_by_text("Popup: None")).to_be_visible()
    expect(page.get_by_text("Tooltip: None")).to_be_visible()

    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').get_by_role(
        "img"
    ).nth(0).click()

    try:
        expect(page.get_by_text("Popup: Popup!")).to_be_visible()
        expect(page.get_by_text("Tooltip: Tooltip!")).to_be_visible()
    except Exception as e:
        page.screenshot(path="screenshot-popup.png")
        raise e


def test_return_on_hover(page: Page):
    page.get_by_role("link", name="simple popup").click()
    page.get_by_role("link", name="simple popup").click()

    expect(page.get_by_text("Popup: None")).to_be_visible()
    expect(page.get_by_text("Tooltip: None")).to_be_visible()

    page.get_by_text("Return on hover?").click()

    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').get_by_role(
        "img"
    ).nth(1).hover()

    try:
        expect(page.get_by_text("Popup: Popup 2!")).to_be_visible()
        expect(page.get_by_text("Tooltip: Tooltip 2!")).to_be_visible()
    except Exception as e:
        page.screenshot(path="screenshot-popup2.png")
        raise e


def test_responsiveness(page: Page):
    page.get_by_role("link", name="responsive").click()

    page.set_viewport_size({"width": 500, "height": 3000})

    initial_bbox = (
        page.frame_locator("div:nth-child(2) > iframe")
        .locator("#map_div")
        .bounding_box()
    )

    page.set_viewport_size({"width": 1000, "height": 3000})

    sleep(1)

    new_bbox = (
        page.frame_locator("div:nth-child(2) > iframe")
        .locator("#map_div")
        .bounding_box()
    )

    print(initial_bbox)
    print(new_bbox)

    assert initial_bbox is not None

    assert new_bbox is not None

    assert new_bbox["width"] > initial_bbox["width"] + 300

    page.set_viewport_size({"width": 2000, "height": 2000})


def test_geojson_styles(page: Page):
    page.get_by_role("link", name="geojson styles").click()
    page.get_by_role("link", name="geojson styles").click()

    page.get_by_text("Show generated code").click()
    expect(page.get_by_text('"fillOpacity"')).to_be_visible()
