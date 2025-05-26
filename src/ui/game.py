from .random_map import generate_path_map
from .core import *
from ..data import vars
from ..data.consts import *
import random


class GameMan(Page):
    go_back = True

    def _build(self):
        while self.go_back:
            if is_pygame_quit():
                exit_app()
            else:
                GameChooseDiff()()
                GameChooseCharacter()()
                CardBag()()

        GameScene()()
        MapUI()()
        return []


class GameChooseDiff(Page):
    def _build(self):

        @lazy
        def set_diff_and_quit(level: DiffLevel) -> None:
            vars.diff_level = level
            quit_current_loop()

        easy_btn = mkButton("Easy", set_diff_and_quit(DiffLevel.EASY))
        hard_btn = mkButton("Hard", set_diff_and_quit(DiffLevel.HARD))
        master_btn = mkButton("Master", set_diff_and_quit(DiffLevel.MASTER))
        box = mkTitleBox("Choose Difficulty", [easy_btn, hard_btn, master_btn], "h")
        Screen.center(box)

        return [box]


class GameChooseCharacter(Page):
    def _build(self):

        @lazy
        def set_player_and_quit(character: Character) -> None:
            vars.character = character
            quit_current_loop()

        warrior_btn = mkButton("Warrior", set_player_and_quit(Character.WARRIOR))
        archer_btn = mkButton("Archer", set_player_and_quit(Character.ARCHER))
        box = mkTitleBox("Choose Player", [warrior_btn, archer_btn], "h")
        Screen.center(box)

        return [box]


class CardBag(Page):
    def _build(self):
        title = OutlinedText("Card Deck", 24)
        Screen.topleft(title)

        @lazy
        def set_flag_and_quit(go_back: bool) -> None:
            GameMan.go_back = go_back
            quit_current_loop()

        back_btn = mkImageButton("back_72dp.png", set_flag_and_quit(True))
        Screen.bottomleft(back_btn)

        play_btn = mkImageButton("play_72dp.png", set_flag_and_quit(False))
        Screen.bottomright(play_btn)

        card_elements: list[Text] = []
        for card in cards:
            element = Text(f"{card['name']}\n({card['type']})", font_size=18)
            element.set_size((120, 80))
            element.set_bck_color(card['color'])
            card_elements.append(element)

        rows: list[Box] = []
        for i in range(0, len(card_elements), 5):
            row = mkBox(card_elements[i:i + 5], "h")
            rows.append(row)
        deck = Group(rows)

        return [title, back_btn, play_btn, deck]


class GameScene(Page):
    def __init__(self, on_battle_end=None):
        super().__init__()
        self.on_battle_end = on_battle_end

    def _build(self):
        self.player_text = Text(f"Player's HP: {vars.player_hp}", font_color=GREEN)
        self.enemy_text = Text(f"Enemy HP: {vars.enemy_hp}", font_color=RED)
        status_group = Group([self.player_text, self.enemy_text])
        Screen.center(status_group)

        self.generate_cards(5)
        card_area = mkBox(self.cards, 'h')
        card_area.set_size((Screen.width(), 150))
        card_area.set_bck_color((50, 50, 70))
        Screen.bottomleft(card_area)

        close_btn = mkImageButton("close_72dp.png", quit_current_loop)
        Screen.topright(close_btn)

        # define logger
        self.logger = Text("", 20, BLACK)
        self.log("Select One")

        return [status_group, card_area, close_btn, self.logger]

    # bug
    def generate_cards(self, count: int) -> None:
        self.cards: list[Button] = []
        for _ in range(count):
            card_type = random.choice(list(CardType))
            if card_type == CardType.ATTACK:
                card = mkButton("Attack\n(10dmg)", lambda c=card_type: self.use_card(c))
            else:
                card = mkButton("Defense\n(3def)", lambda c=card_type: self.use_card(c))
            card.set_size((120, 80))
            self.cards.append(card)

    def log(self, text: str) -> None:
        self.logger.set_text(text)
        Screen.topleft(self.logger)

    def use_card(self, card_type) -> None:
        if card_type == CardType.ATTACK:
            vars.enemy_hp -= 10
            self.log("Use Attack Card! Enemy takes 10 damage")
        else:
            vars.player_defense += 3
            self.log("Use Defense Card! Gain 3 defense points")

        self.update_status()
        self.enemy_turn()

        if random.random() < 0.5:
            self.generate_cards(1)

        self.check_game_over()

    def enemy_turn(self):
        damage = random.randint(0, 10)
        actual_damage = max(0, damage - vars.player_defense)
        vars.player_hp -= actual_damage
        vars.player_defense = max(0, vars.player_defense - damage)

        self.log(
            f"{self.logger.text}\n"
            f"Enemy Attack! Causes {damage} Points dmg, Actual damage {actual_damage} Points"
        )
        self.update_status()

    def update_status(self):
        self.player_text.set_text(f"Player's HP: {vars.player_hp} (Defense: {vars.player_defense})")
        self.enemy_text.set_text(f"Enemy's HP: {vars.enemy_hp}")

    def check_game_over(self):
        if vars.player_hp <= 0:
            self.log("You Lose!")
            quit_current_loop()
        elif vars.enemy_hp <= 0:
            self.log("You Win!")
            quit_current_loop()
            if self.on_battle_end:
                self.on_battle_end()


#####

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
        # 判断类型，进入战斗或下一步
        if node.node_type in ("battle", "elite"):
            # 进入战斗前重置血量
            vars.player_hp = 100  # 或者根据难度/关卡调整  完善了所有游戏逻辑了才更改可玩性这部分
            vars.player_defense = 0
            vars.enemy_hp = 50 if node.node_type == "battle" else 100
            def after_battle():
                MapUI()()  # 战斗后回到地图页面
            GameScene(on_battle_end=after_battle)()
        else:
            # shop/event类型直接回到地图页面
            MapUI()()


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
    global all_buttons
    all_buttons.clear()
    y_spacing = 100
    x_spacing = 150
    elements = []

    def make_handler(n):
        return lambda: on_node_click(n)

    for layer_index, layer in enumerate(map_layers):
        total_width = len(layer) * x_spacing
        offset_x = (Screen.width() - total_width) // 2

        for node_index, node in enumerate(layer):
            btn = mkButton(
                node.node_type[0].upper(),
                make_handler(node)
            )
            btn.set_topleft(offset_x + node_index * x_spacing, 50 + layer_index * y_spacing)
            elements.append(btn)
            all_buttons.append((btn, node))
    return elements


# # 创建界面
# map_buttons = render_map_buttons(map_layers)
# box = thorpy.Box(map_buttons)
# menu = thorpy.Menu(box)
# for element in menu.get_population():
#     element.surface = screen

# 初始刷新按钮颜色
refresh_button_states()


class MapUI(Page):
    def _build(self):
        map_buttons = []
        map_buttons = render_map_buttons(map_layers)
        return map_buttons
