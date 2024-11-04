from Enemy_wave import Wave

class Stage:
    def __init__(self, wave_data, is_maintenance = False):
        self.waves = [Wave(wave) for wave in wave_data]
        self.current_wave_index = 0
        self.is_maintenance = is_maintenances

    def update(self):
        if not self.is_maintenance:
            if self.current_wave_index < len(self.waves):
                current_wave = self.waves[self.current_wave_index]
                new_enemy = current_wave.update()
                if current_wave.is_finished():
                    self.current_wave_index += 1
                return new_enemy
        return None
    
    def is_finished(self):
        if self.is_maintenance:
            return False
        return self.current_wave_index >= len(self.waves)