import pygame
import settings as s

class Bullet:
    def __init__(self, x, y, speed, damage, direction = (1, 0), max_range = None, color = s.BLACK, source = None):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = speed
        self.damage = damage
        self.direction = direction
        self.start_x = x
        self.max_range = max_range
        self.color = color
        self.image = source

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if self.max_range and abs(self.rect.x - self.start_x) > self.max_range:
            return False
        return True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)