import setuptools

setuptools.setup(
    name="streamlit_folium",
    version="0.6.0alpha3",
    author="Randy Zwitch",
    author_email="randy@streamlit.io",
    description="Render Folium objects in Streamlit",
    long_description="",
    long_description_content_type="text/plain",
    url="https://github.com/randyzwitch/streamlit-folium",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "folium>=0.11"],
)
