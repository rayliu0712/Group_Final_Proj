import pygame
from pygame import Surface
from thorpy import Group, ImageButton, get_screen, Button
from thorpy.canonical import Element, arrow_cursor
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional
from functools import reduce
import operator

type Action = Callable[[], Any]


def SimpleGroup(elements: list[Element], mode: Optional[str] = None, gap: int = 0) -> Group:
    '''
    NOTE : SimpleGroup __init__ default parameters greatly differ from tp.Group

    - params
        gap = 0
        when mode is None, gap will not be used
    '''
    assert isinstance(elements, list) and all(isinstance(e, Element) for e in elements), 'method "_build()" should return list[Element]'
    assert (mode is None or isinstance(mode, str)) and isinstance(gap, int)
    group = Group(elements, mode, (0, 0), gap)
    return group


def SimpleImageButton(filename: str, onclick: Optional[Action]) -> ImageButton:
    assert isinstance(filename, str) and (onclick is None or callable(onclick))
    btn = ImageButton('', pygame.image.load(f'assets/image/{filename}'))
    btn.at_unclick = onclick
    return btn


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
        assert isinstance(element, Element)
        element.center_on(Screen())

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()


class KeyEventHandler:
    class __KeyAction:
        def __init__(self, action: Action, mods: int, keys: list[int]) -> None:
            assert callable(action) and isinstance(mods, int) and isinstance(keys, list) and all(isinstance(k, int) for k in keys)
            self.occupied = False
            self.action = action
            self.mods = mods
            self.keys = keys

    def __init__(self) -> None:
        self.__kactions: set[KeyEventHandler.__KeyAction] = set()

    def __iadd__(self, args: tuple[Button | Action, list[int], list[int]]) -> "KeyEventHandler":
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
        mods = reduce(operator.or_, args[1], 0)
        keys = args[2]
        kaction = KeyEventHandler.__KeyAction(action, mods, keys)

        assert kaction not in self.__kactions, f'mod keys "{mods}", keys "{keys}" has already been registered'
        self.__kactions.add(kaction)
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
            else:
                kaction.occupied = False  # others actions are not occupied


def LauncherWrapper(launcher: Action) -> Action:
    assert callable(launcher)

    def action() -> None:
        pygame.mouse.set_cursor(arrow_cursor)  # patch
        launcher()
    return action


class PageWrapper(ABC):
    def __init__(self) -> None:
        self._key_handler = KeyEventHandler()

    def __call__(self) -> None:
        elements = self._build()
        assert isinstance(elements, list) and all(isinstance(e, Element) for e in elements), 'method "_build()" should return list[Element]'
        elements = elements[0] if len(elements) == 1 else SimpleGroup(elements)

        launcher = LauncherWrapper(lambda: elements.get_updater(esc_quit=True).launch(self._key_handler))
        launcher()

    @abstractmethod
    def _build(self) -> list[Element]:
        pass
