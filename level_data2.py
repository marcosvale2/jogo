from pygame import Rect

# --- Textures ---
ground_textures_anim = ["ground/floor_bw_d1", "ground/floor_bw_d2", "ground/floor_bw_d3", "ground/floor_bw_d4", "ground/floor_bw_d5"]
ground_texture_fixed = "ground/floor_bwg_d"
vertical_textures = ["ground/floor_bw_dd", "ground/floor_bw_dd2", "ground/floor_bw_dd3", "ground/floor_bw_dd4"]

platforms = []

def add_ground_block(x, y, width=50, height=50, animated=False):
    if animated:
        index = (x // 50) % len(ground_textures_anim)
        texture = ground_textures_anim[index]
    else:
        texture = ground_texture_fixed
    return {"rect": Rect(x, y, width, height), "texture": texture}

# AREA 1 — INÍCIO LEVEL 2
for x in range(2000, 2800, 50):
    platforms.append(add_ground_block(x, 550, 50, 50, animated=False))

platforms += [
    add_ground_block(2100, 450, 150, 20, animated=True),
    add_ground_block(2300, 400, 150, 20, animated=True),
    add_ground_block(2500, 350, 150, 20, animated=True),
    add_ground_block(2700, 300, 200, 20, animated=True),
]

enemies = [
    {"pos": (2100, 0), "patrol": (2100, 2250), "speed": 2.0},
    {"pos": (2300, 0), "patrol": (2300, 2450), "speed": 1.8},
    {"pos": (3100, 0), "patrol": (3100, 3250), "speed": 1.5},
    {"pos": (3300, 0), "patrol": (3300, 3450), "speed": 1.2},
]

# vertical layers
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
