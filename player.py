import pygame
import settings as s
from bullet import Bullet
from weapon import *
from collision_detection import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = s.PLAYER_SPEED

        self.last_dash_time = 0
        self.last_key_time = {"left": 0, "right": 0, "up": 0, "down": 0}
        self.last_key_input = None
        self.key_released = {"left": True, "right": True, "up": True, "down": True}

        self.weapon = Pistol()
        self.bullets = []

        self.hp = 3

        self.last_hit_time = 0
        self.invincibility_duration = 2000

    def move(self):
        self.x_vel = 0
        self.y_vel = 0
        keys = pygame.key.get_pressed()

        # 방향키별 이동 및 대쉬 조건 확인
        if keys[pygame.K_LEFT]:
            self.x_vel = -self.speed
            if self.key_released['left']:  # 키가 처음 눌렸을 때만 대쉬 확인
                self.check_dash('left', -s.DASH_DISTANCE, 0)
                self.key_released['left'] = False  # 대쉬 실행 후 릴리즈 초기화
        else:
            self.key_released['left'] = True

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.speed
            if self.key_released['right']:
                self.check_dash('right', s.DASH_DISTANCE, 0)
                self.key_released['right'] = False
        else:
            self.key_released['right'] = True

        if keys[pygame.K_UP]:
            self.y_vel = -self.speed
            if self.key_released['up']:
                self.check_dash('up', 0, -s.DASH_DISTANCE)
                self.key_released['up'] = False
        else:
            self.key_released['up'] = True

        if keys[pygame.K_DOWN]:
            self.y_vel = self.speed
            if self.key_released['down']:
                self.check_dash('down', 0, s.DASH_DISTANCE)
                self.key_released['down'] = False
        else:
            self.key_released['down'] = True

        # 위치 업데이트
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # 화면 밖으로 나가지 못하게 위치 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > s.SCREEN_WIDTH:
            self.rect.right = s.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > s.SCREEN_HEIGHT:
            self.rect.bottom = s.SCREEN_HEIGHT

    def check_dash(self, direction, dx, dy):
        current_time = pygame.time.get_ticks()

        # 쿨타임 확인
        if current_time - self.last_dash_time < s.DASH_COOLDOWN:
            return

        last_key_time = self.last_key_time[direction]
        # 같은 방향키가 설정된 간격 내에 두 번 눌렸을 경우에만 대쉬 실행
        if direction == self.last_key_input and current_time - last_key_time < s.DASH_DOUBLE_TAP_TIME:
            print("dashed")
            self.rect.x += dx
            self.rect.y += dy
            self.last_dash_time = current_time

        # 현재 키 입력 시간과 방향 업데이트
        self.last_key_time[direction] = current_time
        self.last_key_input = direction

    def switch_weapon(self, weapon_type):
        if weapon_type == 'pistol':
            self.weapon = Pistol()
        elif weapon_type == 'machinegun':
            self.weapon = MachineGun()
        elif weapon_type == 'shotgun':
            self.weapon = Shotgun()

    def is_pistol(self):
        return isinstance(self.weapon, Pistol)

    def attack(self):
        if self.is_pistol():
            self.weapon.fire(self.rect.right, self.rect.centery, self.bullets)
        
        elif pygame.key.get_pressed()[pygame.K_x]:
            self.weapon.fire(self.rect.right, self.rect.centery, self.bullets)

    def update_bullets(self):
        self.bullets = [i for i in self.bullets if i.update()]

    def check_bullet_collision(self, enemies):
        for bullet in self.bullets:
            for enemy in enemies:
                if aabb(bullet.rect, enemy.rect):
                    if not enemy.take_damage(bullet.damage):
                        enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break

    def check_enemy_bullet_collision(self, enemies):
        for enemy in enemies:
            for bullet in enemy.bullets:
                if aabb(self.rect, bullet.rect):  
                    self.take_damage()  
                    enemy.bullets.remove(bullet) 
                    break 

    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.invincibility_duration:
            self.hp -= 1
            self.last_hit_time = current_time
             
        if self.hp <= 0:
            print("Game Over")

    def get_dash_cooldown(self):
        time_since_dash = ((pygame.time.get_ticks() / 1000) - (self.last_dash_time / 1000))
        remaining_time = max(0, (s.DASH_COOLDOWN / 1000) - time_since_dash)
        return remaining_time
    
    def draw_UI(self, screen):
        # 체력 UI
        for i in range(self.hp):
            pygame.draw.rect(screen, s.RED, (10 + i * 30, 10, 20, 20))

        # 무기 UI
        font = pygame.font.Font(None, 24)
        weapon_text = font.render(f"Weapon : {self.weapon.__class__.__name__.upper()}", True, s.BLACK)
        screen.blit(weapon_text, (10, 40))

        # 대쉬 쿨타임 UI
        dash_cooldown = self.get_dash_cooldown()
        dash_color = s.GRAY if dash_cooldown > 0 else s.WHITE
        dash_rect = pygame.Rect(10, 70, 120, 30)

        pygame.draw.rect(screen, s.BLACK, dash_rect, 2)
        pygame.draw.rect(screen, dash_color, dash_rect.inflate(-4, -4))
        if dash_cooldown > 0:
            cooldown_text = font.render(f"{dash_cooldown:.1f}s", True, s.BLACK)
            screen.blit(cooldown_text, (20, 75))

        else:
            dash_text = font.render("Dash Ready", True, s.BLACK)
            text_pos = dash_text.get_rect(center=dash_rect.center)
            screen.blit(dash_text, (20, 75))

    def draw(self, screen):
        pygame.draw.rect(screen, s.BLUE, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_UI(screen)
