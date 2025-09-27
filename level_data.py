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
    add_ground_block(1100, 650, 150, 20, animated=True),
    add_ground_block(1400, 600, 150, 20, animated=True),
    add_ground_block(1700, 650, 150, 20, animated=True),
]

enemies += [
    {"pos": (1200, 0), "patrol": (1100, 1300), "speed": 1.2},
    {"pos": (1600, 0), "patrol": (1500, 1700), "speed": 1.5},
]

# =====================
# AREA 3 – TOWER
# =====================
for x in range(2100, 2500, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))  # chão base

# Plataformas laterais soltas
platforms += [
    add_ground_block(2200, 500, 100, 20, animated=True),
    add_ground_block(2300, 450, 100, 20, animated=True),
    add_ground_block(2400, 400, 100, 20, animated=True),
    add_ground_block(2300, 350, 100, 20, animated=True),
    add_ground_block(2200, 300, 100, 20, animated=True),
    add_ground_block(2100, 250, 100, 20, animated=True),
]

# Topo da torre
for x in range(2000, 2600, 50):
    platforms.append(add_ground_block(x, 200, 50, 50, animated=False))

enemies.append({"pos": (2300, 0), "patrol": (2100, 2500), "speed": 2.5})

# =====================
# AREA 4 – PLAIN
# =====================
for x in range(2700, 3700, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))  # chão

# Obstáculos soltos
platforms += [
    add_ground_block(2800, 500, 100, 20, animated=True),
    add_ground_block(3100, 450, 100, 20, animated=True),
    add_ground_block(3400, 500, 100, 20, animated=True),
]

enemies += [
    {"pos": (2900, 0), "patrol": (2800, 3000), "speed": 2.2},
    {"pos": (3200, 0), "patrol": (3100, 3300), "speed": 2.0},
]

# =====================
# AREA 5 – MOUNTAIN
# =====================
for x in range(3800, 4500, 50):
    y = 550 - ((x - 3800) // 50) * 25
    platforms.append(add_ground_block(x, y, 50, 50, animated=False))  # subida montanha

# Topo da montanha
for x in range(4500, 5200, 50):
    platforms.append(add_ground_block(x, 200, 50, 50, animated=False))

# Plataformas suspensas soltas
platforms += [
    add_ground_block(4700, 150, 150, 20, animated=True),
    add_ground_block(5000, 100, 150, 20, animated=True),
]

enemies += [
    {"pos": (4800, 0), "patrol": (4700, 5000), "speed": 2.0},
    {"pos": (5050, 0), "patrol": (5000, 5200), "speed": 1.8},
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
