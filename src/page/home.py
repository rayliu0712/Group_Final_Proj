from .core import *


class Home(Page):
    def _build(self):
        title = tp.OutlinedText('ERIKA', 50)
        title.set_center(self.screen_width() / 2, self.screen_height() / 2 - 37)  # 25*1.5

        def make_imgbtn(filename: str, onclick: Callable[[], None]) -> tp.ImageButton:
            img = pg.image.load('assets/image/' + filename)
            scaledimg = pg.transform.scale(img, (50, 50))
            imgbtn = tp.ImageButton('', scaledimg)
            imgbtn.at_unclick = onclick
            return imgbtn

        playbtn = make_imgbtn('play_button.png', lambda: Play(self.screen))
        playbtn.set_center(self.screen_width() / 2, self.screen_height() / 2 + 37)  # 25*1.5

        settingsbtn = make_imgbtn('gear.png', lambda: print('setting'))
        settingsbtn.set_topleft(25, 25)

        closebtn = make_imgbtn('close.png', tp.exit_app)
        closebtn.set_topright(self.screen_width() - 25, 25)

        return title, playbtn, settingsbtn, closebtn
