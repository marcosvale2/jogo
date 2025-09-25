from pygame import Rect
import random
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
    # quando começa,altura do bloor ,onde termina,latitude
    {"rect": Rect(800, 550, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 600, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 650, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 700, 800, 50), "texture": "platform1"},
    {"rect": Rect(800, 750, 800, 50), "texture": "platform1"},

    # buraco
    # parte 3
    {"rect": Rect(1150, 550, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 600, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 650, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 700, 500, 50), "texture": "platform1"},
    {"rect": Rect(1150, 750, 500, 50), "texture": "platform1"},

    # parte 4
    {"rect": Rect(1900, 550, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 600, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 650, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 700, 300, 50), "texture": "platform1"},
    {"rect": Rect(1900, 750, 300, 50), "texture": "platform1"},

    # parte 5
    {"rect": Rect(2350, 550, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 600, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 650, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 700, 500, 50), "texture": "platform1"},
    {"rect": Rect(2350, 750, 500, 50), "texture": "platform1"},

    # parkour
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

    # parte 6
    {"rect": Rect(6700, 550, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 600, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 650, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 700, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 750, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 800, 1050, 50), "texture": "floor"},
    {"rect": Rect(6700, 850, 1050, 50), "texture": "floor"},

    # final
    {"rect": Rect(7850, 550, 300, 50), "texture": "floor"},
    # Plataformas manuais
    {"rect": Rect(100, 400, 150, 20), "texture": "plant"},
    {"rect": Rect(350, 400, 150, 20), "texture": "platform2"},
    {"rect": Rect(650, 350, 150, 20), "texture": "floor"},
    {"rect": Rect(900, 300, 200, 20), "texture": "platform1"},
    {"rect": Rect(1200, 400, 150, 20), "texture": "platform2"},
    {"rect": Rect(1450, 300, 250, 20), "texture": "platform2"},
]

enemies = []

# Escolhe algumas plataformas elevadas (y < 550 e largura >= 200)
platform_indices = [
    i for i, plat in enumerate(platforms)
    if plat["rect"].y < 550 and plat["rect"].width >= 200
]

# Sorteia plataformas que terão inimigos
random.shuffle(platform_indices)
chosen_platforms = platform_indices[:min(6, len(platform_indices))]  # no máx 6

for plat_index in chosen_platforms:
    plat_rect = platforms[plat_index]["rect"]
    x_pos = random.randint(plat_rect.left + 30, plat_rect.right - 30)
    patrol_start = plat_rect.left + 20
    patrol_end = plat_rect.right - 20
    enemies.append({
        "pos": (x_pos, 0),
        "platform_index": plat_index,
        "patrol": (patrol_start, patrol_end),
        "speed": random.uniform(1.0, 1.5)  # mais lentos
    })

# --- Inimigos fixos no chão (sempre aparecem) ---
ground_rects = [
    p["rect"] for p in platforms if p["rect"].y >= 550
]

if ground_rects:
    ground = ground_rects[0]  # chão inicial
    ground_positions = [200, 600, 1000, 1500, 2000, 2600, 3300, 4000, 4700, 5300, 6000, 7000]
    for gx in ground_positions:
        patrol_range = (gx - 150, gx + 150)
        enemies.append({
            "pos": (gx, 0),
            "patrol": patrol_range,
            "speed": random.uniform(2.0, 3.0)
        })