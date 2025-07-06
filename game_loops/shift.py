import random

import pygame
import pygame_gui

import init
import elements.main_loop_elements as main_loop_elements
from queries import ticket_ids,threats



def shift_introduction(connect, cursor):

    window_surface, clock, background = init.pygame_init()
    manager = init.pygame_gui_init()

    back_button = main_loop_elements.back_button_func(manager)

    introduction_text = """
        The cyberspace has neve been this dangerous. As an L1 SOC Analyst at Meeps Security, you must correctly
        access 80% of the tickets to protect our clients.
    """
    main_loop_elements.introduction_tbox_func(manager, introduction_text)

    continue_button = main_loop_elements.continue_button_func(manager)

    running = True
    while running:

        time_delta = clock.tick(60) / 1000.0

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

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


class ShiftLoop:

    def __init__ (self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self.window_surface, self.clock, self.background = init.pygame_init()
        self.manager = init.pygame_gui_init()

        self.ticket_ids_list = ticket_ids(self.cursor)
        self.total_tickets = len(self.ticket_ids_list)
        threat_list = threats(self.cursor)

        self.ticket_timer = 0
        self.randomized_ticket_entry = random.uniform(5, 12)
        self.popup_window_close_timer = 0
        self.popup_window_sla_countdown = 15

        self.main_sla_timer = 0
        self.main_sla_countdown = 180

        self.mid_difficulty_marker = self.total_tickets / 2
        self.final_difficulty_marker = self.mid_difficulty_marker / 2

        self.ticket_presence = False
        self.caller_popup_window = None
        self.popup_button_accepted = False
        self.ticket_transcript_channel = None

        self.total_score = 0
        self.missed_calls = 0
        self.missed_tickets = 0
        self.current_ticket_id_index = 0

        title_image_path = 'assets/images/general/title.png'
        self.back_button = main_loop_elements.back_button_func(self.manager)
        self.title_label = main_loop_elements.title_image_func(self.manager, title_image_path)

        self.main_sla_timer_label = main_loop_elements.main_sla_timer_label_func(self.manager)
        self.caller_profile_tbox = main_loop_elements.caller_profile_tbox_func(self.manager)

        self.submit_button = main_loop_elements.submit_button_func(self.manager)
        self.threat_entry_title_box = main_loop_elements.threat_entry_title_tbox_func(self.manager)
        self.threat_entry_slist = main_loop_elements.threat_entry_slist_func(self.manager, threat_list)

        self.threat_panel, self.threat_title_tbox, self.threat_image, self.threat_description_tbox = main_loop_elements.threat_panel_func(self.manager)
        self.ticket_title_tbox = main_loop_elements.ticket_title_tbox_func(self.manager)
        self.ticket_entry_tbox = main_loop_elements.ticket_entry_tbox_func(self.manager)


        self.incoming_call_music_path = 'assets/sounds/incoming_call_2.mp3'
        pygame.mixer.music.load(self.incoming_call_music_path)
        self.incoming_call_channel = pygame.mixer.Channel(0)

        self.background_music_path = 'assets/sounds/background2.mp3'
        pygame.mixer.music.load(self.background_music_path)
        self.background_music_channel = pygame.mixer.Channel(1)

        self.list_click_music_path = 'assets/sounds/list_click2.mp3'
        pygame.mixer.music.load(self.list_click_music_path)
        self.list_click_music_channel = pygame.mixer.Channel(2)

        self.incorrect_submit_music_path = 'assets/sounds/incorrect_submit.mp3'
        pygame.mixer.music.load(self.incorrect_submit_music_path)
        self.incorrect_submit_music_channel = pygame.mixer.Channel(3)

        self.correct_submit_music_path = 'assets/sounds/correct_submit.mp3'
        pygame.mixer.music.load(self.correct_submit_music_path)
        self.correct_submit_music_channel = pygame.mixer.Channel(4)

        self.back_button_music_path = 'assets/sounds/back_button.mp3'
        pygame.mixer.music.load(self.back_button_music_path)
        self.back_button_music_channel = pygame.mixer.Channel(5)
        self.back_button_music_channel.set_volume(0.2)


    def shift_loop(self):

        self.background_music_channel.play(pygame.mixer.Sound(self.background_music_path), loops=-1)

        running = True
        while running:

            time_delta = self.clock.tick(60) / 1000.0
            self.ticket_timer += time_delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == self.threat_entry_slist:

                        selected_threat = event.text
                        print(selected_threat)

                        self.list_click_music_channel.play(pygame.mixer.Sound(self.list_click_music_path))

                        self.cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
                        description, indicators, countermeasures, image_file = self.cursor.fetchone()
                        image_path = f'assets/images/threats/{image_file}'
                        self.threat_title_tbox.set_text(f'<b>{selected_threat.upper()}</b>')

                        try:
                            threat_image_load = pygame.image.load(image_path)
                            self.threat_image.set_image(new_image=threat_image_load)
                            self.threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')

                        except:
                            default_image_path = 'assets/images/threats/default.png'
                            threat_image_load = pygame.image.load(default_image_path)
                            self.threat_image.set_image(new_image=threat_image_load)
                            self.threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')

                if event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == self.back_button:
                        self.back_button_music_channel.play(pygame.mixer.Sound(self.back_button_music_path))
                        self.back_button_music_channel.stop()

                        if self.ticket_transcript_channel:
                            self.ticket_transcript_channel.stop()
                        
                        pygame.mixer.music.unload()
                        
                        running = False

                    if event.ui_element == self.submit_button and self.ticket_presence and selected_threat is not None:

                        self.ticket_title_tbox.set_text("")
                        self.ticket_entry_tbox.set_text("AWAITING TICKET...")
                        
                        caller_profile_image.kill()
                        self.caller_profile_tbox.set_text("NO CALLER")

                        self.ticket_presence = False
                        self.ticket_timer = 0

                        self.main_sla_timer_label.set_text("SLA: ")

                        if selected_threat == answer:
                            self.correct_submit_music_channel.play(pygame.mixer.Sound(self.correct_submit_music_path))
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Correct")
                            self.total_score += 1

                        else:
                            self.incorrect_submit_music_channel.play(pygame.mixer.Sound(self.incorrect_submit_music_path))
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Wrong")

                        self.ticket_transcript_channel.stop()
                        pygame.mixer.music.unload()

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))


            if self.ticket_timer >= self.randomized_ticket_entry and not self.ticket_presence and self.caller_popup_window is None:

                self.caller_popup_window, accept_button, popup_window_countdown = main_loop_elements.caller_popup_window_func(self.manager)
                self.popup_window_close_timer = 0

                self.incoming_call_channel.play(pygame.mixer.Sound(self.incoming_call_music_path))
                self.incoming_call_channel.set_volume(0.3) 
            
            if not self.ticket_ids_list and not self.ticket_presence:

                self.background_music_channel.stop()

                run_shift_report = ShiftReport(self.window_surface, self.clock, self.background,
                                               self.total_score, self.total_tickets, self.missed_calls,
                                               self.missed_tickets)
                
                run_shift_report.shift_report()              
                running = False

            else:

                if self.caller_popup_window:

                    self.caller_popup_window.show()
                    self.manager.draw_ui(self.window_surface)

                    popup_window_sla_countdown_difference = self.popup_window_sla_countdown - self.popup_window_close_timer
                    popup_window_countdown.set_text("SLA: {:.1f}".format(max(0, popup_window_sla_countdown_difference)))
                    self.popup_window_close_timer += time_delta

                    if popup_window_sla_countdown_difference <= 0:
                        
                        self.caller_popup_window.hide()
                        self.caller_popup_window = None
                        
                        selected_id = random.choice(self.ticket_ids_list)
                        self.ticket_ids_list.remove(selected_id)

                        self.ticket_timer = 0
                        self.missed_calls += 1

                        self.incoming_call_channel.stop()

                    for event in pygame.event.get():

                        if event.type == pygame_gui.UI_BUTTON_PRESSED:

                            if event.ui_element == accept_button:

                                self.incoming_call_channel.stop()
                                self.main_sla_timer = 0

                                selected_id = self.ticket_ids_list[0]
                                self.cursor.execute('SELECT t.title, t.entry, t.answer, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?',
                                                [selected_id])
                                
                                title, current_ticket, answer, caller_name, caller_org, caller_email, caller_contact, caller_picture_file = self.cursor.fetchone()
                                caller_picture = f'assets/images/accounts/{caller_picture_file}'

                                selected_threat = None

                                ticket_title_text = f'<b>ID#{selected_id} | {title}</b>'
                                self.ticket_title_tbox.set_text(ticket_title_text)

                                self.ticket_entry_tbox.set_text(current_ticket)
                                caller_profile_image = main_loop_elements.caller_profile_image_func(self.manager, caller_picture)

                                caller_profile_text = f'Name: {caller_name}\nOrganization: {caller_org}\nEmail: {caller_email}\nContact: {caller_contact}'
                                self.caller_profile_tbox.set_text(caller_profile_text)

                                self.ticket_presence = True
                                self.ticket_ids_list.remove(selected_id)

                                self.caller_popup_window.hide()
                                self.caller_popup_window = None

                                self.cursor.execute('SELECT transcript_path FROM tickets WHERE id=?', [selected_id])
                                ticket_transcript_path = self.cursor.fetchone()[0]
                                pygame.mixer.music.load(ticket_transcript_path)

                                self.ticket_transcript_channel = pygame.mixer.Channel(6)
                                self.ticket_transcript_channel.play(pygame.mixer.Sound(ticket_transcript_path))

                        self.manager.process_events(event)

                else:
                    self.manager.draw_ui(self.window_surface)

                if len(self.ticket_ids_list) <= self.final_difficulty_marker:
                    self.main_sla_countdown = 60

                elif len(self.ticket_ids_list) <= self.mid_difficulty_marker:
                    self.main_sla_countdown = 120

                if self.ticket_presence and self.caller_popup_window is None:

                    main_sla_countdown_difference = self.main_sla_countdown - self.main_sla_timer
                    self.main_sla_timer_label.set_text("SLA: {:.1f}".format(max(0, main_sla_countdown_difference)))

                    self.main_sla_timer += time_delta

                    if main_sla_countdown_difference <= 0:

                        self.ticket_title_tbox.set_text("")
                        self.ticket_entry_tbox("AWAITING TICKET...")

                        caller_profile_image.kill()
                        self.caller_profile_tbox.set_text("NO CALLER")

                        self.ticket_presence = False
                        self.ticket_timer = 0
                        self.missed_tickets += 1

                        self.main_sla_timer_label.set_text("SLA: ")

                self.manager.draw_ui(self.window_surface)
                pygame.display.update()



class ShiftReport:

    def __init__ (self, window_surface, clock, background, manager,
                  total_score, total_tickets, missed_calls, missed_tickets):
        
        self.window_surface = window_surface
        self.clock = clock
        self.background = background
        self.manager = manager

        self.missed_calls = missed_calls
        self.missed_tickets = missed_tickets

        self.total_score = total_score
        self.total_tickets = total_tickets

        self.assessment_percentage = (self.total_score / self.total_tickets) * 100
        
        if self.assessment_percentage >= 80:
            assessment_result = "PASS"

        else:
            assessment_result = "FAIL"

        main_loop_elements.shift_report_tbox_func(self.manager, self.total_score, self.total_tickets, 
                                            self.missed_calls, self.missed_tickets, assessment_result)
        
        main_loop_elements.end_shift_button_func(self.manager)
        self.end_shift_button = main_loop_elements.end_shift_button_func(self.manager)


    def shift_report(self):

        running = True
        while running:

            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.end_shift_button:
                        running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            
            pygame.display.update()