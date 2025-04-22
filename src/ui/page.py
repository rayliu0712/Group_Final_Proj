import pygame as pg
from thorpy.canonical import Element
from abc import ABC, abstractmethod
from .simple import SimpleGroup


class Page(ABC):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.screen_width = self.screen.get_width
        self.screen_height = self.screen.get_height
        self.screen.fill((250, 250, 250))

        elements = self._build()
        if isinstance(elements, Element):
            elements.get_updater().launch()
        else:
            SimpleGroup(elements).get_updater().launch()

    @abstractmethod
    def _build(self) -> Element | list[Element]:
        pass

    def _center(self, element: Element) -> None:
        element.center_on(self.screen)
