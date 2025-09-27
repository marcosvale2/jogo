from pygame import Rect

# --- Texturas de chão ---
ground_textures = ["ground/floor_bwg_d", "ground/floor_bwg_d2", "ground/floor_bwg_d3"]
vertical_textures = ["ground/floor_bw_dd", "ground/floor_bw_dd2", "ground/floor_bw_dd3"]

platforms = []

def add_ground_block(x, y, width=50, height=50):
    index = (x // 50) % len(ground_textures)
    texture = ground_textures[index]
    return {"rect": Rect(x, y, width, height), "texture": texture}

# =====================
# ÁREA 1 — CHÃO INICIAL
# =====================
for x in range(0, 600, 50):
    platforms.append(add_ground_block(x, 550))

# Plataformas extras
platforms += [
    {"rect": Rect(200, 450, 150, 20), "texture": "platform1"},
    {"rect": Rect(400, 400, 150, 20), "texture": "platform2"},
]

# =====================
# ÁREA 2 — SUBIDA
# =====================
for x in range(650, 950, 50):
    y = 550 - ((x - 650) // 50) * 25  # sobe gradualmente
    platforms.append(add_ground_block(x, y))

platforms += [
    {"rect": Rect(950, 350, 150, 20), "texture": "platform3"},
    {"rect": Rect(1100, 300, 150, 20), "texture": "platform2"},
]

# =====================
# ÁREA 3 — TOPO
# =====================
for x in range(1150, 1350, 50):
    platforms.append(add_ground_block(x, 250))

# =====================
# INIMIGOS
# =====================
enemies = [
    {"pos": (250, 0), "patrol": (200, 350), "speed": 2.0},
    {"pos": (450, 0), "patrol": (400, 550), "speed": 1.5},
    {"pos": (1000, 0), "patrol": (950, 1100), "speed": 1.8},
]

# =====================
# CAMADAS VERTICAIS DO CHÃO
# =====================
block_width = 80
layer_height = 50
ground_blocks = [b for b in platforms if b["rect"].y == 550]

for block in ground_blocks:
    x_start = block["rect"].x
    for layer_index, texture in enumerate(vertical_textures):
        y = 600 + layer_index * layer_height
        platforms.append({
            "rect": Rect(x_start, y, block_width, layer_height),
            "texture": texture
        })
