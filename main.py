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

pygame.mixer.set_num_channels(32)

player = Player(s.SCREEN_WIDTH * 0.25, s.SCREEN_HEIGHT // 2)

stage_index = 0

current_stage = Stage(stage_data[0])
enemies = []

font = pygame.font.Font(None, 80)
ui_manager = UIManager(screen, font)

loopFinished = False
clock = pygame.time.Clock()

background_image = pygame.image.load("asset/image/space_background.jpg")
background_image = pygame.transform.scale(background_image, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

pygame.mixer.music.load("asset/sound/bgm.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

flipped_background_image = pygame.transform.flip(background_image, True, False)

background_location = 0

main_stage_check = True

game_clear = False

chosen = False

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

            elif event.key == pygame.K_h:
                if player.show_key:
                    player.show_key = False
                else:
                    player.show_key = True

            elif event.key == pygame.K_s and main_stage_check:
                main_stage_check = False
                if stage_index < (len(stage_data) - 1):
                    stage_index += 1
                    fade_out(screen)
                    fade_in(screen)
                    chosen = False
                    player.player_position_reset()
                    current_stage = Stage(stage_data[stage_index])
                    ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Start!")
                    enemies = []
                else:
                    ui_manager.display_stage_ui("THE END")
                    ui_manager.display_stage_ui("Congratulation!! Game Clear!")
                    ui_manager.display_stage_ui("Made by LSH")
                    ui_manager.display_stage_ui("Press ESC to QUIT", duration=2000)
                    game_clear = True
                    chosen = False

            elif event.key == pygame.K_c:
                if player.special_attack_count > 0:
                    player.make_special_attack()
                    player.special_attack_count -= 1

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
    player.check_special_attack_collision(enemies)
    player.update_specialAttack()

    new_enemy = current_stage.update(enemies)
    if new_enemy:
        enemies.append(new_enemy)

    screen.fill(s.WHITE)

    background_location -= 3
    if background_location < -(s.SCREEN_WIDTH * 2):
        background_location = 0

    screen.blit(background_image, (background_location, 0))
    screen.blit(flipped_background_image, (background_location + s.SCREEN_WIDTH, 0))
    screen.blit(background_image, (background_location + s.SCREEN_WIDTH * 2, 0))

    if player.hp <= 0:
        font = pygame.font.Font(None, 50)

        game_over_text = font.render("GAME OVER", True, s.WHITE)
        press_esc_text = font.render("Press ESC to QUIT", True, s.WHITE)

        game_over_rect = game_over_text.get_rect(center=(s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 2 - 20))
        press_esc_rect = press_esc_text.get_rect(center=(s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 2 + 40))

        flag = False
        while True:
            screen.fill(s.BLACK)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(press_esc_text, press_esc_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loopFinished = True
                    flag = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loopFinished = True
                        flag = True
            if flag:
                break
                        

    player.draw(screen)

    if game_clear:
        font = pygame.font.Font(None, 40)
        weapon_text = font.render("Press ESC to QUIT", True, s.BLACK)
        screen.blit(weapon_text, (s.SCREEN_WIDTH // 2 - 50, 100))
    
    if current_stage.stage_type == 1:
        font = pygame.font.Font(None, 24)
        portal = pygame.Rect(s.SCREEN_WIDTH * 0.9, s.SCREEN_HEIGHT // 2, 50, 50)
        text_surface = font.render("NEXT STAGE", True, s.WHITE)
        text_rect = text_surface.get_rect(midbottom=(portal.centerx, portal.top - 5))
        screen.blit(text_surface, text_rect)
        player.hp = player.maxhp
        player.special_attack_count = player.max_special_attack_count
        pygame.draw.rect(screen, s.GREEN, portal)
                
        if not chosen:
            portal1 = pygame.Rect(s.SCREEN_WIDTH * 0.7, s.SCREEN_HEIGHT * 0.25, 50, 50)
            portal2 = pygame.Rect(s.SCREEN_WIDTH * 0.7, s.SCREEN_HEIGHT * 0.5, 50, 50)
            portal3 = pygame.Rect(s.SCREEN_WIDTH * 0.7, s.SCREEN_HEIGHT * 0.75, 50, 50)
            portal_texts = ["Damage + 10%", "MaxHP + 1", "SpecialATTCK + 1"]
            text_surfaces = [font.render(text, True, s.WHITE) for text in portal_texts]
            text_rects = [text_surface.get_rect(midbottom=(portal.centerx, portal.top - 5))
                          for text_surface, portal in zip(text_surfaces , [portal1, portal2, portal3])]
            for text_surface, text_rect in zip(text_surfaces, text_rects):
                    screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, s.GREEN, portal1)
            pygame.draw.rect(screen, s.GREEN, portal2)
            pygame.draw.rect(screen, s.GREEN, portal3)
            

        if aabb(player.rect, portal):
            if stage_index < (len(stage_data) - 1):
                stage_index += 1
                fade_out(screen)
                fade_in(screen)
                chosen = False
                player.player_position_reset()
                current_stage = Stage(stage_data[stage_index])
                ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Start!")
                enemies = []
            else:
                ui_manager.display_stage_ui("THE END")
                ui_manager.display_stage_ui("Congratulation!! Game Clear!")
                ui_manager.display_stage_ui("Made by LSH")
                ui_manager.display_stage_ui("Press ESC to QUIT", duration=2000)
                game_clear = True
                chosen = False

        elif aabb(player.rect, portal1) and not chosen:
            chosen = True
            player.attack_bonus += 0.1
            text_surface = font.render("Damage + 10%", True, s.WHITE)
            text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
            screen.blit(text_surface, text_rect)
            
        elif aabb(player.rect, portal2) and not chosen:
            chosen = True
            player.maxhp += 1
            player.hp = player.maxhp
            text_surface = font.render("MaxHP + 1", True, s.WHITE)
            text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
            screen.blit(text_surface, text_rect)

        elif aabb(player.rect, portal3) and not chosen:
            chosen = True
            player.max_special_attack_count += 1
            player.special_attack_count = player.max_special_attack_count
            text_surface = font.render("SpecialATTCK + 1", True, s.WHITE)
            text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
            screen.blit(text_surface, text_rect)

    if current_stage.stage_type == 2:
        title_font = pygame.font.Font(None, 100)
        instruction_font = pygame.font.Font(None, 50)

        title_text = title_font.render("Space Runner", True, (255, 255, 255))
        instruction_text = instruction_font.render('Press "S" to start', True, (255, 255, 255))

        title_rect = title_text.get_rect(center=(s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 4))
        instruction_rect = instruction_text.get_rect(center=(s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT * 2 / 3))
        screen.blit(title_text, title_rect)
        screen.blit(instruction_text, instruction_rect)

    
    for enemy in enemies:
        enemy.move()
        enemy.fire_bullet(player.rect.center)
        enemy.update_bullets()
        enemy.update_missiles(player.rect.center)
        enemy.update_meteors(player.rect.center)
        enemy.draw(screen)
    
    if current_stage.is_finished() and not enemies and not game_clear:
        if stage_index < (len(stage_data) - 1):
            ui_manager.display_stage_ui(f"Stage {current_stage.stage_index} Clear!!")
            stage_index += 1
            fade_out(screen)
            fade_in(screen)
            current_stage = Stage(stage_data[stage_index])
            player.player_position_reset()
            if current_stage.stage_type == 1:
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