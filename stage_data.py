# 스테이지 1
stage_1_data = [[

    [
        {"type": "boss", "x": 1000, "y": 450, "delay": 0.5},
    ]
    
], 1, 0]

# 스테이지 2
stage_2_data = [[
    # Wave 1
    [
        {"type": "small", "x": 800, "y": 200, "delay": 0.5},
        {"type": "medium", "x": 850, "y": 250, "delay": 1.0},
        {"type": "large", "x": 950, "y": 300, "delay": 1.5},
    ],
    # Wave 2
    [
        {"type": "homing_small", "x": 800, "y": 300, "delay": 2.0},
        {"type": "homing_medium", "x": 850, "y": 350, "delay": 3.0},
        {"type": "homing_large", "x": 950, "y": 400, "delay": 4.0},
    ],
    # Wave 3
    [
        {"type": "elite", "x": 1000, "y": 450, "delay": 0.5},
    ]

], 2, 0]

main_stage = [[], 0, 2]

maintenance_stage = [[], 0, 1]

stage_data = [main_stage, stage_1_data, maintenance_stage, stage_2_data, ]
