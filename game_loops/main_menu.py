import pygame
import pygame_gui

import elements.main_menu as main_menu_element
from constants import Settings, StateTracker, ButtonAction, \
    ButtonSFX, ImagePaths
from sound_manager import ButtonSoundManager




class MenuUIManager():

    def __init__(self, pygame_manager):
        self.manager = pygame_manager
        self.build_ui()

    def build_ui(self):
        self.start_button = main_menu_element.start_button_func(self.manager)
        self.ticket_management_button = main_menu_element.ticket_management_button_func(self.manager)
        self.account_management_button = main_menu_element.accounts_management_button_func(self.manager)
        self.threat_management_button = main_menu_element.threat_entries_button_func(self.manager)
        self.logoff_button = main_menu_element.quit_button_func(self.manager)

        self.main_title_image = main_menu_element.main_title_image_func(self.manager, ImagePaths.TITLE.value)
        self.title_slogan = main_menu_element.main_title_slogan_label_func(self.manager)
        self.version = main_menu_element.version_label_func(self.manager, Settings.VERSION.value)
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


class MenuEventHandler():

    def __init__(self, connect, cursor, pygame_manager, ui_manager: MenuUIManager):
        self.manager = pygame_manager
        self.connect = connect
        self.cursor = cursor
        self.ui = ui_manager
        self.button_sfx = ButtonSoundManager()

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.start_button:
            return ButtonAction.SHIFT
        
        if event.ui_element == self.ui.ticket_management_button:
            return ButtonAction.TICKET

        if event.ui_element == self.ui.account_management_button:
            return ButtonAction.ACCOUNT
        
        if event.ui_element == self.ui.threat_management_button:
            return ButtonAction.THREAT

        if event.ui_element == self.ui.logoff_button:
            return ButtonAction.EXIT

    

class MenuController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager
        self.button_sfx = ButtonSoundManager()

        self.ui = MenuUIManager(self.manager)
        self.event_handler = MenuEventHandler(self.connect, self.cursor, self.manager, self.ui)

    def game_loop(self, events):
        for event in events:
            action = self._handle_events(event)

            if action == ButtonAction.SHIFT:
                return StateTracker.SHIFT
            if action == ButtonAction.TICKET:
                return StateTracker.TICKET_MANAGEMENT
            if action == ButtonAction.ACCOUNT:
                return StateTracker.ACCOUNT_MANAGEMENT
            if action == ButtonAction.THREAT:
                return StateTracker.THREAT_MANAGEMENT
            if action == ButtonAction.EXIT:
                return StateTracker.EXIT
        
    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event:
                return self._handle_button_action(button_event)
            
        self.manager.process_events(event)
        return None
    
    def _handle_button_action(self, button_event):
        self.button_sfx.play_sfx(ButtonSFX.MENU_BUTTON)
        self.ui.destroy_elements()
        action = button_event
        return action