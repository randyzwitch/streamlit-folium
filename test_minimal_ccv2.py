import streamlit as st
import streamlit.components.v2 as components_v2

st.set_page_config(page_title="CCv2 test")

JS = """
export default function(component) {
    const { parentElement, data, setStateValue } = component;
    const div = document.createElement('div');
    div.style.padding = '20px';
    div.style.background = '#eef';
    div.style.border = '2px solid blue';
    div.innerHTML = '<h2>CCv2 works! Data: ' + JSON.stringify(data) + '</h2>';
    parentElement.appendChild(div);
    setStateValue('loaded', true);
}
"""

my_comp = components_v2.component("test_ccv2", js=JS, html=" ")

result = my_comp(
    data={"message": "hello from python"},
    default={"loaded": False},
    height=100,
    on_loaded_change=lambda: None,
)

st.write(f"Result: {result}")
st.write(f"Loaded: {result.loaded if result else 'N/A'}")
