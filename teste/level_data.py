from pygame import Rect

# Cada plataforma ou chão pode ter um "tipo" de textura
# "floor" = chão, "grass", "stone", "wood" = plataformas
# Cada item: {"rect": Rect(...), "texture": "nome_da_imagem"}

platforms = [
    # Chão inicial
    {"rect": Rect(0, 550, 800, 50), "texture": "floor"},
    {"rect": Rect(0, 600, 800, 50), "texture": "floor"},
    {"rect": Rect(0, 650, 800, 50), "texture": "floor"},
    {"rect": Rect(0, 700, 800, 50), "texture": "floor"},
    {"rect": Rect(0, 750, 800, 50), "texture": "floor"},
    {"rect": Rect(0, 800, 800, 50), "texture": "floor"},
    #quando começa,altura do bloor ,onde termina,latitude
    {"rect": Rect(800, 550, 1800, 50), "texture": "platform1"},
    {"rect": Rect(800, 600, 1800, 50), "texture": "platform1"},
    {"rect": Rect(800, 650, 1800, 50), "texture": "platform1"},
    {"rect": Rect(800, 700, 1800, 50), "texture": "platform1"},
    {"rect": Rect(800, 750, 1800, 50), "texture": "platform1"},
    # Plataformas manuais
    {"rect": Rect(100, 400, 150, 20), "texture": "plant"},
    {"rect": Rect(350, 400, 200, 20), "texture": "platform2"},
    {"rect": Rect(650, 350, 150, 20), "texture": "platform3"},
    {"rect": Rect(900, 300, 200, 20), "texture": "platform1"},
    {"rect": Rect(1200, 450, 150, 20), "texture": "platform2"},
]

# Inimigos
enemies = [
    {"pos": (500, 500), "patrol": (450, 700)},
    {"pos": (250, 400), "patrol": (200, 350)}
]
