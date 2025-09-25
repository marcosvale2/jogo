from pgzero.actor import Actor
from pygame import Rect
from config import GRAVITY

class Enemy:
    def __init__(self, start_pos, patrol_range):
        self.animations = {
            "run_right": ["enemy_run_right_1", "enemy_run_right_2", "enemy_run_right_3", "enemy_run_right_4"],
            "run_left": ["enemy_run_left_1", "enemy_run_left_2", "enemy_run_left_3", "enemy_run_left_4"]
        }
        self.current_animation = "run_right"
        self.frame_index = 0
        self.frame_timer = 0

        self.actor = Actor(self.animations[self.current_animation][0], pos=start_pos)

        self.vx = 2
        self.vy = 0
        self.patrol_range = patrol_range
        self.rect = Rect(self.actor.x - 15, self.actor.y - 15, 15, 15)

    def update(self, platforms):
        self.rect.x += self.vx
        if self.rect.left < self.patrol_range[0] or self.rect.right > self.patrol_range[1]:
            self.vx *= -1
            self.current_animation = "run_left" if self.vx < 0 else "run_right"

        self.vy += GRAVITY
        self.rect.y += self.vy

        for plat_data in platforms:
            plat = plat_data["rect"]
            if self.rect.colliderect(plat) and self.vy >= 0:
                self.rect.bottom = plat.top
                self.vy = 0

        self.actor.x = self.rect.centerx
        self.actor.y = self.rect.centery

        # Animação
        self.frame_timer += 1
        if self.frame_timer >= 15:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.actor.image = self.animations[self.current_animation][self.frame_index]

    def draw(self, offset_x=0, offset_y=0):
        self.actor.x = self.rect.centerx + offset_x
        self.actor.y = self.rect.centery + offset_y
        self.actor.draw()
