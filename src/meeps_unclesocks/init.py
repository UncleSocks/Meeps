import sqlite3
import pygame
import pygame_gui

from constants import WindowConfig




def database_init(database):
    connect = sqlite3.connect(database, timeout=10)
    cursor = connect.cursor()
    return connect, cursor


class PygameRenderer:

    def __init__(self):
        pygame.init()
        self.window_surface, self.background = self.window_init()
        self.manager = pygame_gui.UIManager(
            (WindowConfig.WIDTH.value, WindowConfig.HEIGHT.value),
            WindowConfig.THEME.value
        )
        self.clock = pygame.time.Clock()
        
    def window_init(self):
        pygame.display.set_caption(WindowConfig.CAPTION.value)
        window_icon_load = pygame.image.load(WindowConfig.ICON.value)
        pygame.display.set_icon(window_icon_load)

        window_surface = pygame.display.set_mode((WindowConfig.WIDTH.value, WindowConfig.HEIGHT.value))
        background = pygame.Surface((WindowConfig.WIDTH.value, WindowConfig.HEIGHT.value))
        background.fill(pygame.Color(WindowConfig.BACKGROUND.value))
        return window_surface, background

    def ui_renderer(self, time_delta):
        self.manager.update(time_delta)
        self.window_surface.blit(self.background, (0,0))
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()
    