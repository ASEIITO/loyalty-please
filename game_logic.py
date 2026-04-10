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


def build_end_message(state: dict) -> str:
    """強化版終了分析（教育用）"""

    resources = state["resources"]
    loyalty = state["loyalty"]
    anger = state["public_anger"]
    coup = state["coup_risk"]
    reason = state.get("ending_reason", None)

    lines = []

    # タイトル
    lines.append("=== 政権分析レポート ===\n")

    # 生存結果
    if reason:
        lines.append("あなたの政権は崩壊しました。\n")
    else:
        lines.append("あなたは任期を全うしました。\n")

    # 崩壊理由
    if reason:
        lines.append("■ 崩壊の直接原因")
        if reason == "coup":
            lines.append("・軍・支持層によるクーデター")
        elif reason == "riot":
            lines.append("・民衆の暴動・革命")
        elif reason == "economy":
            lines.append("・財政破綻")
        elif reason == "loyalty":
            lines.append("・支持層の離反")
        lines.append("")

    # 状態評価
    lines.append("■ 最終状態")
    lines.append(f"・国家資源: {resources}")
    lines.append(f"・忠誠度: {loyalty}")
    lines.append(f"・民衆不満: {anger}")
    lines.append(f"・クーデターリスク: {coup}\n")

    # プレイスタイル分析（コア）
    lines.append("■ 統治スタイル分析")

    if loyalty > 70 and anger > 70:
        style = "抑圧的配分型（強権政治）"
        explanation = "支持層への私的利益配分を優先し、民衆の不満を抑圧する戦略です。"
    elif anger < 40 and loyalty < 40:
        style = "公共財重視型（ポピュリズム）"
        explanation = "広い層への配分を重視しましたが、支持層の忠誠が弱まりました。"
    elif loyalty > 60 and anger < 60:
        style = "バランス型"
        explanation = "支持層と民衆の両方に配慮した安定志向の統治です。"
    elif loyalty < 30:
        style = "支持層軽視型"
        explanation = "支持層への配分が不足し、政権の基盤が弱体化しました。"
    elif anger > 80:
        style = "民衆軽視型"
        explanation = "民衆の不満が極度に蓄積しました。"
    else:
        style = "不安定型"
        explanation = "一貫した戦略が見られず、各指標が不安定でした。"

    lines.append(f"・{style}")
    lines.append(f"　{explanation}\n")

    # 理論接続（ここが教育的に重要）
    lines.append("■ 理論的解釈（セレクトレート理論）")

    lines.append(
        "このゲームでは、指導者は限られた資源を\n"
        "「支持層（勝利連合）」と「一般市民」に配分する必要があります。"
    )

    lines.append("")

    if loyalty < 40:
        lines.append("・支持層への配分不足 → クーデターのリスク増大")
    if anger > 70:
        lines.append("・公共財不足 → 民衆不満の増大 → 暴動リスク増加")
    if resources < 30:
        lines.append("・資源不足 → 配分能力の低下 → 全体的不安定化")

    lines.append("")

    lines.append(
        "独裁者は合理的に、少数の支持層に集中して資源を配分する傾向があります。\n"
        "しかし、それは民衆の不満を高め、別の不安定要因を生み出します。"
    )

    # 改善アドバイス
    lines.append("\n■ 改善のヒント")

    if reason == "coup":
        lines.append("・支持層（軍・エリート）への配分を増やす必要があります")
    if reason == "riot":
        lines.append("・民衆向けの公共財支出を増やす必要があります")
    if resources < 20:
        lines.append("・財政を維持するため、支出配分の見直しが必要です")

    if not reason:
        lines.append("・安定したバランスを維持できていますが、長期的にはさらなる最適化が可能です")

    return "\n".join(lines)
