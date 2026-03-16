from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime
from html import escape
from typing import Any

import pandas as pd
import streamlit as st

from .theme import apply_wireframe_theme as _apply_wireframe_theme


def apply_wireframe_theme() -> None:
    _apply_wireframe_theme()


def page_header(title: str, description: str, badge: str = "Planner Workspace") -> None:
    st.markdown(
        f"""
        <div class="planner-page-header">
            <div class="planner-badge">{escape(badge)}</div>
            <div class="planner-title">{escape(title)}</div>
            <div class="planner-description">{escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(
    title: str,
    description: str | None = None,
    badge: str | None = None,
) -> None:
    badge_markup = ""
    if badge:
        badge_markup = f'<span class="planner-status">{escape(badge)}</span>'

    description_markup = ""
    if description:
        description_markup = (
            f'<div class="planner-section-description">{escape(description)}</div>'
        )

    st.markdown(
        f"""
        <div class="planner-section">
            <div class="planner-section-title">{escape(title)}{badge_markup}</div>
            {description_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: Sequence[Mapping[str, Any]]) -> None:
    if not metrics:
        return

    columns = st.columns(len(metrics))
    for column, metric in zip(columns, metrics):
        label = escape(str(metric.get("label", "")))
        value = escape(_stringify(metric.get("value", "-")))
        note = metric.get("note")
        note_markup = ""
        if note:
            note_markup = f'<div class="planner-metric-note">{escape(str(note))}</div>'

        with column:
            st.markdown(
                f"""
                <div class="planner-metric-card">
                    <div class="planner-metric-label">{label}</div>
                    <div class="planner-metric-value">{value}</div>
                    {note_markup}
                </div>
                """,
                unsafe_allow_html=True,
            )


def table_panel(
    title: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    description: str | None = None,
    key: str,
    selection_field: str | None = None,
    selection_label: str = "Detail target",
    selection_format: Callable[[Mapping[str, Any]], str] | None = None,
    empty_message: str = "No rows to show.",
) -> dict[str, Any] | None:
    section_header(title, description)

    normalized_rows = [dict(row) for row in rows]
    if not normalized_rows:
        st.info(empty_message)
        return None

    selected_row = normalized_rows[0]
    if selection_field:
        options = [row.get(selection_field) for row in normalized_rows]
        selected_value = st.selectbox(
            selection_label,
            options=options,
            index=0,
            format_func=lambda value: _format_selected_value(
                normalized_rows, selection_field, value, selection_format
            ),
            key=f"{key}_selector",
        )
        for row in normalized_rows:
            if row.get(selection_field) == selected_value:
                selected_row = row
                break

    dataframe = pd.DataFrame(normalized_rows)
    dataframe.index = range(1, len(dataframe) + 1)
    st.dataframe(dataframe, use_container_width=True)
    return selected_row


def detail_panel(
    title: str,
    items: Mapping[str, Any] | Sequence[tuple[str, Any]],
    *,
    description: str | None = None,
    badge: str | None = None,
) -> None:
    section_header(title, description, badge=badge)

    if isinstance(items, Mapping):
        entries = list(items.items())
    else:
        entries = list(items)

    if not entries:
        st.info("No detail available.")
        return

    for index in range(0, len(entries), 2):
        columns = st.columns(2)
        for column, (label, value) in zip(columns, entries[index : index + 2]):
            with column:
                st.markdown(
                    f"""
                    <div class="planner-kv">
                        <div class="planner-kv-label">{escape(str(label))}</div>
                        <div class="planner-kv-value">{escape(_stringify(value))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def form_panel(
    title: str,
    fields: Sequence[Mapping[str, Any]],
    *,
    form_key: str,
    submit_label: str = "Submit",
    description: str | None = None,
) -> tuple[bool, dict[str, Any]]:
    section_header(title, description)

    values: dict[str, Any] = {}
    current_group: str | None = None

    with st.form(form_key):
        for field in fields:
            group = field.get("group")
            if group and group != current_group:
                st.markdown(f"**{group}**")
                current_group = str(group)

            field_key = str(field["key"])
            values[field_key] = _render_field(field)

        submitted = st.form_submit_button(submit_label)

    return submitted, values


def action_bar(
    actions: Sequence[Mapping[str, Any]],
    *,
    key: str,
    title: str | None = None,
    description: str | None = None,
) -> str | None:
    if title or description:
        section_header(title or "Next actions", description)

    if not actions:
        return None

    clicked: str | None = None
    columns = st.columns(len(actions))
    for index, (column, action) in enumerate(zip(columns, actions)):
        action_id = str(action.get("id", index))
        label = str(action.get("label", f"Action {index + 1}"))
        help_text = action.get("help")
        disabled = bool(action.get("disabled", False))

        with column:
            if st.button(
                label,
                key=f"{key}_{action_id}",
                help=help_text,
                disabled=disabled,
                use_container_width=True,
            ):
                clicked = action_id

    return clicked


def _format_selected_value(
    rows: Sequence[Mapping[str, Any]],
    selection_field: str,
    selected_value: Any,
    selection_format: Callable[[Mapping[str, Any]], str] | None,
) -> str:
    for row in rows:
        if row.get(selection_field) == selected_value:
            if selection_format:
                return selection_format(row)
            return str(selected_value)
    return str(selected_value)


def _render_field(field: Mapping[str, Any]) -> Any:
    field_type = str(field.get("type", "text"))
    label = str(field.get("label", field["key"]))
    help_text = field.get("help")
    placeholder = field.get("placeholder")
    options = list(field.get("options", []))
    value = field.get("value")
    widget_key = str(field["key"])

    if field_type == "textarea":
        return st.text_area(
            label,
            value=str(value or ""),
            help=help_text,
            placeholder=placeholder,
            key=widget_key,
        )
    if field_type == "select":
        current_value = value if value in options else options[0]
        return st.selectbox(
            label,
            options=options,
            index=options.index(current_value),
            help=help_text,
            key=widget_key,
        )
    if field_type == "multiselect":
        default_values = value if isinstance(value, list) else []
        return st.multiselect(
            label,
            options=options,
            default=default_values,
            help=help_text,
            key=widget_key,
        )
    if field_type == "number":
        return st.number_input(
            label,
            min_value=field.get("min_value"),
            max_value=field.get("max_value"),
            step=field.get("step", 1),
            value=value if value is not None else 0,
            help=help_text,
            key=widget_key,
        )
    if field_type == "date":
        return st.date_input(
            label,
            value=_coerce_date(value),
            help=help_text,
            key=widget_key,
        )
    if field_type == "radio":
        current_value = value if value in options else options[0]
        return st.radio(
            label,
            options=options,
            index=options.index(current_value),
            help=help_text,
            key=widget_key,
        )
    if field_type in {"toggle", "checkbox"}:
        return st.checkbox(
            label,
            value=bool(value),
            help=help_text,
            key=widget_key,
        )

    return st.text_input(
        label,
        value=str(value or ""),
        help=help_text,
        placeholder=placeholder,
        key=widget_key,
    )


def _coerce_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    return date.today()


def _stringify(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return ", ".join(_stringify(item) for item in value)
    return str(value)