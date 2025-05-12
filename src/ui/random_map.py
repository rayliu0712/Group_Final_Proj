import random

# ------------------ 原 tile map 部分 -------------------

TILE_SIZE = 20
MAP_WIDTH = 30
MAP_HEIGHT = 25

THEMES = {
    "forest": {
        "ground": (34, 139, 34),
        "obstacle": (0, 100, 0)
    },
    "snow": {
        "ground": (173, 216, 230),
        "obstacle": (135, 206, 250)
    },
    "volcano": {
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

# ------------------ 地图路径系统（路线图） -------------------

class MapNode:
    def __init__(self, layer, position, node_type):
        self.layer = layer  # 第几层
        self.position = position  # 同层中第几个
        self.node_type = node_type  # 'battle', 'elite', 'shop', 'event'
        self.connected_to = []  # 连接到下一层哪些节点
        self.theme = random.choice(list(THEMES.keys()))  # 随机地图主题
        self.tile_index = random.randint(0, 4)  # 使用的 tile map index

    def connect(self, other_node):
        self.connected_to.append(other_node)

    def get_map_data(self):
        return get_map(self.theme, self.tile_index)

def generate_path_map(layers=7, min_nodes=2, max_nodes=4):
    node_types = ['battle', 'elite', 'shop', 'event']
    map_layers = []

    for layer_index in range(layers):
        num_nodes = random.randint(min_nodes, max_nodes)
        layer = []
        for i in range(num_nodes):
            node_type = random.choices(
                node_types,
                weights=[0.5, 0.2, 0.2, 0.1],  # 生成概率
                k=1
            )[0]
            node = MapNode(layer_index, i, node_type)
            layer.append(node)
        map_layers.append(layer)

    # 连接每一层节点 → 下一层的 1~2 个节点
    for i in range(len(map_layers) - 1):
        for node in map_layers[i]:
            next_layer = map_layers[i + 1]
            if next_layer:
                targets = random.sample(next_layer, k=min(len(next_layer), random.randint(1, 2)))
                for target in targets:
                    node.connect(target)

    return map_layers
