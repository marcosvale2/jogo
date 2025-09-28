from pygame import Rect
from pgzero.actor import Actor
from config import WIDTH, HEIGHT
from pgzero import clock

class Menu:
    def __init__(self):
        self.show_controls = False
        self.show_thank_you = False

        # Background
        self.background = Actor("back", pos=(WIDTH//2, HEIGHT//2))

        # Botões
        self.start_button = Actor("start", pos=(400, 275))
        self.exit_button = Actor("sair", pos=(400, 345))
        self.settings_icon = Actor("settings", pos=(WIDTH - 50, 50))
        self.music_button = Actor("music_icon", pos=(WIDTH - 50, 120))  # novo botão de música

        # Hitboxes
        self.start_hitbox = Rect(400 - 100, 275 - 25, 200, 50)
        self.exit_hitbox = Rect(400 - 100, 345 - 25, 200, 50)
        self.settings_hitbox = Rect(WIDTH - 75, 25, 50, 50)
        self.music_hitbox = Rect(WIDTH - 75, 95, 50, 50)

        self.buttons = [
            {"actor": self.start_button, "action": "start", "hitbox": self.start_hitbox},
            {"actor": self.exit_button, "action": "exit", "hitbox": self.exit_hitbox},
            {"actor": self.settings_icon, "action": "settings", "hitbox": self.settings_hitbox},
            {"actor": self.music_button, "action": "music_toggle", "hitbox": self.music_hitbox},
        ]

    def draw(self, screen):
        # Tela de agradecimento
        if self.show_thank_you:
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), "black")
            screen.draw.text(
                "Obrigado por jogar!",
                center=(WIDTH//2, HEIGHT//2),
                fontsize=60,
                color="yellow"
            )
            return  # não desenha mais nada

        # Menu normal
        self.background.draw()
        for button in self.buttons:
            button["actor"].draw()

        # Tela de controles
        if self.show_controls:
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
        pass

    def check_click(self, pos):
        # Fechar tela de controles ao clicar fora
        if self.show_controls:
            if not Rect(150, 100, WIDTH-300, HEIGHT-200).collidepoint(pos):
                self.show_controls = False
            return None

        # Checa clique nos botões
        for button in self.buttons:
            if button["hitbox"].collidepoint(pos):
                return button["action"]
        return None

    def show_thank_you_message(self):
        self.show_thank_you = True
        clock.schedule(self._exit_game, 5.0)
         
    def _exit_game(self):
        quit()
