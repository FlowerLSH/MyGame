import pygame
import settings as s

class EnemyBullet:
    def __init__(self, x, y, speed, direction = (-1,0)):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if(self.rect.x < 0 or self.rect.x > s.SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > s.SCREEN_HEIGHT):
            return False
        return True
    
    def draw(self, screen):
        pygame.draw.rect(screen, s.RED, self.rect)