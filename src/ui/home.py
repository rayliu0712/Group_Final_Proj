import thorpy as tp
from .page import Page
from .simple import SimpleImageButton, SimpleGroup, pop_up


class Home(Page):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', tp.exit_app)
        close_btn.set_topright(self.screen_width(), 0)

        settings_btn = SimpleImageButton('settings_72dp.png', None)
        settings_btn.set_topleft(0, 0)

        title = tp.OutlinedText('ERIKA', 72)
        play_btn = SimpleImageButton('play_72dp.png', lambda: print('play'))
        center_group = SimpleGroup([title, play_btn], 'v')

        other = SimpleGroup([close_btn, settings_btn, center_group])

        credits_box = tp.TitleBox('Credits', [tp.Text('test')])
        credits_box.set_opacity_bck_color(255)
        self._center(credits_box)

        settings_box = tp.TitleBox('Settings', [tp.Button('test')])
        settings_box.set_opacity_bck_color(255)
        self._center(settings_box)

        title.at_unclick = lambda: pop_up(credits_box, other)
        settings_btn.at_unclick = lambda: pop_up(settings_box, other)

        return other
