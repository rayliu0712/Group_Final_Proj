import pygame as pg
import thorpy as tp
from thorpy.canonical import Element
from typing import Callable, Optional


class SimpleImageButton(tp.ImageButton):
    def __init__(self, filename: str, onclick: Optional[Callable[[], None]]) -> None:
        super().__init__('', pg.image.load(f'assets/image/{filename}'))
        self.at_unclick = onclick


class SimpleGroup(tp.Group):
    def __init__(self, elements: list[Element], mode: Optional[str] = None, gap=0, margin: tuple[int, int] = (0, 0)) -> None:
        '''
        NOTE : SimpleGroup __init__ default parameters greatly differ from tp.Group

        - params
            gap = 0
            margin = (0,0)
            when mode is None, margin and gap will not be used
        '''
        super().__init__(elements, mode, margin, gap)


def pop_up(element: Element, other: Element) -> None:
    '''
    pop up an element

    - params
        element: the element you want to pop up
        other: the element you want to stay visible, it can be a group or box if multiple elements should stay visible.
    '''
    element.launch_and_lock_others(other, click_outside_cancel=True)
