from pygame import Rect

def create_platforms():
    return [
        Rect(0, 550, 800, 50),   # chão
        Rect(200, 450, 150, 20),
        Rect(300, 350, 200, 20),
    ]