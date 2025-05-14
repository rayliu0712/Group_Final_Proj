import thorpy
import pygame
from random_map import generate_path_map  # 你整合后的地图脚本

# 初始化 pygame 和 thorpy
pygame.init()
screen = pygame.display.set_mode((1000, 800))
thorpy.init()

# 生成地图路径结构
map_layers = generate_path_map()
current_layer_index = 0
current_node = None
selected_path = []  # 玩家选过的节点

# 用于保存所有按钮
all_buttons = []


def on_node_click(node):
    global current_layer_index, current_node

    if current_layer_index == 0 or (current_node and node in current_node.connected_to):
        print(f"Onto node：{node.node_type} | Theme：{node.theme} | map code：{node.tile_index}")
        selected_path.append(node)
        current_node = node
        current_layer_index = node.layer + 1

        # 刷新按钮高亮状态
        refresh_button_states()

        # TODO: 这里可以加入进入战斗场景逻辑
        # map_data = node.get_map_data()
        # launch_battle(map_data)


def refresh_button_states():
    for btn, node in all_buttons:
        if node.layer == current_layer_index:
            if current_node is None or node in current_node.connected_to:
                btn.set_font_color((0, 255, 0))  # 可点击 → 绿色
            else:
                btn.set_font_color((100, 100, 100))  # 不可达 → 灰色
        elif node in selected_path:
            btn.set_font_color((255, 215, 0))  # 已选 → 金色
        else:
            btn.set_font_color((255, 255, 255))  # 默认白色

# 渲染节点按钮


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


# 创建界面
map_buttons = render_map_buttons(map_layers)
box = thorpy.Box(map_buttons)
menu = thorpy.Menu(box)
for element in menu.get_population():
    element.surface = screen

# 初始刷新按钮颜色
refresh_button_states()

# 主循环
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
