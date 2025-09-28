import pgzrun
from pgzero import clock
from hero import Hero
from enemy import Enemy
from menu import Menu
from level_data import platforms as level_platforms, enemies as level_enemies
import level_data2
from config import WIDTH, HEIGHT
from pygame import Rect

class AudioZone:
    def __init__(self, rect, sound_name):
        self.rect = rect
        self.sound_name = sound_name
        self.activated = False
        self.playing = False
        self.started_at = 0
        self.duration = 3.0  # fallback duration

class Game:
    def __init__(self):
        # Botão de música durante o jogo
        self.music_button_actor = Actor("music_icon", pos=(WIDTH - 50, 50))
        self.music_hitbox_in_game = Rect(WIDTH - 75, 25, 50, 50)
        self.state = "MENU"
        self.menu = Menu()
        self.player = None
        self.enemies = []
        self.platforms = []
        self.camera_x = 0
        self.camera_y = 0
        self.music_playing = False
        self.death_played = False

        self.audio_zone = AudioZone(Rect(2000, 480, 150, 40), "fim")

    def draw_background(self, screen):
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
        self.menu.show_thank_you = False

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

        try:
            music.stop()
            music.play("background")
            music.set_volume(0.25)
            self.music_playing = True
        except:
            print("Erro: música de fundo não encontrada!")

    def toggle_music(self):
        if self.music_playing:
            music.stop()
            self.music_playing = False
        else:
            try:
                music.play("background")
                music.set_volume(0.25)
                self.music_playing = True
            except:
                print("Erro: música de fundo não encontrada!")

    def load_level2(self):
        self.platforms = [plat.copy() for plat in level_data2.platforms]
        self.enemies = [Enemy(e["pos"], e["patrol"], e.get("speed", 2)) for e in level_data2.enemies]
        floor_rect = self.platforms[0]["rect"]
        self.player.rect.bottom = floor_rect.top
        self.player.rect.x = floor_rect.x + 50
        self.player.vx = 0
        self.player.vy = 0
        self.camera_x = 0
        self.camera_y = 0

    def update(self, keys):
        # se estiver na tela de agradecimento, não atualiza nada
        if self.menu.show_thank_you:
            return

        if self.state == "MENU":
            self.menu.update()
            return

        player_was_alive = self.player.lives > 0
        self.player.update(self.platforms, keys)

        for enemy in self.enemies:
            enemy.update(self.platforms, self.enemies)

        # collision
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.attacking:
                    enemy.take_hit(self.player.direction)
                    try: sounds.attack.play()
                    except: pass
                elif self.player.invincible_timer <= 0:
                    self.player.take_damage()
                    if self.player.lives <= 0 and player_was_alive:
                        try: sounds.death.play()
                        except: pass
                        music.stop()
                        self.state = "GAME_OVER"

        self.enemies = [e for e in self.enemies if not getattr(e, "kill", False)]

        if self.player.rect.top > HEIGHT + 100:
            if not self.death_played:
                try: sounds.death.play()
                except: pass
                music.stop()
                self.death_played = True
            self.state = "GAME_OVER"

        # Portal detection
        for plat_data in self.platforms:
            if plat_data.get("destination") and self.player.rect.colliderect(plat_data["rect"]):
                if plat_data["destination"] == "level2":
                    self.load_level2()
                    break

        # Audio zone activation
        if not self.audio_zone.activated and self.player.rect.colliderect(self.audio_zone.rect):
            self.audio_zone.activated = True
            self.audio_zone.playing = True
            self.audio_zone.started_at = 0
            if self.music_playing:
                music.stop()
                self.music_playing = False
            try:
                sounds.fim.play()
                self.audio_zone.duration = sounds.fim.get_length()
            except:
                self.audio_zone.duration = 3.0

        # Audio timer check
        if self.audio_zone.playing:
            self.audio_zone.started_at += 1/60
            if self.audio_zone.started_at >= self.audio_zone.duration:
                self.audio_zone.playing = False
                self.state = "MENU"
                self.menu.show_thank_you_message()  # chama tela de agradecimento e fecha o jogo em 5s

        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_y = self.player.rect.centery - HEIGHT // 2

    def draw(self, screen):
        if self.state == "MENU":
            self.menu.draw(screen)
            return

        if self.state == "GAME_OVER":
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), "black")
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
            screen.draw.text("Clique para voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=40, color="white")
            return
        if self.music_playing:
          self.music_button_actor.image = "music_icon"
        else:
          self.music_button_actor.image = "music_off"
        offset_x = -self.camera_x
        offset_y = -self.camera_y

        self.draw_background(screen)

        # draw platforms
        for plat_data in self.platforms:
            rect = plat_data["rect"]
            texture_name = plat_data["texture"]
            try:
                for x in range(rect.x, rect.x + rect.width, 50):
                    screen.blit(texture_name, (x + offset_x, rect.y + offset_y))
            except:
                screen.draw.filled_rect(Rect(rect.x + offset_x, rect.y + offset_y, rect.width, rect.height), "gray")

        # portal visual
        for plat in self.platforms:
            if plat.get("destination"):
                screen.draw.filled_rect(Rect(plat["rect"].x + offset_x, plat["rect"].y + offset_y,
                                             plat["rect"].width, plat["rect"].height), (255, 0, 255))
        
        # hearts
        heart_spacing = 50
        for i in range(self.player.lives):
            try:
                screen.surface.blit(images.heart, (10 + i * heart_spacing, 10))
            except:
                screen.draw.filled_rect(Rect(10 + i * heart_spacing, 10, 50, 50), "red")

        self.player.draw(offset_x, offset_y)
        for enemy in self.enemies:
            enemy.draw(offset_x, offset_y)
       # Desenha botão de música durante o jogo
        self.music_button_actor.draw()

    def on_mouse_down(self, pos):
     if self.state == "MENU":
        action = self.menu.check_click(pos)
        if action == "start":
            self.start_game()
        elif action == "exit":
            quit()
        elif action == "music_toggle":
            self.toggle_music()  # liga/desliga música
        elif action == "settings":
            self.menu.show_controls = True

     elif self.state == "GAME":
        # Clique no botão de música durante o jogo
        if self.music_hitbox_in_game.collidepoint(pos):
            self.toggle_music()

     elif self.state == "GAME_OVER":
        self.state = "MENU"

         
game = Game()

def draw(): game.draw(screen)
def update(): game.update(keyboard)
def on_mouse_down(pos): game.on_mouse_down(pos)

pgzrun.go()
