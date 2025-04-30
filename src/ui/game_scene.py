from .core import *
from enum import Enum
import random

class CardType(Enum):
    ATTACK = 0
    DEFENSE = 1

class GameScene(Page):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_defense = 0
        self.cards = []
        
    def _build(self):

        divider = thorpy.Line.make(
            (Screen.width()//2, 50),
            (Screen.width()//2, Screen.height()-150),
            color=(255, 255, 255), thickness=2
        )
        
        self.player_text = thorpy.Text(f"Player's HP: {self.player_hp}", font_color=(0, 255, 0))
        self.enemy_text = thorpy.Text(f"Enemy HP: {self.enemy_hp}", font_color=(255, 0, 0))
        status_group = Group([self.player_text, self.enemy_text], "h")
        
        self.card_area = thorpy.Box.make([], size=(Screen.width(), 150))
        self.card_area.set_topleft((0, Screen.height()-150))
        self.card_area.set_main_color((50, 50, 70))
        self.generate_cards(5)
        
        back_btn = SimpleButton("Back", quit_current_loop)
        Screen.bottomright(back_btn)
        
        self.info_text = thorpy.Text("Select One", font_size=20)
        Screen.topleft(self.info_text)
        
        return [divider, status_group, self.card_area, back_btn, self.info_text]
    
    def generate_cards(self, count):

        self.cards = []
        for _ in range(count):
            card_type = random.choice(list(CardType))
            if card_type == CardType.ATTACK:
                card = SimpleButton("Attack\n(10dmg)", lambda c=card_type: self.use_card(c))
            else:
                card = SimpleButton("Defense\n(3def)", lambda c=card_type: self.use_card(c))
            card.set_size((120, 80))
            self.cards.append(card)
        
        card_group = Group(self.cards, "h")
        card_group.center()
        self.card_area.empty()
        self.card_area.add_child(card_group)
    
    def use_card(self, card_type):
        if card_type == CardType.ATTACK:
            self.enemy_hp -= 10
            self.info_text.set_text("Use Attack Card! Enemy takes 10 damage")
        else:
            self.player_defense += 3
            self.info_text.set_text("Use Defense Card! Gain 3 defense points")
        
        self.update_status()
        self.enemy_turn()
        
        if random.random() < 0.5:
            self.generate_cards(1)
        
        self.check_game_over()
    
    def enemy_turn(self):
        damage = random.randint(0, 10)
        actual_damage = max(0, damage - self.player_defense)
        self.player_hp -= actual_damage
        self.player_defense = max(0, self.player_defense - damage)
        
        self.info_text.set_text(
            f"{self.info_text.get_text()}\n"
            f"Enemy Attack! Causes{damage}Points dmg£¨Actual{actual_damage}µã£©"
        )
        self.update_status()
    
    def update_status(self):
        self.player_text.set_text(f"Player's HP: {self.player_hp} (Defense: {self.player_defense})")
        self.enemy_text.set_text(f"Enemy's HP: {self.enemy_hp}")
    
    def check_game_over(self):
        if self.player_hp <= 0:
            self.info_text.set_text("You Lose!")
            self.disable_cards()
        elif self.enemy_hp <= 0:
            self.info_text.set_text("You Win!")
            self.disable_cards()
    
    def disable_cards(self):
        for card in self.cards:
            card.set_main_color((150, 150, 150))
            card.at_unclick = None