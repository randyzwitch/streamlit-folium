# Pattern Guide

## List plus detail
Use this for:
- Review queues
- Approval waiting lists
- Any screen where someone picks a row and inspects the detail panel

Start from:
- The 91 sample page in `pages/`

Rules:
- Keep only a few filters at the top.
- Use one main table.
- Put only the decision points in the right panel.
- Keep buttons to two or three actions.

## Input form
Use this for:
- New request intake
- Supplier registration
- Approval request entry

Start from:
- The 92 sample page in `pages/`

Rules:
- Group fields into sections.
- Keep only what must be reviewed now.
- After submit, show a summary panel instead of real save logic.

## Mixed screen
Use this when you need both table and form blocks.

Start from:
- `planner/starter_page.py`

Rules:
- Keep the same header and metric layout.
- Pick one main block first.
- If the screen starts feeling long, remove one major block before adding style.