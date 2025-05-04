from .core import *
from .game import GameMan


class Home(Page):

    def _build(self):
        close_btn = mkImageButton("close_72dp.png", exit_app)
        Screen.topright(close_btn)

        settings_btn = mkImageButton("settings_72dp.png")
        Screen.topleft(settings_btn)

        title = OutlinedText("ERIKA", 72)
        play_btn = mkImageButton("play_72dp.png", GameMan())
        center_group = Group([title, play_btn])
        Screen.center(center_group)

        main_elements = [close_btn, settings_btn, center_group]

        settings_btn.at_unclick = self.__popup_settings(main_elements)

        return main_elements

    def __popup_settings(self, be_locked_elements: list) -> Popup:
        credits_btn = Button("Credits(F1)")
        settings_box = mkTitleBox("Settings", [credits_btn])
        Screen.center(settings_box)
        settings_popup = Popup.LockAndLaunch(be_locked_elements, settings_box)

        credits_box = mkTitleBox("Credits", [Text("Me")])
        Screen.center(credits_box)

        credits_btn.at_unclick = Popup.LockAndLaunch(be_locked_elements, credits_box)
        settings_popup.kandler += credits_btn, [], [K_F1]

        return settings_popup
