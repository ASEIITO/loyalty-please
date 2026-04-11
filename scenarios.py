SCENARIOS = [
    {
        "id": "control_state",
        "name": "統制国家",
        "description": "強固な統治体制を持つが、民衆の自由は制限されている。",
        "initial_state": {
            "resources": 50,
            "loyalty": 70,
            "public_anger": 55,
            "coup_risk": 20,
        },
    },
    {
        "id": "resource_state",
        "name": "資源依存国家",
        "description": "資源収入に依存。財政は豊かだが政治は不安定。",
        "initial_state": {
            "resources": 80,
            "loyalty": 40,
            "public_anger": 35,
            "coup_risk": 50,
        },
    },
    {
        "id": "fragile_state",
        "name": "不安定な国家",
        "description": "政権基盤が弱く、暴動とクーデターの危険が高い。",
        "initial_state": {
            "resources": 35,
            "loyalty": 30,
            "public_anger": 60,
            "coup_risk": 60,
        },
    },
]
