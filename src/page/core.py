# EXPERIMENTAL

import pygame as pg
import thorpy as tp
from thorpy.canonical import Element as TpElement
from abc import ABC, abstractmethod
from typing import *


class Page(ABC):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.screen.fill((250, 250, 250))
        elements = self._build()
        assert isinstance(elements, list) and all(isinstance(item, TpElement)
                                                  for item in elements), 'method _build() should return list[TpElement]'

        tp.Group(elements, mode=None).get_updater().launch()

    @abstractmethod
    def _build(self) -> list[TpElement]:
        pass
