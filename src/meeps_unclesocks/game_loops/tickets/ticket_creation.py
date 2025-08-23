import pygame
import pygame_gui
import pyttsx3
from dataclasses import dataclass

import init
import elements.game_elements.ticket_elements.ticket_creation_elements as tce
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, \
    ImagePaths, ButtonSFX 
from sound_manager import ButtonSoundManager
from db_manager import DatabaseQueries




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
    image: str = ""


class TicketCreationStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = DatabaseQueries(self.cursor)
        self.ticket = TicketDetails()
        self.transcript_engine = pyttsx3.init()
        self.ticket_creation_variables()

    def ticket_creation_variables(self):
        self.threat_list = self.fetch_threat_list()
        self.account_list = self.fetch_account_list()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self.account_id_name_map = self.account_id_name_mapper()
        self.confirm_window = False

    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.fetch_threat_names_ids()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map

    def account_id_name_mapper(self):
        account_id_name_list = self.query.fetch_account_names_ids()
        account_id_name_map = {account[1]: account[0] for account in account_id_name_list}
        return account_id_name_map

    def fetch_ticket_titles(self):
        ticket_title_list = self.query.fetch_ticket_titles()
        return ticket_title_list

    def fetch_threat_list(self):
        threat_list = self.query.fetch_threat_names()
        return threat_list
    
    def fetch_account_list(self):
        account_list = self.query.fetch_account_names()
        return account_list
    
    def fetch_threat_details(self):
        threat_details = self.query.fetch_threat_details(self.ticket.threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def _generate_new_ticket_id(self):
        max_id = self.query.fetch_max_id(table='tickets')
        ticket_id = max_id + 1
        return ticket_id
    
    def _generate_ticket_transcript(self):
        ticket_transcript_filename = f'assets/sounds/transcripts/{self.ticket.id}_transcript.wav'
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
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_dropdowns()
        self._draw_ticket_creation_elements()        

    def _draw_images(self):
        add_ticket_image = tce.NewTicketImage(self.manager)
        add_ticket_image_load = pygame.image.load(ImagePaths.TICKET_CREATION.value)
        add_ticket_image.INPUT = add_ticket_image_load
        self.add_ticket_image = add_ticket_image.draw_image()

    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.add_button = tce.AddTicketButton(self.manager).draw_button()

    def _draw_dropdowns(self):
        self.account_dropdown_label = tce.AccountDropDownLabel(self.manager).draw_label()

        account_dropdown = tce.AccountDropDown(self.manager)
        account_dropdown.INPUT = self.state.account_list
        self.account_dropdown = account_dropdown.draw_dropdown()

    def _draw_ticket_creation_elements(self):
        self.new_ticket_title = tce.NewTicketTitle(self.manager).draw_textentrybox()
        self.new_ticket_description = tce.NewTicketDescription(self.manager).draw_textentrybox()
        self.threat_list_textbox = tce.ThreatListTextBox(self.manager).draw_textbox()
        self.threat_description = tce.ThreatDescription(self.manager).draw_textbox()

        threat_selection_list = tce.ThreatList(self.manager)
        threat_selection_list.INPUT = self.state.threat_list
        self.threat_selection_list = threat_selection_list.draw_selectionlist()

    def capture_new_ticket_details(self):
        self.state.ticket.title = self.new_ticket_title.get_text()
        self.state.ticket.entry = self.new_ticket_description.get_text()

    def display_threat_textbox(self, threat):
        self.threat_description.set_text(
            f"<b>{threat.name.upper()}</b>\n"
            f"<b>Description</b>:\n{threat.description}\n"
            f"<b>Indicators:\n</b>{threat.indicators}\n"
            f"<b>Countermeasures:</b>\n{threat.countermeasures}"
        )

    def display_confirm_window(self):
        self.state.confirm_window = tce.ConfirmWindow(self.manager).draw_window()

        confirm_label = tce.ConfirmLabel(self.manager)
        confirm_label.CONTAINER = self.state.confirm_window
        self.confirm_label = confirm_label.draw_label()

        confirm_button = se.ConfirmButton(self.manager)
        confirm_button.CONTAINER = self.state.confirm_window
        self.confirm_button = confirm_button.draw_button()
        
    def refresh_creation_page(self):
        self.new_ticket_title.set_text("")
        self.new_ticket_description.set_text("")
        self.threat_description.set_text("")


class TicketCreationEventHandler():

    def __init__(self, pygame_manager, state_manager: TicketCreationStateManager, ui_manager: TicketCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = ButtonSoundManager()

    def handle_threat_selection(self, selected_threat):
        self.button_sfx.play_sfx(ButtonSFX.LIST_BUTTON)
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
        
        if event.ui_element == self.ui.add_button:
            return ButtonAction.CREATE

        if self.state.confirm_window \
            and event.ui_element == self.ui.confirm_button:
            return ButtonAction.CONFIRM_CREATE


class TicketCreationController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = init.PygameRenderer()
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
            and event.ui_element == self.ui.threat_selection_list:
            selected_threat = event.text
            self.event_handler.handle_threat_selection(selected_threat)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED \
            and event.ui_element == self.ui.account_dropdown:
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
        
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.state.add_new_ticket()
        self.ui.display_confirm_window()

    def _handle_confirm_button(self):
        self.button_sfx.play_sfx(ButtonSFX.CONFIRM_BUTTON)
        self.ui.refresh_creation_page()
        self.state.confirm_window.kill()
        self.state.ticket = TicketDetails()
    
    def _handle_exit_action(self):
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT