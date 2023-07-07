def test_release():
    from streamlit_folium import _RELEASE

    assert _RELEASE, "Release needs to be set to True after finished testing locally"
