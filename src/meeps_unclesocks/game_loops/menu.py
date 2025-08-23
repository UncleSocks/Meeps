import pygame
import pygame_gui

import elements.game_elements.menu_elements as me
from constants import StateTracker, ButtonAction, \
    ButtonSFX, ImagePaths
from managers.sound_manager import ButtonSoundManager




class MenuUIManager():

    def __init__(self, pygame_manager):
        self.manager = pygame_manager
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._menu_elements()

    def _draw_images(self):
        title_image = me.MenuImage(self.manager)
        title_image_load = pygame.image.load(ImagePaths.TITLE.value)
        title_image.INPUT = title_image_load
        self.title_image = title_image.draw_image()

    def _draw_buttons(self):
        self.shift_button = me.ShiftButton(self.manager).draw_button()
        self.ticket_button = me.TicketButton(self.manager).draw_button()
        self.account_button = me.AccountButton(self.manager).draw_button()
        self.threat_button = me.ThreatButton(self.manager).draw_button()
        self.logoff_button = me.LogOffButton(self.manager).draw_button()

    def _menu_elements(self):
        self.title_slogan = me.TitleSloganLabel(self.manager).draw_label()
        self.version = me.VersionLabel(self.manager).draw_label()
        self.github = me.GitHubLabel(self.manager).draw_label()

    def destroy_elements(self):
        self.shift_button.kill()
        self.ticket_button.kill()
        self.account_button.kill()
        self.threat_button.kill()
        self.logoff_button.kill()

        self.title_image.kill()
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
        if event.ui_element == self.ui.shift_button:
            return ButtonAction.SHIFT
        
        if event.ui_element == self.ui.ticket_button:
            return ButtonAction.TICKET

        if event.ui_element == self.ui.account_button:
            return ButtonAction.ACCOUNT
        
        if event.ui_element == self.ui.threat_button:
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
        self.manager.clear_and_reset()
        action = button_event
        return action