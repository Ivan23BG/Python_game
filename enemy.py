import pygame
import random
from typing import List, Union
from game_object import GameObject


class Enemy(GameObject):
    """
    Represents an enemy in the game, including movement, collision handling, 
    health management, and rendering.

    Attributes:
        pos (pygame.Vector2): The current position of the enemy.
        radius (int): The radius of the enemy's representation.
        speed (float): The speed of the enemy's movement.
        dmg (int): The damage dealt by the enemy to the player.
        hp (int): The current health points of the enemy.
    """

    def __init__(self, x: float, y: float, radius: int) -> None:
        """
        Initializes an Enemy object with a position, radius, speed, damage, and health.

        Args:
            x (float): The x-coordinate of the enemy's position.
            y (float): The y-coordinate of the enemy's position.
            radius (int): The radius of the enemy.
        """
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.speed = 200 / 60  # Speed per frame
        self.dmg = 10
        self.hp = 50


    def update(self, player: "Player", enemies: List["Enemy"], screen: pygame.Surface) -> None:
        """
        Updates the enemy's state, including movement, collisions, and death handling.

        Args:
            player (Player): The player object.
            enemies (List[Enemy]): The list of all enemies in the game.
            screen (pygame.Surface): The game screen surface.
        """
        self.handle_movement(player)
        self.handle_collision(player, enemies)
        self.handle_death(enemies)


    def handle_movement(self, player: "Player") -> None:
        """
        Handles the movement logic of the enemy to chase the player.

        Args:
            player (Player): The player object.
        """
        self.chase_player(player.pos)


    def chase_player(self, player_pos: pygame.Vector2) -> None:
        """
        Moves the enemy toward the player's position.

        Args:
            player_pos (pygame.Vector2): The position of the player.
        """
        direction = player_pos - self.pos
        direction.normalize_ip()
        self.pos += direction * self.speed


    def handle_collision(self, player: "Player", enemies: List["Enemy"]) -> None:
        """
        Handles collisions with the player and other enemies.

        Args:
            player (Player): The player object.
            enemies (List[Enemy]): The list of all enemies in the game.
        """
        if self.check_collision(player):
            player.take_damage(self.dmg)
            self.take_damage(10)
            self.knockback(player.pos)

        for enemy in enemies:
            if enemy != self and self.check_collision(enemy):
                self.knockback(enemy.pos, 10)


    def check_collision(self, entity: Union["Player", "Enemy"]) -> bool:
        """
        Checks if the enemy collides with another entity.

        Args:
            entity (Union[Player, Enemy]): The other entity to check collision with.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        return (self.pos - entity.pos).length() < self.radius + entity.radius


    def take_damage(self, dmg: int) -> None:
        """
        Reduces the enemy's health by a specified amount.

        Args:
            dmg (int): The damage amount to inflict on the enemy.
        """
        self.hp -= dmg


    def knockback(self, entity_pos: pygame.Vector2, force: float = 50) -> None:
        """
        Moves the enemy away from another entity as a result of a collision.

        Args:
            entity_pos (pygame.Vector2): The position of the other entity.
            force (float): The force of the knockback. Defaults to 50.
        """
        direction = self.pos - entity_pos
        direction.normalize_ip()
        self.pos += direction * force


    def handle_death(self, enemies: List["Enemy"]) -> None:
        """
        Checks if the enemy's health is zero or below and removes it from the game.

        Args:
            enemies (List[Enemy]): The list of all enemies in the game.
        """
        if self.hp <= 0:
            self.die(enemies)


    def die(self, enemies: List["Enemy"]) -> None:
        """
        Removes the enemy from the game.

        Args:
            enemies (List[Enemy]): The list of all enemies in the game.
        """
        enemies.remove(self)


    def handle_display(self, screen: pygame.Surface) -> None:
        """
        Renders the enemy as a red circle on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        pygame.draw.circle(screen, "red", self.pos, self.radius)


    def draw_with_offset(self, screen: pygame.Surface, offset_x: float, offset_y: float) -> None:
        """
        Draws the enemy with an offset, useful for camera systems.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset_x (float): The horizontal offset.
            offset_y (float): The vertical offset.
        """
        pygame.draw.circle(screen, "red", self.pos - pygame.Vector2(offset_x, offset_y), self.radius)
