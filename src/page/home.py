from .core import *


class Home(Page):
    def _build(self):
        title = tp.OutlinedText('ERIKA', 50)
        title.set_center(self.screen.get_width()/2,
                         self.screen.get_height()/2-37)  # 25*1.5

        def makeImgBtn(filename: str, onClick: Callable[[], None]) -> tp.ImageButton:
            img = pg.image.load('assets/image/'+filename)
            scaledImg = pg.transform.scale(img, (50, 50))
            imgBtn = tp.ImageButton('', scaledImg)
            imgBtn.at_unclick = onClick
            return imgBtn

        playBtn = makeImgBtn('play_button.png', lambda: print('play'))
        playBtn.set_center(self.screen.get_width()/2,
                           self.screen.get_height()/2+37)  # 25*1.5

        settingsBtn = makeImgBtn('gear.png', lambda: print('setting'))
        settingsBtn.set_topleft(25, 25)

        closeBtn = makeImgBtn('close.png', tp.exit_app)
        closeBtn.set_topright(self.screen.get_width()-25, 25)

        return [title, playBtn, settingsBtn, closeBtn]
