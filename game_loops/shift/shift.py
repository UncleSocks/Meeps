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
    transcript: str = ""


@dataclass
class ThreatDetails:
    name: str = ""
    description: str = ""
    indicators: str = ""
    countermeasures: str = ""
    image: str = ""


class ShiftStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.ticket_interval = self.randomize_ticket_interval()
        self.introduction_variables()
        self.shift_variables()

    def shift_variables(self):
        self.ticket_id_list = self.fetch_ticket_ids()
        self.total_tickets = self.identify_total_tickets()
        self.threat_list = self.fetch_threats()
        self.threat_id_name_map = self.threat_id_name_mapper()
        self._ticket_variables()
        self._popup_variables()
        self._timer_variabbles()
        self._score_variables()

    def introduction_variables(self):
        self.introduction_page = False

    def _ticket_variables(self):
        self.selected_ticket_id = 0
        self.ticket_present = False
        self.ticket_answer = None
        self.ticket_transcript = None
        self.ticket_account_picture = None
        self.selected_threat = None
        self.selected_threat_id = 0

    def _popup_variables(self):
        self.popup_window = False
        #self.popup_accept_button = False
    
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
        popup_sla_countdown = self.max_popup_sla - self.popup_sla_timer
        return popup_sla_countdown

    def fetch_ticket_ids(self):
        ticket_id_list = self.query.ticket_ids_query()
        return ticket_id_list
    
    def fetch_ticket_details(self):
        ticket_detail = self.query.ticket_detail_query(self.selected_ticket_id)
        ticket = TicketDetails(*ticket_detail)
        return ticket
    
    def identify_total_tickets(self):
        total_tickets = len(self.ticket_id_list)
        return total_tickets
    
    def fetch_threats(self):
        threat_list = self.query.threat_list_query()
        return threat_list
    
    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.threat_id_name_query()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map
    
    def fetch_threat_details(self):
        self.selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.threat_management_selection_query(self.selected_threat_id)
        threat = ThreatDetails(*threat_details)
        return threat
    
    def update_difficulty(self):
        mid_difficulty_marker = self.total_tickets / 2
        final_difficulty_marker = mid_difficulty_marker / 2

        if len(self.ticket_id_list) <= final_difficulty_marker:
            self.max_ticket_sla = 60
        elif len(self.ticket_id_list) <= mid_difficulty_marker:
            self.max_ticket_sla = 120
    

class ShiftUIManager():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.build_introduction_ui()

    def build_introduction_ui(self):
        introduction_text = " The cyberspace has neve been this dangerous."
        self.state.introduction_page, \
            self.continue_shift_button = main_loop_elements.introduction_tbox_func(self.manager, introduction_text)

    def build_shift_ui(self, threat_list):
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

    def display_ticket(self, ticket_id, ticket):
        self.ticket_title_tbox.set_text(f'<b>ID#{ticket_id} | {ticket.title}</b>')
        self.ticket_entry_tbox.set_text(ticket.entry)

        account_picture_path = "".join(constants.ACCOUNT_ASSETS_PATH, ticket.account_picture)
        self.caller_profile_image = main_loop_elements.caller_profile_image_func(self.manager, account_picture_path)
        self.caller_profile_tbox.set_text(
            f'Name: {ticket.account}\n'
            f'Organization: {ticket.account_organization}\n'
            f'Email: {ticket.account_email}\n'
            f'Contact: {ticket.account_contact}'
        )

    def display_popup_window(self):
        self.state.popup_window, self.popup_accept_button, \
            self.popup_countdown = main_loop_elements.caller_popup_window_func(self.manager)
        
    def refresh_ticket(self):
        self.ticket_title_tbox.set_text("")
        self.ticket_entry_tbox("AWAITING TICKET...")
        self.caller_profile_tbox.set_text("NO CALLER")
        self.main_sla_timer_label.set_text("SLA: ")


class ShiftSoundController():

    def __init__(self, state_manager: ShiftStateManager):
        self.state = state_manager
        self.sound = sound_manager
        self.button_sfx = self.sound.ButtonSoundManager()
        self.call_sfx = self.sound.LoopingSoundManager(constants.INCOMING_CALL_MUSIC_PATH, constants.INCOMMING_CALL_CHANNEL)
        self.background_music = self.sound.BackgroundMusicManager(constants.BACKGROUND_MUSIC_PATH)

    def transcribe_ticket(self, ticket_transcript):
        self.state.ticket_transcript = self.sound.TicketTranscriptManager(ticket_transcript)
        self.state.ticket_transcript.load_trancript()
        self.state.ticket_transcript.play_transcript()

    def stop_transcribing_ticket(self):
        self.state.ticket_transcript.stop_transcript()
        pygame.mixer.music.unload()

    def stop_background_music(self):
        self.background_music.stop_music()
        pygame.mixer.music.unload()

    def reload_background_music(self):
        self.background_music.load_music()
        self.background_music.play_music()

    def end_shift_music(self):
        self.state.ticket_transcript.stop_transcript() if self.state.ticket_transcript else None
        self.background_music.stop_music()
        pygame.mixer.music.unload()


class ShiftEventHandler():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller

    def handle_threat_selection(self, selected_threat):
        self.sound.button_sfx.play_sfx(constants.LIST_BUTTON_SFX)
        self.state.selected_threat = selected_threat
        self._update_threat_textbox()

    def _update_threat_textbox(self):
        threat = self.state.fetch_threat_details()

        self._load_threat_image(threat.image)
        self.ui.threat_title_tbox.set_text(f"<b>{threat.name.upper()}</b>")
        self.ui.threat_description_tbox.set_text(
            f"<b>Description</b>:\n{threat.description}\n"
            f"<b>Indicators:\n</b>{threat.indicators}\n"
            f"<b>Countermeasures:</b>\n{threat.countermeasures}"
        )

    def _load_threat_image(self, image_file):
        threat_image_path = "".join(constants.THREAT_ASSETS_PATH, image_file)

        try:
            load_threat_image = pygame.image.load(threat_image_path)
        except:
            load_threat_image = pygame.image.load(constants.DEFAULT_THREAT_IMAGE_PATH)
        
        self.ui.threat_image.set_image(new_image=load_threat_image)
        return
    
    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()
        
        if self.state.introduction_page and event.ui_element == self.ui.continue_shift_button:
            self.state.introduction_page = False
            return constants.CONTINUE_SHIFT_ACTION
        
        if self.state.popup_window and event.ui_element == self.ui.popup_accept_button:
            generate_ticket = GenerateTicket(self.manager, self.state, self.ui, self.sound)
            generate_ticket.generate_ticket()
        
        if event.ui_elemnent == self.ui.submit_button and self.state.ticket_present \
            and self.state.selected_threat:
            self._handle_submit_button()

    def _handle_back_button(self):
        self.sound.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.sound.end_shift_music()
        return constants.EXIT_ACTION
    
    def _handle_submit_button(self):
        self.ui.refresh_ticket()
        self._check_ticket_answer()
        self.sound.stop_transcribing_ticket()
        self.sound.reload_background_music()

    def _check_ticket_answer(self):
        if self.state.selected_ticket_id == self.state.ticket_answer:
            self.sound.button_sfx.play_sfx(constants.CORRECT_SUBMIT_SFX)
            self.state.total_score += 1
        else:
            self.sound.button_sfx.play_sfx(constants.INCORRECT_SUBMIT_SFX)


class GenerateTicket():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller
        self._restart_state_variables()
        self._stop_call()

    def _restart_state_variables(self):
        self.state.ticket_sla_timer = 0
        self.state.selected_threat = None

    def _stop_call(self):
        self.sound.call_sfx.stop_loop()
        self.state.popup_window.hide()
        self.state.popup_window = False

    def generate_ticket(self):
        self.state.selected_ticket_id = self.state.ticket_id_list[0]
        ticket = self.state.fetch_ticket_details()
        self.ui.display_ticket(self.state.selected_ticket_id, ticket)
        self._update_ticket_state()
        self.sound.transcribe_ticket(ticket.transcript)
        self.state.ticket_answer = ticket.threat
        return
    
    def _update_ticket_state(self):
        self.state.ticket_present = True
        self.state.ticket_id_list.remove(self.state.selected_ticket_id)


class ShiftIntroduction():

    def __init__(self, pygame_manager):
        self.manager = pygame_manager



class ShiftController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

        self.state = ShiftStateManager(self.connect, self.cursor)
        self.ui = ShiftUIManager(self.manager, self.state)
        self.sound = ShiftSoundController(self.state)
        self.event_handler = ShiftEventHandler(self.manager, self.state, self.ui, self.sound)

    def shift_loop(self):
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

            if button_action == constants.CONTINUE_SHIFT_ACTION:
                self.ui.build_shift_ui(self.state.threat_list)
            elif button_action == constants.EXIT_ACTION:
                return False