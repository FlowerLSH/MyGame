import pygame
import settings as s
from enemy_bullet import EnemyBullet
import math

class Enemy:
    def __init__(self, x, y, hp, speed, size_x, size_y, fire_rate, bullet_direction = (-1,0), bullet_speed = 5):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.hp = hp
        self.speed = speed
        self.size_x = size_x
        self.size_y = size_y
        self.fire_rate = fire_rate
        self.last_shot_time = 0
        self.bullets = []
        self.bullet_direction = bullet_direction
        self.bullet_speed = bullet_speed
        self.move_direction = 1
        
    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            return False
        return True
    
    def move(self):
        self.rect.y += self.move_direction * self.speed

        if self.rect.top <= 20:
            self.move_direction = 1
        elif self.rect.bottom >= s.SCREEN_HEIGHT - 20:
            self.move_direction = -1

    def fire_bullet(self, player_position = None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.fire_rate:
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed = self.bullet_speed, direction = self.bullet_direction)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
    
    def update_bullets(self):
        self.bullets = [i for i in self.bullets if i.update()]

    def draw(self, screen):
        pygame.draw.rect(screen, s.RED, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

class HomingEnemy(Enemy):
    def __init__(self, x, y, hp, speed, size_x, size_y, fire_rate, bullet_speed=5):
        super().__init__(x, y, hp, speed, size_x, size_y, fire_rate, bullet_speed=bullet_speed)
    
    def fire_bullet(self, player_position = None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.fire_rate:
            dx, dy = player_position[0] - self.rect.centerx, player_position[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            direction = (dx / distance, dy / distance)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
            self.bullets.append(bullet)
            self.last_shot_time = current_time