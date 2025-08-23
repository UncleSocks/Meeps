import pygame
import pygame_gui
from dataclasses import dataclass, astuple

import elements.game_elements.threat_elements.threat_creation_elements as tce
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, \
    ImagePaths, ButtonSFX 
from init import PygameRenderer
from managers.sound_manager import ButtonSoundManager
from managers.db_manager import DatabaseQueries




@dataclass
class ThreatDetails:
    id: int = 0
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image_path: str = ""


class ThreatCreationStateManager:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = DatabaseQueries(self.cursor)
        self.threat = ThreatDetails()
        self.threat_confirm_window = False

    def fetch_threat_names(self):
        threat_name_list = self.query.fetch_threat_names()
        return threat_name_list
    
    def _generate_new_threat_id(self):
        max_id = self.query.fetch_max_id(table='threats')
        print(max_id)
        threat_id = max_id + 1
        return threat_id
    
    def add_new_threat(self):
        self.threat.id = self._generate_new_threat_id()
        new_threat_entry = astuple(self.threat)
        
        self.cursor.execute('INSERT INTO threats VALUES (?, ?, ?, ?, ?, ?)', new_threat_entry)
        self.connect.commit()


class ThreatCreationUIManager:

    def __init__(self, pygame_manager, state_manager: ThreatCreationStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_threat_creation_elements()
        
    def _draw_images(self):
        add_threat_image = tce.NewThreatImage(self.manager)
        add_threat_image_load = pygame.image.load(ImagePaths.THREAT_CREATION.value)
        add_threat_image.INPUT = add_threat_image_load
        self.add_threat_image = add_threat_image.draw_image()
        
    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.add_threat_button = tce.AddThreatButton(self.manager).draw_button()

    def _draw_threat_creation_elements(self):
        self.new_threat_name = tce.NewThreatName(self.manager).draw_textentrybox()
        self.new_threat_description = tce.NewThreatDescription(self.manager).draw_textentrybox()
        self.new_threat_indicators = tce.NewThreatIndicators(self.manager).draw_textentrybox()
        self.new_threat_countermeasures = tce.NewThreatCountermeasures(self.manager).draw_textentrybox()
        self.new_threat_image_filename = tce.NewThreatImageFileName(self.manager).draw_textentrybox()
        self._unfocus_text_entry_box_elements()

    def text_entry_box_elements(self):
        return [
            self.new_threat_name,
            self.new_threat_description,
            self.new_threat_indicators,
            self.new_threat_countermeasures,
            self.new_threat_image_filename
        ]

    def capture_new_threat_details(self):
        self.state.threat.name = self.new_threat_name.get_text()
        self.state.threat.description = self.new_threat_description.get_text()
        self.state.threat.indicators = self.new_threat_indicators.get_text()
        self.state.threat.countermeasures = self.new_threat_countermeasures.get_text()
        self.state.threat.image_path = self.new_threat_image_filename.get_text()

    def display_confirm_window(self):
        self.state.threat_confirm_window = tce.ConfirmWindow(self.manager).draw_window()

        confirm_label = tce.ConfirmLabel(self.manager)
        confirm_label.CONTAINER = self.state.threat_confirm_window
        self.confirm_label = confirm_label.draw_label()

        confirm_button = se.ConfirmButton(self.manager)
        confirm_button.CONTAINER = self.state.threat_confirm_window
        self.confirm_button = confirm_button.draw_button()
    
    def refresh_creation_page(self):
        for element in self.text_entry_box_elements():
            element.set_text("")
            element.unfocus()

    def _unfocus_text_entry_box_elements(self):
        for element in self.text_entry_box_elements():
            element.unfocus()


class ThreatCreationEventHandler:

    def __init__(self, pygame_manager, state_manager: ThreatCreationStateManager, ui_manager: ThreatCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT

        if event.ui_element == self.ui.add_threat_button:
            return ButtonAction.CREATE

        if self.state.threat_confirm_window \
            and event.ui_element == self.ui.confirm_button:
            return ButtonAction.CONFIRM_CREATE


class ThreatCreationController:

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
        self.window_surface = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = ThreatCreationStateManager(self.connect, self.cursor)
        self.ui = ThreatCreationUIManager(self.manager, self.state)
        self.event_handler = ThreatCreationEventHandler(self.manager, self.state, self.ui)

    def game_loop(self, events):
        for event in events:
            action = self._handle_events(event)
            if action == ButtonAction.EXIT:
                return StateTracker.THREAT_MANAGEMENT

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == ButtonAction.EXIT:
                return self._handle_exit_action()
            
            button_action_map = {
                ButtonAction.CREATE: self._handle_create_button,
                ButtonAction.CONFIRM_CREATE: self._handle_confirm_button
            }
            
            button_action = button_action_map.get(button_event)
            if button_action:
                button_action()

        self.manager.process_events(event)
        return True
    
    def _handle_create_button(self) -> None:
        self.ui.capture_new_threat_details()

        if not all([
            self.state.threat.name,
            self.state.threat.description,
            self.state.threat.indicators,
            self.state.threat.countermeasures,
            self.state.threat.image_path
        ]):
            return
        
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.state.add_new_threat()
        self.ui.display_confirm_window()

    def _handle_confirm_button(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.CONFIRM_BUTTON)
        self.ui.refresh_creation_page()
        self.state.threat_confirm_window.kill()
        self.state.threat = ThreatDetails()

    def _handle_exit_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT