import pygame
import settings as s
import math

class EnemyBullet:
    def __init__(self, x, y, speed, direction = (-1,0)):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load("asset/image/enemy_bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.angle = math.atan2(self.direction[1], self.direction[0])

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if(self.rect.x < 0 or self.rect.x > s.SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > s.SCREEN_HEIGHT):
            return False
        return True
    
    def calculate_direction(self, target_position):
        dx, dy = target_position[0] - self.rect.centerx, target_position[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return dx / distance, dy / distance

    def rotate_vector(self, vector, angle):
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return vector[0] * cos_a - vector[1] * sin_a, vector[0] * sin_a + vector[1] * cos_a

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Missile:
    def __init__(self, x, y, speed, direction = (-1,0), duration = 7000):
        self.rect = pygame.Rect(x, y, 30, 10)
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load("asset/image/missile.png")
        self.image = pygame.transform.scale(self.image, (30, 10))
        self.angle = math.atan2(self.direction[1], self.direction[0])
        self.acceleration = 0.1
        self.max_speed = 10
        self.turn_speed = 0.06
        self.angle = math.atan2(self.direction[1], self.direction[0])
        self.spawn_time = pygame.time.get_ticks()
        self.missile_duration = duration

    def calculate_acceleration(self, player_position):
        player_x, player_y = player_position
        missile_x, missile_y = self.rect.center

        dx = player_x - missile_x
        dy = player_y - missile_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.acceleration = min(5, distance / 30)

        target = (dx / distance, dy / distance)

        new_dx = (1 - self.turn_speed) * self.direction[0] + self.turn_speed * target[0]
        new_dy = (1 - self.turn_speed) * self.direction[1] + self.turn_speed * target[1]

        distance = math.sqrt(new_dx ** 2 + new_dy ** 2)

        self.direction = (new_dx / distance, new_dy / distance)
       
        

    def update(self, target_position):
        self.calculate_acceleration(target_position)

        self.angle = math.atan2(self.direction[1], self.direction[0])

        self.rect.x += self.direction[0] * min(self.speed + self.acceleration, self.max_speed)
        self.rect.y += self.direction[1] * min(self.speed + self.acceleration, self.max_speed)

        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time > self.missile_duration:
            return False
        
        return True
    
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(-self.angle))  # 각도는 -self.angle로 설정
        rotated_rect = rotated_image.get_rect(center=self.rect.center)  # 중심을 self.rect.center에 맞춤
        screen.blit(rotated_image, rotated_rect.topleft)

        
