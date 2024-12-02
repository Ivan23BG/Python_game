import pygame
import random

from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class XpOrb:
    def __init__(self, radius=15, xp=5):
        x = random.randint(0, SCREEN_WIDTH) 
        y = random.randint(0, SCREEN_HEIGHT)
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.xp = xp


    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.pos, self.radius)


    def draw_with_offset(self, screen, offset):
        pygame.draw.circle(screen, "blue", self.pos - offset, self.radius)


    def update(self, player):
        if self.check_player_collision(player):
            return 1 # collision detected


    def check_player_collision(self, player):
        if self.collision_detected(player):
            return 1 # collision detected


    def collision_detected(self, player):
        return pygame.Vector2(player.pos - self.pos).length() < player.radius + self.radius