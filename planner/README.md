# Planner UI Workspace

This workspace helps planners sketch Streamlit screens quickly. The goal is review speed, not production completeness.

## Five minute start
1. Open the 91 sample page or the 92 sample page inside `pages/` and pick the closer pattern.
2. Copy `planner/starter_page.py` to `pages/95_your_screen_name.py`.
3. Change the title, description, and mock data first.
4. Keep the screen self-contained. Do not add API, DB, or secret dependencies.
5. Run `streamlit run Overview.py` and review the page from the full app.

## Safe things to change first
- Title and description
- Table rows
- Detail panel text
- Button labels and next-step copy
- Form fields and defaults

## Leave for later
- Real persistence
- Backend integration
- Auth and permissions
- Detailed edge-case handling