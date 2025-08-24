import os
from typing import Optional
from dataclasses import dataclass

import pygame
import pygame_gui

import elements.game_elements.threat_elements.threat_management_elements as tme
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, AssetBasePath, ImagePaths, ButtonSFX
from init import PygameRenderer
from managers.sound_manager import ButtonSoundManager
from managers.db_manager import DatabaseQueries, DatabaseModification




@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image_filename: str = ""


class ThreatStateManager:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = DatabaseQueries(self.cursor)
        self.modify = DatabaseModification(self.cursor, self.connect)
        self.threat_variables()
    
    def threat_variables(self) -> None:
        self.threat_name_list = self.fetch_threat_names()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self.selected_threat = None
        self.threat_delete_confirm_window = False
    
    def threat_id_name_mapper(self) -> dict:
        threat_id_name_list = self.query.fetch_threat_names_ids()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map

    def fetch_threat_names(self) -> list:
        threat_name_list = self.query.fetch_threat_names()
        return threat_name_list

    def fetch_threat_details(self) -> ThreatDetails:
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.fetch_threat_details(selected_threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def delete_selected_threat(self, threat_image_filename) -> None:
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        self.modify.delete_entry(table='tickets', key='threat_id', param=[selected_threat_id])
        self.modify.delete_entry(table='threats', key='id', param=[selected_threat_id])
        self._delete_threat_image(threat_image_filename)

    def _delete_threat_image(self, threat_image_filename):
        threat_image_path = "".join([AssetBasePath.THREAT_ASSETS.value, threat_image_filename])
        if os.path.exists(threat_image_path):
            os.remove(threat_image_path)
    

class ThreatUIManager:

    def __init__(self, pygame_manager, state_manager: ThreatStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_threat_elements()
        
    def _draw_images(self):
        threat_manager_image = tme.TitleImage(self.manager)
        threat_manager_image_load = pygame.image.load(ImagePaths.THREAT_MANAGEMENT.path)
        threat_manager_image.INPUT = threat_manager_image_load
        self.threat_manager_image = threat_manager_image.draw_image()
        
    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.create_button = se.CreateButton(self.manager).draw_button()
        self.delete_button = se.DeleteButton(self.manager).draw_button()

    def _draw_threat_elements(self):
        self.threat_selection_list_title = tme.ThreatListTitle(self.manager).draw_textbox()
        
        threat_selection_list = tme.ThreatList(self.manager)
        threat_selection_list.INPUT = self.state.threat_name_list
        self.threat_selection_list = threat_selection_list.draw_selectionlist()

        self.threat_details_label = tme.ThreatDetailLabel(self.manager).draw_label()
        self.threat_title = tme.ThreatTitle(self.manager).draw_textbox()
        self.threat_description = tme.ThreatDescription(self.manager).draw_textbox()
        self.threat_indicators = tme.ThreatIndicators(self.manager).draw_textbox()
        self.threat_countermeasures = tme.ThreatCountermeasures(self.manager).draw_textbox()
        self.threat_image_filename = tme.ThreatImageFileName(self.manager).draw_textbox()
        
    def set_threat_details(self, threat: ThreatDetails) -> None:
        self.threat_title.set_text(f"<b>{threat.name}</b>")
        self.threat_description.set_text(f"DESCRIPTION:\n{threat.description}")
        self.threat_indicators.set_text(f"INDICATORS:\n{threat.indicators}")
        self.threat_countermeasures.set_text(f"COUNTERMEASURES:\n{threat.countermeasures}")
        self.threat_image_filename.set_text(f"{threat.image_filename}")
        
    def display_confirm_window(self):
        self.state.threat_delete_confirm_window = tme.DeleteConfirmWindow(self.manager).draw_window()

        confirm_delete_label = tme.DeleteConfirmLabel(self.manager)
        confirm_delete_label.CONTAINER = self.state.threat_delete_confirm_window
        self.confirm_delete_label = confirm_delete_label.draw_label()

        confirm_delete_warning_label = tme.DeleteConfirmWarningLabel(self.manager)
        confirm_delete_warning_label.CONTAINER = self.state.threat_delete_confirm_window
        self.confirm_delete_warning_label = confirm_delete_warning_label.draw_label()
        
        confirm_delete_yes_button = se.DeleteYesButton(self.manager)
        confirm_delete_yes_button.CONTAINER = self.state.threat_delete_confirm_window
        self.confirm_yes_button = confirm_delete_yes_button.draw_button()

        confirm_delete_no_button = se.DeleteNoButton(self.manager)
        confirm_delete_no_button.CONTAINER = self.state.threat_delete_confirm_window
        self.confirm_delete_no_button = confirm_delete_no_button.draw_button()
        
    def refresh_threat_list(self, updated_threat_list):
        self.threat_selection_list.set_item_list(updated_threat_list)
        self.state.threat_id_name_map = self.state.threat_id_name_mapper()


class ThreatEventHandler:

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
        self.threat = self.state.fetch_threat_details()
        self.ui.set_threat_details(self.threat)

    def handle_button_pressed(self, event) -> Optional[ButtonAction]:
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if event.ui_element == self.ui.create_button:
            return ButtonAction.CREATE
        
        if event.ui_element == self.ui.delete_button and self.state.selected_threat is not None:
            return ButtonAction.DELETE

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.confirm_yes_button:
            return ButtonAction.CONFIRM_DELETE

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.confirm_delete_no_button:
            return ButtonAction.CANCEL_DELETE


class ThreatManagementController:

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
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
            and event.ui_element == self.ui.threat_selection_list:
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
        self.manager.clear_and_reset()
        return ButtonAction.CREATE

    def _handle_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.ui.display_confirm_window()

    def _handle_confirm_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.DELETE_BUTTON)
        self.state.threat_delete_confirm_window.kill()
        self.state.delete_selected_threat(self.event_handler.threat.image_filename)
        self.state.threat_name_list = self.state.fetch_threat_names()
        self.ui.refresh_threat_list(self.state.threat_name_list)

    def _handle_cancel_delete_action(self) -> None: 
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.state.threat_delete_confirm_window.kill()

    def _handle_exit_action(self) -> False:
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT