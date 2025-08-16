import pygame
import pygame_gui
from typing import Optional
from dataclasses import dataclass

import constants
from constants import ButtonAction, StateTracker, ButtonSFX
import init
from sound_manager import ButtonSoundManager
from queries import SqliteQueries
from .threat_creation import ThreatCreationController
import elements.threats_elements as threat_element




@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image_file: str = ""


class ThreatStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.threat_variables()
    
    def threat_variables(self) -> None:
        self.threat_name_list = self.fetch_threat_names()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self.selected_threat = None
        self.threat_delete_confirm_window = False
    
    def threat_id_name_mapper(self) -> dict:
        threat_id_name_list = self.query.threat_id_name_query()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map

    def fetch_threat_names(self) -> list:
        threat_name_list = self.query.threat_list_query()
        return threat_name_list

    def fetch_threat_details(self) -> tuple:
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.threat_management_selection_query(selected_threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def delete_selected_threat(self) -> None:
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        self.cursor.execute('DELETE FROM tickets WHERE threat_id=?', [selected_threat_id])
        self.cursor.execute('DELETE FROM threats WHERE id=?', [selected_threat_id])
        self.connect.commit()
    

class ThreatUIManager():

    def __init__(self, pygame_manager, state_manager: ThreatStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.threat_list = self.state.threat_name_list
        self.build_ui(self.threat_list)

    def build_ui(self, threat_list):
        self.back_button = threat_element.back_button_func(self.manager)
        self.create_button = threat_element.create_button_func(self.manager)
        self.delete_button = threat_element.delete_button_func(self.manager)

        self.threat_database_image = threat_element.threat_database_image_func(self.manager, constants.THREAT_DATABASE_IMAGE_PATH)
        self.threat_entry_title_tbox = threat_element.threat_entry_slist_misc_func(self.manager)
        self.threat_entry_slist = threat_element.threat_entry_slist_func(self.manager, threat_list)

        self.threat_details_label, self.selected_threat_title_tbox, self.selected_threat_description_tbox, \
            self.selected_threat_indicators_tbox, self.selected_threat_countermeasures_tbox, \
                self.selected_threat_image_path_tbox = threat_element.threat_details_func(self.manager)
        
    def destroy_elements(self):
        self.back_button.kill()
        self.create_button.kill()
        self.delete_button.kill()

        self.threat_database_image.kill()
        self.threat_entry_title_tbox.kill()
        self.threat_entry_slist.kill()
        self.threat_details_label.kill()
        self.selected_threat_title_tbox.kill()
        self.selected_threat_description_tbox.kill()
        self.selected_threat_indicators_tbox.kill()
        self.selected_threat_countermeasures_tbox.kill()
        self.selected_threat_image_path_tbox.kill()
        
    def set_threat_details(self, threat: ThreatDetails) -> None:
        self.selected_threat_title_tbox.set_text(f"<b>{threat.name}</b>")
        self.selected_threat_description_tbox.set_text(f"DESCRIPTION:\n{threat.description}")
        self.selected_threat_indicators_tbox.set_text(f"INDICATORS:\n{threat.indicators}")
        self.selected_threat_countermeasures_tbox.set_text(f"COUNTERMEASURES:\n{threat.countermeasures}")
        self.selected_threat_image_path_tbox.set_text(f"{threat.image_file}")
        
    def display_confirm_window(self):
        self.state.threat_delete_confirm_window, self.threat_delete_confirm_yes_button, \
            self.threat_delete_confirm_no_button = threat_element.threat_delete_confirm_window_func(self.manager)
        
    def refresh_threat_list(self, updated_threat_list):
        self.threat_entry_slist.set_item_list(updated_threat_list)
        self.state.threat_id_name_map = self.state.threat_id_name_mapper()


class ThreatEventHandler():

    def __init__(self, pygame_manager, state_manager: ThreatStateManager, ui_manager: ThreatUIManager,
                 sound_manager: ButtonSoundManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager

    def handle_threat_selection(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.LIST_BUTTON)
        self._update_threat_textbox()
        
    def _update_threat_textbox(self) -> None:
        threat = self.state.fetch_threat_details()
        self.ui.set_threat_details(threat)

    def handle_button_pressed(self, event) -> Optional[ButtonAction]:
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if event.ui_element == self.ui.create_button:
            return ButtonAction.CREATE
        
        if event.ui_element == self.ui.delete_button and self.state.selected_threat is not None:
            return ButtonAction.DELETE

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.threat_delete_confirm_yes_button:
            return ButtonAction.CONFIRM_DELETE

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.threat_delete_confirm_no_button:
            return ButtonAction.CANCEL_DELETE


class ThreatManagementController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = init.PygameRenderer()
        #self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = ThreatStateManager(self.connect, self.cursor)
        self.ui = ThreatUIManager(self.manager, self.state)
        self.event_handler = ThreatEventHandler(self.manager, self.state, self.ui, self.button_sfx)

    def game_loop(self, events) -> None:
        for event in events:
            action = self._handle_events(event)

            if action == ButtonAction.EXIT:
                return StateTracker.MAIN_MENU
            if action == ButtonAction.CREATE:
                return StateTracker.THREAT_CREATION

    def _handle_events(self, event) -> bool:
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.threat_entry_slist:
            self.state.selected_threat = event.text
            self.event_handler.handle_threat_selection()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == ButtonAction.EXIT:
                return self._handle_exit_action()
            
            if button_event == ButtonAction.CREATE:
                return self._handle_create_action()
            
            button_action_map = {
                ButtonAction.DELETE: self._handle_delete_action,
                ButtonAction.CONFIRM_DELETE: self._handle_confirm_delete_action,
                ButtonAction.CANCEL_DELETE: self._handle_cancel_delete_action
            }

            button_action = button_action_map.get(button_event)
            if button_action:
                button_action()
            
        self.manager.process_events(event)
        return True
    
    def _handle_create_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.ui.destroy_elements()
        return ButtonAction.CREATE
        #threat_creation_page = ThreatCreationController(self.state.connect, self.state.cursor)
        #self.state.threat_name_list  = threat_creation_page.threat_creation_loop()
        #self.ui.refresh_threat_list(self.state.threat_name_list)

    def _handle_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.ui.display_confirm_window()

    def _handle_confirm_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.DELETE_BUTTON)
        self.state.threat_delete_confirm_window.kill()
        self.state.delete_selected_threat()
        self.state.threat_name_list = self.state.fetch_threat_names()
        self.ui.refresh_threat_list(self.state.threat_name_list)

    def _handle_cancel_delete_action(self) -> None: 
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.state.threat_delete_confirm_window.kill()

    def _handle_exit_action(self) -> False:
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.ui.destroy_elements()
        return ButtonAction.EXIT