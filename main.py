import pygame
import sys
import random

# pygame setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire Survivors-style Game")
clock = pygame.time.Clock()
running = True
dt = 0

# Player setup
PLAYER_RADIUS = 40
PLAYER_SPEED = 300

# Player stats
player_hp = 100
player_max_hp = 100
player_xp = 0
player_xp_to_next_level = 10
player_level = 1


# Xp orbs setup
XP_ORB_RADIUS = 10
XP_ORB_SPAWN_RATE = 0.01
XP_ORB_SPAWN_MIN = 1
XP_ORB_SPAWN_MAX = 10
xp_orbs = []


# Enemy setup
ENEMY_RADIUS = 40
ENEMY_SPEED = 200
ENEMY_SPAWN_RATE = 0.01
ENEMY_SPAWN_MIN = 1
ENEMY_SPAWN_MAX = 10
enemies = []
ENEMY_DAMAGE = 10
ENEMY_HP = 50
ENEMY_ATTACK_RATE = 1/60

# World coordinates tracking
world_x = 0
world_y = 0

# Screen center (where player will always be drawn)
player_screen_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # Movement vectors
    move_x = 0
    move_y = 0
    
    # Update world coordinates and movement based on key presses
    if keys[pygame.K_z] or keys[pygame.K_w]:
        move_y = PLAYER_SPEED * dt
        world_y += move_y
    if keys[pygame.K_s]:
        move_y = -PLAYER_SPEED * dt
        world_y += move_y
    if keys[pygame.K_q] or keys[pygame.K_a]:
        move_x = PLAYER_SPEED * dt
        world_x += move_x
    if keys[pygame.K_d]:
        move_x = -PLAYER_SPEED * dt
        world_x += move_x

    # Draw player at screen center
    pygame.draw.circle(screen, "white", player_screen_pos, PLAYER_RADIUS)

    # Spawn xp orbs
    if len(xp_orbs) < XP_ORB_SPAWN_MIN or (len(xp_orbs) < XP_ORB_SPAWN_MAX and random.random() < XP_ORB_SPAWN_RATE):
        xp_orbs.append(pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    
    # Update and draw xp orbs
    for orb in xp_orbs:
        # Move orbs in the opposite direction of player movement
        orb.x += move_x
        orb.y += move_y
        
        # Draw orbs at their updated positions
        pygame.draw.circle(screen, "blue", orb, XP_ORB_RADIUS)

    # Handle player collision with xp orbs
    for orb in xp_orbs:
        if pygame.Vector2(player_screen_pos - orb).length() < PLAYER_RADIUS + XP_ORB_RADIUS:
            xp_orbs.remove(orb)
            print("Player collected an xp orb!")
            player_xp += 1
            if player_xp >= player_xp_to_next_level:
                player_level += 1
                player_xp -= player_xp_to_next_level
                player_xp_to_next_level *= 1.5
                print("Player leveled up!")
                print("New xp to next level:", player_xp_to_next_level)
                player_max_hp += 10
                player_hp = player_max_hp

    # Spawn enemies
    if len(enemies) < ENEMY_SPAWN_MIN or (len(enemies) < ENEMY_SPAWN_MAX and random.random() < ENEMY_SPAWN_RATE):
        enemies.append(pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
        
    # Update and draw enemies
    for enemy in enemies:
        # Move enemies in the opposite direction of player movement
        enemy.x += move_x
        enemy.y += move_y
        
        # Draw enemies at their updated positions
        pygame.draw.circle(screen, "red", enemy, ENEMY_RADIUS)
        
    # Handle enemy collision with player
    for enemy in enemies:
        if pygame.Vector2(player_screen_pos - enemy).length() < PLAYER_RADIUS + ENEMY_RADIUS:
            player_hp -= ENEMY_DAMAGE
            enemies.remove(enemy)
            print("Player hit by enemy!")
            print("Player HP:", player_hp)
            if player_hp <= 0:
                print("Player died!")
                running = False
                
    
    






    # Update display
    pygame.display.flip()

    # Limit FPS and calculate delta time
    dt = clock.tick(60) / 1000

pygame.quit()
sys.exit()