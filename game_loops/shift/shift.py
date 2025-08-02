import random
from dataclasses import dataclass

import pygame
import pygame_gui

import constants
import sound_manager
import init
import elements.main_loop_elements as main_loop_elements
from queries import SqliteQueries



@dataclass
class TicketDetails:
    title: str = ""
    entry: str = ""
    threat: str = ""
    account: str = ""
    account_organization: str = ""
    account_email: str = ""
    account_contact: str = ""
    account_picture: str = ""


@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    picture: str = ""


class ShiftStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.ticket_interval = self.randomize_ticket_interval()
        self.shift_variables()

    def shift_variables(self):
        self.ticket_title_list = self.fetch_tickets()
        self.total_tickets = self.identify_total_tickets()
        self.threat_list = self.fetch_threats()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self._ticket_variables()
        self._popup_variables()
        self._timer_variabbles()
        self._score_variables()

    def _ticket_variables(self):
        self.selected_ticket_id = 0
        self.ticket_present = False
        self.ticket_answer = None
        self.ticket_transcript = None
        self.ticket_account_picture = None
        self.selected_threat = None

    def _popup_variables(self):
        self.popup_window = False
        self.popup_accept_button = False
    
    def _timer_variabbles(self):
        self.ticket_generate_timer = 0

        self.max_ticket_sla = 180
        self.max_popup_sla = 15
        self.ticket_sla_timer = 0
        self.popup_sla_timer = 0

    def _score_variables(self):
        self.total_score = 0
        self.missed_calls = 0
        self.missed_tickets = 0

    def randomize_ticket_interval(self):
        ticket_interval = random.uniform(constants.MIN_CALL_INTERVAL, constants.MAX_CALL_INTERVAL)
        return ticket_interval
    
    def ticket_sla_countdown(self):
        ticket_sla_countdown = self.max_ticket_sla - self.ticket_sla_timer
        return ticket_sla_countdown
    
    def popup_sla_countdown(self):
        popup_sla_countdown = self.max_popup_sla - self.popup_close_timer
        return popup_sla_countdown

    def fetch_tickets(self):
        ticket_title_list = self.query.ticket_ids_query()
        return ticket_title_list
    
    def fetch_ticket_details(self):
        ticket_detail = self.query.ticket_query(self.selected_ticket_id)
        ticket = ticket_detail(*TicketDetails)
        return ticket
    
    def identify_total_tickets(self):
        total_tickets = len(self.ticket_title_list)
        return total_tickets
    
    def fetch_threats(self):
        threat_list = self.query.threat_list_query()
        return threat_list
    
    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.threat_id_name_query()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map
    
    def fetch_threat_details(self):
        selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.threat_management_selection_query(selected_threat_id)
        threat = threat_details(*ThreatDetails)
        return threat
    

class ShiftUIManager():

    def __init__(self, pygame_manager, threat_list):
        self.manager = pygame_manager
        self.build_ui(threat_list)

    def build_ui(self, threat_list):
        self.back_button = main_loop_elements.back_button_func(self.manager)
        self.title_label = main_loop_elements.title_image_func(self.manager, constants.TITLE_IMAGE_PATH)

        self.main_sla_timer_label = main_loop_elements.main_sla_timer_label_func(self.manager)
        self.caller_profile_tbox = main_loop_elements.caller_profile_tbox_func(self.manager)

        self.submit_button = main_loop_elements.submit_button_func(self.manager)
        self.threat_entry_title_box = main_loop_elements.threat_entry_title_tbox_func(self.manager)
        self.threat_entry_slist = main_loop_elements.threat_entry_slist_func(self.manager, threat_list)

        self.threat_panel, self.threat_title_tbox, \
            self.threat_image, self.threat_description_tbox = main_loop_elements.threat_panel_func(self.manager)
        
        self.ticket_title_tbox = main_loop_elements.ticket_title_tbox_func(self.manager)
        self.ticket_entry_tbox = main_loop_elements.ticket_entry_tbox_func(self.manager)


class ShiftEventHandler():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, ui_manager: ShiftUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self._init_sounds()
        
    def _init_sounds(self):
        self.button_sfx = sound_manager.ButtonSoundManager()
        self.call_sfx = sound_manager.LoopingSoundManager(constants.INCOMING_CALL_MUSIC_PATH, constants.INCOMMING_CALL_CHANNEL)
        self.background_music = sound_manager.BackgroundMusicManager(constants.BACK_BUTTON_MUSIC_PATH)