import pygame
import pygame_gui
from dataclasses import dataclass

import constants
import init
import sound_manager
from queries import SqliteQueries
from .threat_creation import ThreatCreationController
import elements.threats_elements as threat_element




@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image_path: str = ""


class ThreatStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.threat_variables()
    
    def threat_variables(self):
        self.threat_name_list = self.fetch_threat_names()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self.selected_threat = None
        self.threat_delete_confirm_window = False
    
    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.threat_id_name_query()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map

    def fetch_threat_names(self):
        threat_name_list = self.query.threat_list_query()
        return threat_name_list

    def fetch_threat_details(self):
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.threat_management_selection_query(selected_threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def delete_selected_threat(self):
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        self.cursor.execute('DELETE FROM tickets WHERE threat_id=?', [selected_threat_id])
        self.cursor.execute('DELETE FROM threats WHERE id=?', [selected_threat_id])
        self.connect.commit()
        return
    

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
        
    def display_confirm_window(self):
        self.state.threat_delete_confirm_window, self.threat_delete_confirm_yes_button, \
            self.threat_delete_confirm_no_button = threat_element.threat_delete_confirm_window_func(self.manager)
        
    def refresh_threat_list(self, updated_threat_list):
        self.threat_entry_slist.set_item_list(updated_threat_list)


class ThreatEventHandler():

    def __init__(self, pygame_manager, state_manager: ThreatStateManager, ui_manager: ThreatUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_threat_selection(self, selected_threat):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        self.state.selected_threat = selected_threat
        self._update_threat_textbox()
        
    def _update_threat_textbox(self):
        threat = self.state.fetch_threat_details()

        self.ui.selected_threat_title_tbox.set_text(f"<b>{threat.name}</b>")
        self.ui.selected_threat_description_tbox.set_text(f"DESCRIPTION:\n{threat.description}")
        self.ui.selected_threat_indicators_tbox.set_text(f"INDICATORS:\n{threat.indicators}")
        self.ui.selected_threat_countermeasures_tbox.set_text(f"COUNTERMEASURES:\n{threat.countermeasures}")
        self.ui.selected_threat_image_path_tbox.set_text(f"{threat.image_path}")

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()
        
        if event.ui_element == self.ui.create_button:
            self._handle_create_button()

        if event.ui_element == self.ui.delete_button and self.state.selected_threat is not None:
            self._handle_delete_button()

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.threat_delete_confirm_yes_button:
            self._handle_confirm_yes_button()

        if self.state.threat_delete_confirm_window and event.ui_element == self.ui.threat_delete_confirm_no_button:
            self._handle_confirm_no_window()

        
    def _handle_back_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    
    def _handle_create_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.threat_name_list = ThreatCreationController(self.state.connect, self.state.cursor).threat_creation_loop()
        self.ui.refresh_threat_list(self.state.threat_name_list)
        self.state.threat_id_name_map = self.state.threat_id_name_mapper()

    def _handle_delete_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.ui.display_confirm_window()

    def _handle_confirm_yes_button(self):
        self.button_sfx.play_sfx(constants.DELETE_BUTTON_SFX)
        self.state.delete_selected_threat()
        self.state.threat_name_list = self.state.fetch_threat_names()
        self.ui.refresh_threat_list(self.state.threat_name_list)
        self.state.threat_id_name_map = self.state.threat_id_name_mapper()

        self.state.threat_delete_confirm_window.kill()

    def _handle_confirm_no_window(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.state.threat_delete_confirm_window.kill()


class ThreatManagementController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

        self.state = ThreatStateManager(self.connect, self.cursor)
        self.ui = ThreatUIManager(self.manager, self.state)
        self.event_handler = ThreatEventHandler(self.manager, self.state, self.ui)

    def threat_management_loop(self):
        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()

            for event in events:
                if not self._handle_events(event):
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)
                
    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.threat_entry_slist:
            selected_threat = event.text
            self.event_handler.handle_threat_selection(selected_threat)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_action = self.event_handler.handle_button_pressed(event)

            if button_action == 'exit':
                return False
            
        self.manager.process_events(event)
        return True