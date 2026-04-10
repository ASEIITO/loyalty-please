from __future__ import annotations

from typing import Any, Dict, Tuple


GameState = Dict[str, Any]


def create_initial_state(max_turns: int = 10) -> GameState:
    """ゲームの初期状態を作る。"""
    return {
        "turn": 1,
        "max_turns": max_turns,
        "resources": 50,
        "loyalty": 45,
        "public_anger": 50,
        "coup_risk": 30,
        "riot_active": False,
        "coup_attempt": False,
        "private_goods_score": 0,
        "public_goods_score": 0,
        "repression_score": 0,
        "history": [],
        "game_over": False,
        "ending_reason": None,
    }


def clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    """値を指定範囲内に収める。"""
    return max(minimum, min(maximum, value))


def apply_choice(state: GameState, choice: Dict[str, Any]) -> None:
    """選択肢の効果を状態に反映する。"""
    effects = choice.get("effects", {})

    for key, delta in effects.items():
        if key not in state:
            continue
        state[key] += delta

    state["resources"] = clamp(state["resources"])
    state["loyalty"] = clamp(state["loyalty"])
    state["public_anger"] = clamp(state["public_anger"])
    state["coup_risk"] = clamp(state["coup_risk"])

    update_governance_scores(state, choice, effects)


def update_governance_scores(
    state: GameState,
    choice: Dict[str, Any],
    effects: Dict[str, int],
) -> None:
    """プレイスタイル診断用スコアを更新する。"""
    loyalty_delta = effects.get("loyalty", 0)
    anger_delta = effects.get("public_anger", 0)
    label = choice.get("label", "")

    if loyalty_delta > 0:
        state["private_goods_score"] += loyalty_delta

    if anger_delta < 0:
        state["public_goods_score"] += abs(anger_delta)

    if "抑え込" in label or "治安" in label or "弾圧" in label:
        state["repression_score"] += 1


def record_history(
    state: GameState,
    event: Dict[str, Any],
    choice: Dict[str, Any],
    before: Dict[str, int],
) -> None:
    """各ターンの選択と変化量を履歴に保存する。"""
    entry = {
        "turn": state["turn"],
        "event_title": event["title"],
        "choice_label": choice["label"],
        "feedback": choice["feedback"],
        "before": before,
        "after": {
            "resources": state["resources"],
            "loyalty": state["loyalty"],
            "public_anger": state["public_anger"],
            "coup_risk": state["coup_risk"],
        },
        "delta": {
            "resources": state["resources"] - before["resources"],
            "loyalty": state["loyalty"] - before["loyalty"],
            "public_anger": state["public_anger"] - before["public_anger"],
            "coup_risk": state["coup_risk"] - before["coup_risk"],
        },
    }
    state["history"].append(entry)


def check_game_over(state: GameState) -> Tuple[bool, str | None]:
    """敗北条件を判定する。"""
    if state["loyalty"] <= 0:
        return True, "側近が離反し、政権は内部から崩壊しました。"

    if state["resources"] <= 0:
        return True, "財政が破綻し、政権運営が不可能になりました。"

    if state["public_anger"] >= 100:
        return True, "大規模な民衆蜂起により政権が崩壊しました。"
    elif state["public_anger"] >= 60:
        state["riot_active"] = True
    else:
        state["riot_active"] = False

    if state["coup_risk"] >= 100:
        return True, "軍部によるクーデターが成功しました。"
    elif state["coup_risk"] >= 60:
        state["coup_attempt"] = True
    else:
        state["coup_attempt"] = False

    return False, None


def advance_turn(state: GameState) -> None:
    """ターンを進め、体制に自然な劣化圧力をかける。"""
    state["turn"] += 1

    state["public_anger"] = clamp(state["public_anger"] + 2)

    coup_drift = 1
    if state["loyalty"] < 40:
        coup_drift += 3
    if state["loyalty"] < 25:
        coup_drift += 5

    state["coup_risk"] = clamp(state["coup_risk"] + coup_drift)

    if state["riot_active"]:
        state["resources"] = clamp(state["resources"] - 5)
        state["loyalty"] = clamp(state["loyalty"] - 3)

    if state["coup_attempt"]:
        state["loyalty"] = clamp(state["loyalty"] - 5)
        state["coup_risk"] = clamp(state["coup_risk"] + 5)


def get_governance_type(state: GameState) -> str:
    """ざっくりした統治タイプを返す。"""
    private_score = state["private_goods_score"]
    public_score = state["public_goods_score"]
    repression_score = state["repression_score"]

    if repression_score >= 3 and repression_score > private_score / 10:
        return "弾圧依存型"
    if private_score > public_score + 10:
        return "支持層優遇型"
    if public_score > private_score + 10:
        return "公共財重視型"
    return "均衡型"


def identify_failure_type(state: GameState) -> str:
    """敗北の主因を分類する。"""
    reason = state["ending_reason"] or ""

    if "クーデター" in reason:
        return "クーデター型崩壊"
    if "蜂起" in reason:
        return "民衆革命型崩壊"
    if "財政" in reason:
        return "財政崩壊型"
    if "離反" in reason:
        return "支持連合崩壊型"
    return "生存"


def build_analysis(state: GameState) -> str:
    """終了時の詳細分析を作る。"""
    governance_type = get_governance_type(state)
    failure_type = identify_failure_type(state)

    lines = []

    if state["ending_reason"] is None:
        lines.append(f"あなたは {state['max_turns']} ターン政権を維持しました。")
        lines.append(f"統治タイプ: {governance_type}")
        lines.append("")
        lines.append("分析:")
        lines.append("支持層・民衆・財政の3つを完全には満たせない中で、一定の均衡を保てました。")
    else:
        lines.append(f"ゲームオーバー: {state['ending_reason']}")
        lines.append(f"崩壊の型: {failure_type}")
        lines.append(f"統治タイプ: {governance_type}")
        lines.append("")
        lines.append("分析:")

        if failure_type == "クーデター型崩壊":
            lines.append("支持連合、とくに軍や側近の忠誠維持に失敗しました。")
            lines.append("私的利益の配分不足、または忠誠低下の放置が崩壊につながりました。")
        elif failure_type == "民衆革命型崩壊":
            lines.append("公共財の不足や強権的対応の積み重ねで、民衆不満が限界を超えました。")
            lines.append("支持層を優遇できても、非支持層の圧力を無視し続けると体制は不安定化します。")
        elif failure_type == "財政崩壊型":
            lines.append("支持層維持や危機対応のコストが重なり、国家資源が枯渇しました。")
            lines.append("配分政治は資源があってこそ機能することがわかります。")
        elif failure_type == "支持連合崩壊型":
            lines.append("中核支持層が政権維持の利益を見いだせなくなりました。")
            lines.append("独裁体制では、広い民意より先に近い支持者の離反が致命傷になります。")

    lines.append("")
    lines.append("最終状態:")
    lines.append(f"- 国家資源: {state['resources']}")
    lines.append(f"- 忠誠度: {state['loyalty']}")
    lines.append(f"- 民衆不満: {state['public_anger']}")
    lines.append(f"- クーデターリスク: {state['coup_risk']}")

    if state["history"]:
        total_loyalty = sum(entry["delta"]["loyalty"] for entry in state["history"])
        total_anger = sum(entry["delta"]["public_anger"] for entry in state["history"])
        total_resources = sum(entry["delta"]["resources"] for entry in state["history"])
        total_coup = sum(entry["delta"]["coup_risk"] for entry in state["history"])

        lines.append("")
        lines.append("プレイ集計:")
        lines.append(f"- 忠誠度の累積変化: {total_loyalty:+}")
        lines.append(f"- 民衆不満の累積変化: {total_anger:+}")
        lines.append(f"- 国家資源の累積変化: {total_resources:+}")
        lines.append(f"- クーデターリスクの累積変化: {total_coup:+}")

    return "\n".join(lines)


def build_end_message(state: GameState) -> str:
    """終了時メッセージを返す。"""
    return build_analysis(state)
