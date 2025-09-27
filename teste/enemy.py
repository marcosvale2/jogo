from pgzero.actor import Actor
from pygame import Rect
from config import GRAVITY
import random

class Enemy:
    def __init__(self, start_pos, patrol_range, speed=2):
        self.actor = Actor("enemy_run_right_1", pos=start_pos)
        self.vy = 0

        # Ajuste do range mínimo
        patrol_start, patrol_end = patrol_range
        if patrol_end - patrol_start < 100:
            mid = (patrol_start + patrol_end) // 2
            patrol_start = mid - 50
            patrol_end = mid + 50
        self.patrol_range = (patrol_start, patrol_end)

        # Velocidade inicial aleatória
        self.vx = speed if random.choice([True, False]) else -speed

        # Rect para colisão
        self.rect = Rect(self.actor.x - 15, self.actor.y - 15, 30, 30)

        # Animações
        self.animations = {
            "run_right": [
                "enemy_run_right_1", "enemy_run_right_2",
                "enemy_run_right_3", "enemy_run_right_4"
            ],
            "run_left": [
                "enemy_run_left_1", "enemy_run_left_2",
                "enemy_run_left_3", "enemy_run_left_4"
            ],
            # opcional, se quiser animação de hit
            "hit": ["enemy_run_right_1"]
        }
        self.current_animation = "run_right" if self.vx > 0 else "run_left"
        self.frame_index = 0
        self.frame_timer = 0

        # Vida e controle de morte
        self.hit_points = 3
        self.kill = False

    def take_hit(self, direction):
        """O inimigo leva dano, é empurrado e pode morrer"""
        self.hit_points -= 1
        push = 50
        if direction == "right":
            self.rect.x += push
        else:
            self.rect.x -= push

        # Trocar para animação de hit se existir
        if "hit" in self.animations:
            self.current_animation = "hit"
            self.frame_index = 0
            self.frame_timer = 0
            self.actor.image = self.animations[self.current_animation][0]

        # Se morrer
        if self.hit_points <= 0:
            self.kill = True

    def update(self, platforms, enemies=None):
        if self.kill:
            return

        # --- Horizontal movement ---
        self.rect.x += self.vx

        # Patrulha (limites do range)
        if self.rect.left < self.patrol_range[0] or self.rect.right > self.patrol_range[1]:
            self.vx *= -1
            self.current_animation = "run_left" if self.vx < 0 else "run_right"

        # --- Gravidade ---
        self.vy += GRAVITY
        self.rect.y += self.vy

        # --- Collision with platforms ---
        for plat_data in platforms:
            plat = plat_data["rect"]
            if self.rect.colliderect(plat) and self.vy >= 0:
                self.rect.bottom = plat.top
                self.vy = 0

        # --- Collision with other enemies ---
        if enemies:
            for other in enemies:
                if other is not self and self.rect.colliderect(other.rect):
                    if self.vx > 0:
                        self.rect.right = other.rect.left
                    else:
                        self.rect.left = other.rect.right
                    self.vx *= -1
                    self.current_animation = "run_left" if self.vx < 0 else "run_right"

        # --- Update actor position ---
        self.actor.x = self.rect.centerx
        self.actor.y = self.rect.centery

        # --- Animation ---
        self.frame_timer += 1
        if self.frame_timer >= 15:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.actor.image = self.animations[self.current_animation][self.frame_index]

    def draw(self, offset_x=0, offset_y=0):
        if self.kill:
            return
        self.actor.x = self.rect.centerx + offset_x
        self.actor.y = self.rect.centery + offset_y
        self.actor.draw()
