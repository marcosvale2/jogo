from pygame import Rect

# Cada plataforma ou chão pode ter um "tipo" de textura
# "floor" = chão, "grass", "stone", "wood" = plataformas
# Cada item: {"rect": Rect(...), "texture": "nome_da_imagem"}

platforms = [
    # Chão inicial
    {"rect": Rect(-800, 550, 1600, 50), "texture": "floor"},
    {"rect": Rect(-800, 600, 1600, 50), "texture": "floor"},
    {"rect": Rect(-800, 650, 1600, 50), "texture": "floor"},
    {"rect": Rect(-800, 700, 1600, 50), "texture": "floor"},
    {"rect": Rect(-800, 750, 1600, 50), "texture": "floor"},
    {"rect": Rect(-800, 800, 1600, 50), "texture": "floor"},
    #quando começa,altura do bloor ,onde termina,latitude
    {"rect": Rect(800, 550, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 600, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 650, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 700, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 750, 800, 50), "texture": "platform1"},
    
    #buraco
    #parte 3
    {"rect": Rect(1150, 550, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 600, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 650, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 700, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 750, 500, 50), "texture": "platform1"},

    #parte 4
    {"rect": Rect(1900, 550, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 600, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 650, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 700, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 750, 300, 50), "texture": "platform1"},

    #parte 5
    {"rect": Rect(2350, 550, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 600, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 650, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 700, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 750, 500, 50), "texture": "platform1"},

    #parkour
    {"rect": Rect(3000, 600, 80, 50), "texture": "plant"},
    {"rect": Rect(3200, 650, 80, 50), "texture": "plant"},
    {"rect": Rect(3400, 700, 80, 50), "texture": "plant"},
    {"rect": Rect(3600, 750, 80, 50), "texture": "plant"},
    {"rect": Rect(3800, 850, 80, 50), "texture": "plant"},
    {"rect": Rect(4000, 900, 80, 50), "texture": "plant"},
    {"rect": Rect(4200, 950, 80, 50), "texture": "plant"},
    {"rect": Rect(4400, 1000, 80, 50), "texture": "plant"},
    {"rect": Rect(4600, 1050, 80, 50), "texture": "plant"},
    {"rect": Rect(4800, 1000, 80, 50), "texture": "plant"},
    {"rect": Rect(5000, 950, 80, 50), "texture": "plant"},
    {"rect": Rect(5200, 900, 80, 50), "texture": "plant"},
    {"rect": Rect(5400, 850, 80, 50), "texture": "plant"},
    {"rect": Rect(5600, 800, 80, 50), "texture": "plant"},
    {"rect": Rect(5800, 750, 80, 50), "texture": "plant"},
    {"rect": Rect(6000, 700, 80, 50), "texture": "plant"},
    {"rect": Rect(6200, 650, 80, 50), "texture": "plant"},
    {"rect": Rect(6400, 600, 80, 50), "texture": "plant"},
    {"rect": Rect(6600, 550, 80, 50), "texture": "plant"},

    #parte 6
    {"rect": Rect(6700, 550, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 600, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 650, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 700, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 750, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 800, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 850, 1050, 50), "texture": "floor"},
 
    #final
    {"rect": Rect(7850, 550, 300, 50), "texture": "floor"},
    # Plataformas manuais
    {"rect": Rect(100, 400, 150, 20), "texture": "plant"},
    {"rect": Rect(350, 400, 150, 20), "texture": "platform2"},
    {"rect": Rect(650, 350, 150, 20), "texture": "floor"},
    {"rect": Rect(900, 300, 200, 20), "texture": "platform1"},
    {"rect": Rect(1200, 400, 150, 20), "texture": "platform2"},
    {"rect": Rect(1450, 300, 250, 20), "texture": "platform2"},
]

# Inimigos
enemies = [
    {"pos": (500, 500), "patrol": (450, 700)},
    {"pos": (250, 400), "patrol": (200, 350)},
    {"pos": (800, 400), "patrol": (750, 1600)},
    {"pos": (850, 400), "patrol": (800, 1600)},
    {"pos": (900, 400), "patrol": (850, 1600)},
    {"pos": (950, 400), "patrol": (900, 1600)},
    {"pos": (1000, 400), "patrol": (950, 1600)},
    {"pos": (1050, 400), "patrol": (1000, 1600)},
    {"pos": (350, 400), "patrol": (300, 500)},
    {"pos": (1950, 400), "patrol": (1900, 2200)},
    {"pos": (6750, 400), "patrol": (6700, 7750)},
    {"pos": (6950, 400), "patrol": (6700, 7750)},
    {"pos": (7150, 400), "patrol": (6700, 7750)},
    {"pos": (7350, 400), "patrol": (6700, 7750)},
    {"pos": (7550, 400), "patrol": (6700, 7750)},
    {"pos": (7750, 400), "patrol": (6700, 7750)},
]
