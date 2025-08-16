import random
from dataclasses import dataclass

import pygame
import pygame_gui

import constants
from constants import ButtonAction, StateTracker, \
    ButtonSFX, MusicPaths, MixerChannels, AssetBasePath
from sound_manager import ButtonSoundManager, LoopingSoundManager, \
    BackgroundMusicManager, TicketTranscriptManager
import init
import elements.main_loop_elements as main_loop_elements
from queries import SqliteQueries



@dataclass
class TicketDetails:
    title: str = ""
    entry: str = ""
    threat: str = ""
    transcript: str = ""
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
        self.introduction_page = None

    def _ticket_variables(self):
        self.selected_ticket_id = 0
        self.ticket_present = False
        self.ticket_answer = None
        self.ticket_transcript = None
        self.selected_threat = None
        self.selected_threat_id = 0

    def _popup_variables(self):
        self.popup_window = None
    
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

    def reset_ticket_state(self):
        self.ticket_present = False
        self.ticket_generate_timer = 0
        self.ticket_sla_timer = 0
        self.popup_window = None

    def update_ticket_state(self):
        self.ticket_present = True
        self.selected_threat = None
        self.popup_window = None
        self.ticket_sla_timer = 0

    def dequeue_ticket(self):
        self.selected_ticket_id = self.ticket_id_list.pop(0)
    

class ShiftUIManager():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.build_introduction_ui()

    def build_introduction_ui(self):
        self.back_button = main_loop_elements.back_button_func(self.manager)

        introduction_text = " The cyberspace has neve been this dangerous."
        self.state.introduction_page, \
            self.continue_shift_button = main_loop_elements.introduction_tbox(self.manager, introduction_text)
        
    def destroy_introduction_ui(self):
        self.back_button.kill()
        self.state.introduction_page.kill()
        self.continue_shift_button.kill()

        self.state.introduction_page = None

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
        self.caller_profile_image = None

    def destroy_elements(self):
        self.back_button.kill()
        self.title_label.kill()

        self.main_sla_timer_label.kill()
        self.caller_profile_tbox .kill()

        self.submit_button.kill()
        self.threat_entry_title_box.kill()
        self.threat_entry_slist.kill()

        self.threat_panel.kill()
        self.threat_title_tbox.kill()
        self.threat_image.kill()
        self.threat_description_tbox.kill()
        
        self.ticket_title_tbox.kill()
        self.ticket_entry_tbox.kill()

        self.state.popup_window.kill() if self.state.popup_window else None
        self.caller_profile_image.kill() if self.caller_profile_image else None

    def display_ticket(self, ticket_id, ticket):
        self.ticket_title_tbox.set_text(f'<b>ID#{ticket_id} | {ticket.title}</b>')
        self.ticket_entry_tbox.set_text(ticket.entry)

        account_picture_path = "".join([AssetBasePath.ACCOUNT_ASSETS.value, ticket.account_picture])
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
        self.ticket_entry_tbox.set_text("AWAITING TICKET...")
        self.caller_profile_tbox.set_text("NO CALLER")
        self.main_sla_timer_label.set_text("SLA: ")
        self.caller_profile_image.kill()


class ShiftSoundController():

    def __init__(self, state_manager: ShiftStateManager):
        self.state = state_manager
        self.button_sfx = ButtonSoundManager()
        self.call_sfx = LoopingSoundManager(MusicPaths.INCOMING_CALL.value, MixerChannels.INCOMING_CALL.value)
        self.background_music = BackgroundMusicManager(MusicPaths.BACKGROUND_MUSIC.value)

    def transcribe_ticket(self, ticket_transcript):
        self.state.ticket_transcript = TicketTranscriptManager(ticket_transcript)
        self.state.ticket_transcript.load_transcript()
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


class GenerateTicket():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, 
                 ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller

    def generate_ticket(self):
        self._stop_call()
        self.state.dequeue_ticket()
        self.state.update_ticket_state()
        ticket = self.state.fetch_ticket_details()
        self.ui.display_ticket(self.state.selected_ticket_id, ticket)
        self.sound.transcribe_ticket(ticket.transcript)
        self.state.ticket_answer = ticket.threat

    def _stop_call(self):
        self.sound.call_sfx.stop_loop()
        self.state.popup_window.kill()


class CountdownManager():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, 
                 ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller

    def ticket_sla_countdown(self, time_delta):
        ticket_sla_difference = self.state.max_ticket_sla - self.state.ticket_sla_timer
        self.ui.main_sla_timer_label.set_text('SLA: {:.1f}'.format(max(0, ticket_sla_difference)))                            
        self.state.ticket_sla_timer += time_delta

        if ticket_sla_difference <= 0:
            self._ticket_sla_timeout()

    def _ticket_sla_timeout(self):
        self.ui.refresh_ticket()
        self.state.dequeue_ticket()
        self.state.reset_ticket_state()
        self.state.missed_tickets += 1

    def popup_sla_countdown(self, time_delta):
        popup_sla_difference = self.state.max_popup_sla - self.state.popup_sla_timer
        self.ui.popup_countdown.set_text('SLA: {:.1f}'.format(max(0, popup_sla_difference)))
        self.state.popup_sla_timer += time_delta

        if popup_sla_difference <= 0:
            self._popup_sla_timeout()

    def _popup_sla_timeout(self):
        self.state.popup_window.kill()
        self.state.dequeue_ticket()
        self.state.reset_ticket_state()
        self.state.missed_calls += 1
        self.sound.call_sfx.stop_loop()


class ShiftEventHandler():

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, 
                 ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller

    def handle_threat_selection(self, selected_threat):
        self.sound.button_sfx.play_sfx(ButtonSFX.LIST_BUTTON)
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
        image_file = str(image_file)
        threat_image_path = "".join([AssetBasePath.THREAT_ASSETS.value, image_file])

        try:
            load_threat_image = pygame.image.load(threat_image_path)
        except (pygame.error, FileNotFoundError):
            load_threat_image = pygame.image.load(constants.DEFAULT_THREAT_IMAGE_PATH)
        
        self.ui.threat_image.set_image(new_image=load_threat_image)
        return
    
    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if self.state.introduction_page and event.ui_element == self.ui.continue_shift_button:
            return ButtonAction.CONTINUE
        
        if self.state.popup_window and event.ui_element == self.ui.popup_accept_button:
            return ButtonAction.ANSWER
        
        if event.ui_element == self.ui.submit_button and self.state.ticket_present \
            and self.state.selected_threat:
            return ButtonAction.SUBMIT
    

class ShiftController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = init.PygameRenderer()
        #self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

        self.state = ShiftStateManager(self.connect, self.cursor)
        self.ui = ShiftUIManager(self.manager, self.state)
        self.sound = ShiftSoundController(self.state)
        self.event_handler = ShiftEventHandler(self.manager, self.state, self.ui, self.sound)
        self.countdown = CountdownManager(self.manager, self.state, self.ui, self.sound)

    def game_loop(self, events):
        time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
        self.state.ticket_generate_timer += time_delta
        #events = pygame.event.get()

        for event in events:
            action = self._handle_events(event)

            if action == ButtonAction.EXIT:
                return StateTracker.MAIN_MENU

        if self.state.ticket_generate_timer >= self.state.ticket_interval \
            and self.state.ticket_id_list and not self.state.ticket_present \
                and self.state.popup_window is None:
            self._handle_incoming_call()

        if self.state.popup_window:
            self.countdown.popup_sla_countdown(time_delta)

        if self.state.ticket_present and self.state.popup_window is None:
            self.countdown.ticket_sla_countdown(time_delta)
        
        self.state.update_difficulty()

    def _handle_incoming_call(self):
        self.ui.display_popup_window()
        self.state.popup_sla_timer = 0

        self.sound.stop_background_music()
        self.sound.call_sfx.play_loop()

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.threat_entry_slist:
            selected_threat = event.text
            self.event_handler.handle_threat_selection(selected_threat)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == ButtonAction.EXIT:
                return self._handle_exit_button()
            
            button_event_map = {
                ButtonAction.CONTINUE: self._handle_continue_action,
                ButtonAction.ANSWER: self._handle_answer_action,
                ButtonAction.SUBMIT: self._handle_submit_action
            }

            button_action = button_event_map.get(button_event)
            if button_action:
                button_action()
            
        self.manager.process_events(event)
        return True
    
    def _handle_continue_action(self):
        self.ui.destroy_introduction_ui()
        self.ui.build_shift_ui(self.state.threat_list)

    def _handle_answer_action(self):
        generate_ticket = GenerateTicket(self.manager, self.state, self.ui, self.sound)
        generate_ticket.generate_ticket()
    
    def _handle_submit_action(self):
        self.ui.refresh_ticket()
        self.state.reset_ticket_state()
        self._check_ticket_answer()
        self.sound.stop_transcribing_ticket()
        self.sound.reload_background_music()

    def _check_ticket_answer(self):
        if self.state.selected_threat_id == self.state.ticket_answer:
            print(f"Correct {self.state.selected_threat_id}:{self.state.ticket_answer}")
            self.sound.button_sfx.play_sfx(ButtonSFX.CORRECT_SUBMISSION)
            self.state.total_score += 1
        else:
            print("Incorrect")
            self.sound.button_sfx.play_sfx(ButtonSFX.INCORRECT_SUBMISSION)

    def _handle_exit_button(self):
        self.sound.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.sound.end_shift_music()
        self.sound.call_sfx.stop_loop()

        if self.state.introduction_page:
            self.ui.destroy_introduction_ui()
        else:
            self.ui.destroy_elements()
        return ButtonAction.EXIT