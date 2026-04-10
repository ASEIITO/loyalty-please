from __future__ import annotations

import random

from events import EVENTS
from game_logic import (
    advance_turn,
    apply_choice,
    build_end_message,
    check_game_over,
    create_initial_state,
    record_history,
)


def print_status(state: dict) -> None:
    print("\n" + "=" * 40)
    print(f"Turn {state['turn']} / {state['max_turns']}")
    print(f"国家資源         : {state['resources']}")
    print(f"勝利連合の忠誠度 : {state['loyalty']}")
    print(f"民衆不満         : {state['public_anger']}")
    print(f"クーデターリスク : {state['coup_risk']}")
    if state["riot_active"]:
        print("⚠️ 大規模な暴動が発生しています")
    if state["coup_attempt"]:
        print("⚠️ クーデター未遂の兆候があります")
    print("=" * 40)


def choose_event(used_event_ids: set[str]) -> dict:
    """未使用イベントを優先して返す。足りなくなったら全体から選ぶ。"""
    unused_events = [event for event in EVENTS if event["id"] not in used_event_ids]
    pool = unused_events if unused_events else EVENTS
    event = random.choice(pool)
    used_event_ids.add(event["id"])
    return event


def ask_choice(event: dict) -> dict:
    print(f"\nイベント: {event['title']}")
    print(event["description"])
    print("\n選択肢:")

    for i, choice in enumerate(event["choices"], start=1):
        print(f"{i}. {choice['label']}")

    while True:
        raw = input("\n番号を入力してください: ").strip()
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(event["choices"]):
                return event["choices"][index]
        print("入力が正しくありません。1, 2, 3 のいずれかを入力してください。")


def snapshot_state(state: dict) -> dict:
    return {
        "resources": state["resources"],
        "loyalty": state["loyalty"],
        "public_anger": state["public_anger"],
        "coup_risk": state["coup_risk"],
    }


def print_turn_summary(state: dict) -> None:
    """直近ターンの履歴を表示する。"""
    if not state["history"]:
        return

    entry = state["history"][-1]
    delta = entry["delta"]

    print("\n今回の変化:")
    print(
        f"資源 {delta['resources']:+} / "
        f"忠誠 {delta['loyalty']:+} / "
        f"不満 {delta['public_anger']:+} / "
        f"クーデター {delta['coup_risk']:+}"
    )
    print(f"解説: {entry['feedback']}")


def print_history(state: dict) -> None:
    """全プレイ履歴を表示する。"""
    print("\n" + "=" * 40)
    print("プレイ履歴")
    print("=" * 40)

    for entry in state["history"]:
        delta = entry["delta"]
        print(f"Turn {entry['turn']}: {entry['event_title']}")
        print(f"  選択: {entry['choice_label']}")
        print(
            f"  変化: 資源 {delta['resources']:+}, "
            f"忠誠 {delta['loyalty']:+}, "
            f"不満 {delta['public_anger']:+}, "
            f"クーデター {delta['coup_risk']:+}"
        )
        print(f"  解説: {entry['feedback']}")
        print("-" * 40)


def get_event_weight(event: dict, state: dict) -> int:
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

def choose_event(state: dict, used_event_ids: set[str]) -> dict:
    unused_events = [event for event in EVENTS if event["id"] not in used_event_ids]
    pool = unused_events if unused_events else EVENTS

    weights = [get_event_weight(event, state) for event in pool]
    event = random.choices(pool, weights=weights, k=1)[0]
    used_event_ids.add(event["id"])
    return event

def main() -> None:
    print("Loyalty, Please（プロトタイプ版）")
    print("あなたは架空国家の独裁者です。10ターン政権維持を目指してください。")

    state = create_initial_state(max_turns=10)
    used_event_ids: set[str] = set()

    while True:
        print_status(state)

        event = choose_event(state, used_event_ids)
        choice = ask_choice(event)

        before = snapshot_state(state)
        apply_choice(state, choice)
        record_history(state, event, choice, before)

        print_turn_summary(state)

        game_over, reason = check_game_over(state)
        if game_over:
            state["game_over"] = True
            state["ending_reason"] = reason
            print_history(state)
            print("\n" + "=" * 40)
            print(build_end_message(state))
            print("=" * 40)
            break

        if state["turn"] >= state["max_turns"]:
            print_history(state)
            print("\n" + "=" * 40)
            print(build_end_message(state))
            print("=" * 40)
            break

        advance_turn(state)

    print("\nプレイありがとうございました。")


if __name__ == "__main__":
    main()