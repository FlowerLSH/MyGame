# 스테이지 1
stage_1_data = [[
    # Wave 1
    [
        {"type": "small", "x": 600, "y": 200, "delay": 0.5},
        {"type": "small", "x": 600, "y": 250, "delay": 1.0},
    ],
    # Wave 2
    [
        {"type": "medium", "x": 600, "y": 300, "delay": 0.5},
        {"type": "small", "x": 600, "y": 350, "delay": 1.0},
        {"type": "small", "x": 600, "y": 400, "delay": 1.5},
    ],
    # Wave 3
    [
        {"type": "large", "x": 600, "y": 450, "delay": 0.5},
    ]
    
], 1, False]

# 스테이지 2
stage_2_data = [[
    # Wave 1
    [
        {"type": "small", "x": 600, "y": 200, "delay": 0.5},
        {"type": "medium", "x": 600, "y": 250, "delay": 1.0},
        {"type": "large", "x": 600, "y": 300, "delay": 1.5},
    ]

], 2, False]

maintenance_stage = [[], 0, True]

stage_data = [stage_1_data, maintenance_stage, stage_2_data, ]
