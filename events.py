from __future__ import annotations

EVENTS = [

    # =========================
    # 通常イベント
    # =========================

    {
        "id": "military_budget",
        "title": "軍部の追加予算要求",
        "tags": ["military", "elite", "coup"],
        "description": "将軍たちは国境警備の強化を理由に、特別手当を求めている。",
        "choices": [
            {
                "label": "全額支給する",
                "effects": {
                    "resources": -20,
                    "loyalty": 12,
                    "coup_risk": -10,
                    "public_anger": 8,
                },
                "feedback": "支持層への私的利益配分により忠誠は強化されるが、民衆の不満は高まる。",
            },
            {
                "label": "一部だけ認める",
                "effects": {
                    "resources": -10,
                    "loyalty": 2,
                    "coup_risk": -3,
                },
                "feedback": "支持層と財政の間で妥協した対応。",
            },
            {
                "label": "拒否する",
                "effects": {
                    "loyalty": -10,
                    "coup_risk": 15,
                },
                "feedback": "支持連合の不満が蓄積し、クーデターの危険が高まる。",
            },
        ],
    },

    {
        "id": "food_prices",
        "title": "食料価格の高騰",
        "tags": ["public", "economy", "riot"],
        "description": "都市部で食料価格が急騰し、市民の不満が広がっている。",
        "choices": [
            {
                "label": "補助金を出す",
                "effects": {
                    "resources": -12,
                    "public_anger": -15,
                },
                "feedback": "公共財支出により民衆不満を抑制するが、財政負担が増す。",
            },
            {
                "label": "市場に任せる",
                "effects": {
                    "public_anger": 8,
                },
                "feedback": "財政は守られるが、民衆不満は増大する。",
            },
            {
                "label": "治安部隊で抑え込む",
                "effects": {
                    "resources": -5,
                    "public_anger": 10,
                    "loyalty": 3,
                    "coup_risk": -2,
                },
                "feedback": "強権的対応により短期的安定を得るが、長期的には不満を蓄積させる。",
            },
        ],
    },

    {
        "id": "corruption_scandal",
        "title": "側近の汚職発覚",
        "tags": ["elite", "politics"],
        "description": "有力な側近の横領が報道された。",
        "choices": [
            {
                "label": "厳しく処罰する",
                "effects": {
                    "loyalty": -10,
                    "public_anger": -8,
                },
                "feedback": "正統性は向上するが、支持層の不安を招く。",
            },
            {
                "label": "内密に済ませる",
                "effects": {
                    "loyalty": 5,
                    "public_anger": 15,
                },
                "feedback": "支持層の結束は維持されるが、民衆の怒りは増す。",
            },
            {
                "label": "軽い処分にする",
                "effects": {
                    "loyalty": -5,
                    "public_anger": 5,
                },
                "feedback": "両者に中途半端な影響を与える。",
            },
        ],
    },

    {
        "id": "education_budget",
        "title": "教育予算の提案",
        "tags": ["public", "policy"],
        "description": "教育投資の拡大が提案されている。",
        "choices": [
            {
                "label": "拡充する",
                "effects": {
                    "resources": -10,
                    "public_anger": -10,
                    "loyalty": -3,
                },
                "feedback": "公共財により民衆支持は向上するが、支持層の直接利益は減少。",
            },
            {
                "label": "現状維持",
                "effects": {
                    "public_anger": 5,
                },
                "feedback": "問題を先送りする。",
            },
            {
                "label": "削減する",
                "effects": {
                    "resources": 5,
                    "public_anger": 8,
                    "loyalty": 2,
                },
                "feedback": "財政と支持層を優先するが、民衆不満が増加。",
            },
        ],
    },

    {
        "id": "electoral_reform",
        "title": "限定的選挙制度改革",
        "tags": ["public", "reform"],
        "description": "一部地域で選挙導入案が浮上。",
        "choices": [
            {
                "label": "導入する",
                "effects": {
                    "public_anger": -8,
                    "loyalty": -10,
                    "coup_risk": 8,
                },
                "feedback": "セレクター拡大により民衆満足は上がるが、支持層は不安定化。",
            },
            {
                "label": "検討だけする",
                "effects": {
                    "public_anger": -1,
                },
                "feedback": "象徴的譲歩。",
            },
            {
                "label": "拒否する",
                "effects": {
                    "loyalty": 3,
                    "public_anger": 9,
                },
                "feedback": "支持層は安心するが、民衆は反発。",
            },
        ],
    },

    # =========================
    # 危機イベント
    # =========================

    {
        "id": "barracks_unrest",
        "title": "兵舎で不穏な動き",
        "tags": ["military", "coup", "crisis"],
        "description": "軍内部で反政府的な動きが報告された。",
        "choices": [
            {
                "label": "資金で懐柔する",
                "effects": {
                    "resources": -12,
                    "loyalty": 10,
                    "coup_risk": -8,
                    "public_anger": 4,
                },
                "feedback": "私的利益でクーデターを回避。",
            },
            {
                "label": "粛清する",
                "effects": {
                    "loyalty": -5,
                    "coup_risk": -3,
                    "public_anger": 6,
                },
                "feedback": "恐怖による統治。",
            },
            {
                "label": "放置する",
                "effects": {
                    "coup_risk": 12,
                    "loyalty": -8,
                },
                "feedback": "クーデターの危険が急上昇。",
            },
        ],
    },

    {
        "id": "urban_protest",
        "title": "大規模デモ",
        "tags": ["public", "riot", "crisis"],
        "description": "首都で抗議活動が拡大。",
        "choices": [
            {
                "label": "補助金を拡大",
                "effects": {
                    "resources": -10,
                    "public_anger": -12,
                },
                "feedback": "公共財で沈静化。",
            },
            {
                "label": "武力で鎮圧",
                "effects": {
                    "resources": -4,
                    "public_anger": 6,
                    "loyalty": 3,
                },
                "feedback": "短期安定、長期不安。",
            },
            {
                "label": "無視する",
                "effects": {
                    "public_anger": 8,
                },
                "feedback": "暴動の拡大。",
            },
        ],
    },

    {
        "id": "reserve_crisis",
        "title": "外貨準備の急減",
        "tags": ["economy", "crisis"],
        "description": "国家財政が不安定化している。",
        "choices": [
            {
                "label": "緊縮財政",
                "effects": {
                    "resources": 8,
                    "public_anger": 8,
                },
                "feedback": "財政改善と引き換えに不満増加。",
            },
            {
                "label": "援助を受ける",
                "effects": {
                    "resources": 12,
                    "loyalty": -4,
                },
                "feedback": "資源増加と支持層不安。",
            },
            {
                "label": "支持層維持",
                "effects": {
                    "resources": -10,
                    "loyalty": 4,
                    "public_anger": 5,
                },
                "feedback": "支持層優先で財政悪化。",
            },
        ],
    },
]
