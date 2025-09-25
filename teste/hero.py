from pgzero.actor import Actor
from pygame import Rect
from config import GRAVITY, PLAYER_SPEED, JUMP_STRENGTH, INVINCIBILITY_TIME

class Hero:
    def __init__(self, start_pos):
        self.animations = {
            "idle": ["player_idle_1", "player_idle_2", "player_idle_3", "player_idle_4", "player_idle_5"],
            "run_laft": ["player_run_laft_1", "player_run_laft_2", "player_run_laft_3"],
            "run_right": ["player_run_right_1", "player_run_rigth_2", "player_run_rigth_3"]
        }
        self.current_animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0

        self.actor = Actor(self.animations[self.current_animation][0], pos=start_pos)

        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.lives = 5
        self.invincible_timer = 0

        self.rect = Rect(self.actor.x - 15, self.actor.y - 100, 30, 100)

    def update(self, platforms, keys):
        # Movimento horizontal
        self.vx = 0
        if keys.left:
            self.vx = -PLAYER_SPEED
            self.current_animation = "run_laft"
        elif keys.right:
            self.vx = PLAYER_SPEED
            self.current_animation = "run_right"
        else:
            self.current_animation = "idle"
        self.rect.x += self.vx

        # Pulo
        if keys.space and self.on_ground:
            self.vy = -JUMP_STRENGTH
            self.on_ground = False

        # Gravidade
        self.vy += GRAVITY
        self.rect.y += self.vy

        # Colisão com plataformas
        self.on_ground = False
        for plat_data in platforms:
            plat = plat_data["rect"]
            if self.rect.colliderect(plat) and self.vy >= 0:
                self.rect.bottom = plat.top
                self.vy = 0
                self.on_ground = True

        # Atualizar actor
        self.actor.x = self.rect.centerx
        self.actor.y = self.rect.centery

        # Animação
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.actor.image = self.animations[self.current_animation][self.frame_index]

        # Invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def take_damage(self):
        if self.invincible_timer == 0:
            self.lives -= 1
            self.invincible_timer = INVINCIBILITY_TIME

    def draw(self, offset_x=0, offset_y=0):
        self.actor.x = self.rect.centerx + offset_x
        self.actor.y = self.rect.centery + offset_y
        self.actor.draw()
