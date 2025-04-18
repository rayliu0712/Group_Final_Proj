import pygame as pg
import thorpy as tp
from typing import Callable


class Home:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.run()

    def run(self) -> None:
        title = tp.OutlinedText('ERIKA', 50)
        title.at_unclick = lambda: print('start')
        title.center_on(self.screen)

        def makeImgBtn(path: str, onClick: Callable[[], None]) -> tp.ImageButton:
            img = pg.image.load(path)
            scaledImg = pg.transform.scale(img, (50, 50))
            imgBtn = tp.ImageButton('', scaledImg)
            imgBtn.at_unclick = onClick
            return imgBtn

        settingsBtn = makeImgBtn(
            'assets/image/gear.png', lambda: print('setting'))
        settingsBtn.set_bottomleft(25, self.screen.get_height()-25)

        closeBtn = makeImgBtn('assets/image/close.png', lambda: print('close'))
        closeBtn.set_topright(self.screen.get_width()-25, 25)

        group = tp.Group([title, settingsBtn, closeBtn], mode=None)
        group.get_updater().launch()
