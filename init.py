import sqlite3
import pygame
import pygame_gui

import constants




def database_init(database):

    connect = sqlite3.connect(database, timeout=10)
    cursor = connect.cursor()

    return connect, cursor



class PygameRenderer:

    def __init__(self):

        pygame.init()
        self.window_surface, self.background = self.window_init()

        self.manager = pygame_gui.UIManager((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT), constants.THEME_PATH)
        self.clock = pygame.time.Clock()
        
    
    def window_init(self):

        pygame.display.set_caption(constants.WINDOW_CAPTION)

        window_icon_load = pygame.image.load(constants.WINDOW_ICON_PATH)
        pygame.display.set_icon(window_icon_load)

        window_surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

        background = pygame.Surface((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        background.fill(pygame.Color(constants.BACKGROUND_COLOR_RGB))

        return window_surface, background

    
    def ui_renderer(self, time_delta):

        self.manager.update(time_delta)
        self.window_surface.blit(self.background, (0,0))
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()
    