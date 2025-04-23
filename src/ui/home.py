from pygame import KMOD_ALT, K_q
from thorpy import exit_app, OutlinedText, TitleBox, Text, Button
from .core import Screen, Page
from .simple import SimpleImageButton, SimpleGroup, SimplePopup


class Home(Page):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        close_btn.set_topright(Screen.width(), 0)
        mods = (KMOD_ALT, )
        keys = (K_q, )
        self._bind_keys(close_btn, mods, keys)  # for example

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = OutlinedText('ERIKA', 72)
        play_btn = SimpleImageButton('play_72dp.png', lambda: print('play'))
        center_group = SimpleGroup([title, play_btn], 'v')

        other = SimpleGroup([close_btn, settings_btn, center_group])

        credits_box = TitleBox('Credits', [Text('test')])
        credits_box.set_opacity_bck_color(255)
        Screen.center(credits_box)

        settings_box = TitleBox('Settings', [Button('test')])
        settings_box.set_opacity_bck_color(255)
        Screen.center(settings_box)

        title.at_unclick = SimplePopup(credits_box, other)
        settings_btn.at_unclick = SimplePopup(settings_box, other)

        return [other]
