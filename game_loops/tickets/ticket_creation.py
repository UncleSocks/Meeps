import pygame
import pygame_gui
from dataclasses import dataclass
import pyttsx3

import constants
from constants import ButtonAction, StateTracker
import init
import sound_manager
from sound_manager import ButtonSoundManager
from queries import SqliteQueries
import elements.ticket_elements as ticket_elements



@dataclass
class TicketDetails:
    id: int = 0
    title: str = ""
    entry: str = ""
    threat_id: int = 0
    account_id: int = 1
    transcript: str = ""

@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""


class TicketCreationStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.ticket = TicketDetails()
        self.transcript_engine = pyttsx3.init()
        self.ticket_creation_variables()

    def ticket_creation_variables(self):
        self.threat_list = self.fetch_threat_list()
        self.account_list = self.fetch_account_list()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self.account_id_name_map = self.account_id_name_mapper()
        self.ticket_confirm_window = False

    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.threat_id_name_query()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map

    def account_id_name_mapper(self):
        account_id_name_list = self.query.account_id_name_list()
        account_id_name_map = {account[1]: account[0] for account in account_id_name_list}
        return account_id_name_map

    def fetch_ticket_titles(self):
        ticket_title_list = self.query.ticket_titles_query()
        return ticket_title_list

    def fetch_threat_list(self):
        threat_list = self.query.threat_list_query()
        return threat_list
    
    def fetch_account_list(self):
        account_list = self.query.account_name_list_query()
        return account_list
    
    def fetch_threat_details(self):
        threat_details = self.query.threat_ticket_selection_query(self.ticket.threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def _generate_new_ticket_id(self):
        max_id = self.query.max_ticket_id_query()
        ticket_id = max_id + 1
        return ticket_id
    
    def _generate_ticket_transcript(self):
        ticket_transcript_filename = f'assets/sounds/{self.ticket.id}_transcript.wav'
        self.transcript_engine.save_to_file(self.ticket.entry, ticket_transcript_filename)
        self.transcript_engine.runAndWait()
        return ticket_transcript_filename

    def add_new_ticket(self):
        self.ticket.id = self._generate_new_ticket_id()
        self.ticket.transcript = self._generate_ticket_transcript()
        new_ticket_entry = (self.ticket.id,
                            self.ticket.title,
                            self.ticket.entry,
                            self.ticket.threat_id,
                            self.ticket.account_id,
                            self.ticket.transcript)
        
        self.cursor.execute('INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)', new_ticket_entry)
        self.connect.commit()


class TicketCreationUIManager():

    def __init__(self, pygame_manager, state_manger: TicketCreationStateManager):
        self.manager = pygame_manager
        self.state = state_manger
        self.threat_list = self.state.threat_list
        self.account_list = self.state.account_list
        self.build_ui(self.threat_list, self.account_list)

    def build_ui(self, threat_list, account_list):
        self.back_button = ticket_elements.back_button_func(self.manager)
        self.new_ticket_image = ticket_elements.new_ticket_image_func(self.manager, constants.NEW_TICKET_IMAGE_PATH)
        self.ticket_title_text_entry = ticket_elements.title_text_entry_func(self.manager)
        self.ticket_text_entry = ticket_elements.ticket_text_entry_func(self.manager)

        self.threat_description_tbox = ticket_elements.threat_description_tbox_func(self.manager)
        self.add_ticket_button, self.threat_entry_title_tbox, \
            self.threat_entry_slist = ticket_elements.threat_entry_slist_func(self.manager, threat_list)
        
        self.caller_dropdown_label, \
            self.caller_dropdown = ticket_elements.caller_dropdown_func(self.manager, account_list)
        
    def destroy_elements(self):
        self.back_button.kill()
        self.new_ticket_image.kill()
        self.ticket_title_text_entry.kill()
        self.ticket_text_entry.kill()

        self.threat_description_tbox.kill()
        self.add_ticket_button.kill()
        self.threat_entry_title_tbox.kill()
        self.threat_entry_slist.kill()
        
        self.caller_dropdown_label.kill()
        self.caller_dropdown.kill()

    def capture_new_ticket_details(self):
        self.state.ticket.title = self.ticket_title_text_entry.get_text()
        self.state.ticket.entry = self.ticket_text_entry.get_text()

    def display_threat_textbox(self, threat):
        self.threat_description_tbox.set_text(
            f"<b>{threat.name.upper()}</b>\n"
            f"<b>Description</b>:\n{threat.description}\n"
            f"<b>Indicators:\n</b>{threat.indicators}\n"
            f"<b>Countermeasures:</b>\n{threat.countermeasures}"
        )

    def display_confirm_window(self):
        self.state.ticket_confirm_window, \
            self.ticket_confirm_close_button = ticket_elements.ticket_confirm_window_func(self.manager)
        
    def refresh_creation_page(self):
        self.ticket_title_text_entry.set_text("")
        self.ticket_text_entry.set_text("")
        self.threat_description_tbox.set_text("")


class TicketCreationEventHandler():

    def __init__(self, pygame_manager, state_manager: TicketCreationStateManager, ui_manager: TicketCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_threat_selection(self, selected_threat):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        self.state.ticket.threat_id = self.state.threat_id_name_map[selected_threat]
        self._updated_threat_textbox()

    def _updated_threat_textbox(self):
        threat = self.state.fetch_threat_details()
        self.ui.display_threat_textbox(threat)

    def handle_account_dropdown(self, selected_account):
        self.state.ticket.account_id = self.state.account_id_name_map[selected_account]

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if event.ui_element == self.ui.add_ticket_button:
            return ButtonAction.CREATE

        if self.state.ticket_confirm_window \
            and event.ui_element == self.ui.ticket_confirm_close_button:
            return ButtonAction.CONFIRM_CREATE


class TicketCreationController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = init.PygameRenderer()
        #self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = TicketCreationStateManager(self.connect, self.cursor)
        self.ui = TicketCreationUIManager(self.manager, self.state)
        self.event_handler = TicketCreationEventHandler(self.manager, self.state, self.ui)

    def game_loop(self, events):
        for event in events:
            action = self._handle_events(event)
            if action == ButtonAction.EXIT:
                return StateTracker.TICKET_MANAGEMENT

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.threat_entry_slist:
            selected_threat = event.text
            self.event_handler.handle_threat_selection(selected_threat)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED \
            and event.ui_element == self.ui.caller_dropdown:
            selected_account = event.text
            self.event_handler.handle_account_dropdown(selected_account)

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
    
    def _handle_create_button(self):
        self.ui.capture_new_ticket_details()

        if not all([
            self.state.ticket.title,
            self.state.ticket.entry,
            self.state.ticket.threat_id,
            self.state.ticket.account_id
        ]):
            return
        
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.add_new_ticket()
        self.ui.display_confirm_window()

    def _handle_confirm_button(self):
        self.ui.refresh_creation_page()
        self.state.ticket_confirm_window.kill()
        self.state.ticket = TicketDetails()
    
    def _handle_exit_action(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.ui.destroy_elements()
        return ButtonAction.EXIT