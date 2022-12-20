old = """
class ComponentsTest(BaseCase):
    def test_basic(self):

        # open the app and take a screenshot
        self.open("http://localhost:8501")
        time.sleep(10)
        self.save_screenshot("current-screenshot.png")

        # automated visual regression testing
        # tests page has identical structure to baseline
        # https://github.com/seleniumbase/SeleniumBase/tree/master/examples/visual_testing
        # level 2 chosen, as id values dynamically generated on each page run
        self.check_window(name="first_test", level=2)

        # check folium app-specific parts
        # automated test level=2 only checks structure, not content
        self.assert_text("streamlit-folium")

        # test screenshots look exactly the same
        original = cv2.imread("visual_baseline/test_basic/first_test/baseline.png")
        duplicate = cv2.imread("current-screenshot.png")

        assert original.shape == duplicate.shape

        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        assert cv2.countNonZero(b) == cv2.countNonZero(g) == cv2.countNonZero(r) == 0
"""


def test_layer_control():
    import folium

    from streamlit_folium import generate_leaflet_string

    map = folium.Map()
    folium.LayerControl().add_to(map)
    map.render()
    leaflet = generate_leaflet_string(map)
    assert "var tile_layer_0_0 = L.tileLayer(" in leaflet
    assert '"openstreetmap" : tile_layer_0_0,' in leaflet
