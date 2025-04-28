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
        center_group = Group([title, play_btn])

        main_elements = [close_btn, settings_btn, center_group]

        settings_btn.at_unclick = self.__popup_settings(main_elements)

        return main_elements

    def __popup_settings(self, be_locked_elements: list[Element]) -> Popup:
        credits_btn = Button('Credits(F1)')
        settings_box = SimpleTitleBox('Settings', [credits_btn])
        Screen.center(settings_box)
        settings_popup = Popup.LockAndLaunch(be_locked_elements, settings_box)

        credits_box = SimpleTitleBox('Credits', [Text('Me')])
        Screen.center(credits_box)

        credits_btn.at_unclick = Popup.LockAndLaunch(be_locked_elements, credits_box)
        settings_popup.kandler += credits_btn, [], [K_F1]

        return settings_popup
