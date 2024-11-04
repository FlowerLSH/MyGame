import pygame
from enemy_types import *
import settings as s
from player import Player
from stage import Stage
from stage_data import *

def fade_out(screen, speed=5):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface = fade_surface.convert()
    for i in range(0, 255, speed):
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(i)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def fade_in(screen, speed=5):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface = fade_surface.convert()
    for i in range(255, -1, -speed):
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(i)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


pygame.init()

screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
pygame.display.set_caption("SWCON Project")

player = Player(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2)

stage_index = 0

current_stage = Stage(stage_data[0])
enemies = []

loopFinished = False
clock = pygame.time.Clock()

while not loopFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.switch_weapon("pistol")
            elif event.key == pygame.K_2:
                player.switch_weapon("machinegun")
            elif event.key == pygame.K_3:
                player.switch_weapon("shotgun")

            elif event.key == pygame.K_x:
                if player.is_pistol():
                    player.attack()
                    
    if pygame.key.get_pressed()[pygame.K_x] and not player.is_pistol():
        player.attack()

    player.move()
    
    player.update_bullets()
    player.check_bullet_collision(enemies)
    player.check_enemy_bullet_collision(enemies)

    new_enemy = current_stage.update()
    if new_enemy:
        enemies.append(new_enemy)

    screen.fill(s.WHITE)
    player.draw(screen)

    if current_stage.is_maintenance:
        portal = pygame.Rect(350, 250, 50, 50)
        pygame.draw.rect(screen, s.GREEN, portal)

        if player.rect.colliderect(portal):
            if stage_index < (len(stage_data) - 1):
                stage_index += 1
                fade_out(screen)
                fade_in(screen)
                current_stage = Stage(stage_data[stage_index])
                enemies = []
            else:
                print("Game Clear")

    for enemy in enemies:
        enemy.move()
        enemy.fire_bullet()
        enemy.update_bullets()
        enemy.draw(screen)
    
    if current_stage.is_finished() and not enemies:
        if stage_index < (len(stage_data) - 1):
            print("Stage", current_stage.stage_index, "Clear")
            stage_index += 1
            fade_out(screen)
            fade_in(screen)
            current_stage = Stage(stage_data[stage_index])
            enemies = []
        else:
            print("Game Clear")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()