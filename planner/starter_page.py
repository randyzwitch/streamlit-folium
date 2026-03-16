"""Copy this file into pages/95_*.py and edit the constants first."""

import streamlit as st

from planner import (
    action_bar,
    apply_wireframe_theme,
    detail_panel,
    form_panel,
    metric_row,
    page_header,
    table_panel,
)


PAGE_TITLE = "New screen draft"
PAGE_DESC = "Copy this template, then change the title, text, and mock data before touching anything else."
PAGE_BADGE = "Starter Template"

SUMMARY_METRICS = [
    {"label": "Status", "value": "Draft", "note": "Lock message and layout first."},
    {"label": "Core blocks", "value": "3", "note": "Header, main table, action bar"},
    {"label": "Integrations", "value": "None", "note": "Explain the flow with mock data only."},
]

TABLE_ROWS = [
    {
        "screen_id": "DRAFT-01",
        "screen_name": "Request intake screen",
        "owner": "Planning",
        "status": "Drafting",
        "updated_at": "2026-03-16",
    },
    {
        "screen_id": "DRAFT-02",
        "screen_name": "Review summary screen",
        "owner": "Operations",
        "status": "Structure review",
        "updated_at": "2026-03-17",
    },
]

DETAIL_BY_SCREEN = {
    "DRAFT-01": {
        "Purpose": "Collect only the fields the reviewer truly needs.",
        "Users": "Requester / Reviewer",
        "Key question": "What must be captured before review starts?",
        "Next move": "Reduce the required fields to five or fewer.",
    },
    "DRAFT-02": {
        "Purpose": "Show review output and the next step in one view.",
        "Users": "Reviewer / Approver",
        "Key question": "How much detail should live in the summary?",
        "Next move": "Compare top summary cards vs lower note panel.",
    },
}

NOTE_FIELDS = [
    {
        "group": "Review notes",
        "key": "review_focus",
        "label": "What should this screen optimize first?",
        "type": "textarea",
        "value": "Reduce field count and make the information structure obvious.",
    },
    {
        "group": "Review notes",
        "key": "layout_choice",
        "label": "Primary layout to validate",
        "type": "select",
        "options": ["Single form", "List + detail", "Top summary + bottom table"],
        "value": "Single form",
    },
]


st.set_page_config(page_title=PAGE_TITLE, layout="wide")


def render_page() -> None:
    apply_wireframe_theme()
    page_header(PAGE_TITLE, PAGE_DESC, badge=PAGE_BADGE)
    metric_row(SUMMARY_METRICS)

    left, right = st.columns([1.4, 1])
    with left:
        selected_row = table_panel(
            "Main table",
            TABLE_ROWS,
            description="A table and one selector are enough for an early screen story.",
            key="starter_template_table",
            selection_field="screen_id",
            selection_label="Detail target",
            selection_format=lambda row: f"{row['screen_id']} | {row['screen_name']}",
        )

    with right:
        if selected_row:
            detail_panel(
                "Detail panel",
                DETAIL_BY_SCREEN[selected_row["screen_id"]],
                description="Keep only the decision points in the detail area.",
                badge=selected_row["status"],
            )

    submitted, values = form_panel(
        "Review notes",
        NOTE_FIELDS,
        form_key="starter_template_form",
        submit_label="Apply note",
        description="Use a form for flow explanation, not for real persistence.",
    )

    if submitted:
        st.session_state["starter_template_notes"] = values
        st.success("Mock notes updated. This template is intentionally non-persistent.")

    stored_notes = st.session_state.get("starter_template_notes")
    if stored_notes:
        detail_panel("Latest values", stored_notes, badge="Mock Result")

    clicked = action_bar(
        [
            {"id": "share", "label": "Review copy"},
            {"id": "trim", "label": "Reduce fields"},
            {"id": "handoff", "label": "Dev handoff note"},
        ],
        key="starter_template_actions",
        title="Action bar",
        description="Buttons should explain the next action before they trigger real logic.",
    )

    if clicked == "share":
        st.info("Suggested review copy: purpose, user, key question.")
    elif clicked == "trim":
        st.info("Recommended move: remove optional fields before styling anything else.")
    elif clicked == "handoff":
        st.info("Dev handoff should describe screen flow and state changes, not backend detail.")


render_page()