from enemy import *
from enemy_bullet import EnemyBullet
import math
import pygame
import random
import time

class SmallEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 50, speed = 3, size_x = 20, size_y = 20, fire_rate = 1000)

class MediumEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 100, speed = 2, size_x = 30, size_y = 30, fire_rate = 1500)
        
class LargeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 200, speed = 1, size_x = 40, size_y = 40, fire_rate = 2000)

class HomingEnemySmall(HomingEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp=20, speed=1.5, size_x=20, size_y=20, fire_rate=1500, bullet_speed=3)

class HomingEnemyMedium(HomingEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp=40, speed=1.2, size_x=30, size_y=30, fire_rate=1800, bullet_speed=2.5)

class HomingEnemyLarge(HomingEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp=60, speed=1, size_x=40, size_y=40, fire_rate=2000, bullet_speed=2)

class EliteEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp=200, speed=0.8, size_x=100, size_y=100, fire_rate=500, bullet_speed=7)
        
        self.straight_fire_rate = 400
        self.diagonal_fire_rate = 600
        self.targeted_fire_rate = 700
        self.last_straight_shot_time = 0
        self.last_diagonal_shot_time = 0
        self.last_targeted_shot_time = 0

    def fire_bullet(self, player_position):
        self.fire_straight()
        self.fire_diagonal()
        self.fire_targeted(player_position)

    def fire_straight(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_straight_shot_time >= self.straight_fire_rate:
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=(-1, 0))
            self.bullets.append(bullet)
            self.last_straight_shot_time = current_time

    def fire_diagonal(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_diagonal_shot_time >= self.diagonal_fire_rate:
            directions = [self.rotate_vector((-1, 0), 30), self.rotate_vector((-1, 0), -30)]
            for direction in directions:
                bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
                self.bullets.append(bullet)
            self.last_diagonal_shot_time = current_time

    def fire_targeted(self, player_position):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_targeted_shot_time >= self.targeted_fire_rate:
            direction = self.calculate_direction(player_position)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
            self.bullets.append(bullet)
            self.last_targeted_shot_time = current_time

    def calculate_direction(self, target_position):
        dx, dy = target_position[0] - self.rect.centerx, target_position[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return dx / distance, dy / distance

    def rotate_vector(self, vector, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return vector[0] * cos_a - vector[1] * sin_a, vector[0] * sin_a + vector[1] * cos_a











class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 1000, speed=0.8, size_x=100, size_y=100, fire_rate=500, bullet_speed=5)
        self.phase = 1
        self.pattern_num = 2
        self.current_pattern = 0
        self.maxhp = 1000

        
        self.check_time = 0


        self.spread_fire_rate = 500
        self.targeted_fire_rate = 700
        self.last_spread_shot_time = 0
        self.last_targeted_shot_time = 0
        self.barrage_duration = 7000  # 탄막 발사 지속 시간 (밀리초)

        self.fast_fire_rate = 25
        self.last_fast_fire_time = 0

        self.fast_target_shot_duration = 3000
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < (self.maxhp * 0.6):
            self.phase = 2
        if self.hp <= 0:
            return False
        return True

    def fire_bullet(self, player_position = None):
        current_time = pygame.time.get_ticks()
        if self.current_pattern:
            match self.current_pattern:
                case 1:
                    if current_time - self.check_time > self.barrage_duration:
                        self.check_time = current_time
                        self.current_pattern = 0
                        self.speed = 0.8
                        return
                    self.spread_shot(player_position)
                case 2:
                    if current_time - self.check_time > self.fast_target_shot_duration:
                        self.check_time = current_time
                        self.current_pattern = 0
                        self.bullet_speed = 5
                        return
                    self.fast_target_shot(player_position)
        else:
            if current_time - self.check_time > 2500:
                self.current_pattern = random.randint(2, self.pattern_num)
                self.check_time = current_time


    def spread_shot(self, player_position):
        if self.phase == 1:
            self.fire_spread()
            self.fire_targeted(player_position)
        else:
            self.speed = 4
            self.fire_spread(True)
            self.fire_targeted(player_position, True)

    def fast_target_shot(self, player_position):
        if self.phase == 2:
            self.fast_target_shot_duration = 7000
        self.bullet_speed = 40
        self.fire_targeted_fastshot(player_position)

    def fire_spread(self, advanced = False):
        """5갈래 방향으로 확산 발사"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spread_shot_time >= self.spread_fire_rate:
            if advanced:
                angles = [-30, -20, -5, 0, 5, 20, 30]
            else:
                angles = [-40, -20, 0, 20, 40]  # 5갈래 각도
            for angle in angles:
                direction = self.rotate_vector((-1, 0), angle)
                if advanced:
                    bullet = EnemyBullet(self.rect.topleft[0], self.rect.topleft[1], speed=self.bullet_speed, direction=direction)
                    self.bullets.append(bullet)
                    bullet = EnemyBullet(self.rect.bottomleft[0], self.rect.bottomleft[1], speed=self.bullet_speed, direction=direction)
                    self.bullets.append(bullet)
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
                    self.bullets.append(bullet)
                else:
                    bullet = EnemyBullet(self.rect.topleft[0], self.rect.topleft[1], speed=self.bullet_speed, direction=direction)
                    self.bullets.append(bullet)
                    bullet = EnemyBullet(self.rect.bottomleft[0], self.rect.bottomleft[1], speed=self.bullet_speed, direction=direction)
                    self.bullets.append(bullet)
            self.last_spread_shot_time = current_time

    def fire_targeted(self, player_position, advanced = False):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_targeted_shot_time >= self.targeted_fire_rate:
            direction = self.calculate_direction(player_position)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
            self.bullets.append(bullet)
            self.last_targeted_shot_time = current_time

    def fire_targeted_fastshot(self, player_position):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fast_fire_time >= self.fast_fire_rate:
            direction = self.calculate_direction(player_position)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, direction=direction)
            self.bullets.append(bullet)
            self.last_fast_fire_time = current_time

    def calculate_direction(self, target_position):
        dx, dy = target_position[0] - self.rect.centerx, target_position[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return dx / distance, dy / distance

    def rotate_vector(self, vector, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return vector[0] * cos_a - vector[1] * sin_a, vector[0] * sin_a + vector[1] * cos_a