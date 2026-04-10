from __future__ import annotations

from typing import Any, Dict, Tuple
import random

SCENARIOS = [
    {
        "id": "control_state",
        "name": "統制国家",
        "description": "強固な統治体制を持つが、民衆の自由は制限されている。",
        "initial_state": {
            "resources": 60,
            "loyalty": 70,
            "public_anger": 50,
            "coup_risk": 20,
        },
    },
    {
        "id": "resource_state",
        "name": "資源依存国家",
        "description": "資源収入に依存。財政は豊かだが政治は不安定。",
        "initial_state": {
            "resources": 90,
            "loyalty": 40,
            "public_anger": 40,
            "coup_risk": 40,
        },
    },
    {
        "id": "fragile_state",
        "name": "不安定な国家",
        "description": "政権基盤が弱く、暴動とクーデターの危険が高い。",
        "initial_state": {
            "resources": 50,
            "loyalty": 30,
            "public_anger": 70,
            "coup_risk": 50,
        },
    },
]

GameState = Dict[str, Any]


def create_initial_state(max_turns: int = 10, scenario_id: str | None = None) -> GameState:
    """シナリオ付き初期状態"""

    if scenario_id is None or scenario_id == "random":
        scenario = random.choice(SCENARIOS)
    else:
        scenario = next(s for s in SCENARIOS if s["id"] == scenario_id)

    state = {
        "turn": 1,
        "max_turns": max_turns,
        "resources": 50,
        "loyalty": 45,
        "public_anger": 30,
        "coup_risk": 30,
        "riot_active": False,
        "coup_attempt": False,
        "private_goods_score": 0,
        "public_goods_score": 0,
        "repression_score": 0,
        "history": [],
        "pending_events": [],
        "chain_notes": [],
        "game_over": False,
        "ending_reason": None,

        # ▼ 追加
        "scenario_name": scenario["name"],
        "scenario_description": scenario["description"],
    }

    state.update(scenario["initial_state"])
    return state


def clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, value))


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

    if "抑え込" in label or "治安" in label or "弾圧" in label or "粛清" in label or "武力" in label:
        state["repression_score"] += 1


def queue_event_chain(state: GameState, event: Dict[str, Any], choice: Dict[str, Any]) -> None:
    """選択内容に応じて次ターン以降の危機イベントを予約する。"""
    event_id = event["id"]
    choice_label = choice["label"]

    def add_pending(event_id_to_add: str, note: str) -> None:
        if event_id_to_add not in state["pending_events"]:
            state["pending_events"].append(event_id_to_add)
            state["chain_notes"].append(note)

    # 軍部冷遇 → 兵舎不穏
    if event_id == "military_budget" and choice_label == "拒否する":
        add_pending(
            "barracks_unrest",
            "軍部要求の拒否により、兵舎で不穏な動きが広がった。"
        )

    # 食料問題を放置・弾圧 → 大規模デモ
    if event_id == "food_prices" and choice_label in ["市場に任せる", "治安部隊で抑え込む"]:
        add_pending(
            "urban_protest",
            "生活苦への不満が蓄積し、首都で抗議活動が拡大した。"
        )

    # 選挙改革を拒否 → 抗議運動
    if event_id == "electoral_reform" and choice_label == "拒否する":
        add_pending(
            "urban_protest",
            "制度改革の拒否が反体制デモを刺激した。"
        )

    # 資源を大きく減らす、あるいは支持層優先の財政対応 → 外貨危機
    if event_id in ["military_budget", "foreign_aid", "reserve_crisis"]:
        if choice_label in ["全額支給する", "支持層向け配分を維持する"]:
            add_pending(
                "reserve_crisis",
                "支持層への高コスト配分が財政を圧迫した。"
            )

    # 都市デモを武力鎮圧・無視 → さらに不満固定化
    if event_id == "urban_protest" and choice_label in ["武力で鎮圧", "無視する"]:
        add_pending(
            "urban_protest",
            "デモ対応の失敗により、抗議運動は収束しなかった。"
        )

    # 汚職隠蔽 → 民衆不満由来の危機
    if event_id == "corruption_scandal" and choice_label == "内密に済ませる":
        add_pending(
            "urban_protest",
            "汚職隠蔽が政権への怒りを強めた。"
        )


def apply_choice(state: GameState, event: Dict[str, Any], choice: Dict[str, Any]) -> None:
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
    queue_event_chain(state, event, choice)


def record_history(
    state: GameState,
    event: Dict[str, Any],
    choice: Dict[str, Any],
    before: Dict[str, int],
) -> None:
    """各ターンの選択と変化量を履歴に保存する。"""
    entry = {
        "turn": state["turn"],
        "event_id": event["id"],
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
    elif state["public_anger"] >= 80:
        state["riot_active"] = True
    else:
        state["riot_active"] = False

    if state["coup_risk"] >= 100:
        return True, "軍部によるクーデターが成功しました。"
    elif state["coup_risk"] >= 80:
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


def get_governance_type(state: dict) -> str:
    """プレイ履歴から統治スタイルを返す。"""
    private_score = state.get("private_goods_score", 0)
    public_score = state.get("public_goods_score", 0)
    repression_score = state.get("repression_score", 0)

    if repression_score >= 3 and repression_score > private_score / 10:
        return "弾圧依存型"
    if private_score > public_score + 10:
        return "支持層優遇型"
    if public_score > private_score + 10:
        return "公共財重視型"
    return "均衡型"


def identify_failure_type(state: dict) -> str:
    """敗北の主因を分類する。"""
    reason = state.get("ending_reason") or ""

    if "クーデター" in reason:
        return "クーデター型崩壊"
    if "蜂起" in reason or "暴動" in reason:
        return "民衆革命型崩壊"
    if "財政" in reason:
        return "財政崩壊型"
    if "離反" in reason:
        return "支持連合崩壊型"
    return "生存"


def build_end_message(state: dict) -> str:
    """授業用の強化版終了分析を返す。"""
    lines.append(f"■ シナリオ: {state.get('scenario_name')}")
    lines.append(f"{state.get('scenario_description')}\n")
    governance_type = get_governance_type(state)
    failure_type = identify_failure_type(state)

    resources = state["resources"]
    loyalty = state["loyalty"]
    public_anger = state["public_anger"]
    coup_risk = state["coup_risk"]
    ending_reason = state.get("ending_reason")

    lines = []

    lines.append("=== 政権分析レポート ===")
    lines.append("")

    if ending_reason is None:
        lines.append(f"あなたは {state['max_turns']} ターン政権を維持しました。")
        lines.append("結果: 政権維持")
    else:
        lines.append("あなたの政権は崩壊しました。")
        lines.append(f"結果: {failure_type}")
        lines.append(f"直接原因: {ending_reason}")

    lines.append("")
    lines.append("■ 最終状態")
    lines.append(f"・国家資源: {resources}")
    lines.append(f"・忠誠度: {loyalty}")
    lines.append(f"・民衆不満: {public_anger}")
    lines.append(f"・クーデターリスク: {coup_risk}")

    lines.append("")
    lines.append("■ 統治スタイル分析")
    lines.append(f"・分類: {governance_type}")

    if governance_type == "支持層優遇型":
        lines.append("・支持層への私的利益配分を優先した統治でした。")
        lines.append("・短期的には忠誠維持に役立ちますが、民衆不満と財政悪化を招きやすくなります。")
    elif governance_type == "公共財重視型":
        lines.append("・民衆不満を抑える公共財支出を重視した統治でした。")
        lines.append("・広い層には利益がありますが、支持連合への直接的見返りが弱くなります。")
    elif governance_type == "弾圧依存型":
        lines.append("・治安部隊や強硬策に依存する統治でした。")
        lines.append("・短期的には秩序を回復できますが、長期的には不満の蓄積を招きやすいです。")
    else:
        lines.append("・支持層・民衆・財政のあいだで均衡を取ろうとする統治でした。")
        lines.append("・一貫した危機管理ができれば安定しやすい一方、中途半端になると各方面の不満を招きます。")

    lines.append("")
    lines.append("■ 理論的解釈（セレクトレート理論）")
    lines.append("・独裁者は限られた資源を、支持層（勝利連合）と一般市民に配分しなければなりません。")
    lines.append("・支持層への私的利益は忠誠を高めますが、公共財の不足は民衆不満を高めます。")
    lines.append("・そのため、政権維持は常に『支持層の離反』と『民衆の反乱』のあいだの綱渡りになります。")

    if loyalty < 40:
        lines.append("・今回のプレイでは、支持層への配分不足または忠誠低下が大きな不安定要因になりました。")
    if public_anger >= 70:
        lines.append("・公共財不足または強権的対応の蓄積により、民衆不満が危険水準まで上昇しました。")
    if resources < 30:
        lines.append("・資源不足のため、支持層にも民衆にも十分な配分ができず、体制全体が不安定化しました。")
    if coup_risk >= 80:
        lines.append("・クーデター危機が深刻化しており、政権中枢の維持に失敗していました。")

    if state.get("history"):
        total_loyalty = sum(entry["delta"]["loyalty"] for entry in state["history"])
        total_anger = sum(entry["delta"]["public_anger"] for entry in state["history"])
        total_resources = sum(entry["delta"]["resources"] for entry in state["history"])
        total_coup = sum(entry["delta"]["coup_risk"] for entry in state["history"])

        lines.append("")
        lines.append("■ プレイ集計")
        lines.append(f"・忠誠度の累積変化: {total_loyalty:+}")
        lines.append(f"・民衆不満の累積変化: {total_anger:+}")
        lines.append(f"・国家資源の累積変化: {total_resources:+}")
        lines.append(f"・クーデターリスクの累積変化: {total_coup:+}")

        worst_anger_turn = max(state["history"], key=lambda x: x["delta"]["public_anger"])
        worst_coup_turn = max(state["history"], key=lambda x: x["delta"]["coup_risk"])
        best_loyalty_turn = max(state["history"], key=lambda x: x["delta"]["loyalty"])

        lines.append("")
        lines.append("■ 重要だった意思決定")
        lines.append(
            f"・民衆不満を最も増やした判断: Turn {worst_anger_turn['turn']} "
            f"「{worst_anger_turn['event_title']}」→「{worst_anger_turn['choice_label']}」"
        )
        lines.append(
            f"・クーデター危機を最も高めた判断: Turn {worst_coup_turn['turn']} "
            f"「{worst_coup_turn['event_title']}」→「{worst_coup_turn['choice_label']}」"
        )
        lines.append(
            f"・忠誠を最も高めた判断: Turn {best_loyalty_turn['turn']} "
            f"「{best_loyalty_turn['event_title']}」→「{best_loyalty_turn['choice_label']}」"
        )

    if state.get("chain_notes"):
        lines.append("")
        lines.append("■ 危機の連鎖")
        unique_notes = []
        for note in state["chain_notes"]:
            if note not in unique_notes:
                unique_notes.append(note)
        for note in unique_notes[:5]:
            lines.append(f"・{note}")

    lines.append("")
    lines.append("■ 改善のヒント")

    if failure_type == "クーデター型崩壊":
        lines.append("・軍部や支持層への配分をもう少し重視すると、政権中枢の安定化につながります。")
    elif failure_type == "民衆革命型崩壊":
        lines.append("・公共財支出や譲歩を増やし、民衆不満の蓄積を抑える必要があります。")
    elif failure_type == "財政崩壊型":
        lines.append("・危機対応のたびに資源を使いすぎないよう、長期的な財政維持を意識する必要があります。")
    elif failure_type == "支持連合崩壊型":
        lines.append("・独裁体制では、広い民衆より先に近い支持層の離反が致命傷になります。")
    else:
        lines.append("・異なる戦略でもう一度プレイし、どの危機が増幅されるか比較してみてください。")

    return "\n".join(lines)
