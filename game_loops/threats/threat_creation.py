import pygame
import pygame_gui
from dataclasses import dataclass

import init
import sound_manager
import constants
import elements.threats_elements as threat_element
from queries import SqliteQueries



@dataclass
class ThreatDetails:
    id: int = 0
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image_path: str = ""


class ThreatCreationStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.threat = ThreatDetails()
        self.threat_confirm_window = False

    def fetch_threat_names(self):
        threat_name_list = self.query.threat_list_query()
        return threat_name_list
    
    def _generate_new_threat_id(self):
        max_id = self.query.max_threat_id_query()
        threat_id = max_id + 1
        return threat_id
    
    def add_new_threat(self):
        self.threat.id = self._generate_new_threat_id()
        new_threat_entry = (self.threat.id,
                            self.threat.name,
                            self.threat.description,
                            self.threat.indicators,
                            self.threat.countermeasures,
                            self.threat.image_path)
        
        self.cursor.execute('INSERT INTO threats VALUES (?, ?, ?, ?, ?, ?)', new_threat_entry)
        self.connect.commit()


class ThreatCreationUIManager():

    def __init__(self, pygame_manager):
        self.manager = pygame_manager
        self.build_ui()

    def build_ui(self):
        self.threat_create_image = threat_element.add_threat_image_func(self.manager, constants.THREAT_CREATE_IMAGE_PATH)
        
        self.back_button = threat_element.back_button_func(self.manager)
        self.add_threat_button = threat_element.threat_entry_add_button_func(self.manager)

        self.threat_entry_name, self.threat_entry_description, self.threat_entry_indicators, \
            self.threat_entry_countermeasures, self.threat_entry_image_path = threat_element.threat_entry_func(self.manager)
        
    def refresh_creation_page(self):
        self.threat_entry_name.set_text("")
        self.threat_entry_description.set_text("")
        self.threat_entry_indicators.set_text("")
        self.threat_entry_countermeasures.set_text("")
        self.threat_entry_image_path.set_text("") 


class ThreatCreationEventHandler():

    def __init__(self, pygame_manager, state_manager: ThreatCreationStateManager, ui_manager: ThreatCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()

        if event.ui_element == self.ui.add_threat_button:
            self._handle_add_button()

        if self.state.threat_confirm_window and event.ui_element == self.threat_confirm_close_button:
            self.ui.refresh_creation_page()
            self.state.threat_confirm_window.kill()
            self.state.threat = ThreatDetails()

    def _handle_back_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    
    def _handle_add_button(self):
        self._get_new_threat_details()

        if not all([
            self.state.threat.name,
            self.state.threat.description,
            self.state.threat.indicators,
            self.state.threat.countermeasures,
            self.state.threat.image_path
        ]):
            return
        
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.add_new_threat()

        self.state.threat_confirm_window, self.threat_confirm_close_button = threat_element.threat_confirm_window_func(self.manager)
        self.state.threat_confirm_window.show()

    def _get_new_threat_details(self):
        self.state.threat.name = self.ui.threat_entry_name.get_text()
        self.state.threat.description = self.ui.threat_entry_description.get_text()
        self.state.threat.indicators = self.ui.threat_entry_indicators.get_text()
        self.state.threat.countermeasures = self.ui.threat_entry_countermeasures.get_text()
        self.state.threat.image_path = self.ui.threat_entry_image_path.get_text()


class ThreatCreationController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

        self.state = ThreatCreationStateManager(self.connect, self.cursor)
        self.ui = ThreatCreationUIManager(self.manager)
        self.event_handler = ThreatCreationEventHandler(self.manager, self.state, self.ui)

    def threat_creation_loop(self):
        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            events = pygame.event.get()
            for event in events:
                if not self._handle_events(event):
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)
        
        updated_threat_list = self.state.fetch_threat_names()
        return updated_threat_list

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_action = self.event_handler.handle_button_pressed(event)

            if button_action == constants.EXIT_ACTION:
                return False
            
        self.manager.process_events(event)
        return True