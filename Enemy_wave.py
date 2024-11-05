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
                elif enemy_info["type"] == "homing_small":
                    new_enemy = HomingEnemySmall(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "homing_medium":
                    new_enemy = HomingEnemyMedium(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "homing_large":
                    new_enemy = HomingEnemyLarge(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "elite":
                    new_enemy = EliteEnemy(enemy_info["x"], enemy_info["y"])
                elif enemy_info["type"] == "boss":
                    new_enemy = BossEnemy(enemy_info["x"], enemy_info["y"])
                self.spawned_enemies.append(enemy_info)
                return new_enemy
        return None
    
    def is_finished(self, enemies):
        return len(self.spawned_enemies) == len(self.enemy_data) and not enemies
    
    def new_wave_start(self):
        self.start_time = time.time()