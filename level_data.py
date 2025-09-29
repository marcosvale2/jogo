from pygame import Rect

# --- Textures ---
ground_textures_anim = ["ground/floor_bw_d1", "ground/floor_bw_d2", "ground/floor_bw_d3", "ground/floor_bw_d4", "ground/floor_bw_d5"]
ground_texture_fixed = "ground/floor_bwg_d"  # textura padrão para chão e plataformas encostadas
vertical_textures = ["ground/floor_bw_dd", "ground/floor_bw_dd2", "ground/floor_bw_dd3", "ground/floor_bw_dd4", "ground/floor_bw_dd5", "ground/floor_bw_dd6","ground/floor_bw_dd6"]
vertical_textures2 = ["ground/floor_bw_dd", "ground/floor_bw_dd2", "ground/floor_bw_dd3", "ground/floor_bw_dd4", "ground/floor_bw_dd5", "ground/floor_bw_dd6","ground/floor_bw_dd6","ground/floor_bw_dd6","ground/floor_bw_dd6","ground/floor_bw_dd6","ground/floor_bw_dd6"]
platforms = []

def add_ground_block(x, y, width=50, height=50, animated=False):
    if animated:
        index = (x // 50) % len(ground_textures_anim)
        texture = ground_textures_anim[index]
    else:
        texture = ground_texture_fixed
    return {"rect": Rect(x, y, width, height), "texture": texture}

# =====================
# EXPANSÃO À ESQUERDA (SEM PLATAFORMAS) ATÉ -4000
# =====================
for x in range(-4500, -50, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False)) 
    
for x in range(-7000,-4000, 50):
    platforms.append(add_ground_block(x, 250, 50, 50, animated=False))# chão principal

# Inimigos espalhados na expansão
enemies = [
    {"pos": (-3950, 0), "patrol": (-4000, -3900), "speed": 1.5},
    {"pos": (-3700, 0), "patrol": (-3750, -3650), "speed": 1.8},
    {"pos": (-3450, 0), "patrol": (-3500, -3400), "speed": 1.6},
    {"pos": (-3200, 0), "patrol": (-3250, -3150), "speed": 2.0},
    {"pos": (-2950, 0), "patrol": (-3000, -2900), "speed": 1.3},
    {"pos": (-2700, 0), "patrol": (-2750, -2650), "speed": 1.7},
    {"pos": (-2450, 0), "patrol": (-2500, -2400), "speed": 1.4},
    {"pos": (-2200, 0), "patrol": (-2250, -2150), "speed": 1.9},
    {"pos": (-1950, 0), "patrol": (-2000, -1900), "speed": 1.5},
    {"pos": (-1700, 0), "patrol": (-1750, -1650), "speed": 1.6},
    {"pos": (-1450, 0), "patrol": (-1500, -1400), "speed": 1.8},
    {"pos": (-1200, 0), "patrol": (-1250, -1150), "speed": 1.7},
    {"pos": (-950, 0), "patrol": (-1000, -900), "speed": 1.9},
    {"pos": (-700, 0), "patrol": (-750, -650), "speed": 1.4},
    {"pos": (-450, 0), "patrol": (-500, -400), "speed": 2.0},
]




# Camadas verticais do chão da expansão
block_width = 80
layer_height = 50

# agora só pega os blocos da camada y=250 no intervalo [-4000, -50]
ground_blocks = [b for b in platforms if -7000 <= b["rect"].x <= -4600 and b["rect"].y == 250]

for block in ground_blocks:
    x_start = block["rect"].x
    for layer_index, texture in enumerate(vertical_textures2):
        y = 300 + layer_index * layer_height
        platforms.append({
            "rect": Rect(x_start, y, block_width, layer_height),
            "texture": texture
        })

# =====================
# AREA 1 – START (mantido original)
# =====================
for x in range(-200, 800, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))

platforms += [
    add_ground_block(200, 450, 150, 20, animated=True),
    add_ground_block(450, 400, 150, 20, animated=True),
    add_ground_block(700, 350, 150, 20, animated=True),
    add_ground_block(950, 300, 200, 20, animated=True),
    
    add_ground_block(-3850, 450, 200, 20, animated=True),
    add_ground_block(-3600, 400, 200, 20, animated=True),
    add_ground_block(-3900, 300, 200, 20, animated=True),
    add_ground_block(-4000, 250, 200, 20, animated=True),
]

enemies += [
    {"pos": (300, 0), "patrol": (200, 400), "speed": 2.0},
    {"pos": (500, 0), "patrol": (450, 600), "speed": 1.8},
    
   {"pos": (-4600, 0), "patrol": (-5000, -4550), "speed": 1.5}

]

# =====================
# AREA 2 – CAVE
# =====================
for x in range(1300, 2000, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))  # chão

for x in range(1000, 2000, 50):
    platforms.append(add_ground_block(x, 700, 50, 50, animated=False))

platforms += [
    add_ground_block(1100, 600, 150, 20, animated=True),
    add_ground_block(1400, 600, 150, 20, animated=True),
    add_ground_block(1700, 650, 150, 20, animated=True),
]

enemies += [
    {"pos": (1200, 0), "patrol": (1100, 1300), "speed": 1.2},
    {"pos": (1600, 0), "patrol": (1500, 1700), "speed": 1.5},
]

# =====================
# PORTAL LEVEL 1 → LEVEL 2
# =====================
platforms.append({
    "rect": Rect(2000, 500, 150, 20),
    "texture": "ground/floor_bwg_d",
    "destination": "level2"
})

# =====================
# VERTICAL LAYERS DO CHÃO
# =====================
ground_blocks = [b for b in platforms if -4500 <= b["rect"].x <= 2000 and b["rect"].y == 550]
for block in ground_blocks:
    x_start = block["rect"].x
    for layer_index, texture in enumerate(vertical_textures):
        y = 600 + layer_index * layer_height
        platforms.append({
            "rect": Rect(x_start, y, block_width, layer_height),
            "texture": texture
        })
