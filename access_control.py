"""
Lightweight class-wide access gate and daily token budget guard, so a
single shared ANTHROPIC_API_KEY doesn't rack up unexpected or unbounded
cost when the AI Tutor Chat is opened up to a whole class.

Configure via Streamlit secrets (both optional -- the app works fine with
neither set, it just has no gate/cap):

    CLASS_ACCESS_CODE   -- if set, students must enter this code once per
                           browser session before using AI Tutor Chat.
    MAX_DAILY_TOKENS    -- total Claude input+output tokens allowed across
                           ALL students combined per calendar day
                           (default 200000).

Usage is tracked in a small local JSON file next to the app. Streamlit
Community Cloud's filesystem is ephemeral across redeploys/restarts, so
the counter resets then too -- this is a soft safety net against a chatty
class running up a bill overnight, not a hard billing guarantee. For
strict cost control, also set a spending limit at console.anthropic.com.
"""

import json
import os
from datetime import datetime, timezone

import streamlit as st

USAGE_FILE = os.path.join(os.path.dirname(__file__), ".daily_usage.json")
DEFAULT_MAX_DAILY_TOKENS = 200_000


def _get_secret(key: str, default=None):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)


def is_access_gated() -> bool:
    return bool(_get_secret("CLASS_ACCESS_CODE"))


def check_access_code(code: str) -> bool:
    expected = _get_secret("CLASS_ACCESS_CODE")
    return bool(expected) and code.strip() == str(expected).strip()


def _today_str() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _load_usage() -> dict:
    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        data = {}
    if data.get("date") != _today_str():
        data = {"date": _today_str(), "tokens": 0}
    return data


def _save_usage(data: dict) -> None:
    try:
        with open(USAGE_FILE, "w") as f:
            json.dump(data, f)
    except OSError:
        pass  # best-effort -- never crash the app over the usage counter


def get_daily_limit() -> int:
    try:
        return int(_get_secret("MAX_DAILY_TOKENS", DEFAULT_MAX_DAILY_TOKENS))
    except (TypeError, ValueError):
        return DEFAULT_MAX_DAILY_TOKENS


def get_usage_today() -> int:
    return _load_usage().get("tokens", 0)


def daily_limit_reached() -> bool:
    return get_usage_today() >= get_daily_limit()


def record_usage(tokens: int) -> None:
    if tokens <= 0:
        return
    data = _load_usage()
    data["tokens"] = data.get("tokens", 0) + tokens
    _save_usage(data)
