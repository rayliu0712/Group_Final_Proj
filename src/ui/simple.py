import pygame
from thorpy import ImageButton, Group
from thorpy.canonical import Element, arrow_cursor
from typing import Callable, Optional, Any

type Action = Callable[[], Any]


def SimpleImageButton(filename: str, onclick: Optional[Action]) -> ImageButton:
    btn = ImageButton('', pygame.image.load(f'assets/image/{filename}'))
    btn.at_unclick = onclick
    return btn


def SimpleGroup(elements: list[Element], mode: Optional[str] = None, gap=0) -> Group:
    '''
    NOTE : SimpleGroup __init__ default parameters greatly differ from tp.Group

    - params
        gap = 0
        when mode is None, gap will not be used
    '''
    assert isinstance(elements, list), 'param "elements" should be list[Element]'
    group = Group(elements, mode, (0, 0), gap)
    return group


def SimplePopup(element: Element, other: Element) -> Action:
    '''
    Create an action that pops up an element

    Parameters:
        element: the element you want to pop up
        other: the element you want to stay visible, it can be a group or box if multiple elements should stay visible
    '''
    def func():
        new_loop_cursor_fix()
        element.launch_and_lock_others(other, click_outside_cancel=True)

    return func


# not my fault, blame tp2 author
def new_loop_cursor_fix():
    '''
    call it before launching a new loop
    '''
    pygame.mouse.set_cursor(arrow_cursor)
