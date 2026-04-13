from __future__ import annotations

EVENTS = [

    # =========================
    # 通常イベント
    # =========================

    {
        "id": "military_budget",
        "title": "軍部の追加予算要求",
        "tags": ["military", "elite", "coup"],
        "description": "将軍たちは国境警備の強化を理由に、特別手当を求めている。最近は隣国の軍備増強が盛んに報じられ、軍部は危機感を強めている。",
        "choices": [
            {
                "label": "全額支給する",
                "effects": {
                    "resources": -20,
                    "loyalty": 12,
                    "coup_risk": -10,
                    "public_anger": 5,
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
        "description": "都市部で食料価格が急騰し、市民の不満が広がっている。市場では政府の備蓄放出が遅れているとの批判も出ている。",
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
                    "public_anger": 3,
                },
                "feedback": "財政は守られるが、民衆不満は増大する。",
            },
            {
                "label": "治安部隊で抑え込む",
                "effects": {
                    "resources": -5,
                    "public_anger": 6,
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
        "description": "有力な側近の横領が報道された。野党系メディアは政権中枢の腐敗の象徴だと批判している。",
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
                    "public_anger": 10,
                },
                "feedback": "支持層の結束は維持されるが、民衆の怒りは増す。",
            },
            {
                "label": "軽い処分にする",
                "effects": {
                    "loyalty": -5,
                    "public_anger": 3,
                },
                "feedback": "両者に中途半端な影響を与える。",
            },
        ],
    },

    {
        "id": "education_budget",
        "title": "教育予算の提案",
        "tags": ["public", "policy"],
        "description": "教育投資の拡大が提案されている。官僚は長期的には労働生産性の改善につながると説明している。",
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
                    "public_anger": 3,
                     "loyalty": 2,
                },
                "feedback": "問題を先送りする。",
            },
            {
                "label": "削減する",
                "effects": {
                    "resources": 5,
                    "public_anger": 6,
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
        "description": "一部地域で選挙導入案が浮上。知識人層はこれを体制の柔軟性を示す試金石とみなしている。",
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
    # 追加通常イベント（理論別20個）
    # =========================

    {
        "id": "elite_bonus",
        "title": "軍幹部への特別報酬",
        "tags": ["elite", "military", "coup"],
        "description": "軍幹部が特別報酬を求めている。最近の作戦協力を理由に、政権への忠誠には見返りが必要だと主張している。",
        "choices": [
            {
                "label": "支給する",
                "effects": {"resources": -12, "loyalty": 10, "coup_risk": -6, "public_anger": 4},
                "feedback": "private goods によって支持層の結束を強化する。",
            },
            {
                "label": "一部支給する",
                "effects": {"resources": -6, "loyalty": 3, "coup_risk": -2},
                "feedback": "妥協によって一定の不満を抑える。",
            },
            {
                "label": "拒否する",
                "effects": {"loyalty": -8, "coup_risk": 10},
                "feedback": "支持層の見返り期待を裏切り、離反を招く。",
            },
        ],
    },

    {
        "id": "business_contract",
        "title": "政商への優遇契約",
        "tags": ["elite", "economy"],
        "description": "政権に近い実業家が独占契約を求めている。彼らは政権の選挙資金や治安協力の重要な提供者でもある。",
        "choices": [
            {
                "label": "独占契約を与える",
                "effects": {"resources": -8, "loyalty": 8, "public_anger": 6},
                "feedback": "支持層を優遇し、見返りとして体制維持資源を確保する。",
            },
            {
                "label": "限定的に認める",
                "effects": {"loyalty": 3, "public_anger": 2},
                "feedback": "利益配分を抑えつつ関係維持を図る。",
            },
            {
                "label": "公開入札にする",
                "effects": {"loyalty": -6, "public_anger": -3},
                "feedback": "正統性は上がるが、支持層の不満を買う。",
            },
        ],
    },

    {
        "id": "family_patronage",
        "title": "親族への官職配分",
        "tags": ["elite", "politics"],
        "description": "大統領の親族を高官に登用する案が浮上している。側近は血縁を使った統治のほうが裏切りを防げると進言している。",
        "choices": [
            {
                "label": "重要職に就ける",
                "effects": {"loyalty": 6, "coup_risk": -3, "public_anger": 5},
                "feedback": "身内統治で忠誠は固まるが、公正性への批判が増す。",
            },
            {
                "label": "形式的な職だけ与える",
                "effects": {"loyalty": 2, "public_anger": 2},
                "feedback": "限定的な縁故配置。",
            },
            {
                "label": "能力主義を優先する",
                "effects": {"loyalty": -4, "public_anger": -2},
                "feedback": "正統性は上がるが、身内ネットワークは不満を持つ。",
            },
        ],
    },

    {
        "id": "security_allowance",
        "title": "治安部隊の待遇改善要求",
        "tags": ["elite", "repression", "military"],
        "description": "治安部隊が危険手当の増額を求めている。彼らは最近の取り締まり強化で負担が増したと訴えている。",
        "choices": [
            {
                "label": "全面的に改善する",
                "effects": {"resources": -10, "loyalty": 8, "coup_risk": -4, "public_anger": 3},
                "feedback": "抑圧装置の忠誠を資源で買う。",
            },
            {
                "label": "一部だけ認める",
                "effects": {"resources": -5, "loyalty": 3},
                "feedback": "コストを抑えながら協力を維持する。",
            },
            {
                "label": "拒否する",
                "effects": {"loyalty": -7, "coup_risk": 6},
                "feedback": "抑圧機構の協力度が低下する。",
            },
        ],
    },

    {
        "id": "regional_bosses",
        "title": "地方有力者への資金配分",
        "tags": ["elite", "politics"],
        "description": "地方の有力者が中央からの資金配分を求めている。彼らは地域の票と治安を取りまとめる重要な仲介者である。",
        "choices": [
            {
                "label": "厚く配分する",
                "effects": {"resources": -11, "loyalty": 9, "public_anger": 3},
                "feedback": "仲介者を通じて支持連合を安定させる。",
            },
            {
                "label": "限定的に配る",
                "effects": {"resources": -5, "loyalty": 3},
                "feedback": "最低限の関係維持。",
            },
            {
                "label": "断る",
                "effects": {"loyalty": -6, "coup_risk": 5},
                "feedback": "地域支配の基盤が不安定になる。",
            },
        ],
    },

    {
        "id": "healthcare",
        "title": "医療制度の拡充",
        "tags": ["public", "policy"],
        "description": "医療サービス改善が求められている。地方では基礎医療の不足が慢性化し、不満の原因になっている。",
        "choices": [
            {
                "label": "拡充する",
                "effects": {"resources": -10, "public_anger": -12, "loyalty": -2},
                "feedback": "public goods により広範な支持を得る。",
            },
            {
                "label": "部分対応する",
                "effects": {"resources": -5, "public_anger": -4},
                "feedback": "負担を抑えつつ一定の不満を軽減する。",
            },
            {
                "label": "拒否する",
                "effects": {"public_anger": 8},
                "feedback": "財政を守るが、民衆不満は高まる。",
            },
        ],
    },

    {
        "id": "infrastructure",
        "title": "インフラ投資計画",
        "tags": ["public", "economy"],
        "description": "道路と電力網の老朽化が問題になっている。商工会は投資が成長と生活安定の両方に必要だと訴えている。",
        "choices": [
            {
                "label": "大規模投資を行う",
                "effects": {"resources": -14, "public_anger": -10, "loyalty": -3},
                "feedback": "広い層に利益をもたらす公共投資。",
            },
            {
                "label": "最低限の補修だけ行う",
                "effects": {"resources": -6, "public_anger": -3},
                "feedback": "限定的な改善。",
            },
            {
                "label": "先送りする",
                "effects": {"public_anger": 6},
                "feedback": "財政負担は避けられるが、不満が残る。",
            },
        ],
    },

    {
        "id": "unemployment_program",
        "title": "失業対策プログラム",
        "tags": ["public", "economy"],
        "description": "失業率の上昇により若年層の不満が高まっている。都市部では仕事不足が抗議運動の温床になりつつある。",
        "choices": [
            {
                "label": "公共雇用を創出する",
                "effects": {"resources": -11, "public_anger": -11},
                "feedback": "雇用創出で不満を和らげる。",
            },
            {
                "label": "限定的な補助だけ出す",
                "effects": {"resources": -4, "public_anger": -4},
                "feedback": "最小限の安全網を整える。",
            },
            {
                "label": "市場に任せる",
                "effects": {"public_anger": 7},
                "feedback": "財政は温存するが、社会不安が増す。",
            },
        ],
    },

    {
        "id": "school_meals",
        "title": "学校給食の全国拡充",
        "tags": ["public", "policy"],
        "description": "地方の学校で給食制度の拡充が求められている。子どもの栄養問題が政権の無策として批判されている。",
        "choices": [
            {
                "label": "全国で実施する",
                "effects": {"resources": -9, "public_anger": -9, "loyalty": -2},
                "feedback": "低コストで広い支持を得る public goods。",
            },
            {
                "label": "貧困地域だけ実施する",
                "effects": {"resources": -5, "public_anger": -4},
                "feedback": "限定的な公共支出。",
            },
            {
                "label": "見送る",
                "effects": {"public_anger": 5},
                "feedback": "象徴的政策を拒み、不満を招く。",
            },
        ],
    },

    {
        "id": "pension_expansion",
        "title": "年金制度の拡張要求",
        "tags": ["public", "economy"],
        "description": "退職者団体が年金の引き上げを要求している。高齢者層は政権支持の揺らぎやすい有権者層として注目されている。",
        "choices": [
            {
                "label": "制度を拡張する",
                "effects": {"resources": -12, "public_anger": -9},
                "feedback": "福祉拡大で広範な不満を抑える。",
            },
            {
                "label": "小幅な引き上げにとどめる",
                "effects": {"resources": -5, "public_anger": -3},
                "feedback": "財政負担を抑えた妥協。",
            },
            {
                "label": "拒否する",
                "effects": {"public_anger": 6},
                "feedback": "財政を守るが生活不安は増す。",
            },
        ],
    },

    {
        "id": "secret_police",
        "title": "秘密警察の強化",
        "tags": ["repression", "elite"],
        "description": "反体制活動を抑えるため監視強化が提案された。側近は不穏分子を早期に摘発する必要があると訴えている。",
        "choices": [
            {
                "label": "強化する",
                "effects": {"resources": -6, "loyalty": 5, "public_anger": 8},
                "feedback": "短期的な統制力は増すが、不満が蓄積する。",
            },
            {
                "label": "現状維持する",
                "effects": {},
                "feedback": "コストも効果も限定的。",
            },
            {
                "label": "縮小する",
                "effects": {"public_anger": -6, "loyalty": -4},
                "feedback": "民衆には好意的だが、支持層は不安を感じる。",
            },
        ],
    },

    {
        "id": "crackdown_demo",
        "title": "学生デモへの対応",
        "tags": ["repression", "public", "riot"],
        "description": "大学都市で学生デモが広がっている。運動はまだ限定的だが、知識人層にも支持が広がり始めている。",
        "choices": [
            {
                "label": "強制排除する",
                "effects": {"resources": -4, "public_anger": 9, "loyalty": 4},
                "feedback": "弾圧により短期秩序を回復する。",
            },
            {
                "label": "対話を呼びかける",
                "effects": {"public_anger": -4, "loyalty": -2},
                "feedback": "緊張緩和を試みるが、支持層には弱腰と映る。",
            },
            {
                "label": "要求の一部を受け入れる",
                "effects": {"resources": -5, "public_anger": -6, "loyalty": -3},
                "feedback": "譲歩で不満を下げるが、統治の一貫性は揺らぐ。",
            },
        ],
    },

    {
        "id": "opposition_ban",
        "title": "野党組織の活動禁止",
        "tags": ["repression", "politics"],
        "description": "治安当局が野党組織の活動停止を提案している。選挙前に反体制勢力を封じ込める狙いがある。",
        "choices": [
            {
                "label": "全面禁止する",
                "effects": {"loyalty": 5, "public_anger": 8, "coup_risk": -2},
                "feedback": "体制維持には有効だが、正統性は損なわれる。",
            },
            {
                "label": "一部規制にとどめる",
                "effects": {"public_anger": 3},
                "feedback": "抑圧を抑えつつ統制する。",
            },
            {
                "label": "合法活動を認める",
                "effects": {"public_anger": -5, "loyalty": -4},
                "feedback": "開放は民衆受けするが、支持層には危険と映る。",
            },
        ],
    },

    {
        "id": "media_censorship",
        "title": "メディア規制の強化",
        "tags": ["repression", "public"],
        "description": "政権批判報道が増えている。政府内では情報統制を強めるべきだとの声が高まっている。",
        "choices": [
            {
                "label": "厳しく規制する",
                "effects": {"public_anger": 6, "loyalty": 5, "coup_risk": -2},
                "feedback": "短期安定の代償として不満を蓄積する。",
            },
            {
                "label": "一部制限する",
                "effects": {"public_anger": 2},
                "feedback": "穏健な統制策。",
            },
            {
                "label": "自由を維持する",
                "effects": {"public_anger": -5, "loyalty": -3},
                "feedback": "正統性は高まるが、支持層は不安を抱く。",
            },
        ],
    },

    {
        "id": "franchise_expansion",
        "title": "選挙権拡大要求",
        "tags": ["reform", "public"],
        "description": "より多くの市民に投票権を与える提案が出ている。知識人層はこれは国家統合に資すると主張している。",
        "choices": [
            {
                "label": "拡大する",
                "effects": {"public_anger": -10, "loyalty": -10, "coup_risk": 8},
                "feedback": "Sの拡大は public goods の重要性を高めるが、支持層を動揺させる。",
            },
            {
                "label": "限定的に拡大する",
                "effects": {"public_anger": -3},
                "feedback": "象徴的な改革。",
            },
            {
                "label": "拒否する",
                "effects": {"public_anger": 10, "loyalty": 4},
                "feedback": "支持層は安心するが、民衆は反発する。",
            },
        ],
    },

    {
        "id": "coalition_reshuffle",
        "title": "支持連合の再編圧力",
        "tags": ["elite", "reform", "coalition"],
        "description": "支持連合の構成見直しが議論されている。新興勢力を取り込むべきだという声と、既存支持層を守るべきだという声が対立している。",
        "choices": [
            {
                "label": "新勢力を取り込む",
                "effects": {"loyalty": -6, "public_anger": -3, "coup_risk": 6},
                "feedback": "Wの再編は新しい安定を生むが、既存支持層を不安にさせる。",
            },
            {
                "label": "現行支持層を守る",
                "effects": {"loyalty": 4, "public_anger": 3},
                "feedback": "既存の勝利連合を優先する。",
            },
            {
                "label": "両者を曖昧に扱う",
                "effects": {"loyalty": -2, "public_anger": 2},
                "feedback": "先送りによって不満を温存する。",
            },
        ],
    },

    {
        "id": "elite_rotation",
        "title": "エリート層の入れ替え",
        "tags": ["elite", "politics", "coalition"],
        "description": "長く権力を握る高官を更迭し、新顔を登用する案が浮上している。側近の一部は腐敗抑制に必要だと主張している。",
        "choices": [
            {
                "label": "大幅に入れ替える",
                "effects": {"loyalty": -8, "public_anger": -4, "coup_risk": 8},
                "feedback": "既得権層は不安定化するが、民衆には刷新と映る。",
            },
            {
                "label": "一部だけ更迭する",
                "effects": {"loyalty": -3, "public_anger": -2},
                "feedback": "限定的な刷新。",
            },
            {
                "label": "現状維持する",
                "effects": {"loyalty": 3, "public_anger": 4},
                "feedback": "支持層は安心するが、停滞感が強まる。",
            },
        ],
    },

    {
        "id": "foreign_aid",
        "title": "外国からの援助提案",
        "tags": ["economy", "foreign", "external"],
        "description": "外国政府が資金援助を申し出ている。だが一部の支持層は、外部依存が体制の自立性を損なうと懸念している。",
        "choices": [
            {
                "label": "受け入れる",
                "effects": {"resources": 15, "loyalty": -5, "public_anger": -2},
                "feedback": "資源は増えるが、支持層は体制の弱さを感じる。",
            },
            {
                "label": "条件付きで受け入れる",
                "effects": {"resources": 8},
                "feedback": "利益を得つつ政治コストを抑える。",
            },
            {
                "label": "拒否する",
                "effects": {"loyalty": 5, "resources": -3},
                "feedback": "支持層には好まれるが、財政余力を失う。",
            },
        ],
    },

    {
        "id": "resource_discovery",
        "title": "資源の大規模発見",
        "tags": ["economy", "elite", "external"],
        "description": "新たな資源が発見され、国家収入が増える見込みだ。政権内では、この新収入を誰に配るかで早くも議論が始まっている。",
        "choices": [
            {
                "label": "支持層に重点配分する",
                "effects": {"resources": 0, "loyalty": 10, "coup_risk": -8, "public_anger": 5},
                "feedback": "レントを private goods として使い、支持連合を強化する。",
            },
            {
                "label": "公共投資に回す",
                "effects": {"resources": 0, "public_anger": -10, "loyalty": -5},
                "feedback": "public goods による広範な支持を狙う。",
            },
            {
                "label": "将来のために積み立てる",
                "effects": {"resources": 15, "public_anger": 4, "loyalty": -5,  "coup_risk": 4,},
                "feedback": "短期の見返りは小さいが、財政余力は増す。",
            },
        ],
    },

    {
        "id": "commodity_crash",
        "title": "資源価格の暴落",
        "tags": ["economy", "external", "crisis"],
        "description": "主力輸出資源の国際価格が急落した。国家収入の急減により、既存の配分体制を維持できるかが問題になっている。",
        "choices": [
            {
                "label": "支持層配分を維持する",
                "effects": {"resources": -12, "loyalty": 4, "public_anger": 5},
                "feedback": "支持連合を守るが、財政と民衆の負担が増す。",
            },
            {
                "label": "公共支出を守る",
                "effects": {"resources": -10, "public_anger": -4, "loyalty": -6},
                "feedback": "民衆不満は抑えられるが、支持層は不満を持つ。",
            },
            {
                "label": "全面的に緊縮する",
                "effects": {"resources": -3, "public_anger": 8, "loyalty": -3},
                "feedback": "財政は回復するが、広く不満を生む。",
            },
        ],
    },

    {
        "id": "sanctions",
        "title": "国際制裁の発動",
        "tags": ["external", "economy", "repression"],
        "description": "人権弾圧を理由に国際制裁が発動された。外貨流入が細り、政権内では内向きの統制を強めるべきだとの声が出ている。",
        "choices": [
            {
                "label": "支持層保護を優先する",
                "effects": {"resources": -8, "loyalty": 5, "public_anger": 4},
                "feedback": "勝利連合の維持を優先する典型的対応。",
            },
            {
                "label": "民衆向け補償を行う",
                "effects": {"resources": -10, "public_anger": -6, "loyalty": -3},
                "feedback": "制裁コストを public goods で吸収しようとする。",
            },
            {
                "label": "統制を強化して耐える",
                "effects": {"loyalty": 3, "public_anger": 7},
                "feedback": "弾圧で時間を稼ぐが、不満は蓄積する。",
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
        "description": "軍内部で反政府的な動きが報告された。現場の将校たちは上層部の配分が不公平だと不満を漏らしている。",
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
        "description": "首都で抗議活動が拡大。学生と失業者の合流により、運動は単発の不満表明を超え始めている。",
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
        "description": "国家財政が不安定化している。輸入決済への不安が広がり、政府内でも危機感が急速に高まっている。",
        "choices": [
            {
                "label": "緊縮財政",
                "effects": {
                    "resources": -2,
                    "public_anger": 8,
                },
                "feedback": "財政改善と引き換えに不満増加。",
            },
            {
                "label": "援助を受ける",
                "effects": {
                    "resources": 8,
                    "loyalty": -6,
                },
                "feedback": "資源増加と支持層不安。",
            },
            {
                "label": "支持層維持",
                "effects": {
                    "resources": -12,
                    "loyalty": 4,
                    "public_anger": 5,
                },
                "feedback": "支持層優先で財政悪化。",
            },
        ],
    },
]
