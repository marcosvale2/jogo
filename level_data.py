from pygame import Rect

# --- Textures ---
ground_textures_anim = ["ground/floor_bw_d1", "ground/floor_bw_d2", "ground/floor_bw_d3", "ground/floor_bw_d4", "ground/floor_bw_d5"]
ground_texture_fixed = "ground/floor_bwg_d"  # textura padrão para chão e plataformas encostadas
vertical_textures = ["ground/floor_bw_dd", "ground/floor_bw_dd2", "ground/floor_bw_dd3", "ground/floor_bw_dd4"]

platforms = []

def add_ground_block(x, y, width=50, height=50, animated=False):
    if animated:
        index = (x // 50) % len(ground_textures_anim)
        texture = ground_textures_anim[index]
    else:
        texture = ground_texture_fixed
    return {"rect": Rect(x, y, width, height), "texture": texture}

# =====================
# AREA 1 – START
# =====================
# Chão principal (não animado)
for x in range(-200, 800, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))

# Plataformas soltas (animadas)
platforms += [
    add_ground_block(200, 450, 150, 20, animated=True),
    add_ground_block(450, 400, 150, 20, animated=True),
    add_ground_block(700, 350, 150, 20, animated=True),
    add_ground_block(950, 300, 200, 20, animated=True),
]

enemies = [
    {"pos": (300, 0), "patrol": (200, 400), "speed": 2.0},
    {"pos": (500, 0), "patrol": (450, 600), "speed": 1.8},
]

# =====================
# AREA 2 – CAVE
# =====================
for x in range(1300, 2000, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))  # chão

# Camada subterrânea (caverna)
for x in range(1000, 2000, 50):
    platforms.append(add_ground_block(x, 700, 50, 50, animated=False))

platforms += [
    add_ground_block(1100, 600, 150, 20, animated=True),
    add_ground_block(1400, 600, 150, 20, animated=True),
    add_ground_block(1700, 650, 150, 20, animated=True),
]

# --- Portal para LevelData2 ---
platforms.append({
    "rect": Rect(2000, 500, 150, 20),
    "texture": "ground/floor_bwg_d",
    "destination": "level2"
})

enemies += [
    {"pos": (1200, 0), "patrol": (1100, 1300), "speed": 1.2},
    {"pos": (1600, 0), "patrol": (1500, 1700), "speed": 1.5},
]

# =====================
# VERTICAL LAYERS DO CHÃO
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
