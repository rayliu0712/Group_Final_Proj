import pygame as pg
import thorpy as tp
from src.ui.home import Home

pg.init()
screen = pg.display.set_mode((800, 600))
tp.set_default_font('consolas', 24)
tp.init(screen, tp.theme_game1)

home = Home()
home()
tp.exit_app()
