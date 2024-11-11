import pygame
from bullet import Bullet
import settings as s
import math

class Weapon:
    def __init__(self):
        self.last_shot_time = 0

    def can_fire(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time
    
    def set_image(self, directory, size_x = 5, size_y = 5):
        image = pygame.image.load(directory)
        image = pygame.transform.scale(image, (size_x, size_y))
        return image
    
class Pistol(Weapon):
    def fire(self, x, y, bullets):
        sound = pygame.mixer.Sound("asset/sound/pistol_sound.wav")
        sound.set_volume(0.6)
        sound.play()
        image = self.set_image("asset/image/pistol_bullet2.png", 5, 5)
        bullets.append(Bullet(x, y, s.PISTOL_BULLET_SPEED, s.PISTOL_DAMAGE, source=image))

class MachineGun(Weapon):
    def fire(self, x, y, bullets):
        sound = pygame.mixer.Sound("asset/sound/machinegun_sound.ogg")
        sound.set_volume(0.15)
        image = self.set_image("asset/image/machinegun_bullet2.png", 40, 40)
        if self.can_fire() > s.MACHINEGUN_FIRE_RATE:
            sound.stop()
            sound.play()
            bullets.append(Bullet(x, y, s.MACHINEGUN_BULLET_SPEED, s.MACHINEGUN_DAMAGE, source=image))
            self.last_shot_time = pygame.time.get_ticks()

class Shotgun(Weapon):
    def fire(self, x, y, bullets):
        sound = pygame.mixer.Sound("asset/sound/shotgun_sound.wav")
        sound.set_volume(0.6)
        
        image = self.set_image("asset/image/pistol_bullet2.png", 20, 20)
        if self.can_fire() > s.SHOTGUN_COOLDOWN:
            sound.play()
            angle_increment = s.SHOTGUN_SPREAD_ANGLE / (s.SHOTGUN_BULLET_COUNT - 1)
            start_angle = -s.SHOTGUN_SPREAD_ANGLE / 2
            for i in range(s.SHOTGUN_BULLET_COUNT):
                angle = math.radians(start_angle + i + angle_increment)
                direction = (math.cos(angle), math.sin(angle))
                bullets.append(Bullet(x, y, s.SHOTGUN_BULLET_SPEED, s.SHOTGUN_DAMAGE, direction, s.SHOTGUN_RANGE, source=image, size_x=20, size_y=20))
            self.last_shot_time = pygame.time.get_ticks()