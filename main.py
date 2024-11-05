import pygame
from enemy_types import *
import settings as s
from player import Player
from stage import Stage
from stage_data import *
from ui_manager import UIManager
import time
from collision_detection import *

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

font = pygame.font.Font(None, 80)
ui_manager = UIManager(screen, font)

loopFinished = False
clock = pygame.time.Clock()

game_clear = False
"""
if stage_index == 0 and not ui_manager.ui_active:
    ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Start!")
"""

while not loopFinished:
    if ui_manager.update():
        continue

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

            elif event.key == pygame.K_ESCAPE:
                if game_clear:
                    loopFinished = True
                else:
                    continue
                    
    if pygame.key.get_pressed()[pygame.K_x] and not player.is_pistol():
        player.attack()

    player.move()
    
    player.update_bullets()
    player.check_bullet_collision(enemies)
    player.check_enemy_bullet_collision(enemies)

    new_enemy = current_stage.update(enemies)
    if new_enemy:
        enemies.append(new_enemy)

    screen.fill(s.WHITE)
    player.draw(screen)

    if game_clear:
        font = pygame.font.Font(None, 40)
        weapon_text = font.render("Press ESC to QUIT", True, s.BLACK)
        screen.blit(weapon_text, (s.SCREEN_WIDTH // 2 - 50, 100))
    
    if current_stage.is_maintenance:
        portal = pygame.Rect(350, 250, 50, 50)
        pygame.draw.rect(screen, s.GREEN, portal)

        if aabb(player.rect, portal):
            if stage_index < (len(stage_data) - 1):
                stage_index += 1
                fade_out(screen)
                fade_in(screen)
                current_stage = Stage(stage_data[stage_index])
                ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Start!")
                enemies = []
            else:
                ui_manager.display_stage_ui("THE END")
                ui_manager.display_stage_ui("Congratulation!! Game Clear!")
                ui_manager.display_stage_ui("Made by LSH")
                ui_manager.display_stage_ui("Press ESC to QUIT", duration=2000)
                game_clear = True

    for enemy in enemies:
        enemy.move()
        enemy.fire_bullet(player.rect.center)
        enemy.update_bullets()
        enemy.draw(screen)
    
    if current_stage.is_finished() and not enemies and not game_clear:
        if stage_index < (len(stage_data) - 1):
            ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Clear!!")
            stage_index += 1
            fade_out(screen)
            fade_in(screen)
            current_stage = Stage(stage_data[stage_index])
            if current_stage.is_maintenance:
                ui_manager.display_stage_ui("Maintenance Stage")
            else:
                ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Start!")
            enemies = []
        else:
            ui_manager.display_stage_ui("THE END")
            ui_manager.display_stage_ui("Congratulation! Game Clear!")
            ui_manager.display_stage_ui("Made by LSH")
            ui_manager.display_stage_ui("Press ESC to QUIT", duration=2000)
            game_clear = True
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()