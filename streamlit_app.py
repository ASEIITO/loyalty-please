# ==== 完全修正版（インデント修復済み）====

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

st.set_page_config(page_title=APP_TITLE, layout="wide")

# ---------------- CSS ----------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #e6e1d3; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------- 初期化 ----------------
def init_session() -> None:
    if "state" not in st.session_state:
        st.session_state.state = create_initial_state(max_turns=10)

    if "current_event" not in st.session_state:
        st.session_state.current_event = random.choice(EVENTS)

    if "finished" not in st.session_state:
        st.session_state.finished = False

# ---------------- UI ----------------
def render_metrics(state: dict[str, Any]):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("国家資源", state["resources"])
    c2.metric("忠誠度", state["loyalty"])
    c3.metric("民衆不満", state["public_anger"])
    c4.metric("クーデターリスク", state["coup_risk"])

# ---------------- イベント ----------------
def render_event(event):
    st.subheader(event["title"])
    st.write(event["description"])

    for choice in event["choices"]:
        if st.button(choice["label"]):
            apply_choice(st.session_state.state, event, choice)

            game_over, reason = check_game_over(st.session_state.state)
            if game_over:
                st.session_state.finished = True
                st.session_state.state["ending_reason"] = reason
            else:
                advance_turn(st.session_state.state)
                st.session_state.current_event = random.choice(EVENTS)

            st.rerun()

# ---------------- 終了画面 ----------------
def render_end(state):
    st.header("終了")
    st.text(build_end_message(state))

    if st.button("再スタート"):
        st.session_state.clear()
        st.rerun()

# ---------------- メイン ----------------
def main():
    inject_css()
    init_session()

    state = st.session_state.state

    st.title(APP_TITLE)
    render_metrics(state)

    if st.session_state.finished:
        render_end(state)
    else:
        render_event(st.session_state.current_event)

if __name__ == "__main__":
    main()
