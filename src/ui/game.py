from .core import *
from ..data import vars
from ..data.consts import *
import random


class GamePageMan(Page):
    def _build(self) -> list[Element]:
        GameChooseDiff()()
        GameChooseCharacter()()
        GameScene()()
        return []


class GameChooseDiff(Page):
    def _build(self):
        def set_diff_and_quit(level: DiffLevel) -> None:
            vars.diff_level = level
            quit_current_loop()

        easy_btn = SimpleButton('Easy', lambda: set_diff_and_quit(DiffLevel.EASY))
        hard_btn = SimpleButton('Hard', lambda: set_diff_and_quit(DiffLevel.HARD))
        master_btn = SimpleButton('Master', lambda: set_diff_and_quit(DiffLevel.MASTER))
        box = SimpleTitleBox('Choose Difficulty', [easy_btn, hard_btn, master_btn], 'h')
        Screen.center(box)

        return [box]


class GameChooseCharacter(Page):
    def _build(self):
        def set_player_and_quit(character: Character) -> None:
            vars.character = character
            quit_current_loop()

        warrior_btn = SimpleButton('Warrior', lambda: set_player_and_quit(Character.WARRIOR))
        archer_btn = SimpleButton('Archer', lambda: set_player_and_quit(Character.ARCHER))
        box = SimpleTitleBox('Choose Player', [warrior_btn, archer_btn], 'h')
        Screen.center(box)

        return [box]


class GameScene(Page):
    def _build(self) -> list[Element]:
        self.player_text = Text(f"Player's HP: {vars.player_hp}", font_color=GREEN)
        self.enemy_text = Text(f"Enemy HP: {vars.enemy_hp}", font_color=RED)
        status_group = Group([self.player_text, self.enemy_text])
        Screen.center(status_group)

        self.generate_cards(5)
        card_area = SimpleBox(self.cards, 'h')
        card_area.set_size((Screen.width(), 150))
        card_area.set_bck_color((50, 50, 70))
        Screen.bottomleft(card_area)

        close_btn = SimpleImageButton("close_72dp.png", quit_current_loop)
        Screen.topright(close_btn)

        # define logger
        self.logger = Text("", 20, BLACK)
        self.log("Select One")

        return [status_group, card_area, close_btn, self.logger]

    # bug
    def generate_cards(self, count: int) -> None:
        self.cards: list[SimpleButton] = []
        for _ in range(count):
            card_type = random.choice(list(CardType))
            if card_type == CardType.ATTACK:
                card = SimpleButton("Attack\n(10dmg)", lambda c=card_type: self.use_card(c))
            else:
                card = SimpleButton("Defense\n(3def)", lambda c=card_type: self.use_card(c))
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
            self.disable_cards()
        elif vars.enemy_hp <= 0:
            self.log("You Win!")
            self.disable_cards()

    def disable_cards(self):
        for card in self.cards:
            ...
            # card.set_locked(True)
