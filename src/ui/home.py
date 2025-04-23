from pygame import K_F1
from thorpy import exit_app, OutlinedText, TitleBox, Text, Button
from .core import PopupWrapper, Screen, PageWrapper, SimpleGroup, SimpleImageButton
from .game import Game


class Home(PageWrapper):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        close_btn.set_topright(Screen.width(), 0)

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = OutlinedText('ERIKA', 72)
        subtitle = OutlinedText('F1: Credits\nESC: Quit')
        play_btn = SimpleImageButton('play_72dp.png', Game(False))
        center_group = SimpleGroup([title, subtitle, play_btn], 'v')

        other = SimpleGroup([close_btn, settings_btn, center_group])

        credits_box = TitleBox('Credits', [Text('Credits Test')])
        credits_box.set_opacity_bck_color(255)
        Screen.center(credits_box)

        settings_box = TitleBox('Settings', [Button('Settings Test')])
        settings_box.set_opacity_bck_color(255)
        Screen.center(settings_box)

        self._bind_keys(PopupWrapper(credits_box, other), [], [K_F1])
        settings_btn.at_unclick = PopupWrapper(settings_box, other)

        return [other]
