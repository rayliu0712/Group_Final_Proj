import pygame
import thorpy
from src.ui.home import Home

pygame.init()
screen = pygame.display.set_mode((800, 600))
thorpy.set_default_font('consolas', 24)
thorpy.init(screen, thorpy.theme_game1)

Home()()
thorpy.exit_app()
