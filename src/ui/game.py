from .core import *


class Player(Enum):
    WARRIOR = 'WARRIOR'
    ARCHER = 'ARCHER'


class Game(Page):
    def __init__(self):
        super().__init__()
        self.diff_level: int
        self.player: Player

    def _build(self):
        PageChooseDiff(self)()
        PageChoosePlayer(self)()

        title = OutlinedText('GAME SCENE', 72)
        subtitle = OutlinedText('PRESS ALT+Q TO EXIT')
        group = Group([title, subtitle])
        Screen.center(group)

        self._kandler += quit_current_loop, [KMOD_ALT], [K_q]

        return [group]


class PageChooseDiff(Page):
    def __init__(self, game: Game):
        super().__init__()
        self.__game = game

    def _build(self):
        def set_diff_and_quit(level: int) -> None:
            self.__game.diff_level = level
            quit_current_loop()

        easy_btn = SimpleButton('Easy', lambda: set_diff_and_quit(1))
        hard_btn = SimpleButton('Hard', lambda: set_diff_and_quit(2))
        master_btn = SimpleButton('Master', lambda: set_diff_and_quit(3))
        box = SimpleTitleBox('Choose Difficulty', [easy_btn, hard_btn, master_btn], 'h')
        Screen.center(box)

        return [box]


class PageChoosePlayer(Page):
    def __init__(self, game: Game):
        super().__init__()
        self.__game = game

    def _build(self):
        def set_player_and_quit(player: Player) -> None:
            self.__game.player = player
            quit_current_loop()

        warrior_btn = SimpleButton('Warrior', lambda: set_player_and_quit(Player.WARRIOR))
        archer_btn = SimpleButton('Archer', lambda: set_player_and_quit(Player.ARCHER))
        box = SimpleTitleBox('Choose Player', [warrior_btn, archer_btn], 'h')
        Screen.center(box)

        return [box]
