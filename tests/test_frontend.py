from __future__ import annotations

from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, Response, expect

LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@pytest.fixture(scope="module", autouse=True)
def _before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(autouse=True)
def _before_test(page: Page):
    page.goto(f"localhost:{PORT}")
    page.set_viewport_size({"width": 2000, "height": 2000})
    expect.set_options(timeout=5_000)


# Take screenshot of each page if there are failures for this session
@pytest.fixture(autouse=True)
def _after_test(page: Page, request):
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


def click_button_or_marker(page: Page, nth: int = 0, locator: str | None = None):
    """For some reason, there's a discrepancy between how the map markers are
    selectable locally and on github actions, perhaps related some error in loading
    the actual marker images. This tries both ways to select a marker"""

    frame = page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]')
    if locator is not None:
        frame = frame.locator(locator)
    try:
        frame.get_by_role("button", name="Marker").nth(nth).click(timeout=5_000)
    except Exception:
        frame.get_by_role("img").nth(nth).click(timeout=5_000)


def test_marker_click(page: Page):
    def check_for_404(response: Response):
        if not response.ok:
            print(response)
            print(response.text())
            print(response.url)
            print(response.status)
            raise Exception("404")

    page.on("response", check_for_404)

    # Check page title
    expect(page).to_have_title("streamlit-folium documentation")

    expect(page.get_by_text('"last_object_clicked":NULL')).to_be_visible()

    # Click marker
    try:
        click_button_or_marker(page)
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

    # Should be no drawings
    expect(page.get_by_text('"all_drawings":NULL')).to_be_visible()

    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').get_by_role(
        "link", name="Draw a marker"
    ).click()
    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
        ".leaflet-marker-icon"
    ).first.click()
    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
        "#map_div"
    ).click()

    # Should be one item in drawings after having placed a marker
    expect(page.get_by_text('"all_drawings":NULL')).to_be_hidden()


def test_limit_data(page: Page):
    # Test limit data support
    page.get_by_role("link", name="limit data return").click()
    # Click again to see if it resolves timeout issues
    page.get_by_role("link", name="limit data return").click()

    expect(page).to_have_title("streamlit-folium documentation: Limit Data Return")

    expect(page.get_by_text('{"last_object_clicked":NULL}')).to_be_visible()

    # Click marker
    click_button_or_marker(page, 2)

    # Have to click a second time for some reason, maybe because it doesn't load right
    # away
    click_button_or_marker(page, 2)

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
        click_button_or_marker(page, 0, "#map_div")
        click_button_or_marker(page, 0, "#map_div2")
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
    click_button_or_marker(page)

    expect(
        page.get_by_text('"last_object_clicked_tooltip":"Liberty Bell"')
    ).to_be_visible()


def test_popup_text(page: Page):
    page.get_by_role("link", name="simple popup").click()
    page.get_by_role("link", name="simple popup").click()

    expect(page.get_by_text("Popup: None")).to_be_visible()
    expect(page.get_by_text("Tooltip: None")).to_be_visible()

    click_button_or_marker(page)

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

    click_button_or_marker(page, 1)

    try:
        expect(page.get_by_text("Popup: Popup 2!")).to_be_visible()
        expect(page.get_by_text("Tooltip: Tooltip 2!")).to_be_visible()
    except Exception as e:
        page.screenshot(path="screenshot-popup2.png")
        raise e


def test_responsiveness(page: Page):
    page.get_by_role("link", name="responsive").click()
    page.get_by_role("link", name="responsive").click()

    page.set_viewport_size({"width": 1000, "height": 3000})

    try:
        initial_bbox = (
            page.frame_locator("iframe").nth(2).locator("#map_div").bounding_box()
        )
    except Exception as e:
        page.screenshot(path="screenshot-responsive.png", full_page=True)
        raise e

    page.set_viewport_size({"width": 1500, "height": 3000})

    sleep(1)

    new_bbox = page.query_selector_all("iframe")[2].bounding_box()

    print(initial_bbox)
    print(new_bbox)

    assert initial_bbox is not None

    assert new_bbox is not None

    assert new_bbox["width"] > initial_bbox["width"] + 100

    # Check that the iframe is reasonably tall, which makes sure it hasn't failed to
    # render at all
    assert new_bbox["height"] > 100

    page.set_viewport_size({"width": 2000, "height": 2000})


def test_geojson_styles(page: Page):
    page.get_by_role("link", name="geojson styles").click()
    page.get_by_role("link", name="geojson styles").click()

    page.get_by_text("Show generated code").click()
    expect(page.get_by_text('"fillOpacity"')).to_be_visible()


def test_grouped_layer_control(page: Page):
    page.get_by_role("link", name="grouped layer control").click()
    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').locator(
        "label"
    ).filter(has_text="g2").click()
    page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]').get_by_label(
        "g2"
    ).check()


def test_geojson_popup(page: Page):
    page.get_by_role("link", name="geojson popup").click()

    expect(page.get_by_text("AttributeError")).to_be_hidden()


def test_dynamic_feature_group_update(page: Page):
    page.get_by_role("link", name="dynamic updates").click()

    # Test showing only Parcel layer
    page.get_by_test_id("stRadio").get_by_text("Parcels").click()
    sleep(1)
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .first
    ).to_be_visible()
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .nth(1)
    ).to_be_hidden()

    # Test showing only Building layer
    page.get_by_test_id("stRadio").get_by_text("Buildings").click()
    sleep(1)
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .nth(1)
    ).to_be_hidden()
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .first
    ).to_be_visible()

    # Test showing no layers
    page.get_by_test_id("stRadio").get_by_text("None").click()
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .first
    ).to_be_hidden()

    # Test showing both layers
    page.get_by_test_id("stRadio").get_by_text("Both").click()
    sleep(1)
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .first
    ).to_be_visible()
    expect(
        page.locator('[data-testid="stCustomComponentV1"]')
        .nth(1)
        .content_frame.get_by_role("img")
        .locator("path")
        .nth(1)
    ).to_be_visible()


def test_frame_height_matches_content_height(page: Page):
    """Make sure that the frame height matches the document height to confirm that
    Streamlit.setFrameHeight was called correctly."""

    iframe = page.get_by_test_id("stCustomComponentV1")
    iframe_html = page.frame_locator("[data-testid=stCustomComponentV1]").locator(
        "html"
    )

    # Wait for the iframe to load and have a height - otherwise the test will be flaky
    page.wait_for_function(
        "el => window.getComputedStyle(el).height !== '0px'",
        arg=iframe.element_handle(),
    )
    sleep(1.5)

    # Now make sure that the heights match
    iframe_height = iframe.evaluate("el => window.getComputedStyle(el).height")
    iframe_html_height = iframe_html.evaluate(
        "el => window.getComputedStyle(el).height"
    )

    # Allow for small iframe height differences (within 20px)
    iframe_height_px = int(iframe_height.replace("px", ""))
    iframe_html_height_px = int(iframe_html_height.replace("px", ""))
    assert abs(iframe_height_px - iframe_html_height_px) <= 20
