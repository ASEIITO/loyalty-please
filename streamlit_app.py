from __future__ import annotations

import random
from typing import Any

import streamlit as st

from events import EVENTS
from game_logic import (
    advance_turn,
    apply_choice,
    build_end_message,
    check_game_over,
    create_initial_state,
    record_history,
)


APP_TITLE = "Loyalty, Please"
APP_SUBTITLE = "セレクトレート論をもとにした独裁者意思決定ゲーム"
APP_VERSION = "v0.1 (April 10, 2026)"
APP_AUTHOR = "Asei Ito"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #e6e1d3;
            color: #1f1f1f;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1.5rem;
            max-width: 1400px;
        }

        h1, h2, h3 {
            color: #1b1b1b;
            font-family: Georgia, "Times New Roman", serif;
        }

        .game-subtitle {
            color: #4b4b4b;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }

        .paper-card {
            background: #f6f1e6;
            border: 2px solid #8a7f6a;
            border-radius: 8px;
            padding: 1.1rem 1.2rem 1rem 1.2rem;
            box-shadow: 2px 2px 0 rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        }

        .paper-header {
            font-size: 0.88rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: #5b5140;
            margin-bottom: 0.6rem;
        }

        .paper-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1f1f1f;
            margin-bottom: 0.8rem;
            font-family: Georgia, "Times New Roman", serif;
        }

        .paper-divider {
            border-top: 1px solid #8a7f6a;
            margin: 0.6rem 0 0.9rem 0;
        }

        .danger-banner {
            background: #5c1f1f;
            color: #fff3f3;
            border-radius: 6px;
            padding: 0.7rem 0.9rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
        }

        .warning-banner {
            background: #7a5c18;
            color: #fff8e8;
            border-radius: 6px;
            padding: 0.7rem 0.9rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
        }

        .memo-card {
            background: #efe8d7;
            border: 1px solid #b4a893;
            border-radius: 10px;
            padding: 1rem 1rem 0.7rem 1rem;
            margin-bottom: 1rem;
        }

        .turn-badge {
            display: inline-block;
            background: #d9d1bf;
            color: #2a2a2a;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .result-box {
            background: #e9efe3;
            border-left: 6px solid #5e7d54;
            padding: 0.9rem 1rem;
            border-radius: 6px;
            margin-top: 0.7rem;
            margin-bottom: 1rem;
        }

        .log-box {
            background: #f7f3ea;
            border: 1px solid #c1b59c;
            border-radius: 8px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.75rem;
        }

        .end-box {
            background: #f7f3ea;
            border: 2px solid #8a7f6a;
            border-radius: 8px;
            padding: 1rem;
            white-space: pre-wrap;
        }

        .title-screen {
            background: #f6f1e6;
            border: 2px solid #8a7f6a;
            border-radius: 10px;
            padding: 2.4rem 2rem;
            box-shadow: 3px 3px 0 rgba(0,0,0,0.08);
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }

        .title-main {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            font-family: Georgia, "Times New Roman", serif;
            color: #1f1f1f;
        }

        .title-sub {
            font-size: 1.15rem;
            color: #4a4a4a;
            margin-bottom: 1.4rem;
        }

        .title-note {
            max-width: 760px;
            margin: 0 auto 1.6rem auto;
            line-height: 1.8;
            color: #333;
            font-size: 1rem;
        }

        .footer-meta {
            text-align: center;
            color: #5b5140;
            font-size: 0.85rem;
            font-family: Georgia, serif;
            letter-spacing: 0.05em;
            margin-top: 1.5rem;
        }

        div[data-testid="stMetric"] {
            background: #f6f1e6;
            border: 1px solid #c1b59c;
            padding: 0.7rem 0.9rem;
            border-radius: 8px;
        }

        div[data-testid="stMetricLabel"] {
            font-weight: 700;
        }

        div.stButton > button {
            height: 3.1rem;
            font-size: 1rem;
            font-weight: 700;
            border-radius: 8px;
            border: 1px solid #6b6252;
            background: #f4efe4;
            color: #1f1f1f;
        }

        div.stButton > button:hover {
            border-color: #222;
            background: #ebe3d4;
            color: #111;
        }

        .start-button-wrap {
            max-width: 420px;
            margin: 0 auto;
        }

        .footer-note {
            color: #5d5d5d;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def snapshot_state(state: dict[str, Any]) -> dict[str, int]:
    return {
        "resources": state["resources"],
        "loyalty": state["loyalty"],
        "public_anger": state["public_anger"],
        "coup_risk": state["coup_risk"],
    }


def get_event_weight(event: dict[str, Any], state: dict[str, Any]) -> int:
    weight = 1
    tags = event.get("tags", [])

    if state["loyalty"] < 40 and any(tag in tags for tag in ["military", "elite", "coup"]):
        weight += 3

    if state["coup_risk"] >= 80 and any(tag in tags for tag in ["military", "coup"]):
        weight += 5

    if state["public_anger"] >= 70 and any(tag in tags for tag in ["public", "riot", "repression"]):
        weight += 4

    if state.get("riot_active", False) and any(tag in tags for tag in ["riot", "repression"]):
        weight += 5

    if state["resources"] < 30 and any(tag in tags for tag in ["budget", "economy", "foreign"]):
        weight += 4

    return weight


def crisis_event_available(event: dict[str, Any], state: dict[str, Any]) -> bool:
    event_id = event["id"]

    if event_id == "barracks_unrest":
        return state["loyalty"] < 40 or state["coup_risk"] >= 70

    if event_id == "urban_protest":
        return state["public_anger"] >= 65 or state.get("riot_active", False)

    if event_id == "reserve_crisis":
        return state["resources"] < 35

    return True


def choose_event(state: dict[str, Any], used_event_ids: set[str]) -> dict[str, Any]:
    unused_events = [event for event in EVENTS if event["id"] not in used_event_ids]
    base_pool = unused_events if unused_events else EVENTS

    pool = [event for event in base_pool if crisis_event_available(event, state)]
    if not pool:
        pool = base_pool

    weights = [get_event_weight(event, state) for event in pool]
    chosen = random.choices(pool, weights=weights, k=1)[0]
    used_event_ids.add(chosen["id"])
    return chosen


def init_session() -> None:
    if "screen" not in st.session_state:
        st.session_state.screen = "title"

    if "state" not in st.session_state:
        st.session_state.state = create_initial_state(max_turns=10)

    if "used_event_ids" not in st.session_state:
        st.session_state.used_event_ids = set()

    if "current_event" not in st.session_state:
        st.session_state.current_event = choose_event(
            st.session_state.state,
            st.session_state.used_event_ids,
        )

    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = None

    if "last_delta" not in st.session_state:
        st.session_state.last_delta = None

    if "finished" not in st.session_state:
        st.session_state.finished = False


def full_reset(to_title: bool = True) -> None:
    keys = [
        "state",
        "used_event_ids",
        "current_event",
        "last_feedback",
        "last_delta",
        "finished",
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

    if to_title:
        st.session_state.screen = "title"
    else:
        st.session_state.screen = "game"

    init_session()


def start_game() -> None:
    full_reset(to_title=False)


def apply_player_choice(choice: dict[str, Any]) -> None:
    state = st.session_state.state
    event = st.session_state.current_event

    before = snapshot_state(state)
    apply_choice(state, choice)
    record_history(state, event, choice, before)

    after = snapshot_state(state)
    st.session_state.last_feedback = choice["feedback"]
    st.session_state.last_delta = {
        key: after[key] - before[key]
        for key in before.keys()
    }

    game_over, reason = check_game_over(state)
    if game_over:
        state["game_over"] = True
        state["ending_reason"] = reason
        st.session_state.finished = True
        return

    if state["turn"] >= state["max_turns"]:
        st.session_state.finished = True
        return

    advance_turn(state)
    st.session_state.current_event = choose_event(
        st.session_state.state,
        st.session_state.used_event_ids,
    )


def danger_text(value: int) -> str:
    if value >= 80:
        return "危機"
    if value >= 60:
        return "警戒"
    return "安定"


def render_footer() -> None:
    st.markdown(
        f"""
        <hr style="margin-top: 2rem; border-top: 1px solid #8a7f6a;">
        <div class="footer-meta">
            {APP_TITLE.upper()} {APP_VERSION}<br>
            CREATED BY {APP_AUTHOR}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_title_screen() -> None:
    top_space_left, center, top_space_right = st.columns([1, 2.8, 1])

    with center:
        st.markdown(
            f"""
            <div class="title-screen">
                <div class="title-main">{APP_TITLE}</div>
                <div class="title-sub">{APP_SUBTITLE}</div>
                <div class="title-note">
                    あなたは架空国家の独裁者です。<br>
                    限られた資源を、支持層・民衆・治安機構のあいだで配分しながら、
                    10ターンにわたって政権維持を目指します。<br><br>
                    私的利益は忠誠を高めますが、不満と財政悪化を招きます。<br>
                    公共財は民衆不満を抑えますが、勝利連合への直接的な見返りにはなりにくいです。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="start-button-wrap">', unsafe_allow_html=True)
        if st.button("START", use_container_width=True):
            start_game()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="footer-note" style="text-align:center;">
                Decision is power. Delay is risk.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_metrics(state: dict[str, Any]) -> None:
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("国家資源", state["resources"])
    with c2:
        st.metric("忠誠度", state["loyalty"])
    with c3:
        st.metric("民衆不満", state["public_anger"], danger_text(state["public_anger"]))
    with c4:
        st.metric("クーデターリスク", state["coup_risk"], danger_text(state["coup_risk"]))

    st.progress(max(0, min(state["resources"], 100)), text="国家資源")
    st.progress(max(0, min(state["loyalty"], 100)), text="忠誠度")
    st.progress(max(0, min(state["public_anger"], 100)), text="民衆不満")
    st.progress(max(0, min(state["coup_risk"], 100)), text="クーデターリスク")

    st.markdown(
        f'<div class="turn-badge">Turn {state["turn"]} / {state["max_turns"]}</div>',
        unsafe_allow_html=True,
    )

    if state.get("riot_active", False):
        st.markdown(
            '<div class="danger-banner">⚠ 暴動が拡大しています。放置すると財政と忠誠が悪化します。</div>',
            unsafe_allow_html=True,
        )

    if state.get("coup_attempt", False):
        st.markdown(
            '<div class="warning-banner">⚠ クーデター未遂の兆候があります。支持連合の離反が進行中です。</div>',
            unsafe_allow_html=True,
        )


def choice_prefix(label: str) -> str:
    if "拒否" in label or "無視" in label or "静観" in label:
        return "❌"
    if "一部" in label or "軽い" in label or "検討" in label:
        return "⚖️"
    if "治安" in label or "粛清" in label or "抑え込" in label:
        return "🪖"
    return "✅"


def render_event(event: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="paper-card">
            <div class="paper-header">📄 国家保安評議会 回覧文書</div>
            <div class="paper-title">{event["title"]}</div>
            <div class="paper-divider"></div>
            <div style="font-size:1.05rem; line-height:1.7;">{event["description"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for idx, choice in enumerate(event["choices"]):
        label = f"{choice_prefix(choice['label'])} {choice['label']}"
        if st.button(
            label,
            key=f"choice_{event['id']}_{idx}",
            use_container_width=True,
        ):
            apply_player_choice(choice)
            st.rerun()

    st.markdown(
        '<div class="footer-note">あなたの判断は即時に反映されます。</div>',
        unsafe_allow_html=True,
    )


def render_last_result() -> None:
    if st.session_state.last_feedback is None or st.session_state.last_delta is None:
        return

    delta = st.session_state.last_delta

    st.markdown(
        f"""
        <div class="result-box">
            <strong>直前の判断の結果</strong><br><br>
            {st.session_state.last_feedback}<br><br>
            資源 {delta["resources"]:+} /
            忠誠 {delta["loyalty"]:+} /
            不満 {delta["public_anger"]:+} /
            クーデター {delta["coup_risk"]:+}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_theory_panel() -> None:
    st.markdown(
        """
        <div class="memo-card">
            <h3 style="margin-top:0;">理論メモ</h3>
            <p>支持層への私的利益は忠誠を高めやすい一方、民衆不満や財政悪化を招きやすい。</p>
            <p>公共財は民衆不満を抑えるが、勝利連合への直接的な見返りにはなりにくい。</p>
            <p>忠誠低下はクーデターへ、民衆不満の蓄積は暴動へつながる。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history(state: dict[str, Any], expanded: bool = False) -> None:
    if not state["history"]:
        return

    with st.expander("📜 国家日報", expanded=expanded):
        for entry in state["history"]:
            delta = entry["delta"]
            st.markdown(
                f"""
                <div class="log-box">
                    <strong>Turn {entry["turn"]}: {entry["event_title"]}</strong><br>
                    選択: {entry["choice_label"]}<br>
                    変化: 資源 {delta["resources"]:+}, 忠誠 {delta["loyalty"]:+}, 不満 {delta["public_anger"]:+}, クーデター {delta["coup_risk"]:+}<br>
                    <span style="color:#5b5b5b;">{entry["feedback"]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_end_screen(state: dict[str, Any]) -> None:
    if state.get("ending_reason"):
        st.error("政権は崩壊しました。")
    else:
        st.success("あなたは任期を全うしました。")

    st.subheader("終了分析")
    st.markdown(
        f'<div class="end-box">{build_end_message(state)}</div>',
        unsafe_allow_html=True,
    )

    render_history(state, expanded=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("もう一度プレイする", use_container_width=True):
            start_game()
            st.rerun()
    with col2:
        if st.button("タイトルへ戻る", use_container_width=True):
            full_reset(to_title=True)
            st.rerun()


def render_game_screen() -> None:
    state = st.session_state.state

    st.title(APP_TITLE)
    st.markdown(
        f'<div class="game-subtitle">{APP_SUBTITLE}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1])

    with left:
        render_metrics(state)
        render_last_result()

        if st.session_state.finished:
            render_end_screen(state)
        else:
            render_event(st.session_state.current_event)

    with right:
        render_theory_panel()
        render_history(state, expanded=False)
        st.button("ゲームをリセット", on_click=start_game, use_container_width=True)
        if st.button("タイトルへ戻る", key="back_to_title_sidebar", use_container_width=True):
            full_reset(to_title=True)
            st.rerun()


def main() -> None:
    inject_css()
    init_session()

    if st.session_state.screen == "title":
        render_title_screen()
    else:
        render_game_screen()

    render_footer()


if __name__ == "__main__":
    main()
