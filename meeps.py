import pygame
import pygame_gui

import init
import sound_manager
import constants
import elements.main_menu as main_menu_element
from game_loops.shift import shift_introduction
from game_loops.tickets.ticket_management import TicketManagementController
from game_loops.accounts.account_management import AccountManagementController
from game_loops.threats.threat_management import ThreatManagementController



class MainMenuUIManager():

    def __init__(self, pygame_manager):
        self.manager = pygame_manager
        self.build_ui()

    def build_ui(self):
        self.start_button = main_menu_element.start_button_func(self.manager)
        self.ticket_management_button = main_menu_element.ticket_management_button_func(self.manager)
        self.account_management_button = main_menu_element.accounts_management_button_func(self.manager)
        self.threat_management_button = main_menu_element.threat_entries_button_func(self.manager)
        self.logoff_button = main_menu_element.quit_button_func(self.manager)

        main_menu_element.main_title_image_func(self.manager, constants.TITLE_IMAGE_PATH)
        main_menu_element.main_title_slogan_label_func(self.manager)
        main_menu_element.version_label_func(self.manager, constants.CURRENT_VERSION)
        main_menu_element.github_label_func(self.manager)


class MainMenuEventHandler():

    def __init__(self, connect, cursor, pygame_manager, ui_manager: MainMenuUIManager):
        self.manager = pygame_manager
        self.connect = connect
        self.cursor = cursor
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_button_pressed(self, event):
        self._handle_menu_button(event)

        if event.ui_element == self.ui.logoff_button:
            return self._handle_logoff_button()
        
    def _handle_menu_button(self, event):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)

        main_menu_button_action_map = {
            self.ui.start_button: lambda: shift_introduction(self.connect, self.cursor),
            self.ui.ticket_management_button: lambda: TicketManagementController(self.connect, self.cursor).ticket_management_loop(),
            self.ui.account_management_button: lambda: AccountManagementController(self.connect, self.cursor).account_management_loop(),
            self.ui.threat_management_button: lambda: ThreatManagementController(self.connect, self.cursor).threat_management_loop(),
        }

        button_action_trigger = main_menu_button_action_map.get(event.ui_element)
        
        if not button_action_trigger:
            return
        
        button_action_trigger()

    def _handle_logoff_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    

class MainMenuController():

    def __init__(self):
        self.connect, self.cursor = init.database_init(constants.DATABASE_FILE)
        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager

        self.ui = MainMenuUIManager(self.manager)
        self.event_handler = MainMenuEventHandler(self.connect, self.cursor, self.manager, self.ui)

    def main_menu_loop(self):
        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()

            for event in events:
                if not self._handle_events(event):
                    running = False
            
            self.pygame_renderer.ui_renderer(time_delta)
        self._shutdown()

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_action = self.event_handler.handle_button_pressed(event)

            if button_action == constants.EXIT_ACTION:
                return False
            
        self.manager.process_events(event)
        return True
    
    def _shutdown(self):
        self.connect.close()
        pygame.quit()


if __name__ == "__main__":
    main_menu = MainMenuController()
    main_menu.main_menu_loop()