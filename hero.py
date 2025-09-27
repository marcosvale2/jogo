from pgzero.actor import Actor
from pygame import Rect
from config import GRAVITY, PLAYER_SPEED, JUMP_STRENGTH, INVINCIBILITY_TIME
import time

class Hero:
    def __init__(self, start_pos):
        # --- Animações ---
        self.animations = {
            "idle": [f"player/player_idle_{i}" for i in range(1, 14)],
            "pre_idle": ["player/player_idle_1", "player/player_idle_2"],
            "run_left": [f"player/player_run_left_{i}" for i in range(1, 7)],
            "run_right": [f"player/player_run_right_{i}" for i in range(1, 7)],
            "run_fast_left": [f"player/transform/player_run_left_turbo_{i}" for i in range(1, 7)],
            "run_fast_right": [f"player/transform/player_run_right_turbo_{i}" for i in range(1, 7)],
            "transform_left": [f"player/transform/turbo{i}" for i in range(1, 9)],
            "transform_right": [f"player/transform/turbo{i}" for i in range(1, 9)],
            "idle_turbo_left": [f"player/transform/idle_turbo_left_{i}" for i in range(1, 7)],
            "idle_turbo_right": [f"player/transform/idle_turbo_right_{i}" for i in range(1, 7)],
            "attack_left": [f"player/player_attack_left_{i}" for i in range(1, 3)],
            "attack_right": [f"player/player_attack_right_{i}" for i in range(1, 3)],
            "attack_turbo_left": [f"player/transform/attack_turbo_left_{i}" for i in range(1, 3)],
            "attack_turbo_right": [f"player/transform/attack_turbo_right_{i}" for i in range(1, 3)],
        }
        self.current_animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.actor = Actor(self.animations[self.current_animation][0], pos=start_pos)

        # --- Física ---
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.rect = Rect(self.actor.x - 15, self.actor.y - 100, 30, 100)

        # --- Estado ---
        self.lives = 5
        self.invincible_timer = 0
        self.state = "normal"  # normal, transform, turbo
        self.direction = "right"
        self.turbo_start = 0
        self.turbo_duration = 3.0
        self.idle_timer = 0
        self.idle_delay = 3.0
        self.pre_idle_played = False

        # --- Ataque ---
        self.attacking = False
        self.attack_frame_index = 0
        self.attack_timer = 0

    def take_damage(self):
        if self.invincible_timer <= 0:
            self.lives -= 1
            self.invincible_timer = INVINCIBILITY_TIME
            try:
                sounds.hit.play()
            except:
                pass

    def set_animation(self, name):
        if self.current_animation != name:
            self.current_animation = name
            self.frame_index = 0
            self.frame_timer = 0
            self.actor.image = self.animations[name][0]

    def update(self, platforms, keys):
        # --- Transform ---
        if self.state == "transform":
            self.vx = 0
            self.invincible_timer = 10
            self.frame_timer += 1
            if self.frame_timer >= 8:
                self.frame_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.animations[self.current_animation]):
                    self.state = "turbo"
                    self.turbo_start = time.time()
                    self.set_animation(f"idle_turbo_{self.direction}")
                else:
                    self.actor.image = self.animations[self.current_animation][self.frame_index]
            return

        # --- Turbo ---
        elif self.state == "turbo":
            self.invincible_timer = 10
            if time.time() - self.turbo_start > self.turbo_duration:
                self.state = "normal"
                self.set_animation("idle")

            speed = PLAYER_SPEED * 2
            self.vx = 0
            if keys.left:
                self.vx = -speed
                self.direction = "left"
                if not self.attacking:
                    self.set_animation("run_fast_left")
            elif keys.right:
                self.vx = speed
                self.direction = "right"
                if not self.attacking:
                    self.set_animation("run_fast_right")
            else:
                if not self.attacking:
                    self.set_animation(f"idle_turbo_{self.direction}")

            if keys.space and self.on_ground:
                self.vy = -JUMP_STRENGTH
                self.on_ground = False
                try:
                    sounds.jump.play()
                except:
                    pass

        # --- Normal ---
        else:
            speed = PLAYER_SPEED
            self.vx = 0
            running = keys.lshift or keys.rshift

            if keys.left:
                self.vx = -speed
                self.direction = "left"
                if not self.attacking:
                    self.set_animation("run_left")
            elif keys.right:
                self.vx = speed
                self.direction = "right"
                if not self.attacking:
                    self.set_animation("run_right")
            else:
                self.vx = 0
                if self.on_ground and not self.attacking:
                    self.idle_timer += 1 / 60
                    if self.idle_timer >= self.idle_delay:
                        self.set_animation("idle")
                    elif not self.pre_idle_played:
                        self.set_animation("pre_idle")
                        self.pre_idle_played = True
                else:
                    self.idle_timer = 0
                    self.pre_idle_played = False

            if running and self.on_ground and not self.attacking:
                self.state = "transform"
                self.set_animation(f"transform_{self.direction}")
                return

            if keys.space and self.on_ground:
                self.vy = -JUMP_STRENGTH
                self.on_ground = False
                self.idle_timer = 0
                self.pre_idle_played = False
                try:
                    sounds.jump.play()
                except:
                    pass

        # --- Ataque ---
        if keys.z and not self.attacking:
            self.attacking = True
            self.attack_frame_index = 0
            self.attack_timer = 0

            # Escolhe animação de ataque dependendo do estado
            if self.state in ["transform", "turbo"]:
                self.set_animation(f"attack_turbo_{self.direction}")
            else:
                self.set_animation(f"attack_{self.direction}")

            try:
                sounds.attack.play()
            except:
                pass

        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer >= 5:
                self.attack_timer = 0
                self.attack_frame_index += 1
                if self.attack_frame_index >= len(self.animations[self.current_animation]):
                    self.attacking = False
                    # Volta para animação normal
                    if self.state == "normal":
                        if self.vx == 0:
                            self.set_animation("idle")
                        else:
                            self.set_animation(f"run_{self.direction}")
                    elif self.state == "turbo":
                        self.set_animation(f"idle_turbo_{self.direction}")
                else:
                    self.actor.image = self.animations[self.current_animation][self.attack_frame_index]

        # --- Física ---
        self.vy += GRAVITY

        # Move X
        self.rect.x += self.vx
        for plat_data in platforms:
            plat = plat_data["rect"]
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                elif self.vx < 0:
                    self.rect.left = plat.right

        # Move Y
        self.rect.y += self.vy
        self.on_ground = False
        for plat_data in platforms:
            plat = plat_data["rect"]
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                    self.vy = 0

        # Atualiza Actor
        self.actor.x = self.rect.centerx
        self.actor.y = self.rect.centery

        # Atualiza animação normal
        self.frame_timer += 1
        if self.frame_timer >= 10 and not self.attacking:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.actor.image = self.animations[self.current_animation][self.frame_index]

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw(self, offset_x=0, offset_y=0):
        if self.invincible_timer > 0 and (self.invincible_timer // 3) % 2 == 0:
            return
        self.actor.x = self.rect.centerx + offset_x
        self.actor.y = self.rect.centery + offset_y
        self.actor.draw()
