import pygame
from thorpy import ImageButton, Group
from thorpy.canonical import Element
from typing import Callable, Optional

type Action = Callable[[], None]


class SimpleImageButton(ImageButton):
    def __init__(self, filename: str, onclick: Optional[Action]) -> None:
        super().__init__('', pygame.image.load(f'assets/image/{filename}'))
        self.at_unclick = onclick


class SimpleGroup(Group):
    def __init__(self, elements: list[Element], mode: Optional[str] = None, gap=0, margin: tuple[int, int] = (0, 0)) -> None:
        '''
        NOTE : SimpleGroup __init__ default parameters greatly differ from tp.Group

        - params
            gap = 0
            margin = (0,0)
            when mode is None, margin and gap will not be used
        '''
        super().__init__(elements, mode, margin, gap)


class SimplePopup:
    def __init__(self, element: Element, other: Element) -> None:
        '''
        Create an action that pops up an element

        Parameters:
            element: the element you want to pop up
            other: the element you want to stay visible, it can be a group or box if multiple elements should stay visible
        '''
        self.element = element
        self.other = other

    def __call__(self) -> None:
        self.element.launch_and_lock_others(self.other, click_outside_cancel=True)
