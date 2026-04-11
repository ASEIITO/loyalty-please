# --- ここから完全修正版 ---

from __future__ import annotations

import random
from typing import Any

import pandas as pd
import streamlit as st

from events import EVENTS
from game_logic import (
    SCENARIOS,
    advance_turn,
    apply_choice,
    build_end_message,
    check_game_over,
    create_initial_state,
    record_history,
)

APP_TITLE = "Loyalty, Please"
APP_SUBTITLE = "セレクトレート論をもとにした独裁者意思決定ゲーム"
APP_VERSION = "v0.3"
APP_AUTHOR = "Asei Ito"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- CSS ----------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #e6e1d3;
            color: #1f1f1f;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------- 基本関数 ----------------
def snapshot_state(state: dict[str, Any]) -> dict[str, int]:
    return {
        "resources": state["resources"],
        "loyalty": state["loyalty"],
        "public_anger": state["public_anger"],
        "coup_risk": state["coup_risk"],
    }

def init_session() -> None:
    if "screen" not in st.session_state:
        st.session_state.screen = "title"

    if "state" not in st.session_state:
        st.session_state.state = create_initial_state(max_turns=10)

    if "current_event" not in st.session_state:
        st.session_state.current_event = random.choice(EVENTS)

    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = None

    if "last_delta" not in st.session_state:
        st.session_state.last_delta = None

    if "finished" not in st.session_state:
        st.session_state.finished = False

def start_game():
    st.session_state.state = create_initial_state(max_turns=10)
    st.session_state.current_event = random.choice(EVENTS)
    st.session_state.finished = False

# ---------------- UI ----------------
def render_metrics(state: dict[str, Any]):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("国家資源", state["resources"])
    c2.metric("忠誠度", state["loyalty"])
    c3.metric("民衆不満", state["public_anger"])
    c4.metric("クーデターリスク", state["coup_risk"])

    st.progress(state["resources"])
    st.progress(state["loyalty"])
    st.progress(state["public_anger"])
    st.progress(state["coup_risk"])

def render_event(event):
    st.subheader(event["title"])
    st.write(event["description"])

    for choice in event["choices"]:
        if st.button(choice["label"]):
            before = snapshot_state(st.session_state.state)
            apply_choice(st.session_state.state, event, choice)

            after = snapshot_state(st.session_state.state)
            st.session_state.last_delta = {
                k: after[k] - before[k] for k in before
            }
            st.session_state.last_feedback = choice["feedback"]

            game_over, reason = check_game_over(st.session_state.state)
            if game_over:
                st.session_state.finished = True
                st.session_state.state["ending_reason"] = reason
            else:
                advance_turn(st.session_state.state)
                st.session_state.current_event = random.choice(EVENTS)

            st.rerun()

def render_last_result():
    if st.session_state.last_feedback:
        st.write("### 選択結果")
        st.write(st.session_state.last_feedback)
        st.write(st.session_state.last_delta)

def render_end_screen(state):
    st.header("ゲーム終了")

    st.write(build_end_message(state))

    if st.button("もう一度プレイ"):
        start_game()
        st.rerun()

# ---------------- メイン ----------------
def main():
    inject_css()
    init_session()

    state = st.session_state.state

    st.title(APP_TITLE)

    render_metrics(state)

    if st.session_state.finished:
        render_end_screen(state)
    else:
        render_event(st.session_state.current_event)
        render_last_result()

if __name__ == "__main__":
    main()
