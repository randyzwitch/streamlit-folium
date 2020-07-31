import streamlit as st
from seleniumbase import BaseCase
import cv2


class ComponentsTest(BaseCase):
    def test_basic(self):

        # open the app
        self.open("http://localhost:8501")

        # automated visual regression testing
        # https://github.com/seleniumbase/SeleniumBase/tree/master/examples/visual_testing
        # level 2 chosen, as id values dynamically generated on each page run
        self.check_window(name="first_test", level=2)

        # check folium app-specific parts
        # automated test level=2 only checks structure, not content
        self.assert_text("streamlit-folium")

        # test screenshots look exactly the same
        self.save_screenshot("current-screenshot.png")
        original = cv2.imread(
            "visual_baseline/test_package.test_basic/first_test/screenshot.png"
        )
        duplicate = cv2.imread("current-screenshot.png")

        assert original.shape == duplicate.shape

        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        assert cv2.countNonZero(b) == cv2.countNonZero(g) == cv2.countNonZero(r) == 0
