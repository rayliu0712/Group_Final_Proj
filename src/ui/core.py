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


type IntTuple = tuple[int, ...]


class Page(ABC):
    class _ActionState:
        def __init__(self, action: Action) -> None:
            self.available = True
            self.action = action

    def __init__(self) -> None:
        Screen().fill((250, 250, 250))
        self._kevents: dict[tuple[int, IntTuple], Page._ActionState] = {}

        es = self._build()
        es = es[0] if len(es) == 1 else SimpleGroup(es)

        def trigger() -> None:
            pressed_mods = pygame.key.get_mods()
            pressed_keys = pygame.key.get_pressed()
            for (mods, keys), action_state in self._kevents.items():
                are_mods_pressed = pressed_mods & mods
                are_keys_pressed = all(pressed_keys[k] for k in keys)
                if (mods == 0 or are_mods_pressed) and are_keys_pressed:
                    if action_state.available:
                        action_state.available = False
                        action_state.action()
                    else:
                        pass  # keys have not been released yet
                else:
                    action_state.available = True  # others actions are available

        es.get_updater().launch(func_after=trigger)

    @abstractmethod
    def _build(self) -> list[Element]:
        pass

    def _bind_keys(self, value: Button | Action, mods: IntTuple, keys: IntTuple) -> None:
        event = Page._ActionState(value.at_unclick if isinstance(value, Button) else value)
        mods: int = reduce(operator.or_, mods, 0) if mods else 0
        self._kevents[(mods, keys)] = event
