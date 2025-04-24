from thorpy import quit_current_loop, OutlinedText
from .core import Screen, PageWrapper, SimpleGroup, SimpleImageButton


class Game(PageWrapper):

    def _build(self):
        title = OutlinedText('GAME SCENE', 72)
        subtitle = OutlinedText('PRESS ESC TO EXIT')
        group = SimpleGroup([title, subtitle], 'v')
        Screen.center(group)

        closebtn = SimpleImageButton('close_72dp.png', quit_current_loop)
        closebtn.set_topright(Screen.width(), 0)

        return [group, closebtn]
