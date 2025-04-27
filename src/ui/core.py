from typing import Callable, Any, Optional, Self
from abc import ABC, abstractmethod

from thorpy.elements import *
from thorpy.canonical import Element
from thorpy.loops import quit_current_loop, exit_app

from pygame.constants import *
from pygame.surface import Surface

import pygame
import thorpy
import functools
import operator

type Action = Callable[[], Any]


class SimpleGroup(Group):
    def __init__(self, elements: list[Element], mode: Optional[str] = None, gap: int = 0) -> None:
        '''
        NOTE : SimpleGroup __init__ default parameters greatly differ from tp.Group

        - params
            gap = 0
            when mode is None, gap will not be used
        '''
        assert isinstance(elements, list) and all(isinstance(e, Element) for e in elements), 'param "elements" should be list[Element]'
        assert (mode is None or isinstance(mode, str)) and isinstance(gap, int)
        super().__init__(elements, mode, (0, 0), gap)


class SimpleImageButton(ImageButton):
    def __init__(self, filename: str, onclick: Optional[Action]) -> None:
        assert isinstance(filename, str) and (onclick is None or callable(onclick))
        super().__init__('', pygame.image.load(f'assets/image/{filename}'))
        self.at_unclick = onclick


class Screen():

    # Singleton
    def __new__(cls) -> Surface:
        return thorpy.parameters.screen

    @staticmethod
    def center(element: Element) -> None:
        assert isinstance(element, Element)
        element.center_on(Screen())

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()


class _KeyEventHandler:
    class _KeyAction:
        def __init__(self, action: Action, mods: int, keys: list[int]) -> None:
            assert callable(action) and isinstance(mods, int) and isinstance(keys, list) and all(isinstance(k, int) for k in keys)
            self.occupied = False
            self.action = action
            self.mods = mods
            self.keys = keys

        def __eq__(self, value: object) -> bool:
            if not isinstance(value, _KeyEventHandler._KeyAction):
                return False
            return self.action == value.action and self.mods == value.mods and self.keys == value.keys

    def __init__(self, esc_quit: bool) -> None:
        self.esc_quit = esc_quit
        self.__kactions: list[_KeyEventHandler._KeyAction] = []

    def __iadd__(self, args: tuple[Button | Action, list[int], list[int]]) -> Self:
        '''
        args[0] : button or action
        args[1] : mod keys, list[int] (can be empty)
        args[2] : keys, list[int] (cannot be empty)
        '''
        assert (isinstance(args, tuple) and
                len(args) == 3 and
                (callable(args[0]) or isinstance(args[0], Button)) and
                isinstance(args[1], list) and all(isinstance(mod, int) for mod in args[1]) and
                isinstance(args[2], list) and all(isinstance(key, int) for key in args[2])
                ), 'param "key_action" should be tuple[Button | Action, list[int], list[int]]'

        assert args[2], 'list "key_action[2]" cannot be empty'

        action = args[0] if callable(args[0]) else args[0].at_unclick
        mods = functools.reduce(operator.or_, args[1], 0)
        keys = args[2]
        kaction = _KeyEventHandler._KeyAction(action, mods, keys)

        assert not self.esc_quit or K_ESCAPE not in keys, 'esc_quit is on, you cannot register esc key'
        assert kaction not in self.__kactions, f'the combination key has already been registered'
        self.__kactions.append(kaction)

        return self

    def __call__(self) -> None:
        Screen().fill((250, 250, 250))

        pressed_mods = pygame.key.get_mods()
        pressed_keys = pygame.key.get_pressed()

        for kaction in self.__kactions:
            action, mods, keys = kaction.action, kaction.mods, kaction.keys

            are_mods_pressed = pressed_mods & mods
            are_keys_pressed = all(pressed_keys[k] for k in keys)
            if (mods == 0 or are_mods_pressed) and are_keys_pressed:
                if not kaction.occupied:
                    kaction.occupied = True
                    action()
                    kaction.occupied = False
            else:
                kaction.occupied = False  # others actions are not occupied

    def clear(self) -> None:
        self.__kactions.clear()


def _fix_new_loop_cursor() -> None:
    pygame.mouse.set_cursor(thorpy.canonical.arrow_cursor)


class Popup:
    def __init__(self) -> None:
        '''
        WARNING : don't construt popup_wrapper by construtor. Instead, use class method
        '''
        self.launcher: Action
        self.kandler = _KeyEventHandler(True)

    @classmethod
    def Alone(cls, element: Element) -> Self:
        popup_wrapper = cls()
        popup_wrapper.launcher = lambda: element.launch_alone(popup_wrapper.kandler)
        return popup_wrapper

    @classmethod
    def LockAndLaunch(cls, be_locked_element: Element, be_launched_element: Element) -> Self:
        popup_wrapper = cls()
        popup_wrapper.launcher = lambda: be_launched_element.launch_and_lock_others(be_locked_element, popup_wrapper.kandler)
        return popup_wrapper

    @classmethod
    def Merge(cls, element: Element, click_outside_cancel: bool) -> Self:
        popup_wrapper = cls()
        popup_wrapper.launcher = lambda: element.launch_nonblocking(click_outside_cancel=click_outside_cancel)
        return popup_wrapper

    def __call__(self) -> None:
        _fix_new_loop_cursor()
        self.launcher()


class Page(ABC):
    def __init__(self) -> None:
        self._kandler = _KeyEventHandler(False)
        self._kandler.esc_quit = False

    def __call__(self) -> None:
        self._kandler.clear()
        es = self._build()
        assert isinstance(es, list) and all(isinstance(e, Element) for e in es), 'method "_build()" should return list[Element]'

        _fix_new_loop_cursor()
        if len(es) == 1:
            es[0].get_updater().launch(self._kandler)
        else:
            SimpleGroup(es).get_updater().launch(self._kandler)

    @abstractmethod
    def _build(self) -> list[Element]:
        pass
