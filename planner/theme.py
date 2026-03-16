from __future__ import annotations

import streamlit as st


WIRE_FRAME_CSS = """
<style>
:root {
    --planner-bg: #f4f6fb;
    --planner-surface: #ffffff;
    --planner-border: #d8e0ea;
    --planner-text: #162033;
    --planner-muted: #5d6981;
    --planner-accent: #1f56a3;
    --planner-accent-soft: #eaf1ff;
}

[data-testid="stAppViewContainer"] {
    background: var(--planner-bg);
    color: var(--planner-text);
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--planner-border);
}

[data-testid="stHeader"] {
    background: rgba(244, 246, 251, 0.92);
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.planner-page-header {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid var(--planner-border);
    border-radius: 20px;
    padding: 1.75rem 1.9rem;
    margin-bottom: 1rem;
    box-shadow: 0 14px 40px rgba(26, 37, 63, 0.05);
}

.planner-badge {
    display: inline-block;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    border: 1px solid #c7d6f3;
    background: var(--planner-accent-soft);
    color: var(--planner-accent);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.planner-title {
    margin-top: 0.9rem;
    font-size: 2rem;
    font-weight: 700;
    color: var(--planner-text);
    letter-spacing: -0.02em;
}

.planner-description {
    margin-top: 0.55rem;
    color: var(--planner-muted);
    font-size: 0.98rem;
    line-height: 1.7;
}

.planner-section {
    margin: 1.2rem 0 0.7rem;
}

.planner-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--planner-text);
    letter-spacing: -0.01em;
}

.planner-section-description {
    margin-top: 0.25rem;
    color: var(--planner-muted);
    font-size: 0.92rem;
    line-height: 1.6;
}

.planner-metric-card {
    background: var(--planner-surface);
    border: 1px solid var(--planner-border);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    min-height: 118px;
    box-shadow: 0 10px 30px rgba(20, 31, 55, 0.04);
}

.planner-metric-label {
    color: var(--planner-muted);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.planner-metric-value {
    color: var(--planner-text);
    font-size: 1.8rem;
    font-weight: 700;
    margin-top: 0.5rem;
}

.planner-metric-note {
    color: var(--planner-muted);
    font-size: 0.86rem;
    margin-top: 0.35rem;
    line-height: 1.5;
}

.planner-kv {
    background: var(--planner-surface);
    border: 1px solid var(--planner-border);
    border-radius: 14px;
    padding: 0.95rem 1rem;
    min-height: 92px;
    margin-bottom: 0.8rem;
}

.planner-kv-label {
    color: var(--planner-muted);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.planner-kv-value {
    color: var(--planner-text);
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.55;
    margin-top: 0.45rem;
    white-space: pre-wrap;
}

.planner-status {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    border: 1px solid #c8d7ec;
    background: #f3f7ff;
    color: #325a97;
    font-size: 0.78rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
</style>
"""


def apply_wireframe_theme() -> None:
    st.markdown(WIRE_FRAME_CSS, unsafe_allow_html=True)