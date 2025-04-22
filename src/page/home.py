from .core import *


class Home(Page):

    def _build(self):
        # tp don't accept svg
        def make_imgbtn(filename: str, onclick: Callable[[], None]) -> tp.ImageButton:
            img = pg.image.load(f'assets/image/{filename}.png')
            btn = tp.ImageButton('', img)
            btn.at_unclick = onclick
            return btn

        close_btn = make_imgbtn('close_72dp', tp.exit_app)
        close_btn.set_topright(self.screen_width(), 0)

        settings_btn = make_imgbtn('settings_72dp', lambda: print('settings'))
        play_btn = make_imgbtn('play_72dp', lambda: print('play'))
        backpack_btn = make_imgbtn('backpack_72dp', lambda: print('backpack'))
        btn_group = tp.Group([settings_btn, play_btn, backpack_btn], 'h', (0, 0), 48)

        title = tp.OutlinedText('ERIKA', 72)
        center_group = tp.Group([title, btn_group], 'v', (0, 0), 24)
        center_group.center_on(self.screen)

        return [close_btn, center_group]
