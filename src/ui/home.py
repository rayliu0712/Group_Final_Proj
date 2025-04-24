from pygame import K_F1
from thorpy import exit_app, OutlinedText, TitleBox, Text, Button
from .core import LauncherWrapper, Screen, PageWrapper, SimpleGroup, SimpleImageButton
from .game import Game


class Home(PageWrapper):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        close_btn.set_topright(Screen.width(), 0)

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = OutlinedText('ERIKA', 72)
        subtitle = OutlinedText('F1: Credits')
        play_btn = SimpleImageButton('play_72dp.png', Game())
        center_group = SimpleGroup([title, subtitle, play_btn], 'v')

        credits_box = TitleBox('Credits', [Text('Credits Test')])
        credits_box.set_opacity_bck_color(255)
        Screen.center(credits_box)

        other = SimpleGroup([close_btn, settings_btn, center_group])

        settings_box = TitleBox('Settings', [Button('Settings Test')])
        settings_box.set_opacity_bck_color(255)
        Screen.center(settings_box)

        credits_wrapper = LauncherWrapper(lambda: credits_box.launch_and_lock_others(other))
        self._key_handler += credits_wrapper, [], [K_F1]

        settings_wrapper = LauncherWrapper(lambda: settings_box.launch_and_lock_others(other))
        settings_btn.at_unclick = settings_wrapper

        return [other]
