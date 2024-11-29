import pygame
import random

class Enemy:
    def __init__(self, x, y, radius):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.speed = 200/60
        self.dmg = 10
        self.hp = 50


    def update(self, player, enemies, screen):
        """
        Update the enemy's position and behavior
        """
        self.handle_movement(player)
        self.handle_collision(player, enemies)
        self.handle_death(enemies)


    def handle_movement(self, player):
        """
        Move the enemy
        """
        self.chase_player(player.pos)


    def chase_player(self, player_pos):
        """
        Move the enemy towards the player
        """
        direction = player_pos - self.pos
        direction.normalize_ip()
        self.pos += direction * self.speed


    def handle_collision(self, player, enemies):
        """
        Handle collision with another object
        """
        if self.check_collision(player):
            player.take_damage(self.dmg)
            self.take_damage(10)
            self.knockback(player.pos)
        
        for enemy in enemies:
            if enemy != self and self.check_collision(enemy):
                self.knockback(enemy.pos, 10)


    def check_collision(self, player):
        """
        Check for collision with the player
        """
        return (self.pos - player.pos).length() < self.radius + player.radius


    def take_damage(self, dmg):
        """
        Take damage
        """
        self.hp -= dmg


    def knockback(self, entity_pos, force=50):
        """
        Apply knockback away from the player
        """
        direction = self.pos - entity_pos
        direction.normalize_ip()
        self.pos += direction * force


    def handle_death(self, enemies):
        """
        Handle enemy death
        """
        if self.hp <= 0:
            self.die(enemies)


    def die(self, enemies):
        """
        Remove the enemy from the game
        """
        enemies.remove(self)


    def handle_display(self, screen):
        """
        Draw the enemy
        """
        pygame.draw.circle(screen, "red", self.pos, self.radius)
    
    
    def draw_with_offset(self, screen, offset_x, offset_y):
        """
        Draw the enemy with offset
        """
        pygame.draw.circle(screen, "red", self.pos - pygame.Vector2(offset_x, offset_y), self.radius)