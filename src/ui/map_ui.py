import thorpy
import pygame
from random_map import generate_path_map  # �����Ϻ�ĵ�ͼ�ű�

# ��ʼ�� pygame �� thorpy
pygame.init()
screen = pygame.display.set_mode((1000, 800))
thorpy.init()

# ���ɵ�ͼ·���ṹ
map_layers = generate_path_map()
current_layer_index = 0
current_node = None
selected_path = []  # ���ѡ���Ľڵ�

# ���ڱ������а�ť
all_buttons = []

def on_node_click(node):
    global current_layer_index, current_node

    if current_layer_index == 0 or (current_node and node in current_node.connected_to):
        print(f"Onto node��{node.node_type} | Theme��{node.theme} | map code��{node.tile_index}")
        selected_path.append(node)
        current_node = node
        current_layer_index = node.layer + 1

        # ˢ�°�ť����״̬
        refresh_button_states()

        # TODO: ������Լ������ս�������߼�
        # map_data = node.get_map_data()
        # launch_battle(map_data)

def refresh_button_states():
    for btn, node in all_buttons:
        if node.layer == current_layer_index:
            if current_node is None or node in current_node.connected_to:
                btn.set_font_color((0, 255, 0))  # �ɵ�� �� ��ɫ
            else:
                btn.set_font_color((100, 100, 100))  # ���ɴ� �� ��ɫ
        elif node in selected_path:
            btn.set_font_color((255, 215, 0))  # ��ѡ �� ��ɫ
        else:
            btn.set_font_color((255, 255, 255))  # Ĭ�ϰ�ɫ

# ��Ⱦ�ڵ㰴ť
def render_map_buttons(map_layers):
    y_spacing = 100
    x_spacing = 150
    elements = []

    for layer_index, layer in enumerate(map_layers):
        layer_buttons = []
        total_width = len(layer) * x_spacing
        offset_x = (screen.get_width() - total_width) // 2

        for node_index, node in enumerate(layer):
            label = node.node_type[0].upper()
            btn = thorpy.make_button(label, func=lambda n=node: on_node_click(n))
            btn.set_topleft((offset_x + node_index * x_spacing, 50 + layer_index * y_spacing))
            elements.append(btn)
            all_buttons.append((btn, node))
    return elements

# ��������
map_buttons = render_map_buttons(map_layers)
box = thorpy.Box(map_buttons)
menu = thorpy.Menu(box)
for element in menu.get_population():
    element.surface = screen

# ��ʼˢ�°�ť��ɫ
refresh_button_states()

# ��ѭ��
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((10, 10, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.react(event)
    menu.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
