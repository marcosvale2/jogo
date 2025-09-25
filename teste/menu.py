import math
import random
from pygame import Rect

sun_angle = 0
clouds = [{"x": random.randint(0, 800), "y": random.randint(50, 200)} for _ in range(5)]
menu_buttons = [
    {"text": "Start", "rect": Rect(300, 250, 200, 50), "action": "start"},
    {"text": "Exit", "rect": Rect(300, 320, 200, 50), "action": "exit"},
]

class Menu:
    def draw(self, screen):
        screen.fill((135, 206, 235))
        screen.draw.filled_circle((700, 100), 50, "yellow")
        for i in range(12):
            angle = sun_angle + i * 30
            x = 700 + 70 * math.cos(math.radians(angle))
            y = 100 + 70 * math.sin(math.radians(angle))
            screen.draw.line((700, 100), (x, y), "yellow")
        for cloud in clouds:
            screen.draw.filled_circle((cloud["x"], cloud["y"]), 30, "white")
            screen.draw.filled_circle((cloud["x"] + 40, cloud["y"] + 10), 40, "white")
            screen.draw.filled_circle((cloud["x"] + 80, cloud["y"]), 30, "white")
        screen.draw.text("Meu Jogo Incrível", center=(400, 150), fontsize=60, color="black")
        for button in menu_buttons:
            screen.draw.filled_rect(button["rect"], (200, 200, 200))
            screen.draw.text(button["text"], center=button["rect"].center, color="black")

    def update(self):
        global sun_angle, clouds
        sun_angle += 1
        for cloud in clouds:
            cloud["x"] -= 1
            if cloud["x"] < -100:
                cloud["x"] = 900

    def check_click(self, pos):
        for button in menu_buttons:
            if button["rect"].collidepoint(pos):
                return button["action"]
        return None
