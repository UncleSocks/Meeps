import pygame
import pygame_gui

import init
import sound_manager
import constants
import elements.main_menu as main_menu_element
from game_loops.shift import shift_introduction
from game_loops.tickets import TicketManagement
from game_loops.accounts.account_management import AccountManagementController
from game_loops.threats.threat_management import ThreatManagementController



    
class MainMenu:

    def __init__(self):

        self._init_database()
        self._init_pygame()
        self._init_ui_elements()
        self._init_misc_assets()
        self._init_music()
    
    def _init_database(self):

        self.connect, self.cursor = init.database_init(constants.DATABASE_FILE)

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager

    def _init_ui_elements(self):

        self.start_button = main_menu_element.start_button_func(self.manager)
        self.ticket_management_button = main_menu_element.ticket_management_button_func(self.manager)
        self.account_management_button = main_menu_element.accounts_management_button_func(self.manager)
        self.threat_management_button = main_menu_element.threat_entries_button_func(self.manager)
        self.quit_button = main_menu_element.quit_button_func(self.manager)

    def _init_misc_assets(self):

        main_menu_element.main_title_image_func(self.manager, constants.TITLE_IMAGE_PATH)
        main_menu_element.main_title_slogan_label_func(self.manager)

        main_menu_element.version_label_func(self.manager, constants.CURRENT_VERSION)
        main_menu_element.github_label_func(self.manager)

    def _init_music(self):

        self.button_sound_manager = sound_manager.ButtonSoundManager()


    def main_menu_loop(self) -> None:

        self.running = True
        while self.running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(time_delta)


    def _handle_events(self, events):
            
            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self._handle_button_pressed(event)

                self.manager.process_events(event)

                    
    def _handle_button_pressed(self, event):

        self.button_sound_manager.play_sfx('menu_button')

        menu_button_action_map = {

            self.start_button: lambda: shift_introduction(self.connect, self.cursor),
            self.ticket_management_button: lambda: TicketManagement(self.connect, self.cursor).ticket_management_loop(),
            self.account_management_button: lambda: AccountManagementController(self.connect, self.cursor).account_management_loop(),
            self.threat_management_button: lambda: ThreatManagementController(self.connect, self.cursor).threat_management_loop(),
            self.quit_button: lambda: self._quit()

        }

        button_action_trigger = menu_button_action_map.get(event.ui_element)
        if button_action_trigger:
            button_action_trigger()


    def _quit(self):

        self.running = False
        self.connect.close()
        pygame.quit()


if __name__ == "__main__":

    main_menu = MainMenu()
    main_menu.main_menu_loop()