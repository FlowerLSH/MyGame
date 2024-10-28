import pygame
import settings as s

class Enemy:
    def __init__(self, x, y, hp):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.hp = hp

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            return False
        return True
    
    def draw(self, screen):
        pygame.draw.rect(screen, s.RED, self.rect)