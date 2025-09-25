import pgzrun
from config import WIDTH, HEIGHT
from hero import Hero
from enemy import Enemy
from menu import Menu
from level_data import platforms as level_platforms, enemies as level_enemies
from pygame import Rect

class Game:
    def __init__(self):
        self.state = "MENU"
        self.menu = Menu()
        self.player = None
        self.enemies = []
        self.platforms = []
        self.camera_x = 0
        self.camera_y = 0

    def start_game(self):
        self.state = "GAME"
        self.platforms = [plat.copy() for plat in level_platforms]
        self.enemies = [Enemy(e["pos"], e["patrol"], e.get("speed", 2)) for e in level_enemies]

        if not self.platforms:
            return  # evita crash se não houver plataformas

        # Inicializa jogador
        floor_rect = self.platforms[0]["rect"]
        self.player = Hero((150, floor_rect.top - 50))
        self.player.lives = 5
        self.player.rect.bottom = floor_rect.top

        # Posicionar inimigos no chão ou plataformas
        for enemy, e_data in zip(self.enemies, level_enemies):
            plat_idx = e_data.get("platform_index", None)
            if plat_idx is not None:
                plat_rect = self.platforms[plat_idx]["rect"]
                enemy.rect.bottom = plat_rect.top
            else:
                enemy.rect.bottom = floor_rect.top

        self.camera_x = 0
        self.camera_y = 0

    def update(self, keys):
        if self.state == "MENU":
            self.menu.update()
            return

        self.player.update(self.platforms, keys)
        for enemy in self.enemies:
            enemy.update(self.platforms)

        # Colisão com inimigos
        if self.player.invincible_timer <= 0:
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.player.take_damage()
                    break

        # Game over
        if self.player.lives <= 0:
            self.state = "MENU"

        # Câmera segue o jogador
        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_y = self.player.rect.centery - HEIGHT // 2

    def draw(self, screen):
        if self.state == "MENU":
            self.menu.draw(screen)
            return

        # Fundo infinito/tiled
        bg_width = images.background.get_width()
        bg_height = images.background.get_height()
        tiles_x = (WIDTH // bg_width) + 2
        tiles_y = (HEIGHT // bg_height) + 2

        for i in range(tiles_x):
            for j in range(tiles_y):
                x = (i * bg_width) - (self.camera_x % bg_width)
                y = (j * bg_height) - (self.camera_y % bg_height)
                screen.blit("background3", (x, y))

        offset_x = -self.camera_x
        offset_y = -self.camera_y

        # Plataformas
        for plat_data in self.platforms:
            rect = plat_data["rect"]
            texture_name = plat_data["texture"]
            img = getattr(images, texture_name)
            img_width = img.get_width()
            x = rect.x
            while x < rect.x + rect.width:
                screen.blit(texture_name, (x + offset_x, rect.y + offset_y))
                x += img_width

        # Vidas
        for i in range(self.player.lives):
            life_rect = Rect(10 + i*35, 10, 30, 30)
            screen.draw.filled_rect(life_rect, "red")

        # Jogador e inimigos
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


# Inicializa jogo
game = Game()

def draw():
    game.draw(screen)

def update():
    game.update(keyboard)

def on_mouse_down(pos):
    game.on_mouse_down(pos)

pgzrun.go()
