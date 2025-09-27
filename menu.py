# menu.py
import math
import random
from pygame import Rect
from pgzero.actor import Actor
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self):
        self.music_on = True
        self.show_controls = False  # controla se a tela de instruções está visível

        # Fundo como imagem
        self.background = Actor("back", pos=(WIDTH//2, HEIGHT//2))  # substitua "menu_background" pelo nome do arquivo

        # Botões como sprites
        self.start_button = Actor("start", pos=(400, 275))
        self.exit_button = Actor("sair", pos=(400, 345))
        self.settings_icon = Actor("settings", pos=(WIDTH - 50, 50))

        # Hitboxes específicas
        self.start_hitbox = Rect(400 - 100, 275 - 25, 200, 50)
        self.exit_hitbox = Rect(400 - 100, 345 - 25, 200, 50)
        self.settings_hitbox = Rect(WIDTH - 75, 25, 50, 50)

        self.buttons = [
            {"actor": self.start_button, "action": "start", "hitbox": self.start_hitbox},
            {"actor": self.exit_button, "action": "exit", "hitbox": self.exit_hitbox},
            {"actor": self.settings_icon, "action": "settings", "hitbox": self.settings_hitbox},
        ]

    def draw(self, screen):
        # Desenha o fundo como imagem
        self.background.draw()


        # Desenha os botões
        for button in self.buttons:
            button["actor"].draw()

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
        # Mantém a lógica original do menu
        pass

    def check_click(self, pos):
        # Fecha a tela de instruções se clicar fora
        if self.show_controls:
            if not Rect(150, 100, WIDTH-300, HEIGHT-200).collidepoint(pos):
                self.show_controls = False
            return None

        # Clique nos botões usando hitbox
        for button in self.buttons:
            if button["hitbox"].collidepoint(pos):
                return button["action"]
        return None
