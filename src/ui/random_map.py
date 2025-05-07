import random

TILE_SIZE = 20
MAP_WIDTH = 30
MAP_HEIGHT = 25

THEMES = {
    "É­ÁÖ": {
        "ground": (34, 139, 34),
        "obstacle": (0, 100, 0)
    },
    "±ù¶´": {
        "ground": (173, 216, 230),
        "obstacle": (135, 206, 250)
    },
    "»ðÉ½": {
        "ground": (139, 69, 19),
        "obstacle": (255, 69, 0)
    }
}

map_storage = {
    theme: [None]*5 for theme in THEMES
}

def generate_random_map():
    return [[random.choice([0]*8 + [1]*2) for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def get_map(theme, index):
    if map_storage[theme][index] is None:
        map_storage[theme][index] = generate_random_map()
    return map_storage[theme][index]

def generate_game_maps():
    selected = []
    for theme in THEMES:
        idx = random.randint(0, 4)
        map_data = get_map(theme, idx)
        selected.append({
            "theme": theme,
            "index": idx,
            "map": map_data
        })
    return selected



