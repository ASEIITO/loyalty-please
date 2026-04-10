from __future__ import annotations

EVENTS = [
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
                "feedback": "勝利連合への私的利益の配分です。忠誠を高めますが、民衆には不公平に映ります。",
            },
            {
                "label": "一部だけ認める",
                "effects": {
                    "resources": -10,
                    "loyalty": 2,
                    "coup_risk": -3,
                },
                "feedback": "妥協的な対応です。支持層の不満を抑えつつ、資源流出もある程度抑えます。",
            },
            {
                "label": "拒否する",
                "effects": {
                    "loyalty": -10,
                    "coup_risk": 15,
                },
                "feedback": "支持連合への配分を拒むと、政権中枢の離反リスクが高まります。",
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
                "feedback": "公共財的な支出です。広い層の不満を下げますが、資源を消費します。",
            },
            {
                "label": "市場に任せる",
                "effects": {
                    "public_anger": 12,
                },
                "feedback": "財政負担は避けられますが、市民の不満は強まります。",
            },
            {
                "label": "治安部隊で抑え込む",
                "effects": {
                    "resources": -5,
                    "public_anger": 10,
                    "loyalty": 3,
                    "coup_risk": -2,
                },
                "feedback": "強権的対応です。中核支持層には好まれやすい一方、市民不満は長期的に高まりがちです。",
            },
        ],
    },
    {
        "id": "corruption_scandal",
        "title": "側近の汚職発覚",
        "tags": ["elite", "politics"],
        "description": "有力な側近の横領が報道された。処分を求める声が上がっている。",
        "choices": [
            {
                "label": "厳しく処罰する",
                "effects": {
                    "loyalty": -10,
                    "public_anger": -8,
                },
                "feedback": "正統性は高まりますが、支持連合には『見捨てられるかもしれない』という不安が広がります。",
            },
            {
                "label": "内密に済ませる",
                "effects": {
                    "loyalty": 5,
                    "public_anger": 15,
                },
                "feedback": "支持連合の結束は維持されますが、民衆の不満は強まります。",
            },
            {
                "label": "軽い処分にする",
                "effects": {
                    "loyalty": -5,
                    "public_anger": 5,
                },
                "feedback": "中間的対応です。どちらの反発もある程度に抑えます。",
            },
        ],
    },
    {
        "id": "education_budget",
        "title": "教育予算の提案",
        "tags": ["public", "budget", "policy"],
        "description": "官僚が教育予算の増額を提案している。長期的な経済効果が期待される。",
        "choices": [
            {
                "label": "拡充する",
                "effects": {
                    "resources": -10,
                    "public_anger": -10,
                    "loyalty": -3,
                },
                "feedback": "公共財への支出は広い層に利益をもたらしますが、支持層への直接配分は薄まります。",
            },
            {
                "label": "現状維持する",
                "effects": {"public_anger": 5},
                "feedback": "大きな変化を避ける選択です。短期的には安全ですが、問題も解決しません。",
            },
            {
                "label": "削減する",
                "effects": {
                    "resources": 5,
                    "public_anger": 8,
                    "loyalty": 2,
                },
                "feedback": "資源を節約し支持層向け配分の余地を残しますが、市民の不満を高めます。",
            },
        ],
    },
    {
        "id": "electoral_reform",
        "title": "限定的な選挙制度改革案",
        "tags": ["public", "politics", "reform"],
        "description": "一部の地方で限定選挙を導入する案が持ち上がっている。",
        "choices": [
            {
                "label": "地方選挙を一部導入する",
                "effects": {
                    "public_anger": -8,
                    "loyalty": -10,
                    "coup_risk": 8,
                },
                "feedback": "セレクターを広げる方向です。市民の不満は下がりますが、既得権を持つ支持層は不安定になります。",
            },
            {
                "label": "検討すると発表だけする",
                "effects": {
                    "public_anger": -1,
                },
                "feedback": "象徴的な譲歩です。短期的には不満を少し和らげます。",
            },
            {
                "label": "拒否する",
                "effects": {
                    "loyalty": 3,
                    "public_anger": 9,
                },
                "feedback": "支持層には安心材料ですが、民衆には閉鎖的に映ります。",
            },
        ],
    },
    {
        "id": "foreign_aid",
        "title": "外国からの援助提案",
        "tags": ["budget", "economy", "foreign"],
        "description": "外国政府が経済援助を申し出てきた。ただし政治改革を条件としている。",
        "choices": [
            {
                "label": "条件付きで受け入れる",
                "effects": {
                    "resources": 20,
                    "public_anger": -5,
                    "loyalty": -5,
                },
                "feedback": "外部資源は増えますが、支持層には体制変化の兆候として警戒されます。",
            },
            {
                "label": "無条件の支援だけ求める",
                "effects": {
                    "resources": 5,
                },
                "feedback": "限定的な利益は得られますが、大きな改革も資源流入も起きません。",
            },
            {
                "label": "拒否する",
                "effects": {
                    "loyalty": 3,
                    "public_anger": 5,
                },
                "feedback": "支持層には主権維持として好まれますが、市民には機会損失に見えるかもしれません。",
            },
        ],
    },

    # ここから危機専用イベントを追記
    {
        "id": "barracks_unrest",
        "title": "兵舎で不穏な動き",
        "tags": ["military", "elite", "coup", "crisis"],
        "description": "軍内部で将軍たちの秘密会合が行われているとの報告が入った。",
        "choices": [
            {
                "label": "特別手当を支給する",
                "effects": {
                    "resources": -12,
                    "loyalty": 10,
                    "coup_risk": -8,
                    "public_anger": 4,
                },
                "feedback": "軍への私的利益配分で当面の離反を防ぎます。",
            },
            {
                "label": "首謀者を粛清する",
                "effects": {
                    "loyalty": -5,
                    "coup_risk": -3,
                    "public_anger": 6,
                },
                "feedback": "強硬策で反対派を抑え込みますが、恐怖政治は別の不満も生みます。",
            },
            {
                "label": "静観する",
                "effects": {
                    "coup_risk": 12,
                    "loyalty": -8,
                },
                "feedback": "軍内の不満を放置すると、クーデターの危険が高まります。",
            },
        ],
    },
    {
        "id": "urban_protest",
        "title": "都市で大規模デモ",
        "tags": ["public", "riot", "repression", "crisis"],
        "description": "首都で生活苦に抗議する大規模デモが発生した。",
        "choices": [
            {
                "label": "食料補助を拡大する",
                "effects": {
                    "resources": -10,
                    "public_anger": -12,
                },
                "feedback": "公共財的支出で不満を抑えます。",
            },
            {
                "label": "治安部隊で解散させる",
                "effects": {
                    "resources": -4,
                    "public_anger": 6,
                    "loyalty": 3,
                    "coup_risk": -1,
                },
                "feedback": "短期的には秩序を回復できますが、民衆不満は悪化しやすいです。",
            },
            {
                "label": "要求を無視する",
                "effects": {
                    "public_anger": 14,
                },
                "feedback": "無視は体制への敵意を急速に高めます。",
            },
        ],
    },
    {
        "id": "reserve_crisis",
        "title": "外貨準備の急減",
        "tags": ["budget", "economy", "foreign", "crisis"],
        "description": "輸入価格の上昇で外貨準備が急減し、財政運営が不安定になっている。",
        "choices": [
            {
                "label": "緊縮財政を行う",
                "effects": {
                    "resources": 8,
                    "public_anger": 8,
                    "loyalty": -2,
                },
                "feedback": "財政は改善しますが、広い層に負担が及びます。",
            },
            {
                "label": "外国援助を求める",
                "effects": {
                    "resources": 12,
                    "loyalty": -4,
                },
                "feedback": "資源は増えますが、支持層には体制の弱さと映ります。",
            },
            {
                "label": "支持層向け配分を維持する",
                "effects": {
                    "resources": -10,
                    "loyalty": 4,
                    "public_anger": 5,
                },
                "feedback": "支持連合は維持できますが、財政危機を深めます。",
            },
        ],
    },
]