from typing import Callable, Any, Optional, Self, Literal
from abc import ABC, abstractmethod

import thorpy
from thorpy.loops import quit_current_loop, exit_app
from thorpy.elements import *

import pygame
from pygame.surface import Surface
from pygame.constants import *

import functools
import operator


type Action = Callable[[], None]


def lazy(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        return lambda: func(*args, **kwargs)
    return wrapper


def is_pygame_quit() -> bool:
    return any(e.type == pygame.QUIT for e in pygame.event.get())


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)


def mkButton(text: str, onclick: Optional[Action] = None) -> Button:
    btn = Button(text)
    btn.at_unclick = onclick
    return btn


def mkImageButton(filename: str, onclick: Optional[Action] = None) -> ImageButton:
    imgbtn = ImageButton("", pygame.image.load(f"assets/image/{filename}"))
    imgbtn.at_unclick = onclick
    return imgbtn


def mkBox(children: list, mode: Literal["v", "h", "grid", None] = "v") -> Box:
    box = Box(children, False)
    if mode:
        box.sort_children(mode)
    return box


def mkTitleBox(title: str, children: list, mode: Literal["v", "h", "grid", None] = "v") -> Box:
    titlebox = TitleBox(title, children, False)
    if mode:
        titlebox.sort_children(mode)
    titlebox.set_opacity_bck_color(191)  # 256 * 3/4 - 1
    return titlebox


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
    def center(element: Element, margin: tuple[int, int] = (0, 0)) -> None:
        element.set_center(Screen.width() // 2 + margin[0], Screen.height() // 2 + margin[1])

    @staticmethod
    def topleft(element: Element, margin: tuple[int, int] = (0, 0)) -> None:
        element.set_topleft(0 + margin[0], 0 + margin[1])

    @staticmethod
    def topright(element: Element, margin: tuple[int, int] = (0, 0)) -> None:
        element.set_topright(Screen.width() + margin[0], 0 + margin[1])

    @staticmethod
    def bottomleft(element: Element, margin: tuple[int, int] = (0, 0)) -> None:
        element.set_bottomleft(0 + margin[0], Screen.height() + margin[1])

    @staticmethod
    def bottomright(element: Element, margin: tuple[int, int] = (0, 0)) -> None:
        element.set_bottomright(Screen.width() + margin[0], Screen.height() + margin[1])


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
        """
        args[0] : button or action
        args[1] : mod keys, list[int] (can be empty)
        args[2] : keys, list[int] (cannot be empty)
        """
        action = args[0] if callable(args[0]) else args[0].at_unclick
        mods = functools.reduce(operator.or_, args[1], 0)
        keys = args[2]
        kaction = _KeyEventHandler._KeyAction(action, mods, keys)

        if self.__is_esc_quit and K_ESCAPE in keys:
            raise Exception("esc quit is on, you cannot register esc key")
        if kaction in self.__kactions:
            raise Exception("the combination key has already been registered")
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
        """
        WARNING : don"t construt popup_wrapper by construtor. Instead, use class method
        Popup is lazy, call its instance to show
        """
        self.kandler = _KeyEventHandler(True)

    def __call__(self) -> None:
        _fix_new_loop_cursor()
        self.launch()

    def launch(self) -> None:
        pass

    @classmethod
    def Alone(cls, element: Element) -> Self:
        popup_wrapper = cls()
        popup_wrapper.launch = lambda: element.launch_alone(popup_wrapper.kandler)
        return popup_wrapper

    @classmethod
    def LockAndLaunch(cls, be_locked_elements: list, be_launched_element: Element) -> Self:
        popup_wrapper = cls()

        def launch(le: Element) -> None:
            be_launched_element.launch_and_lock_others(le, popup_wrapper.kandler)

        if len(be_locked_elements) == 1:
            popup_wrapper.launch = lambda: launch(be_locked_elements[0])
        else:
            popup_wrapper.launch = lambda: launch(Group(be_locked_elements, None))

        return popup_wrapper

    @classmethod
    def Merge(cls, element: Element, click_outside_cancel: bool) -> Self:
        popup_wrapper = cls()
        popup_wrapper.launch = lambda: element.launch_nonblocking(click_outside_cancel=click_outside_cancel)
        return popup_wrapper


class Page(ABC):
    def __init__(self) -> None:
        """
        Page is lazy, call its instance to show
        """
        self._kandler = _KeyEventHandler(False)

    def __call__(self) -> None:
        self._kandler.clear()
        es: list[Element] = self._build()

        _fix_new_loop_cursor()
        match len(es):
            case 0:
                pass
            case 1:
                es[0].get_updater().launch(self._kandler)
            case _:
                Group(es, None).get_updater().launch(self._kandler)

    @abstractmethod
    def _build(self) -> list:
        pass
