import pygame
import time
from enemy_types import *

class Wave:
    def __init__(self, enemy_data):
        self.enemy_data = enemy_data
        self.spawned_enemies = []
        self.start_time = time.time()

    def update(self):
        current_time = time.time() - self.start_time
        for enemy_info in self.enemy_data:
            if enemy_info not in self.spawned_enemies and current_time >= enemy_info["delay"]:
                if enemy_info["type"] == "small":
                    new_enemy = SmallEnemy(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "medium":
                    new_enemy = MediumEnemy(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "large":
                    new_enemy = LargeEnemy(enemy_info["x"], enemy_info["y"])
                self.spawned_enemies.append(enemy_info)
                return new_enemy
        return None
    
    def is_finished(self):
        return len(self.spawned_enemies) == len(self.enemy_data)