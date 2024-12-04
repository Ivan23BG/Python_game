import pygame
import sys
import random
from settings import *
from player import Player
from xp_orbs import XpOrbs
from enemies import Enemies  # Enemies manager class
from projectile import Projectile  # Projectile class

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire Survivors-style Game")
clock = pygame.time.Clock()

# Initialize game objects
player = Player()
xp_orbs = XpOrbs()
enemies = Enemies()  # Using the Enemies manager
projectiles = []  # List to hold projectiles

# Game state variables
running = True
paused = False


def handle_events() -> None:
    """
    Handles global game events such as quitting or pausing.
    """
    global running, paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused


def update_projectiles(dt: float) -> None:
    """
    Updates all projectiles, checks for collisions, and removes those that collide or leave the screen.

    Args:
        dt (float): Delta time for frame-independent movement.
    """
    for projectile in projectiles[:]:
        projectile.update(dt)
        # Check for collisions with enemies
        enemy_hit = projectile.check_collision(enemies.enemies)
        if enemy_hit:
            enemy_hit.take_damage(10)  # Example damage
            projectiles.remove(projectile)
        elif not (0 <= projectile.pos.x <= SCREEN_WIDTH and 0 <= projectile.pos.y <= SCREEN_HEIGHT):
            projectiles.remove(projectile)  # Remove projectiles out of bounds


def draw_with_offset(offset: pygame.Vector2) -> None:
    """
    Draws all game objects with a positional offset for a camera-like effect.

    Args:
        offset (pygame.Vector2): The positional offset.
    """
    xp_orbs.draw_with_offset(screen, offset)
    enemies.draw_with_offset(screen, offset)
    for projectile in projectiles:
        projectile.draw_with_offset(screen, offset, "yellow")
    player.draw_with_offset(screen, offset.x, offset.y)


def pause_menu() -> None:
    """
    Displays the pause menu while the game is paused.
    """
    font = pygame.font.Font(None, 36)
    text = font.render("Paused", True, "white")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
    screen.blit(text, text_rect)
    pygame.display.flip()


# Main game loop
while running:
    keys = pygame.key.get_pressed()
    handle_events()

    if paused:
        pause_menu()
        continue

    # Game updates
    dt = clock.tick(60) / 1000
    screen.fill("black")

    # Spawn and update XP orbs
    xp_orbs.spawn(player)
    xp_orbs.update(player)

    # Spawn and update enemies
    enemies.spawn(player)
    enemies.update(player)

    # Handle player shooting
    current_time = pygame.time.get_ticks() / 1000
    if keys[pygame.K_SPACE]:  # Fire weapon
        player.weapon.shoot(player, projectiles, current_time)

    # Update projectiles
    update_projectiles(dt)

    # Update player
    player.update(keys, dt, screen)

    # Calculate camera offset
    offset = pygame.Vector2(player.pos.x - SCREEN_WIDTH / 2, player.pos.y - SCREEN_HEIGHT / 2)

    # Draw everything
    draw_with_offset(offset)

    pygame.display.flip()

pygame.quit()
sys.exit()
