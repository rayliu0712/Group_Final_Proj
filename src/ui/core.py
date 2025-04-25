import pygame
from pygame import K_ESCAPE, Surface
from thorpy import Group, ImageButton, get_screen, Button
from thorpy.canonical import Element, arrow_cursor
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional
from functools import reduce
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
    class KeyAction:
        def __init__(self, action: Action, mods: int, keys: list[int]) -> None:
            assert callable(action) and isinstance(mods, int) and isinstance(keys, list) and all(isinstance(k, int) for k in keys)
            self.occupied = False
            self.action = action
            self.mods = mods
            self.keys = keys

        def __eq__(self, value: object) -> bool:
            if not isinstance(value, KeyEventHandler.KeyAction):
                return False
            return self.action == value.action and self.mods == value.mods and self.keys == value.keys

    def __init__(self, esc_quit: bool) -> None:
        self.__esc_quit = esc_quit
        self.__kactions: list[KeyEventHandler.KeyAction] = []

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
        kaction = KeyEventHandler.KeyAction(action, mods, keys)

        assert not self.__esc_quit or K_ESCAPE not in keys, 'esc_quit is on, you cannot register esc key'
        assert kaction not in self.__kactions, f'mod keys "{mods}", keys "{keys}" has already been registered'
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


class LauncherWrapper:
    def __init__(self, launcher: Action) -> None:
        assert callable(launcher)
        self.__launcher = launcher

    def __call__(self) -> None:
        pygame.mouse.set_cursor(arrow_cursor)  # patch
        self.__launcher()


class PageWrapper(ABC):
    def __init__(self, esc_quit: bool) -> None:
        self._kandler = KeyEventHandler(esc_quit)
        self._esc_quit = esc_quit

    def __call__(self) -> None:
        self._kandler.clear()
        es = self._build()
        assert isinstance(es, list) and all(isinstance(e, Element) for e in es), 'method "_build()" should return list[Element]'
        es = es[0] if len(es) == 1 else SimpleGroup(es)

        def launcher() -> None:
            es.get_updater(esc_quit=self._esc_quit).launch(self._kandler)
        LauncherWrapper(launcher)()

    @abstractmethod
    def _build(self) -> list[Element]:
        pass
