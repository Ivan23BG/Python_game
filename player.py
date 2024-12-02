import pygame
import sys

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(1280/2, 720/2)
        self.radius = 40
        self.speed = 500
        self.max_hp = 100
        self.hp = self.max_hp
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 10


    def handle_xp(self, orb):
        self.xp += orb.xp
        if self.xp >= self.xp_to_next_level:
            self.level_up()


    def update(self, keys, dt, screen):
        self.handle_movement(keys, dt)


    def handle_movement(self, keys, dt):
        move_x, move_y = self.move(keys, dt)
        self.pos += pygame.Vector2(move_x, move_y)


    def move(self, keys, dt):
        move_x, move_y = 0, 0
        if keys[pygame.K_z] or keys[pygame.K_w]:
            move_y = -self.speed * dt
        if keys[pygame.K_s]:
            move_y = self.speed * dt
        if keys[pygame.K_q] or keys[pygame.K_a]:
            move_x = -self.speed * dt
        if keys[pygame.K_d]:
            move_x = self.speed * dt
        return move_x, move_y

    def level_up(self):
        print("leveled up")
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level *= 1.5
        self.max_hp += 10
        self.hp = self.max_hp
        
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            print("Player died!")
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, self.radius)

    def draw_with_offset(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, "white", self.pos - pygame.Vector2(offset_x, offset_y), self.radius)