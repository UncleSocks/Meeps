import random

import pygame
import pygame_gui

import constants
import sound_manager
import init
import elements.main_loop_elements as main_loop_elements
from queries import SqliteQueries




def shift_introduction(connect, cursor):

    pygame_renderer = init.PygameRenderer()
    manager = pygame_renderer.manager

    back_button = main_loop_elements.back_button_func(manager)

    introduction_text = """
        The cyberspace has neve been this dangerous. As an L1 SOC Analyst at Meeps Security, you must correctly
        access 80% of the tickets to protect our clients.
    """
    main_loop_elements.introduction_tbox_func(manager, introduction_text)

    continue_button = main_loop_elements.continue_button_func(manager)

    running = True
    while running:

        time_delta = pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    running = False

                if event.ui_element == continue_button:
                    start_shift = ShiftLoop(connect, cursor)
                    start_shift.shift_loop()
                    return
                
            manager.process_events(event)

        pygame_renderer.ui_renderer(time_delta)


class ShiftLoop:

    def __init__ (self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self._init_pygame()
        self._init_gameplay_elements()
        self._init_ui_elements()
        self._init_music()
        self._init_state_variables()

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager

    def _init_gameplay_elements(self):

        self.ticket_ids_list = SqliteQueries(self.cursor).ticket_ids_query()
        self.total_tickets = len(self.ticket_ids_list)
        self.threat_list = SqliteQueries(self.cursor).threat_list_query()
        self.threat_id_name_list = SqliteQueries(self.cursor).threat_id_name_query()
        self.threat_id_name_map = {threat[1]: threat[0] for threat in self.threat_id_name_list}

        self.randomized_ticket_interval = random.uniform(constants.MIN_CALL_INTERVAL, constants.MAX_CALL_INTERVAL)


    def _init_ui_elements(self):
        
        self.back_button = main_loop_elements.back_button_func(self.manager)
        self.title_label = main_loop_elements.title_image_func(self.manager, constants.TITLE_IMAGE_PATH)

        self.main_sla_timer_label = main_loop_elements.main_sla_timer_label_func(self.manager)
        self.caller_profile_tbox = main_loop_elements.caller_profile_tbox_func(self.manager)

        self.submit_button = main_loop_elements.submit_button_func(self.manager)
        self.threat_entry_title_box = main_loop_elements.threat_entry_title_tbox_func(self.manager)
        self.threat_entry_slist = main_loop_elements.threat_entry_slist_func(self.manager, self.threat_list)

        self.threat_panel, self.threat_title_tbox, \
            self.threat_image, self.threat_description_tbox = main_loop_elements.threat_panel_func(self.manager)
        
        self.ticket_title_tbox = main_loop_elements.ticket_title_tbox_func(self.manager)
        self.ticket_entry_tbox = main_loop_elements.ticket_entry_tbox_func(self.manager)

    
    def _init_music(self):
        self.button_sound_manager = sound_manager.ButtonSoundManager()
        self.incoming_call_manager = sound_manager.LoopingSoundManager(constants.INCOMING_CALL_MUSIC_PATH, constants.INCOMMING_CALL_CHANNEL)
        self.background_music_manager = sound_manager.BackgroundMusicManager(constants.BACKGROUND_MUSIC_PATH)


    def _init_state_variables(self):

        self.ticket_timer = 0
        self.popup_window_close_timer = 0
        self.popup_window_sla_countdown = 15    
        self.main_sla_timer = 0
        self.main_sla_countdown = 180

        self.ticket_presence = False
        self.caller_popup_window = None
        self.caller_profile_image = None
        self.popup_button_accepted = False
        self.ticket_transcript = None

        self.selected_threat = None
        self.answer = None
        self.accept_button = None

        self.total_score = 0
        self.missed_calls = 0
        self.missed_tickets = 0
        self.current_ticket_id_index = 0


    def shift_loop(self):

        self.background_music_manager.load_music()
        self.background_music_manager.play_music()

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            self.ticket_timer += self.time_delta

            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.time_delta)


    def _handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.threat_entry_slist:
                self.selected_threat = event.text
                self._handle_threat_selection(self.selected_threat)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event, self.selected_threat, self.answer)

            self.manager.process_events(event)

        if self.ticket_timer >= self.randomized_ticket_interval and not self.ticket_presence and self.caller_popup_window is None:
            self._display_caller_popup_window()
        
        if not self.ticket_ids_list and not self.ticket_presence:
            self._shift_report()

        else:

            if self.caller_popup_window:
                self._caller_popup_window_countdown()

            else:
                self.manager.draw_ui(self.pygame_renderer.window_surface)

            if self.ticket_presence and self.caller_popup_window is None:
                self._ticket_sla_counter()

            self._difficulty_update_logic()


    def _handle_threat_selection(self, selected_threat):

        self.button_sound_manager.play_sfx('list_button')

        description, indicators, countermeasures, image_file = SqliteQueries(self.cursor).threat_selection_query(selected_threat)

        image_path = f'assets/images/threats/{image_file}'
        self.threat_title_tbox.set_text(f'<b>{selected_threat.upper()}</b>')

        try: 
            threat_image_load = pygame.image.load(image_path)
        except:
            threat_image_load = pygame.image.load(constants.DEFAULT_THREAT_IMAGE_PATH)

        self.threat_image.set_image(new_image=threat_image_load)
        self.threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')


    def _handle_button_pressed(self, event, selected_threat, answer):

        if event.ui_element == self.back_button:

            self.button_sound_manager.play_sfx(constants.BACK_BUTTON_SFX)
            self.ticket_transcript.stop_transcript() if self.ticket_transcript else None
            self.background_music_manager.stop_music()

            pygame.mixer.music.unload()
            self.running = False

        if event.ui_element == self.submit_button and self.ticket_presence and selected_threat is not None:

            self._reset_ticket_ui()
            selected_threat_id = self.threat_id_name_map[self.selected_threat]
            if selected_threat_id == answer:
                self.button_sound_manager.play_sfx('correct_submit')
                self.total_score += 1

            else:
                self.button_sound_manager.play_sfx('incorrect_submit')

            self.ticket_transcript.stop_transcript()
            pygame.mixer.music.unload()

            self.background_music_manager.load_music()
            self.background_music_manager.play_music()


        if self.accept_button and event.ui_element == self.accept_button:
            self._generate_ticket()
        

    def _display_caller_popup_window(self):

        self.background_music_manager.stop_music()
        pygame.mixer.music.unload()

        self.caller_popup_window, self.accept_button, self.popup_window_countdown = main_loop_elements.caller_popup_window_func(self.manager)
        self.popup_window_close_timer = 0

        self.incoming_call_manager.play_loop()
        self.incoming_call_manager.adjust_loop_volume(0.3)

    
    def _caller_popup_window_countdown(self):

        self.caller_popup_window.show()
        self.manager.draw_ui(self.pygame_renderer.window_surface)

        popup_window_sla_countdown_difference = self.popup_window_sla_countdown - self.popup_window_close_timer
        self.popup_window_countdown.set_text("SLA: {:.1f}".format(max(0, popup_window_sla_countdown_difference)))
        self.popup_window_close_timer += self.time_delta

        if popup_window_sla_countdown_difference <= 0:

            self.caller_popup_window.hide()
            self.caller_popup_window = None

            self.selected_id = self.ticket_ids_list[0]
            print(self.selected_id)
            self.ticket_ids_list.remove(self.selected_id)

            self.ticket_timer = 0
            self.missed_calls += 1

            self.incoming_call_manager.stop_loop()


    def _generate_ticket(self):

        self.incoming_call_manager.stop_loop()
        self.main_sla_timer = 0
        self.selected_threat = None

        self.selected_id = self.ticket_ids_list[0]
        print(self.selected_id)
        title, current_ticket, threat_id, caller_name, caller_org, caller_email, caller_contact, caller_picture_file = SqliteQueries(self.cursor).ticket_query(self.selected_id)
        self.answer = threat_id
        caller_picture = f'assets/images/accounts/{caller_picture_file}'

        ticket_title_text = f'<b>ID#{self.selected_id} | {title}</b>'
        self.ticket_title_tbox.set_text(ticket_title_text)

        self.ticket_entry_tbox.set_text(current_ticket)
        self.caller_profile_image = main_loop_elements.caller_profile_image_func(self.manager, caller_picture)

        caller_profile_text = f'Name: {caller_name}\nOrganization: {caller_org}\nEmail: {caller_email}\nContact: {caller_contact}'
        self.caller_profile_tbox.set_text(caller_profile_text)

        self.ticket_presence = True
        self.ticket_ids_list.remove(self.selected_id)

        self.caller_popup_window.hide()
        self.caller_popup_window = None

        ticket_transcript_path = SqliteQueries(self.cursor).ticket_transcript_query(self.selected_id)
       
        self.ticket_transcript = sound_manager.TicketTranscriptManager(ticket_transcript_path)
        self.ticket_transcript.load_transcript()
        self.ticket_transcript.play_transcript()

        return self.answer


    def _difficulty_update_logic(self):
   
        mid_difficulty_marker = self.total_tickets / 2
        final_difficulty_marker = mid_difficulty_marker / 2

        if len(self.ticket_ids_list) <= final_difficulty_marker:
            self.main_sla_countdown = 60

        elif len(self.ticket_ids_list) <= mid_difficulty_marker:
            self.main_sla_countdown = 120


    def _ticket_sla_counter(self):

        main_sla_countdown_difference = self.main_sla_countdown - self.main_sla_timer
        self.main_sla_timer_label.set_text("SLA: {:.1f}".format(max(0, main_sla_countdown_difference)))

        self.main_sla_timer += self.time_delta

        if main_sla_countdown_difference <= 0:
            self._reset_ticket_ui()
            self.missed_tickets += 1


    def _shift_report(self):

        self.background_music_manager.stop_music()

        run_shift_report = ShiftReport(self.total_score, self.total_tickets, self.missed_calls, self.missed_tickets)
        
        run_shift_report.shift_report()
        self.running = False


    def _reset_ticket_ui(self):

        self.randomized_ticket_interval = random.uniform(constants.MIN_CALL_INTERVAL, constants.MAX_CALL_INTERVAL)

        self.ticket_title_tbox.set_text("")
        self.ticket_entry_tbox.set_text("AWAITING TICKET...")

        self.caller_profile_image.kill()
        self.caller_profile_tbox.set_text("NO CALLER")

        self.ticket_presence = False
        self.ticket_timer = 0

        self.main_sla_timer_label.set_text("SLA: ")



class ShiftReport:

    def __init__ (self, total_score, total_tickets, missed_calls, missed_tickets):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager

        self.missed_calls = missed_calls
        self.missed_tickets = missed_tickets

        self.total_score = total_score
        self.total_tickets = total_tickets

        self._assessment_calculation()
        self._init_ui_elements()

    def _assessment_calculation(self):

        self.assessment_percentage = (self.total_score / self.total_tickets) * 100
        
        if self.assessment_percentage >= 80:
            self.assessment_result = "PASS"

        else:
            self.assessment_result = "FAIL"

    def _init_ui_elements(self):

        self.manager.clear_and_reset()

        main_loop_elements.shift_report_tbox_func(self.manager, self.total_score, self.total_tickets, 
                                            self.missed_calls, self.missed_tickets, self.assessment_result)
        
        main_loop_elements.end_shift_title_label_func(self.manager)

        self.end_shift_button = main_loop_elements.end_shift_button_func(self.manager)


    def shift_report(self):

        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.end_shift_button:
                        running = False

                self.manager.process_events(event)

            self.pygame_renderer.ui_renderer(time_delta)