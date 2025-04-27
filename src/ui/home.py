from .core import *
from .game import Game


class Home(Page):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        close_btn.set_topright(Screen.width(), 0)

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = OutlinedText('ERIKA', 72)
        play_btn = SimpleImageButton('play_72dp.png', Game())
        center_group = SimpleGroup([title, play_btn], 'v')

        other = SimpleGroup([close_btn, settings_btn, center_group])

        settings_btn.at_unclick = self.__pop_up_settings(other)

        return [other]

    def __pop_up_settings(self, other: SimpleGroup) -> Popup:
        credits_btn = Button('Credits(F1)')
        settings_box = TitleBox('Settings', [credits_btn])
        settings_box.set_opacity_bck_color(255)
        Screen.center(settings_box)
        settings_popup = Popup.LockAndLaunch(other, settings_box)

        credits_box = TitleBox('Credits', [Text('Me')])
        credits_box.set_opacity_bck_color(255)
        Screen.center(credits_box)

        credits_btn.at_unclick = Popup.LockAndLaunch(other, credits_box)

        settings_popup.kandler += credits_btn, [], [K_F1]

        return settings_popup
