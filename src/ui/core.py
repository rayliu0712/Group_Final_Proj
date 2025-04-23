import pygame
from pygame import Surface
from thorpy import Group, ImageButton, get_screen, Button
from thorpy.canonical import Element, arrow_cursor
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional
from functools import reduce
import operator

type Action = Callable[[], Any]


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


def SimpleImageButton(filename: str, onclick: Optional[Action]) -> ImageButton:
    btn = ImageButton('', pygame.image.load(f'assets/image/{filename}'))
    btn.at_unclick = onclick
    return btn


def fix_new_loop_cursor() -> None:
    '''
    not my fault, blame tp2 author
    call it before launching a new loop
    '''
    pygame.mouse.set_cursor(arrow_cursor)


def PopupWrapper(element: Element, other: Element) -> Action:
    '''
    Create an action that pops up an element

    Parameters:
        element: the element you want to pop up
        other: the element you want to stay visible, it can be a group or box if multiple elements should stay visible
    '''
    def func() -> None:
        fix_new_loop_cursor()
        element.launch_and_lock_others(other, click_outside_cancel=True)

    return func


class Screen():
    __instance: Optional[Surface] = None

    # Singleton
    def __new__(cls) -> Surface:
        if Screen.__instance is None:
            Screen.__instance = get_screen()
        assert Screen.__instance is not None
        return Screen.__instance

    @staticmethod
    def center(element: Element) -> None:
        element.center_on(Screen())

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()


class PageWrapper(ABC):
    class _ActionInfo:
        def __init__(self, action: Action, mods: int, keys: list[int]) -> None:
            self.available = True
            self.action = action
            self.mods = mods
            self.keys = keys

    def __init__(self, esc_quit: bool) -> None:
        self._esc_quit = esc_quit

    # Lazy
    def __call__(self) -> None:
        self._action_infos: list[PageWrapper._ActionInfo] = []

        es = self._build()
        assert isinstance(es, list), 'method "_build()" should return list[Element]'
        es = es[0] if len(es) == 1 else SimpleGroup(es)

        def trigger() -> None:
            pressed_mods = pygame.key.get_mods()
            pressed_keys = pygame.key.get_pressed()

            for action_info in self._action_infos:
                action, mods, keys = action_info.action, action_info.mods, action_info.keys

                are_mods_pressed = pressed_mods & mods
                are_keys_pressed = all(pressed_keys[k] for k in keys)
                if (mods == 0 or are_mods_pressed) and are_keys_pressed:
                    if action_info.available:
                        action_info.available = False
                        action()
                    else:
                        pass  # keys have not been released yet
                else:
                    action_info.available = True  # others actions are available

        fix_new_loop_cursor()
        es.get_updater(esc_quit=self._esc_quit).launch(func_after=trigger)

    @abstractmethod
    def _build(self) -> list[Element]:
        pass

    def _bind_keys(self, value: Button | Action, mods: list[int], keys: list[int]) -> None:
        assert isinstance(mods, list), 'param "mods" should be list[int]'
        assert isinstance(keys, list), 'param "keys" should be list[int]'

        action = value.at_unclick if isinstance(value, Button) else value
        mods: int = reduce(operator.or_, mods, 0) if mods else 0

        action_info = PageWrapper._ActionInfo(action, mods, keys)
        self._action_infos.append(action_info)
