import pygame as pg
import thorpy as tp
from src.home import Home

pg.init()
screen = pg.display.set_mode((800, 600))
screen.fill((255, 255, 255))
tp.init(screen, tp.theme_game1)

try:
    Home(screen)
finally:
    pg.quit()
