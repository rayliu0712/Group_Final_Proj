from pygame import K_F1
from thorpy import Button, exit_app, OutlinedText, TitleBox, Text
from .core import KeyEventHandler, LauncherWrapper, Screen, PageWrapper, SimpleGroup, SimpleImageButton
from .game import Game


class Home(PageWrapper):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        close_btn.set_topright(Screen.width(), 0)

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = OutlinedText('ERIKA', 72)
        play_btn = SimpleImageButton('play_72dp.png', Game(False))
        center_group = SimpleGroup([title, play_btn], 'v')

        other = SimpleGroup([close_btn, settings_btn, center_group])

        settings_btn.at_unclick = self.__wrap_settings(other)

        return [other]

    def __wrap_settings(self, other: SimpleGroup) -> LauncherWrapper:
        kandler = KeyEventHandler(True)
        credits_btn = Button('Credits(F1)')
        settings_box = TitleBox('Settings', [credits_btn])
        settings_box.set_opacity_bck_color(255)
        Screen.center(settings_box)

        credits_box = TitleBox('Credits', [Text('Me')])
        credits_box.set_opacity_bck_color(255)
        Screen.center(credits_box)

        credits_wrapper = LauncherWrapper(lambda: credits_box.launch_and_lock_others(other))
        credits_btn.at_unclick = credits_wrapper
        kandler += credits_btn, [], [K_F1]

        return LauncherWrapper(lambda: settings_box.launch_and_lock_others(other, kandler))
