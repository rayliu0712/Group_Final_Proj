import random

# ------------------ ԭ tile map ���� -------------------

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

# ------------------ ��ͼ·��ϵͳ��·��ͼ�� -------------------

class MapNode:
    def __init__(self, layer, position, node_type):
        self.layer = layer  # �ڼ���
        self.position = position  # ͬ���еڼ���
        self.node_type = node_type  # 'battle', 'elite', 'shop', 'event'
        self.connected_to = []  # ���ӵ���һ����Щ�ڵ�
        self.theme = random.choice(list(THEMES.keys()))  # �����ͼ����
        self.tile_index = random.randint(0, 4)  # ʹ�õ� tile map index

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
                weights=[0.5, 0.2, 0.2, 0.1],  # ���ɸ���
                k=1
            )[0]
            node = MapNode(layer_index, i, node_type)
            layer.append(node)
        map_layers.append(layer)

    # ����ÿһ��ڵ� �� ��һ��� 1~2 ���ڵ�
    for i in range(len(map_layers) - 1):
        for node in map_layers[i]:
            next_layer = map_layers[i + 1]
            if next_layer:
                targets = random.sample(next_layer, k=min(len(next_layer), random.randint(1, 2)))
                for target in targets:
                    node.connect(target)

    return map_layers
