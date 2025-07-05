import pygame
import pygame_gui

import init
import elements.main_menu as main_menu_element
from game_loops.shift import shift_introduction
from game_loops.tickets import ticket_management
from game_loops.accounts import accounts_management
from game_loops.threats import threat_database_management



class MainMenu:

    def __init__ (self):

        #Initializes SQLite database connection and cursor.
        self.database = 'data.db'
        self.connect, self.cursor = init.database_init(self.database)

        #Initializes PyGame and window(s). 
        self.window_surface, self.clock, self.background = init.pygame_init()
        self.manager = init.pygame_gui_init()

        #Displays main menu buttons.
        self.start_button = main_menu_element.start_button_func(self.manager)
        self.ticket_management_button = main_menu_element.ticket_management_button_func(self.manager)
        self.account_management_button = main_menu_element.accounts_management_button_func(self.manager)
        self.threat_entries_button = main_menu_element.threat_entries_button_func(self.manager)
        self.quit_button = main_menu_element.quit_button_func(self.manager)

        #Initializes and displays miscellaneous assets.
        self.title_image_path = 'assets/images/general/title.png'
        main_menu_element.main_title_image_func(self.manager, self.title_image_path)
        main_menu_element.main_title_slogan_label_func(self.manager)

        self.current_version = "v2025.0.1 BETA"
        main_menu_element.version_label_func(self.manager, self.current_version)
        main_menu_element.github_label_func(self.manager)

        
        #Initializes and loads main menu music.
        self.menu_button_music_path = 'assets/sounds/menu_button.mp3'
        pygame.mixer.music.load(self.menu_button_music_path)
        self.menu_button_music_channel = pygame.mixer.Channel(0)


    def main_menu_loop (self):

        running = True
        while running:

            time_delta = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.menu_button_music_channel.play(pygame.mixer.Sound(self.menu_button_music_path))

                    if event.ui_element == self.start_button:
                        shift_introduction(self.connect, self.cursor)

                    elif event.ui_element == self.ticket_management_button:
                        ticket_management(self.connect, self.cursor)

                    elif event.ui_element == self.account_management_button:
                        accounts_management(self.connect, self.cursor)

                    elif event.ui_element == self.threat_entries_button:
                        threat_database_management(self.connect, self.cursor)

                    elif event.ui_element == self.quit_button:
                        running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0,0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()

        self.connect.close()
        pygame.quit()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.main_menu_loop()