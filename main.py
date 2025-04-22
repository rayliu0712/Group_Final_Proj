import pygame as pg
import thorpy as tp
from src.page.home import Home

pg.init()
screen = pg.display.set_mode((800, 600))
tp.set_default_font('consolas', 24)
tp.init(screen, tp.theme_game1)
tp.call_before_gui(lambda: screen.fill((250, 250, 250)))

Home(screen)
tp.exit_app()
