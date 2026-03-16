import streamlit as st

from planner import (
    action_bar,
    apply_wireframe_theme,
    detail_panel,
    form_panel,
    metric_row,
    page_header,
    section_header,
)
from planner.mock_data import FORM_SAMPLE_FIELDS


st.set_page_config(page_title="Input form sample", layout="wide")

apply_wireframe_theme()
page_header(
    "Input form sample",
    "Use this pattern for request intake, supplier registration, or any screen where guided input is the main job.",
    badge="Starter Pattern",
)

metric_row(
    [
        {"label": "Fields", "value": len(FORM_SAMPLE_FIELDS), "note": "Grouped by section"},
        {"label": "Sections", "value": 3, "note": "Basics, layout, ops"},
        {"label": "Persistence", "value": "Session State", "note": "Mock only"},
    ]
)

left, right = st.columns([1.2, 1])

with left:
    submitted, values = form_panel(
        "Screen setup form",
        FORM_SAMPLE_FIELDS,
        form_key="planner_form_sample",
        submit_label="Review values",
        description="Keep the form good enough for structure review, not for production data entry.",
    )

    if submitted:
        st.session_state["planner_form_sample_result"] = values
        st.success("Values captured. This sample updates only the summary panel.")

with right:
    stored_values = st.session_state.get("planner_form_sample_result")
    if stored_values:
        detail_panel(
            "Submitted summary",
            stored_values,
            description="Showing the entered values on the right makes the flow reviewable.",
            badge="Mock Result",
        )
    else:
        section_header("Submitted summary", "Nothing submitted yet.")
        st.info("Submit the form on the left to populate this panel.")

section_header("Form design rules", "Section clarity matters more than total field count.")
st.markdown(
    """
    - Name sections in task language, not system language.
    - Use placeholders and defaults to explain intent.
    - After submit, show what changed instead of pretending the data was saved.
    - Keep uploads and attachments as simple toggles until integration is real.
    """
)

clicked = action_bar(
    [
        {"id": "trim", "label": "Trim fields"},
        {"id": "note", "label": "Review note"},
        {"id": "handoff", "label": "Dev handoff"},
    ],
    key="planner_form_actions",
    title="Follow-up actions",
    description="An action bar below the form helps review the full screen flow, not just input widgets.",
)

if clicked == "trim":
    st.info("Recommended move: keep only the must-have fields for the first draft.")
elif clicked == "note":
    st.info("Example: a note area is usually enough before you build a full comment flow.")
elif clicked == "handoff":
    st.info("Dev handoff text should focus on state changes and user flow.")