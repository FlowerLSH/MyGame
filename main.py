import pygame
from enemy_types import *
import settings as s
from player import Player

pygame.init()

screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
pygame.display.set_caption("SWCON Project")

player = Player(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2)

loopFinished = False
clock = pygame.time.Clock()

enemies = [SmallEnemy(600, 200), MediumEnemy(600, 300), LargeEnemy(600, 400)]

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

    screen.fill(s.WHITE)
    player.draw(screen)

    for enemy in enemies:
        enemy.move()
        enemy.fire_bullet()
        enemy.update_bullets()
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()