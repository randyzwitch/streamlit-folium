LIST_DETAIL_ROWS = [
    {
        "request_id": "REQ-2401",
        "task_name": "New supplier onboarding review",
        "owner": "Minji Kim",
        "status": "In review",
        "priority": "High",
        "due_date": "2026-03-18",
        "channel": "Email",
    },
    {
        "request_id": "REQ-2402",
        "task_name": "Price change approval draft",
        "owner": "Junho Park",
        "status": "Drafting",
        "priority": "Medium",
        "due_date": "2026-03-19",
        "channel": "Messenger",
    },
    {
        "request_id": "REQ-2403",
        "task_name": "Contract review summary",
        "owner": "Subin Lee",
        "status": "Waiting feedback",
        "priority": "High",
        "due_date": "2026-03-20",
        "channel": "Meeting note",
    },
    {
        "request_id": "REQ-2404",
        "task_name": "Purchase intake form refresh",
        "owner": "Doyoon Choi",
        "status": "In review",
        "priority": "Low",
        "due_date": "2026-03-24",
        "channel": "Workshop",
    },
]

LIST_DETAIL_DETAILS = {
    "REQ-2401": {
        "Current step": "Required document check",
        "Goal": "Review the onboarding flow before supplier activation.",
        "Background": "The current screen mixes input order and review points.",
        "Next move": "Lock the list-to-detail transition pattern.",
        "Risk": "Without an attachment area the review story feels incomplete.",
    },
    "REQ-2402": {
        "Current step": "Information structure cleanup",
        "Goal": "Explain request, approval, and result in one screen.",
        "Background": "Approval info and change history are split today.",
        "Next move": "Compare top summary and bottom history layout.",
        "Risk": "State labels are not settled yet.",
    },
    "REQ-2403": {
        "Current step": "Stakeholder feedback collection",
        "Goal": "Split summary cards from long legal notes.",
        "Background": "The screen collapses when findings become too long.",
        "Next move": "Separate note area from action buttons.",
        "Risk": "Without a priority badge important items get buried.",
    },
    "REQ-2404": {
        "Current step": "Field redesign",
        "Goal": "Help requesters input quickly and reviewers scan faster.",
        "Background": "The current form is long and has weak grouping.",
        "Next move": "Restructure into three simple sections.",
        "Risk": "Too much helper text slows wireframe reviews.",
    },
}

LIST_DETAIL_TIMELINES = {
    "REQ-2401": [
        "03/14 Request logged",
        "03/15 Required documents aligned",
        "03/16 Detail panel layout discussion",
    ],
    "REQ-2402": [
        "03/13 Requirement intake",
        "03/15 Approval history grouped",
        "03/16 Layout comparison review",
    ],
    "REQ-2403": [
        "03/12 Draft shared",
        "03/14 Legal feedback applied",
        "03/16 Priority badge position reviewed",
    ],
    "REQ-2404": [
        "03/11 Existing form audit",
        "03/15 Section split drafted",
        "03/16 Field reduction locked",
    ],
}

FORM_SAMPLE_FIELDS = [
    {
        "group": "Basics",
        "key": "screen_name",
        "label": "Screen name",
        "type": "text",
        "value": "Purchase request intake",
        "placeholder": "Example: Supplier review request",
    },
    {
        "group": "Basics",
        "key": "screen_goal",
        "label": "Screen goal",
        "type": "textarea",
        "value": "Help the requester input only what the reviewer actually needs.",
    },
    {
        "group": "Layout",
        "key": "layout_type",
        "label": "Base layout",
        "type": "select",
        "options": ["List + detail", "Single input form", "Top summary + bottom table"],
        "value": "Single input form",
    },
    {
        "group": "Layout",
        "key": "ui_blocks",
        "label": "Needed blocks",
        "type": "multiselect",
        "options": ["Summary metrics", "Filter area", "Data table", "Detail panel", "Action buttons", "Notes area"],
        "value": ["Action buttons", "Notes area"],
    },
    {
        "group": "Ops",
        "key": "owner_team",
        "label": "Owner team",
        "type": "radio",
        "options": ["Planning", "Sales", "Procurement", "Operations"],
        "value": "Planning",
    },
    {
        "group": "Ops",
        "key": "review_cycle_days",
        "label": "Review cycle days",
        "type": "number",
        "value": 7,
        "min_value": 1,
        "step": 1,
    },
    {
        "group": "Ops",
        "key": "has_upload",
        "label": "Includes file upload",
        "type": "toggle",
        "value": False,
    },
    {
        "group": "Ops",
        "key": "target_date",
        "label": "Target review date",
        "type": "date",
        "value": "2026-03-21",
    },
]