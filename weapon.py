import pygame
from bullet import Bullet
import settings as s
import time
import math

class Weapon:
    def __init__(self):
        self.last_shot_time = 0

    def can_fire(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time
    
class Pistol(Weapon):
    def fire(self, x, y, bullets):
        bullets.append(Bullet(x, y, s.PISTOL_BULLET_SPEED, s.PISTOL_DAMAGE))

class MachineGun(Weapon):
    def fire(self, x, y, bullets):
        if self.can_fire() > s.MACHINEGUN_FIRE_RATE:
            bullets.append(Bullet(x, y, s.MACHINEGUN_BULLET_SPEED, s.MACHINEGUN_DAMAGE))
            self.last_shot_time = pygame.time.get_ticks()

class Shotgun(Weapon):
    def fire(self, x, y, bullets):
        if self.can_fire() > s.SHOTGUN_COOLDOWN:
            angle_increment = s.SHOTGUN_SPREAD_ANGLE / (s.SHOTGUN_BULLET_COUNT - 1)
            start_angle = -s.SHOTGUN_SPREAD_ANGLE / 2
            for i in range(s.SHOTGUN_BULLET_COUNT):
                angle = math.radians(start_angle + i + angle_increment)
                direction = (math.cos(angle), math.sin(angle))
                bullets.append(Bullet(x, y, s.SHOTGUN_BULLET_SPEED, s.SHOTGUN_DAMAGE, direction, s.SHOTGUN_RANGE))
            self.last_shot_time = pygame.time.get_ticks()