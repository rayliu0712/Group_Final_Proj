import pygame as pg
import thorpy as tp
from typing import Callable


class Home:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.run()

    def run(self) -> None:
        title = tp.OutlinedText('ERIKA', 50)
        title.set_center(self.screen.get_width()/2,
                         self.screen.get_height()/2-37)  # 25*1.5

        def makeImgBtn(path: str, onClick: Callable[[], None]) -> tp.ImageButton:
            img = pg.image.load(path)
            scaledImg = pg.transform.scale(img, (50, 50))
            imgBtn = tp.ImageButton('', scaledImg)
            imgBtn.at_unclick = onClick
            return imgBtn

        playBtn = makeImgBtn(
            'assets/image/play_button.png', lambda: print('play'))
        playBtn.set_center(self.screen.get_width()/2,
                           self.screen.get_height()/2+37)  # 25*1.5

        settingsBtn = makeImgBtn(
            'assets/image/gear.png', lambda: print('settings'))
        settingsBtn.set_bottomleft(25, self.screen.get_height()-25)

        # "1/0" should be replace by exit function, but i still not found yet
        closeBtn = makeImgBtn('assets/image/close.png',
                              lambda: 1/0)  # raise ZeroDivisionError
        closeBtn.set_topright(self.screen.get_width()-25, 25)

        group = tp.Group([title, playBtn, settingsBtn, closeBtn], mode=None)
        group.get_updater().launch()
