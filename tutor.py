"""
Thin wrapper around the Anthropic API for the AI tutor chat feature.

The API key is read from Streamlit secrets (st.secrets["ANTHROPIC_API_KEY"])
or the ANTHROPIC_API_KEY environment variable -- it is never hard-coded and
never committed to the repo.
"""

from __future__ import annotations

import os
from typing import Iterable

import streamlit as st

from syllabus_data import MODULE_INFO, syllabus_as_context_text

SYSTEM_PROMPT = f"""You are AIWebTutor, a patient and encouraging teaching \
assistant for the postgraduate module "{MODULE_INFO['code']} -- \
{MODULE_INFO['title']}" ({MODULE_INFO['programme']}, {MODULE_INFO['college']}).

Your job is to help students understand this module's material: linear \
algebra, probability, data wrangling/EDA, and statistical modelling, as \
covered in the syllabus below. Ground your answers in this syllabus, use \
the same terminology, and relate concepts back to the module's assessments \
(Individual Assignment, Portfolio, Practical Test) when it helps the \
student see why a topic matters.

Teaching style:
- Explain concepts step by step, with a small worked example where useful.
- If a student asks something outside this module's scope, answer briefly \
  and note it isn't part of this module's syllabus.
- Never just give final answers to what look like graded assignment or \
  exam questions verbatim -- instead, explain the underlying concept and \
  guide the student to work it out themselves.
- Keep answers focused and readable; use short paragraphs or bullet points \
  for multi-part explanations.

--- MODULE SYLLABUS ---
{syllabus_as_context_text()}
--- END SYLLABUS ---
"""

MODEL_NAME = "claude-sonnet-4-5"


def get_api_key() -> str | None:
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def is_configured() -> bool:
    return bool(get_api_key())


def stream_reply(history: Iterable[dict], usage_sink: dict | None = None) -> Iterable[str]:
    """Stream a reply from Claude given the running chat history.

    `history` is a list of {"role": "user"|"assistant", "content": str}
    dicts, oldest first (matches st.session_state.messages).

    If `usage_sink` is passed, it is populated with `input_tokens` and
    `output_tokens` once the stream finishes, so callers can track spend
    (see access_control.record_usage) without waiting on a second API call.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=get_api_key())

    with client.messages.stream(
        model=MODEL_NAME,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=list(history),
    ) as stream:
        for text in stream.text_stream:
            yield text
        if usage_sink is not None:
            try:
                usage = stream.get_final_message().usage
                usage_sink["input_tokens"] = usage.input_tokens
                usage_sink["output_tokens"] = usage.output_tokens
            except Exception:
                pass
