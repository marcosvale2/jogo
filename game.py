# game.py
import pgzrun
import time
from hero import Hero
from enemy import Enemy
from menu import Menu
from level_data import platforms as level_platforms, enemies as level_enemies
from config import WIDTH, HEIGHT
from pygame import Rect


# --- Game class ---
class Game:
    def __init__(self):
        self.state = "MENU"
        self.menu = Menu()
        self.player = None
        self.enemies = []
        self.platforms = []
        self.camera_x = 0
        self.camera_y = 0
        self.music_playing = False
        self.death_played = False

    def draw_background(self, screen):
        """Desenha o fundo contínuo pelo mapa todo"""
        try:
            img_width, img_height = images.background.get_size()
            start_x = -self.camera_x % img_width - img_width
            start_y = -self.camera_y % img_height - img_height

            x = start_x
            while x < WIDTH:
                y = start_y
                while y < HEIGHT:
                    screen.blit("background", (x, y))
                    y += img_height
                x += img_width
        except:
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (135, 206, 235))

    def start_game(self):
        self.state = "GAME"
        self.platforms = [plat.copy() for plat in level_platforms]
        self.enemies = [Enemy(e["pos"], e["patrol"], e.get("speed", 2)) for e in level_enemies]
        self.death_played = False

        if not self.platforms:
            return

        floor_rect = self.platforms[0]["rect"]
        self.player = Hero((150, floor_rect.top - 50))
        self.player.lives = 5
        self.player.rect.bottom = floor_rect.top

        for enemy, e_data in zip(self.enemies, level_enemies):
            plat_idx = e_data.get("platform_index", None)
            if plat_idx is not None:
                plat_rect = self.platforms[plat_idx]["rect"]
                enemy.rect.bottom = plat_rect.top
            else:
                enemy.rect.bottom = floor_rect.top

        self.camera_x = 0
        self.camera_y = 0

        if not self.music_playing:
            try:
                music.play("background")
                music.set_volume(0.5)
                self.music_playing = True
            except:
                print("Erro: música de fundo não encontrada na pasta sounds!")

    def toggle_music(self):
        if self.music_playing:
            music.stop()
            self.music_playing = False
        else:
            try:
                music.play("background")
                music.set_volume(0.5)
                self.music_playing = True
            except:
                print("Erro: música de fundo não encontrada na pasta sounds!")

    def update(self, keys):
        if self.state == "MENU":
            self.menu.update()
            return

        player_was_alive = self.player.lives > 0
        self.player.update(self.platforms, keys)

        for enemy in self.enemies:
            enemy.update(self.platforms, self.enemies)

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.attacking:
                    enemy.take_hit(self.player.direction)
                    try:
                        sounds.attack.play()
                    except:
                        pass
                elif self.player.invincible_timer <= 0:
                    self.player.take_damage()
                    if self.player.lives <= 0 and player_was_alive:
                        try:
                            sounds.death.play()
                        except:
                            pass

        self.enemies = [e for e in self.enemies if not getattr(e, "kill", False)]

        if self.player.rect.top > HEIGHT + 100:
            if not self.death_played:
                try:
                    sounds.death.play()
                except:
                    pass
                self.death_played = True
            self.state = "MENU"

        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_y = self.player.rect.centery - HEIGHT // 2

    def draw(self, screen):
        if self.state == "MENU":
            self.menu.draw(screen)
            return

        offset_x = -self.camera_x
        offset_y = -self.camera_y

        # --- Fundo contínuo ---
        self.draw_background(screen)

        # --- Plataformas com texturas repetidas ---
        for plat_data in self.platforms:
            rect = plat_data["rect"]
            texture_name = plat_data["texture"]
            try:
                # largura de cada bloco de textura
                texture_width = 50
                # repetir a textura ao longo da plataforma
                for x in range(rect.x, rect.x + rect.width, texture_width):
                    screen.blit(texture_name, (x + offset_x, rect.y + offset_y))
            except:
                screen.draw.filled_rect(Rect(rect.x + offset_x, rect.y + offset_y, rect.width, rect.height), "gray")

        # --- Vidas ---
        for i in range(self.player.lives):
            screen.draw.filled_rect(Rect(10 + i*35, 10, 30, 30), "red")

        # --- Herói e inimigos ---
        self.player.draw(offset_x, offset_y)
        for enemy in self.enemies:
            enemy.draw(offset_x, offset_y)

    def on_mouse_down(self, pos):
        if self.state == "MENU":
            action = self.menu.check_click(pos)
            if action == "start":
                self.start_game()
            elif action == "exit":
                quit()
            elif action == "music_toggle":
                self.toggle_music()

# --- Init game ---
game = Game()

def draw():
    game.draw(screen)

def update():
    game.update(keyboard)

def on_mouse_down(pos):
    game.on_mouse_down(pos)

pgzrun.go()
