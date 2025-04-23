import pygame
from pygame import Surface
from thorpy import get_screen, Button
from thorpy.canonical import Element
from abc import ABC, abstractmethod
from .simple import SimpleGroup, Action
from typing import Optional
from functools import reduce
import operator


class Screen():
    __instance: Optional[Surface] = None

    # singleton
    def __new__(cls) -> Surface:
        if Screen.__instance is None:
            Screen.__instance = get_screen()
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


class Page(ABC):
    class _ActionInfo:
        def __init__(self, action: Action, mods: int, keys: list[int]) -> None:
            self.available = True
            self.action = action
            self.mods = mods
            self.keys = keys

    def __init__(self) -> None:
        Screen().fill((250, 250, 250))
        self._action_infoes: list[Page._ActionInfo] = []

        es = self._build()
        es = es[0] if len(es) == 1 else SimpleGroup(es)

        def trigger() -> None:
            pressed_mods = pygame.key.get_mods()
            pressed_keys = pygame.key.get_pressed()

            for action_info in self._action_infoes:
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

        es.get_updater().launch(func_after=trigger)

    @abstractmethod
    def _build(self) -> list[Element]:
        pass

    def _bind_keys(self, value: Button | Action, mods: list[int], keys: list[int]) -> None:
        action = value.at_unclick if isinstance(value, Button) else value
        mods: int = reduce(operator.or_, mods, 0) if mods else 0

        action_info = Page._ActionInfo(action, mods, keys)
        self._action_infoes.append(action_info)
