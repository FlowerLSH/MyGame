import pygame
import settings as s
import math
import random

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


class Meteor:
    def __init__(self):
        self.position = pygame.Vector2(s.SCREEN_WIDTH, random.randint(0, s.SCREEN_HEIGHT))
        self.hp = s.METEORHP
        self.speed = 2
        
        self.vertex_count = random.randint(5, 8)
        self.radius = random.randint(20, 50)
        self.vertices = self.generate_random_shape()
        
        self.direction = pygame.Vector2(-1, 0)
        self.angle = math.degrees(math.atan2(self.direction[1], self.direction[0]))
        self.rotated_vertices = []

    def generate_random_shape(self):
        vertices = []
        angle_step = 360 / self.vertex_count
        for i in range(self.vertex_count):
            angle = math.radians(i * angle_step + random.uniform(-15, 15))
            distance = self.radius + random.uniform(-5, 5)
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            vertices.append((x, y))
        return vertices

    def calculate_direction(self, target_position):
        dx, dy = target_position[0] - self.position[0], target_position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return pygame.Vector2(dx / distance, dy / distance)

    def update(self, player_position):
        self.direction = self.calculate_direction(player_position)

        self.position += self.direction * self.speed


        self.rotated_vertices = [
            (self.position.x + x, self.position.y + y)
            for x, y in self.vertices
        ]
        if self.hp <= 0:
            return False
        return True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            return False
        return True

    def get_distance(self, target_position):
        dx, dy = target_position[0] - self.position[0], target_position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance

    def get_edges(self):
        edges = []
        for i in range(len(self.rotated_vertices)):
            start = self.rotated_vertices[i]
            end = self.rotated_vertices[(i + 1) % len(self.rotated_vertices)] 
            edges.append((start, end))
        return edges
    
    def get_axes(self):
        axes = []
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            normal = (-edge[1], edge[0])
            length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            axes.append((normal[0] / length, normal[1] / length))
        return axes
    
    def project_polygon(self, axis):
        min_proj = max_proj = self.rotated_vertices[0][0] * axis[0] + self.rotated_vertices[0][1] * axis[1]
        for v in self.rotated_vertices:
            projection = v[0] * axis[0] + v[1] * axis[1]
            min_proj = min(min_proj, projection)
            max_proj = max(max_proj, projection)
        return min_proj, max_proj

    def draw(self, screen):
        pygame.draw.polygon(screen, s.GREEN, self.rotated_vertices)

