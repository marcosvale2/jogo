import pgzrun
from config import WIDTH, HEIGHT, FLOOR_HEIGHT
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

        # Carrega plataformas e inimigos
        self.platforms = [plat.copy() for plat in level_platforms]
        self.enemies = [Enemy(e["pos"], e["patrol"]) for e in level_enemies]

        # Jogador
        floor_rect = self.platforms[0]["rect"]
        self.player = Hero((150, floor_rect.top - 50))
        self.player.lives = 5
        self.player.rect.bottom = floor_rect.top

        # Posicionar inimigos no chão
        for enemy in self.enemies:
            enemy.rect.bottom = floor_rect.top

        self.invincible_timer = 0
        self.camera_x = 0
        self.camera_y = 0

    def update(self, keys):
        if self.state == "MENU":
            self.menu.update()
            return

        self.player.update(self.platforms, keys)
        for enemy in self.enemies:
            enemy.update(self.platforms)

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # Colisão com inimigos
        if self.invincible_timer <= 0:
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.player.lives -= 1
                    self.invincible_timer = 60
                    floor_rect = self.platforms[0]["rect"]
                    self.player.rect.bottom = floor_rect.top
                    self.player.rect.centerx = 150 + self.camera_x
                    self.player.vx = 0
                    self.player.vy = 0
                    break

        if self.player.lives <= 0:
            self.state = "MENU"

        # Atualiza câmera: segue o jogador horizontal e verticalmente
        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_y = self.player.rect.centery - HEIGHT // 2

    def draw(self, screen):
        if self.state == "MENU":
            self.menu.draw(screen)
            return

        screen.clear()
        offset_x = -self.camera_x
        offset_y = -self.camera_y

        bg = images.background
    # repete ou apenas desenha a imagem, ajustando à câmera
        screen.blit("background", (offset_x, offset_y))
    
        # Desenha plataformas e chão com repetição de textura
        for plat_data in self.platforms:
            rect = plat_data["rect"]
            texture_name = plat_data["texture"]
            img = getattr(images, texture_name)
            img_width = img.get_width()

            start_x = rect.x
            end_x = rect.x + rect.width
            x = start_x
            while x < end_x:
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


# --- Inicializa o jogo ---
game = Game()

def draw():
    game.draw(screen)

def update():
    game.update(keyboard)

def on_mouse_down(pos):
    game.on_mouse_down(pos)

pgzrun.go()
