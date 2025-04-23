from pygame import KMOD_ALT, K_q
from thorpy import quit_current_loop, OutlinedText
from .core import Screen, Page
from .simple import SimpleGroup


class Game(Page):

    def _build(self):
        title = OutlinedText('GAME SCENE', 72)
        subtitle = OutlinedText('PRESS ALT+Q TO EXIT')
        group = SimpleGroup([title, subtitle], 'v')
        Screen.center(group)

        self._bind_keys(quit_current_loop, [KMOD_ALT], [K_q])

        return [group]
