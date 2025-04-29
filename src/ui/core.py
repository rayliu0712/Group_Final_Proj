from .check import *
from abc import ABC, abstractmethod
from enum import Enum

from thorpy.elements import *
from thorpy.loops import quit_current_loop, exit_app

from pygame.constants import *
from pygame.surface import Surface

import pygame
import thorpy
import functools
import operator


class SimpleButton(Button):
    def __init__(self, text: str, onclick: Optional[Action] = None):
        assert isstr(text) and isoptcall(onclick)
        super().__init__(text)
        self.at_unclick = onclick


class SimpleImageButton(ImageButton):
    def __init__(self, filename: str, onclick: Optional[Action] = None):
        assert isstr(filename) and isoptcall(onclick)
        super().__init__('', pygame.image.load(f'assets/image/{filename}'))
        self.at_unclick = onclick


class SimpleTitleBox(TitleBox):
    def __init__(self, title: str, children: list[Element], mode: Optional[str] = 'v'):
        assert iselist(children), 'param "children" should be list[Element]'
        assert isstr(title)
        super().__init__(title, children, False)
        if mode:
            super().sort_children(mode)
        super().set_opacity_bck_color(191)  # 256 * 3/4 - 1


class Screen:
    # Singleton
    def __new__(cls) -> Surface:
        return thorpy.parameters.screen

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()

    @staticmethod
    def center(element: Element) -> None:
        assert ise(element)
        element.center_on(Screen())

    @staticmethod
    def topleft(element: Element) -> None:
        assert ise(element)
        element.set_topleft(0, 0)

    @staticmethod
    def topright(element: Element) -> None:
        assert ise(element)
        element.set_topright(Screen.width(), 0)

    @staticmethod
    def bottomleft(element: Element) -> None:
        assert ise(element)
        element.set_bottomleft(0, Screen.height())

    @staticmethod
    def bottomright(element: Element) -> None:
        assert ise(element)
        element.set_bottomright(Screen.width(), Screen.height())


class _KeyEventHandler:
    class _KeyAction:
        def __init__(self, action: Action, mods: int, keys: list[int]):
            self.occupied = False
            self.action = action
            self.mods = mods
            self.keys = keys

        def __eq__(self, value: object) -> bool:
            if not isinstance(value, _KeyEventHandler._KeyAction):
                return False
            return self.action == value.action and self.mods == value.mods and self.keys == value.keys

    def __init__(self, is_esc_quit: bool):
        self.__is_esc_quit = is_esc_quit
        self.__kactions: list[_KeyEventHandler._KeyAction] = []

    def __iadd__(self, args: tuple[Button | Action, list[int], list[int]]) -> Self:
        '''
        args[0] : button or action
        args[1] : mod keys, list[int] (can be empty)
        args[2] : keys, list[int] (cannot be empty)
        '''
        assert (istuple3(args) and
                (callable(args[0]) or isinstance(args[0], Button)) and
                isintlist(args[1]) and
                isintlist(args[2])
                ), 'param "key_action" should be tuple[Button | Action, list[int], list[int]]'

        assert args[2], 'list "key_action[2]" cannot be empty'

        action = args[0] if callable(args[0]) else args[0].at_unclick
        mods = functools.reduce(operator.or_, args[1], 0)
        keys = args[2]
        kaction = _KeyEventHandler._KeyAction(action, mods, keys)

        assert not (self.__is_esc_quit and K_ESCAPE in keys), 'esc quit is on, you cannot register esc key'
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
    def __init__(self):
        '''
        WARNING : don't construt popup_wrapper by construtor. Instead, use class method
        Popup is lazy, call its instance to show
        '''
        self.kandler = _KeyEventHandler(True)

    def __call__(self) -> None:
        _fix_new_loop_cursor()
        self.launch()

    def launch(self) -> None:
        pass

    @classmethod
    def Alone(cls, element: Element) -> Self:
        assert ise(element)
        popup_wrapper = cls()
        popup_wrapper.launch = lambda: element.launch_alone(popup_wrapper.kandler)
        return popup_wrapper

    @classmethod
    def LockAndLaunch(cls, be_locked_elements: list[Element], be_launched_element: Element) -> Self:
        assert iselist(be_locked_elements) and ise(be_launched_element)
        be_locked_elements = be_locked_elements[0] if len(be_locked_elements) == 1 else Group(be_locked_elements, None)

        popup_wrapper = cls()
        popup_wrapper.launch = lambda: be_launched_element.launch_and_lock_others(be_locked_elements, popup_wrapper.kandler)
        return popup_wrapper

    @classmethod
    def Merge(cls, element: Element, click_outside_cancel: bool) -> Self:
        assert ise(element)
        popup_wrapper = cls()
        popup_wrapper.launch = lambda: element.launch_nonblocking(click_outside_cancel=click_outside_cancel)
        return popup_wrapper


class Page(ABC):
    def __init__(self) -> None:
        '''
        Page is lazy, call its instance to show
        '''
        self._kandler = _KeyEventHandler(False)

    def __call__(self) -> None:
        self._kandler.clear()
        es = self._build()
        assert iselist(es), 'method "_build()" should return list[Element]'

        _fix_new_loop_cursor()
        if len(es) == 1:
            es[0].get_updater().launch(self._kandler)
        else:
            Group(es, None).get_updater().launch(self._kandler)

    @abstractmethod
    def _build(self) -> list[Element]:
        pass
