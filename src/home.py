import pygame as pg
import thorpy as tp


class Home:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.run()

    def run(self):
        title = tp.OutlinedText('ERIKA', 50)
        title.center_on(self.screen)

        def makeImgBtn(path: str) -> tp.ImageButton:
            img = pg.image.load(path)
            scaledImg = pg.transform.scale(img, (50, 50))
            return tp.ImageButton('', scaledImg)

        settingsBtn = makeImgBtn('assets/image/gear.png')
        settingsBtn.set_bottomleft(25, self.screen.get_height()-25)

        closeBtn = makeImgBtn('assets/image/close.png')
        closeBtn.set_topright(self.screen.get_width()-25, 25)

        group = tp.Group([title, settingsBtn, closeBtn], mode=None)
        group.get_updater().launch()
