import pygame
import pygame_gui

import init
from init import PygameRenderer
import sound_manager
import constants
from constants import StateTracker
import elements.main_menu as main_menu_element
#from game_loops.shift import shift_introduction
from game_loops.shift_s.shift import ShiftController
from game_loops.tickets.ticket_management import TicketManagementController, TicketCreationController
from game_loops.accounts.account_management import AccountManagementController, AccountCreationController
from game_loops.threats.threat_management import ThreatManagementController, ThreatCreationController



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

        self.main_title_image = main_menu_element.main_title_image_func(self.manager, constants.TITLE_IMAGE_PATH)
        self.title_slogan = main_menu_element.main_title_slogan_label_func(self.manager)
        self.version = main_menu_element.version_label_func(self.manager, constants.CURRENT_VERSION)
        self.github = main_menu_element.github_label_func(self.manager)

    def destroy_elements(self):
        self.start_button.kill()
        self.ticket_management_button.kill()
        self.account_management_button.kill()
        self.threat_management_button.kill()
        self.logoff_button.kill()

        self.main_title_image.kill()
        self.title_slogan.kill()
        self.version.kill()
        self.github.kill()


class MainMenuEventHandler():

    def __init__(self, connect, cursor, pygame_manager, ui_manager: MainMenuUIManager):
        self.manager = pygame_manager
        self.connect = connect
        self.cursor = cursor
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.start_button:
            return StateTracker.SHIFT
        
        if event.ui_element == self.ui.ticket_management_button:
            return StateTracker.TICKET_MANAGEMENT

        if event.ui_element == self.ui.account_management_button:
            return StateTracker.ACCOUNT_MANAGEMENT
        
        if event.ui_element == self.ui.threat_management_button:
            return StateTracker.THREAT_MANAGEMENT

        if event.ui_element == self.ui.logoff_button:
            return StateTracker.EXIT

    def _handle_logoff_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    

class MainMenuController():

    def __init__(self, connect, cursor, manager):
        #self.connect, self.cursor = init.database_init(constants.DATABASE_FILE)
        #self.pygame_renderer = init.PygameRenderer()
        #self.manager = self.pygame_renderer.manager
        self.connect = connect
        self.cursor = cursor
        self.manager = manager
        self.button_sfx = sound_manager.ButtonSoundManager()

        self.ui = MainMenuUIManager(self.manager)
        self.event_handler = MainMenuEventHandler(self.connect, self.cursor, self.manager, self.ui)

    def game_loop(self, events):
        for event in events:
            action = self._handle_events(event)
            if action == StateTracker.ACCOUNT_MANAGEMENT:
                return StateTracker.ACCOUNT_MANAGEMENT
            if action == StateTracker.SHIFT:
                return StateTracker.SHIFT
            if action == StateTracker.TICKET_MANAGEMENT:
                return StateTracker.TICKET_MANAGEMENT
            if action == StateTracker.THREAT_MANAGEMENT:
                return StateTracker.THREAT_MANAGEMENT
                
        
    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == StateTracker.SHIFT:
                self.ui.destroy_elements()
                return self._handle_shift_action()
            
            if button_event == StateTracker.THREAT_MANAGEMENT:
                self.ui.destroy_elements()
                return self._handle_threat_management_action()
            
            if button_event == StateTracker.TICKET_MANAGEMENT:
                self.ui.destroy_elements()
                return self._handle_ticket_managemnt_action()
    
            if button_event == StateTracker.ACCOUNT_MANAGEMENT:
                self.ui.destroy_elements()
                return self._handle_account_management_action()
            
            if button_event == StateTracker.EXIT:
                return StateTracker.EXIT
            
        self.manager.process_events(event)
        return True
    
    def _handle_shift_action(self):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        return StateTracker.SHIFT
    
    def _handle_ticket_managemnt_action(self):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        return StateTracker.TICKET_MANAGEMENT
    
    def _handle_account_management_action(self):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        return StateTracker.ACCOUNT_MANAGEMENT
    
    def _handle_threat_management_action(self):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        return StateTracker.THREAT_MANAGEMENT
    
    def _shutdown(self):
        self.connect.close()
        pygame.quit()


if __name__ == "__main__":
    connect, cursor = init.database_init(constants.DATABASE_FILE)
    pygame_renderer = init.PygameRenderer()
    manager = pygame_renderer.manager

    running = True
    current_state = MainMenuController(connect, cursor, manager)
    while running:
        time_delta = pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
        events = pygame.event.get()

        state = current_state.game_loop(events)
        print(state)

        if state == StateTracker.MAIN_MENU:
            current_state = MainMenuController(connect, cursor, manager)

        if state == StateTracker.SHIFT:
            current_state = ShiftController(connect, cursor, manager)

        if state == StateTracker.TICKET_MANAGEMENT:
            current_state = TicketManagementController(connect, cursor, manager)

        if state == StateTracker.TICKET_CREATION:
            current_state = TicketCreationController(connect, cursor, manager)

        if state == StateTracker.ACCOUNT_MANAGEMENT:
            current_state = AccountManagementController(connect, cursor, manager)

        if state == StateTracker.ACCOUNT_CREATION:
            current_state = AccountCreationController(connect, cursor, manager)

        if state == StateTracker.THREAT_MANAGEMENT:
            current_state = ThreatManagementController(connect, cursor, manager)

        if state == StateTracker.THREAT_CREATION:
            current_state = ThreatCreationController(connect, cursor, manager)

        if state == StateTracker.EXIT:
            connect.close()
            pygame.quit()
            

        pygame_renderer.ui_renderer(time_delta)


    #main_menu = MainMenuController()
    #main_menu.main_menu_loop()