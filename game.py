import pygame
import sys
import random
from settings import *
from player import Player
from enemy import Enemy
from xp_orbs import XpOrbs

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire Survivors-style Game")
clock = pygame.time.Clock()

# Initialize game objects
player = Player()
xp_orbs = XpOrbs()
enemies = []

# Game loop variables
offset_x = 0
offset_y = 0
running = True


def handle_events():
    global running, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused


def handle_input():
    global running, keys
    if keys[pygame.K_ESCAPE]:
        running = False


paused = False
# Main game loop
while running:
    keys = pygame.key.get_pressed()
    handle_events()
    handle_input()
    while not paused:
        dt = clock.tick(60) / 1000
        screen.fill("black")

        # Spawn XP orbs
        xp_orbs.spawn()
        
        # Update XP orbs
        xp_orbs.update(player)

        # Spawn enemies
        if len(enemies) < ENEMY_SPAWN_MIN or (len(enemies) < ENEMY_SPAWN_MAX and random.random() < ENEMY_SPAWN_RATE):
            enemies.append(Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), ENEMY_RADIUS))

        # Update enemies
        for enemy in enemies:
            enemy.update(player, enemies, screen)

        # Update player
        player.update(keys, dt, screen)
        
        # Display all with offset to player coordinates
        offset_x = player.pos.x - SCREEN_WIDTH / 2
        offset_y = player.pos.y - SCREEN_HEIGHT / 2
        offset = pygame.Vector2(offset_x, offset_y)
        
        xp_orbs.draw_with_offset(screen, offset)
        
        for enemy in enemies:
            enemy.draw_with_offset(screen, offset_x, offset_y)
        player.draw_with_offset(screen, offset_x, offset_y)

        
        pygame.display.flip()
        break
        
    while paused:
        font = pygame.font.Font(None, 36)
        text = font.render("Paused", True, "white")
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))
        screen.blit(text, text_rect)
        pygame.display.flip()
        break


pygame.quit()
sys.exit()
