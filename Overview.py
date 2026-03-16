import streamlit as st


st.set_page_config(page_title="Agent Demo", layout="wide")

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", "Malgun Gothic", sans-serif;
    }

    .main {
        background: #09111f;
    }

    .block-container {
        max-width: 1200px;
        padding: 3rem 4rem;
    }

    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }

    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #172a49, #0b1830);
        border: 1px solid #274777;
        color: #8dc3ff;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.42rem 1rem;
        border-radius: 999px;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #dce9ff;
        line-height: 1.2;
        margin-bottom: 0.9rem;
    }

    .hero-title span {
        color: #74b0ff;
    }

    .hero-sub {
        color: #8b9fbe;
        font-size: 1rem;
        font-weight: 400;
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.7;
    }

    .section-title {
        color: #7fa4db;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 2rem 0 1.1rem;
    }

    .scenario-card {
        background: #ffffff;
        border: 1px solid #d6dfef;
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 12px 32px rgba(7, 17, 33, 0.08);
    }

    .scenario-number {
        color: #5e7fb0;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .scenario-title {
        color: #152132;
        font-size: 1.08rem;
        font-weight: 700;
        line-height: 1.35;
        margin-bottom: 0.55rem;
    }

    .scenario-body {
        color: #52627d;
        font-size: 0.92rem;
        line-height: 1.65;
    }

    .divider {
        border: none;
        border-top: 1px solid #20314f;
        margin: 2.7rem 0;
    }

    .workspace-panel {
        background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #d6dfef;
        border-radius: 18px;
        padding: 1.5rem;
        min-height: 240px;
        box-shadow: 0 12px 32px rgba(7, 17, 33, 0.08);
    }

    .workspace-title {
        color: #142033;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
    }

    .workspace-body {
        color: #51617c;
        font-size: 0.93rem;
        line-height: 1.7;
    }

    .workspace-list {
        color: #21304a;
        font-size: 0.9rem;
        line-height: 1.75;
        margin: 0.8rem 0 0;
        padding-left: 1.1rem;
    }

    .footer-note {
        text-align: center;
        color: #5f7190;
        font-size: 0.8rem;
        margin-top: 2rem;
        letter-spacing: 0.04em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

workflow_scenarios = [
    {
        "number": "Scenario 01",
        "title": "Smart invoice validation workbench",
        "body": "A workflow-style demo that compares invoice files, purchase records, and review output in one place.",
    },
    {
        "number": "Scenario 02",
        "title": "New supplier risk evaluation agent",
        "body": "A guided onboarding demo that walks through input, review, and supplier risk checkpoints.",
    },
    {
        "number": "Scenario 03",
        "title": "AI compliance and audit manager",
        "body": "A monitoring and review demo focused on surfacing high-risk findings and follow-up actions.",
    },
]

chat_scenarios = [
    {
        "number": "Scenario 04",
        "title": "Policy and purchase guide chatbot",
        "body": "A lightweight chat scenario for quick policy lookup and guidance.",
    },
    {
        "number": "Scenario 05",
        "title": "Contract clause reviewer",
        "body": "A chat-first review flow that summarizes risky clauses and supporting reasoning.",
    },
    {
        "number": "Scenario 06",
        "title": "Natural language order lookup",
        "body": "A conversational lookup flow that explains order status and suggested next actions.",
    },
]

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">CTC AI Agent Demo</div>
        <div class="hero-title">Existing demo scenarios and a<br><span>planner-friendly UI workspace</span></div>
        <div class="hero-sub">
            The original demo flows stay in place. The new 90-series pages give planners a clean area to draft Streamlit screens with reusable blocks and mock data.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Workflow Agent Scenarios</div>', unsafe_allow_html=True)
for scenario in workflow_scenarios:
    st.markdown(
        f"""
        <div class="scenario-card">
            <div class="scenario-number">{scenario['number']}</div>
            <div class="scenario-title">{scenario['title']}</div>
            <div class="scenario-body">{scenario['body']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Chat Agent Scenarios</div>', unsafe_allow_html=True)
for scenario in chat_scenarios:
    st.markdown(
        f"""
        <div class="scenario-card">
            <div class="scenario-number">{scenario['number']}</div>
            <div class="scenario-title">{scenario['title']}</div>
            <div class="scenario-body">{scenario['body']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Planner Workspace</div>', unsafe_allow_html=True)

left, right = st.columns([1.3, 1])
with left:
    st.markdown(
        """
        <div class="workspace-panel">
            <div class="workspace-title">90-series planner workspace</div>
            <div class="workspace-body">
                This area is separate from the legacy demo screens. A planner can copy a sample, change the copy and mock data, and review the draft in the same app navigation.
            </div>
            <ul class="workspace-list">
                <li>90 guide page: workspace rules and quick-start notes</li>
                <li>91 sample page: list plus detail starter</li>
                <li>92 sample page: input form starter</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="workspace-panel">
            <div class="workspace-title">Numbering and rules</div>
            <div class="workspace-body">
                Shared workspace pages stay in the 90 to 94 range. Planner-owned drafts start at 95 and remain mock-only until the screen story is stable.
            </div>
            <ul class="workspace-list">
                <li>90-94: shared samples and guides</li>
                <li>95-99: planner draft screens</li>
                <li>`planner/README.md`: quick start</li>
                <li>`planner/starter_page.py`: copyable base file</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="footer-note">Internal demo workspace</div>', unsafe_allow_html=True)