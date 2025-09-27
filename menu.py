# menu.py
import math
import random
from pygame import Rect
from pgzero.actor import Actor
from config import WIDTH, HEIGHT

sun_angle = 0
clouds = [{"x": random.randint(0, WIDTH), "y": random.randint(50, 200)} for _ in range(5)]

class Menu:
    def __init__(self):
        self.music_on = True
        self.show_controls = False  # controla se a tela de instruções está visível

        # Botões como sprites
        self.start_button = Actor("start", pos=(400, 275))
        self.exit_button = Actor("sair", pos=(400, 345))
        # Ícone de configurações
        self.settings_icon = Actor("butoes-16", pos=(WIDTH - 50, 50))

        self.buttons = [
            {"actor": self.start_button, "action": "start"},
            {"actor": self.exit_button, "action": "exit"},
        ]

    def draw(self, screen):
        # Fundo
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (135, 206, 235))
        
        # Sol
        screen.draw.filled_circle((700, 100), 50, "yellow")
        for i in range(12):
            angle = sun_angle + i * 30
            x = 700 + 70 * math.cos(math.radians(angle))
            y = 100 + 70 * math.sin(math.radians(angle))
            screen.draw.line((700, 100), (x, y), "yellow")

        # Nuvens
        for cloud in clouds:
            screen.draw.filled_circle((cloud["x"], cloud["y"]), 30, "white")
            screen.draw.filled_circle((cloud["x"] + 40, cloud["y"] + 10), 40, "white")
            screen.draw.filled_circle((cloud["x"] + 80, cloud["y"]), 30, "white")

        # Título
        screen.draw.text("My Awesome Game", center=(WIDTH // 2, 150), fontsize=60, color="black")

        # Desenha os botões
        for button in self.buttons:
            button["actor"].draw()

        # Ícone de configurações
        self.settings_icon.draw()

        # Tela de instruções
        if self.show_controls:
            # Fundo semi-transparente
            screen.draw.filled_rect(Rect(150, 100, WIDTH-300, HEIGHT-200), (50, 50, 50))
            screen.draw.text("CONTROLES DO JOGO", center=(WIDTH//2, 150), fontsize=50, color="white")
            instructions = [
                "Setas ← → : Movimentação",
                "Espaço : Pular",
                "Shift (LShift/RShift) : Transformar",
                "Z : Ataque"
            ]
            for i, instr in enumerate(instructions):
                screen.draw.text(instr, center=(WIDTH//2, 250 + i*50), fontsize=35, color="white")
            screen.draw.text("Clique fora da caixa para voltar", center=(WIDTH//2, HEIGHT-120), fontsize=25, color="yellow")

    def update(self):
        global sun_angle
        sun_angle += 1
        for cloud in clouds:
            cloud["x"] -= 1
            if cloud["x"] < -100:
                cloud["x"] = WIDTH + 100

    def check_click(self, pos):
        # Fecha a tela de instruções se clicar fora
        if self.show_controls:
            if not Rect(150, 100, WIDTH-300, HEIGHT-200).collidepoint(pos):
                self.show_controls = False
            return None

        # Clique no ícone de configurações
        if self.settings_icon.collidepoint(pos):
            self.show_controls = True
            return None

        # Clique nos botões
        for button in self.buttons:
            if button["actor"].collidepoint(pos):
                return button["action"]
        return None
