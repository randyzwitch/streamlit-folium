import streamlit as st
import folium
import numpy as np
import pandas as pd
from streamlit_folium import folium_static

def create_test_df():
    data = {"id": range(10000),
            "year": np.random.choice(range(2018, 2021), 10000),
            "type": np.random.choice(["type_a", "type_b", "type_c"], 10000),
            "latitude": np.random.uniform(low=10, high=20, size=10000),
            "longitude": np.random.uniform(low=10, high=20, size=10000)}

    # Respects order
    return pd.DataFrame(data, columns=["id", "year", "type", "latitude", "longitude"])


def _plot_dot(point, map_element, color_col, radius=4, weight=1, color='black'):
    color_dict = {2018: "blue", 2019: "orange", 2020: "red"}

    folium.CircleMarker(location=[point["latitude"], point["longitude"]], radius=radius, weight=weight,
                        color=color, fill=True,
                        fill_color=color_dict[point[color_col]],
                        fill_opacity=0.9,
                        tooltip=f'<b>id: </b>{str(point["id"])}'
                                f'<br></br>'f'<b>year: </b>{str(point["year"])}'
                                f'<br></br>'f'<b>type: </b>{str(point["type"])}',
                        popup=f'<b>id: </b>{str(point["id"])}'
                              f'<br></br>'f'<b>year: </b>{str(point["year"])}'
                              f'<br></br>'f'<b>type: </b>{str(point["type"])}'
                        ).add_to(map_element)


def generate_map(df):
    map_element = folium.Map(location=[15, 15], zoom_start=6, tiles='cartodbpositron')

    df.apply(_plot_dot, axis=1, args=[map_element, "year"])

    return map_element

if __name__ == "__main__":
    st.title("Complex Example")

    df = create_test_df()

    option = st.selectbox('Select year?', df['year'].unique())
    st.write('You selected: ', option)

    dict_years = {}
    for year in df['year'].unique():
        dict_years[year] = generate_map(df[df["year"] == year])

    folium_static(dict_years[option])

