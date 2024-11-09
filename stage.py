from Enemy_wave import Wave

class Stage:
    def __init__(self, stage_data):
        self.waves = [Wave(wave) for wave in stage_data[0]]
        self.current_wave_index = 0
        self.stage_index = stage_data[1]
        self.stage_type = stage_data[2]

    def update(self, enemies):
        if self.stage_type == 0:
            if self.current_wave_index < len(self.waves):
                current_wave = self.waves[self.current_wave_index]
                new_enemy = current_wave.update()
                if current_wave.is_finished(enemies):
                    self.current_wave_index += 1
                    if self.current_wave_index < len(self.waves):
                        self.waves[self.current_wave_index].new_wave_start()
                return new_enemy
        return None
    
    def is_finished(self):
        if self.stage_type != 0:
            return False
        return self.current_wave_index >= len(self.waves)