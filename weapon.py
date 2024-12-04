import random
import pygame
from typing import List, Optional
from game_object import GameObject
from projectile import Projectile
from enemy import Enemy


class Weapon:
    """
    Represents a weapon used by the player to attack enemies.

    Attributes:
        cooldown (float): Time in seconds between shots.
        last_shot_time (float): Time when the last shot was fired.
    """

    def __init__(self, cooldown: float = 0.5) -> None:
        self.cooldown = cooldown
        self.last_shot_time = 0


    def can_shoot(self, current_time: float) -> bool:
        """
        Determines if the weapon can shoot based on cooldown.

        Args:
            current_time (float): The current game time.

        Returns:
            bool: True if the weapon can shoot, False otherwise.
        """
        return current_time - self.last_shot_time >= self.cooldown


    def shoot(self, player: "Player", projectiles: list, current_time: float) -> None:
        """
        Fires a projectile from the player if possible.

        Args:
            player (Player): The player object.
            projectiles (list): The list to store fired projectiles.
            current_time (float): The current game time.
        """
        if self.can_shoot(current_time):
            direction = pygame.Vector2(1, 0).rotate(random.uniform(-15, 15))  # Example spread
            projectiles.append(Projectile(player.pos, direction))
            self.last_shot_time = current_time
