import sqlite3
import pygame
import pygame_gui

import config
from colors import color



def pygame_init():

    pygame.init()
    pygame.display.set_caption(config.WINDOW_CAPTION)

    window_icon_load = pygame.image.load(config.WINDOW_ICON_PATH)
    pygame.display.set_icon(window_icon_load)

    window_surface = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    background = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    background.fill(pygame.Color(color('black')))

    return window_surface, clock, background


def pygame_gui_init():

    manager = pygame_gui.UIManager((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), config.THEME_PATH)
    return manager


def database_init(database):

    connect = sqlite3.connect(database, timeout=10)
    cursor = connect.cursor()

    return connect, cursor


class PygameRenderer:

    def __init__(self):

        pygame.init()
        self.window_surface, self.background = self.window_init()

        self.manager = pygame_gui.UIManager((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), config.THEME_PATH)
        self.clock = pygame.time.Clock()
        
    
    def window_init(self):

        pygame.display.set_caption(config.WINDOW_CAPTION)

        window_icon_load = pygame.image.load(config.WINDOW_ICON_PATH)
        pygame.display.set_icon(window_icon_load)

        window_surface = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

        background = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        background.fill(pygame.Color(color('black')))

        return window_surface, background

    
    def ui_renderer(self, manager, time_delta):

        manager.update(time_delta)
        self.window_surface.blit(self.background, (0,0))
        manager.draw_ui(self.window_surface)
        pygame.display.update()
    