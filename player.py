import pygame
import sys
from typing import Dict, Union
from game_object import GameObject
from weapon import Weapon


class Player(GameObject):
    """
    Represents the player in a game, including movement, experience, level progression, 
    health management, and rendering.

    Attributes:
        pos (pygame.Vector2): The current position of the player.
        radius (int): The radius of the player's representation.
        speed (int): The speed of the player's movement.
        max_hp (int): The maximum health points of the player.
        hp (int): The current health points of the player.
        xp (int): The current experience points of the player.
        level (int): The player's current level.
        xp_to_next_level (float): The experience points required to reach the next level.
    """

    def __init__(self) -> None:
        """
        Initializes a Player object with default attributes.
        """
        self.pos = pygame.Vector2(1280 / 2, 720 / 2)
        self.radius = 40
        self.speed = 300
        self.max_hp = -1
        self.hp = self.max_hp
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 10.0
        self.weapon = Weapon()


    def handle_xp(self, orb: "Orb") -> None:
        """
        Handles experience gain and checks if the player can level up.

        Args:
            orb (Orb): The orb object that grants experience points.
        """
        self.add_xp(orb.xp)
        self.try_level_up()


    def add_xp(self, xp: int) -> None:
        """
        Adds experience points to the player.

        Args:
            xp (int): The amount of experience points to add.
        """
        self.xp += xp
        self.try_level_up()


    def try_level_up(self) -> None:
        """
        Checks if the player has enough experience points to level up 
        and levels up if conditions are met.
        """
        while self.xp >= self.xp_to_next_level:
            self.level_up()


    def level_up(self) -> None:
        """
        Levels up the player, increasing level, adjusting experience, 
        and increasing maximum health.
        """
        print("leveled up")
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level *= 1.1
        self.max_hp += 50
        # self.hp = self.max_hp


    def update(self, keys: Dict[int, bool], dt: float, screen: pygame.Surface) -> None:
        """
        Updates the player's state, including movement.

        Args:
            keys (Dict[int, bool]): The current state of keyboard keys.
            dt (float): The delta time since the last frame.
            screen (pygame.Surface): The game screen surface.
        """
        self.handle_movement(keys, dt)


    def handle_movement(self, keys: Dict[int, bool], dt: float) -> None:
        """
        Handles the movement logic of the player.

        Args:
            keys (Dict[int, bool]): The current state of keyboard keys.
            dt (float): The delta time since the last frame.
        """
        move = self.move(keys, dt)
        self.pos += move


    def move(self, keys: Dict[int, bool], dt: float) -> pygame.Vector2:
        """
        Calculates the player's movement vector based on input keys and delta time.

        Args:
            keys (Dict[int, bool]): The current state of keyboard keys.
            dt (float): The delta time since the last frame.

        Returns:
            pygame.Vector2: The movement vector for the player.
        """
        move_x, move_y = 0, 0
        if keys[pygame.K_z] or keys[pygame.K_w]:
            move_y = -self.speed * dt
        if keys[pygame.K_s]:
            move_y = self.speed * dt
        if keys[pygame.K_q] or keys[pygame.K_a]:
            move_x = -self.speed * dt
        if keys[pygame.K_d]:
            move_x = self.speed * dt
        return pygame.Vector2(move_x, move_y)


    def take_damage(self, dmg: int) -> None:
        """
        Reduces the player's health by a specified amount and checks for player death.

        Args:
            dmg (int): The damage amount to inflict on the player.
        """
        if self.hp > 0:
            self.hp = max(self.hp - dmg, 0)
        if self.hp == 0:
            print("Player died!")
            pygame.quit()
            sys.exit()


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the player as a circle on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        pygame.draw.circle(screen, "white", self.pos, self.radius)

    def draw_with_offset(self, screen: pygame.Surface, offset_x: float, offset_y: float) -> None:
        """
        Draws the player with an offset, useful for camera systems.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset_x (float): The horizontal offset.
            offset_y (float): The vertical offset.
        """
        pygame.draw.circle(screen, "white", self.pos - pygame.Vector2(offset_x, offset_y), self.radius)
