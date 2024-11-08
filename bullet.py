import pygame
import settings as s

class Bullet:
    def __init__(self, x, y, speed, damage, direction = (1, 0), max_range = None, color = s.BLACK, source = None, size_x = 5, size_y = 5):
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
    
    def project_polygon(self, axis):
        corners = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        min_proj = max_proj = corners[0][0] * axis[0] + corners[0][1] * axis[1]
        for corner in corners:
            projection = corner[0] * axis[0] + corner[1] * axis[1]
            min_proj = min(min_proj, projection)
            max_proj = max(max_proj, projection)
        return min_proj, max_proj
    
    def get_axes(self):
        return [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    def get_bullet_edges(self):
        return [(self.rect.topleft,self.rect.topright),
                (self.rect.bottomright, self.rect.bottomleft)]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)