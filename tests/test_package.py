import streamlit as st
from seleniumbase import BaseCase


class ComponentsTest(BaseCase):
    def test_basic(self):

        # open the app
        self.open("http://localhost:8501")

        # automated visual regression testing
        # https://github.com/seleniumbase/SeleniumBase/tree/master/examples/visual_testing
        # level 2 chosen, as id values dynamically generated on each page run
        self.check_window(name="first_test)", level=2)

        # check folium app-specific parts
        # automated test level=2 only checks structure, not content
        self.assert_text("streamlit-folium")
