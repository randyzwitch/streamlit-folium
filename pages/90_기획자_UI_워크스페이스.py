import streamlit as st

from planner import (
    apply_wireframe_theme,
    detail_panel,
    metric_row,
    page_header,
    section_header,
)


st.set_page_config(page_title="Planner UI Workspace", layout="wide")

apply_wireframe_theme()
page_header(
    "Planner UI Workspace",
    "This 90-series area is separate from the existing demo scenarios. Planners can duplicate the starter page, replace text and mock data, and get a usable screen draft quickly.",
)

metric_row(
    [
        {"label": "Shared range", "value": "90-94", "note": "Samples and guides"},
        {"label": "Draft range", "value": "95-99", "note": "Planner-owned experiments"},
        {"label": "Data mode", "value": "Mock Only", "note": "No API or DB dependency"},
    ]
)

left, right = st.columns([1.2, 1])

with left:
    section_header(
        "What this workspace is for",
        "Use it to make structure, flow, and copy reviewable before any backend integration.",
    )
    st.markdown(
        """
        1. Open the closest sample page.
        2. Copy `planner/starter_page.py` into `pages/95_your_screen.py`.
        3. Edit title, description, table rows, and detail copy.
        4. Keep the screen non-persistent and self-contained.
        """
    )

    detail_panel(
        "Reference files",
        {
            "Quick start": "planner/README.md",
            "Pattern guide": "planner/PATTERNS.md",
            "Workspace rules": "planner/RULES.md",
            "Starter template": "planner/starter_page.py",
        },
        description="The docs are intentionally short so they are actually usable.",
    )

with right:
    detail_panel(
        "Page number rule",
        {
            "90-94": "Shared workspace pages and starter samples",
            "95-99": "Planner-owned draft screens",
            "01-06": "Existing demo scenarios that should stay isolated",
            "Default move": "Start a new draft from the 95-series",
        },
        badge="Navigation rule",
    )

    section_header("Working rules", "Keep only what helps someone review the screen.")
    st.markdown(
        """
        - Reuse the common blocks and change purpose-specific copy first.
        - Keep mock data near the top of the file.
        - Highlight status, priority, and next action before styling details.
        - Stay neutral and wireframe-oriented.
        """
    )

section_header("Recommended starting points", "Pick the closest screen type and duplicate from there.")
st.markdown(
    """
    - Queue or review screen: the 91 sample page in `pages/`
    - Entry or request form: the 92 sample page in `pages/`
    - Mixed screen or blank starting point: `planner/starter_page.py`
    """
)