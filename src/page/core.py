import pygame as pg
import thorpy as tp
from thorpy.canonical import Element as TpElement
from abc import ABC, abstractmethod
from typing import *


class Page(ABC):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.screen_width = self.screen.get_width
        self.screen_height = self.screen.get_height
        self.screen.fill((250, 250, 250))

        es = self._build()
        if isinstance(es, TpElement):
            es.get_updater().launch()
        else:
            tp.Group(es, None, (0, 0), 0).get_updater().launch()

    @abstractmethod
    def _build(self) -> TpElement | list[TpElement]:
        pass
