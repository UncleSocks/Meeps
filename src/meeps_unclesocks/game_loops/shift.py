import os
import random
from dataclasses import dataclass

import pygame
import pygame_gui

import elements.game_elements.shift_elements as she
import elements.game_elements.shared_elements as se
from constants import ButtonAction, StateTracker, \
    ButtonSFX, MusicPaths, MixerChannels, AssetBasePath, \
    Timers, Settings, ImagePaths, DefaultImages
from init import PygameRenderer
from managers.sound_manager import ButtonSoundManager, LoopingSoundManager, \
    BackgroundMusicManager, TicketTranscriptManager
from managers.db_manager import DatabaseQueries



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


class ShiftStateManager:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = DatabaseQueries(self.cursor)
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
        self.end_shift_report = None

    def randomize_ticket_interval(self):
        ticket_interval = random.uniform(Timers.MIN_CALL_INTERVAL.value, Timers.MAX_CALL_INTERVAL.value)
        return ticket_interval
    
    def ticket_sla_countdown(self):
        ticket_sla_countdown = self.max_ticket_sla - self.ticket_sla_timer
        return ticket_sla_countdown
    
    def popup_sla_countdown(self):
        popup_sla_countdown = self.max_popup_sla - self.popup_sla_timer
        return popup_sla_countdown

    def fetch_ticket_ids(self):
        ticket_id_list = self.query.fetch_ticket_ids()
        return ticket_id_list
    
    def fetch_ticket_details(self):
        ticket_detail = self.query.fetch_ticket_details(self.selected_ticket_id)
        ticket = TicketDetails(*ticket_detail)
        return ticket
    
    def identify_total_tickets(self):
        total_tickets = len(self.ticket_id_list)
        return total_tickets
    
    def fetch_threats(self):
        threat_list = self.query.fetch_threat_names()
        return threat_list
    
    def threat_id_name_mapper(self):
        threat_id_name_list = self.query.fetch_threat_names_ids()
        threat_id_name_map = {threat[1]: threat[0] for threat in threat_id_name_list}
        return threat_id_name_map
    
    def fetch_threat_details(self):
        self.selected_threat_id = self.threat_id_name_map[self.selected_threat]
        threat_details = self.query.fetch_threat_details(self.selected_threat_id)
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
    

class ShiftUIManager:

    def __init__(self, pygame_manager, state_manager: ShiftStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.end_shift_button = None
        self.draw_introduction_elements()

    def draw_introduction_elements(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.state.introduction_page = she.IntroductionText(self.manager).draw_textbox()
        self.continue_shift_button = she.ContinueButton(self.manager).draw_button()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_shift_elements()
        self._draw_threat_elements()
        self.caller_profile_image = None

    def _draw_images(self):
        shift_title_image = she.ShiftTitleImage(self.manager)
        shift_title_image_load = pygame.image.load(ImagePaths.TITLE.path)
        shift_title_image.INPUT = shift_title_image_load
        self.shift_title_image = shift_title_image.draw_image()

    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.submit_button = she.SubmitButton(self.manager).draw_button()

    def _draw_shift_elements(self):
        self.ticket_sla_timer_label = she.TicketSLATimerLabel(self.manager).draw_label()
        self.caller_information = she.CallerInformation(self.manager).draw_textbox()

        self.threat_list_title = she.ThreatListTitle(self.manager).draw_textbox()
        threat_selection_list = she.ThreatList(self.manager)
        threat_selection_list.INPUT = self.state.threat_list
        self.threat_selection_list = threat_selection_list.draw_selectionlist()

        self.ticket_title = she.TicketTitle(self.manager).draw_textbox()
        self.ticket_information = she.TicketInformation(self.manager).draw_textbox()

    def _draw_threat_elements(self):
        self.threat_information_panel = she.ThreatPanel(self.manager).draw_panel()

        threat_title = she.ThreatTitle(self.manager)
        threat_title.CONTAINER = self.threat_information_panel
        self.threat_title = threat_title.draw_textbox()

        threat_image = she.ThreatImage(self.manager)
        threat_image_load = pygame.image.load(DefaultImages.BLANK.path)
        threat_image.INPUT = threat_image_load
        threat_image.CONTAINER = self.threat_information_panel
        self.threat_image = threat_image.draw_image()

        threat_information = she.ThreatInformation(self.manager)
        threat_information.CONTAINER = self.threat_information_panel
        self.threat_information = threat_information.draw_textbox()

    def display_ticket(self, ticket_id, ticket):
        self.ticket_title.set_text(f'<b>ID#{ticket_id} | {ticket.title}</b>')
        self.ticket_information.set_text(ticket.entry)
        
        self._display_caller_image(ticket)
        self.caller_information.set_text(
            f'Name: {ticket.account}\n'
            f'Organization: {ticket.account_organization}\n'
            f'Email: {ticket.account_email}\n'
            f'Contact: {ticket.account_contact}'
        )

    def _display_caller_image(self, ticket):
        account_picture_path = os.path.join(AssetBasePath.ACCOUNT_ASSETS.value, ticket.account_picture)
        caller_profile_image = she.CallerProfileImagee(self.manager)

        try:
            load_caller_profile_image = pygame.image.load(account_picture_path)
        except (pygame.error, FileNotFoundError):
            load_caller_profile_image = pygame.image.load(DefaultImages.GUEST_ACCOUNT.path)
        
        caller_profile_image.INPUT = load_caller_profile_image
        self.caller_profile_image = caller_profile_image.draw_image()

    def display_popup_window(self):
        self.state.popup_window = she.CallerPopupWindow(self.manager).draw_window()

        popup_window_label = she.CallerPopupWindowLabel(self.manager)
        popup_window_label.CONTAINER = self.state.popup_window
        self.popup_window_label = popup_window_label.draw_label()
        
        popup_countdown = she.CallerPopupWindowSLA(self.manager)
        popup_countdown.CONTAINER = self.state.popup_window
        self.popup_countdown = popup_countdown.draw_label()

        answer_button = she.AnswerButton(self.manager)
        answer_button.CONTAINER = self.state.popup_window
        self.answer_button = answer_button.draw_button()
        
    def display_shift_report(self, assessment_result):
        self.end_shift_label = she.EndShiftLabel(self.manager).draw_label()
        self.end_shift_button = she.EndShiftButton(self.manager).draw_button()

        self.state.end_shift_report = she.EndShiftTextBox(self.manager)
        self.state.end_shift_report.INPUT = (
            f"Employee No: #1934\n"
            f"Title: L1 SOC Analyst\n"
            f"Total Tickets: {self.state.total_tickets}\n"
            f"Accurate Ticket Resolution: {self.state.total_score}\n"
            f"Missed Calls: {self.state.missed_calls}\n"
            f"Missed Tickets: {self.state.missed_tickets}\n"
            f"\n<b>ASSESSMENT RUSULT:<b>{assessment_result}"
        )
        self.state.end_shift_report = self.state.end_shift_report.draw_textbox()

    def refresh_ticket(self):
        self.ticket_title.set_text("")
        self.ticket_information.set_text("AWAITING TICKET...")
        self.caller_information.set_text("NO CALLER")
        self.ticket_sla_timer_label.set_text("SLA: ")
        self.caller_profile_image.kill()


class ShiftSoundController:

    def __init__(self, state_manager: ShiftStateManager):
        self.state = state_manager
        self.button_sfx = ButtonSoundManager()
        self.call_sfx = LoopingSoundManager(MusicPaths.INCOMING_CALL.path, MixerChannels.INCOMING_CALL.value)
        self.background_music = BackgroundMusicManager(MusicPaths.BACKGROUND_MUSIC.path)

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


class GenerateTicket:

    def __init__(self, state_manager: ShiftStateManager, 
                 ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
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


class GenerateReport:

    def __init__(self, state_manager: ShiftStateManager):
        self.state = state_manager

    def generate_shift_report(self):
        assessment_percent = (self.state.total_score / self.state.total_tickets) * 100
        if assessment_percent >= 80: 
            assessment_result = "PASS"
        else:
            assessment_result = "FAIL"
        return assessment_result


class CountdownManager:

    def __init__(self, pygame_manager, state_manager: ShiftStateManager, 
                 ui_manager: ShiftUIManager, sound_controller: ShiftSoundController):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.sound = sound_controller

    def ticket_sla_countdown(self, time_delta):
        ticket_sla_difference = self.state.max_ticket_sla - self.state.ticket_sla_timer
        self.ui.ticket_sla_timer_label.set_text('SLA: {:.1f}'.format(max(0, ticket_sla_difference)))                            
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


class ShiftEventHandler:

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
        self.ui.threat_title.set_text(f"<b>{threat.name.upper()}</b>")
        self.ui.threat_information.set_text(
            f"<b>Description</b>:\n{threat.description}\n"
            f"<b>Indicators:\n</b>{threat.indicators}\n"
            f"<b>Countermeasures:</b>\n{threat.countermeasures}"
        )

    def _load_threat_image(self, image_file):
        image_file = str(image_file)
        threat_image_path = os.path.join(AssetBasePath.THREAT_ASSETS.value, image_file)

        try:
            load_threat_image = pygame.image.load(threat_image_path)
        except (pygame.error, FileNotFoundError):
            load_threat_image = pygame.image.load(DefaultImages.THREAT.path)
        
        self.ui.threat_image.set_image(new_image=load_threat_image)
        return
    
    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if self.state.introduction_page and event.ui_element == self.ui.continue_shift_button:
            return ButtonAction.CONTINUE
        
        if self.state.popup_window and event.ui_element == self.ui.answer_button:
            return ButtonAction.ANSWER
        
        if event.ui_element == self.ui.submit_button and self.state.ticket_present \
            and self.state.selected_threat:
            return ButtonAction.SUBMIT
        
        if self.state.end_shift_report and self.ui.end_shift_button:
            return ButtonAction.EXIT
    

class ShiftController:

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
        self.window_surface = self.pygame_renderer.window_surface

        self.state = ShiftStateManager(self.connect, self.cursor)
        self.ui = ShiftUIManager(self.manager, self.state)
        self.sound = ShiftSoundController(self.state)
        self.event_handler = ShiftEventHandler(self.manager, self.state, self.ui, self.sound)
        self.countdown = CountdownManager(self.manager, self.state, self.ui, self.sound)

    def game_loop(self, events):
        time_delta = self.pygame_renderer.clock.tick(Settings.FPS.value) / Settings.MS_PER_SECOND.value
        if self.state.introduction_page is None:
            self.state.ticket_generate_timer += time_delta

        for event in events:
            action = self._handle_events(event)
            
            if action == ButtonAction.EXIT:
                return StateTracker.MAIN_MENU

        if self.state.ticket_generate_timer >= self.state.ticket_interval \
            and self.state.ticket_id_list and not self.state.ticket_present \
                and self.state.popup_window is None \
                    and self.state.introduction_page is None:
            self._handle_incoming_call()

        if self.state.popup_window:
            self.countdown.popup_sla_countdown(time_delta)

        if self.state.ticket_present and self.state.popup_window is None:
            self.countdown.ticket_sla_countdown(time_delta)

        if self.state.total_tickets != 0 and not self.state.ticket_id_list \
            and not self.state.ticket_present and self.state.introduction_page is None \
                and self.state.end_shift_report is None:
            self._handle_end_shift_report()
        
        self.state.update_difficulty()

    def _handle_incoming_call(self):
        self.ui.display_popup_window()
        self.state.popup_sla_timer = 0

        self.sound.stop_background_music()
        self.sound.call_sfx.play_loop()

    def _handle_end_shift_report(self):
        self.sound.end_shift_music()
        self.manager.clear_and_reset()
        assessment = GenerateReport(self.state).generate_shift_report()
        self.ui.display_shift_report(assessment)

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.threat_selection_list:
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
        self.manager.clear_and_reset()
        self.state.introduction_page = None
        self.ui.draw_ui_elements()

    def _handle_answer_action(self):
        generate_ticket = GenerateTicket(self.state, self.ui, self.sound)
        generate_ticket.generate_ticket()
    
    def _handle_submit_action(self):
        self.ui.refresh_ticket()
        self.state.reset_ticket_state()
        self._check_ticket_answer()
        self.sound.stop_transcribing_ticket()
        self.sound.reload_background_music()

    def _check_ticket_answer(self):
        if self.state.selected_threat_id == self.state.ticket_answer:
            self.sound.button_sfx.play_sfx(ButtonSFX.CORRECT_SUBMISSION)
            self.state.total_score += 1
        else:
            self.sound.button_sfx.play_sfx(ButtonSFX.INCORRECT_SUBMISSION)

    def _handle_exit_button(self):
        self.sound.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.sound.end_shift_music()
        self.sound.call_sfx.stop_loop()
        self.manager.clear_and_reset()
        return ButtonAction.EXIT