import streamlit as st

from planner import (
    action_bar,
    apply_wireframe_theme,
    detail_panel,
    metric_row,
    page_header,
    section_header,
    table_panel,
)
from planner.mock_data import LIST_DETAIL_DETAILS, LIST_DETAIL_ROWS, LIST_DETAIL_TIMELINES


st.set_page_config(page_title="List plus detail sample", layout="wide")

apply_wireframe_theme()
page_header(
    "List plus detail sample",
    "Use this as the default pattern for queues, approval lists, or any screen where a user selects one row and inspects a detail panel.",
    badge="Starter Pattern",
)

status_options = ["All"] + sorted({row["status"] for row in LIST_DETAIL_ROWS})
priority_options = ["All"] + sorted({row["priority"] for row in LIST_DETAIL_ROWS})

filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1.4])
with filter_col1:
    selected_status = st.selectbox("Status", options=status_options, index=0)
with filter_col2:
    selected_priority = st.selectbox("Priority", options=priority_options, index=0)
with filter_col3:
    keyword = st.text_input("Search", placeholder="Type request name or owner")

filtered_rows = []
for row in LIST_DETAIL_ROWS:
    matches_status = selected_status == "All" or row["status"] == selected_status
    matches_priority = selected_priority == "All" or row["priority"] == selected_priority
    search_text = f"{row['task_name']} {row['owner']} {row['request_id']}".lower()
    matches_keyword = not keyword or keyword.lower() in search_text

    if matches_status and matches_priority and matches_keyword:
        filtered_rows.append(row)

metric_row(
    [
        {"label": "Visible rows", "value": len(filtered_rows), "note": "Based on current filters"},
        {"label": "High priority", "value": sum(1 for row in filtered_rows if row["priority"] == "High"), "note": "Needs early attention"},
        {"label": "In review", "value": sum(1 for row in filtered_rows if row["status"] == "In review"), "note": "Good for detail flow demos"},
    ]
)

left, right = st.columns([1.45, 1])

with left:
    selected_row = table_panel(
        "Review queue",
        filtered_rows,
        description="A table plus a simple selector is often enough for an early reviewable mock.",
        key="planner_list_detail_sample",
        selection_field="request_id",
        selection_label="Detail target",
        selection_format=lambda row: f"{row['request_id']} | {row['task_name']}",
        empty_message="No request matches the current filters.",
    )

with right:
    if selected_row:
        detail_items = {
            "Request ID": selected_row["request_id"],
            "Owner": selected_row["owner"],
            "Status": selected_row["status"],
            "Priority": selected_row["priority"],
            "Due date": selected_row["due_date"],
            "Channel": selected_row["channel"],
            **LIST_DETAIL_DETAILS[selected_row["request_id"]],
        }
        detail_panel(
            "Detail panel",
            detail_items,
            description="Use the right panel for decision points, not for every field you have.",
            badge=selected_row["status"],
        )

        section_header("Timeline notes", "Short bullets are enough to explain state progression.")
        for item in LIST_DETAIL_TIMELINES[selected_row["request_id"]]:
            st.markdown(f"- {item}")
    else:
        section_header("Detail panel")
        st.info("Pick a row from the left side to populate this area.")

clicked = action_bar(
    [
        {"id": "approve", "label": "Approval draft"},
        {"id": "hold", "label": "Hold note"},
        {"id": "share", "label": "Share screen story"},
    ],
    key="planner_list_detail_actions",
    title="Next actions",
    description="Buttons should explain the next step even before they trigger real functionality.",
)

if clicked == "approve":
    st.success("Example: show the next state and the key confirmation message here.")
elif clicked == "hold":
    st.info("Example: replace a modal with a simple hold-note area during early planning.")
elif clicked == "share":
    st.info("Example: keep the review message inline instead of building sharing logic first.")