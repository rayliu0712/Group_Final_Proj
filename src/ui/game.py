from .core import *


class Game(Page):

    def _build(self):
        title = OutlinedText('GAME SCENE', 72)
        subtitle = OutlinedText('PRESS ALT+Q TO EXIT')
        group = SimpleGroup([title, subtitle], 'v')
        Screen.center(group)

        self._kandler += quit_current_loop, [KMOD_ALT], [K_q]

        return [group]
