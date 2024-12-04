import pygame
import random
from typing import List
from enemy import Enemy
import math

class Enemies:
    """
    Manages a collection of enemies in the game.

    Attributes:
        enemies (List[Enemy]): The list of currently active enemies.
        max_enemies (int): The maximum number of enemies allowed in the game.
        spawn_rate (float): The probability of spawning a new enemy each tick.
    """

    def __init__(self) -> None:
        """
        Initializes an Enemies manager with default values.
        """
        self.enemies: List[Enemy] = []
        self.max_enemies: int = 20
        self.spawn_rate: float = 1 / 60  # Percent chance per frame.


    def add(self, enemy: Enemy) -> None:
        """
        Adds a new enemy to the collection.

        Args:
            enemy (Enemy): The enemy to add.
        """
        self.enemies.append(enemy)


    def remove(self, enemy: Enemy) -> None:
        """
        Removes an enemy from the collection.

        Args:
            enemy (Enemy): The enemy to remove.
        """
        self.enemies.remove(enemy)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all enemies on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        for enemy in self.enemies:
            enemy.handle_display(screen)


    def draw_with_offset(self, screen: pygame.Surface, offset: pygame.Vector2) -> None:
        """
        Draws all enemies with an offset, useful for camera systems.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset (pygame.Vector2): The offset to apply.
        """
        for enemy in self.enemies:
            enemy.draw_with_offset(screen, offset.x, offset.y)


    def spawn(self, player: "Player") -> None:
        """
        Spawns a new enemy if the maximum number of enemies is not reached
        and the random spawn condition is met.
        """
        if len(self.enemies) < self.max_enemies:
            if random.random() < self.spawn_rate:
                # Generate random spawn position and attributes
                radius = 200  # Distance from player
                angle = random.uniform(0, 2 * math.pi)
                distance = math.sqrt(random.uniform(0, 1)) * radius + 100  # Random distance from player

                # Convert polar coordinates to Cartesian
                x = distance * math.cos(angle) + player.pos.x
                y = distance * math.sin(angle) + player.pos.y
                
                new_enemy = Enemy(x, y, 20)
                self.add(new_enemy)


    def update(self, player: "Player") -> None:
        """
        Updates all enemies, including movement, collisions, and death handling.

        Args:
            player (Player): The player object.
        """
        for enemy in self.enemies[:]:  # Use a copy to avoid iteration issues during removal
            enemy.update(player, self.enemies, None)
