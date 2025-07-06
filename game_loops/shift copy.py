import pygame
import pygame_gui
import random
import init
import elements.main_loop_elements as main_loop_elements
from queries import ticket_ids, threats


def shift_introduction(connect, cursor):

    window_surface, clock, background = init.pygame_init()
    manager = init.pygame_gui_init()

    back_button = main_loop_elements.back_button_func(manager)

    introduction_text = "The cyberspace has never been this dangerous. As an L1 SOC Analyst at MEEPS SECURITY, you must successfully assess 80% of the tickets to protect the clients."
    introduction_tbox = main_loop_elements.introduction_tbox_func(manager, introduction_text)

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
                    start_shift(connect, cursor)
                    return

            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()




def start_shift(connect, cursor):

    
    def music_init():

        incoming_call_music_path = "assets/sounds/incoming_call_2.mp3"
        pygame.mixer.music.load(incoming_call_music_path)
        incoming_call_channel = pygame.mixer.Channel(0)

        background_music_path = "assets/sounds/background2.mp3"
        pygame.mixer.music.load(background_music_path)
        background_music_channel = pygame.mixer.Channel(1)

        list_click_music_path = "assets/sounds/list_click2.mp3"
        pygame.mixer.music.load(list_click_music_path)
        list_click_music_channel = pygame.mixer.Channel(2)

        incorrect_submit_music_path = "assets/sounds/incorrect_submit.mp3"
        pygame.mixer.music.load(incorrect_submit_music_path)
        incorrect_submit_music_channel = pygame.mixer.Channel(3)

        correct_submit_music_path = "assets/sounds/correct_submit.mp3"
        pygame.mixer.music.load(correct_submit_music_path)
        correct_submit_music_channel = pygame.mixer.Channel(4)

        return incoming_call_music_path, incoming_call_channel, background_music_path, background_music_channel, \
            list_click_music_path, list_click_music_channel, incorrect_submit_music_path, incorrect_submit_music_channel, \
            correct_submit_music_path, correct_submit_music_channel
    
    
    def start_shift_init(connect, cursor):

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        ticket_ids_list = ticket_ids(cursor)
        total_tickets = len(ticket_ids_list)
        threat_list = threats(cursor)

        ticket_timer = 0
        randomized_ticket_entry = random.uniform(5, 12)
        popup_window_close_timer = 0
        popup_window_sla_countdown = 15
        
        main_sla_timer = 0
        main_sla_countdown = 180

        mid_difficulty_marker = total_tickets / 2
        final_difficulty_marker = mid_difficulty_marker / 2

        ticket_presence = False
        caller_popup_window = None
        popup_button_accepted = False

        total_score = 0
        missed_calls = 0
        missed_tickets = 0
        current_ticket_id_index = 0
        
        title_image_path = "assets/images/general/title.png"
        
        back_button = main_loop_elements.back_button_func(manager)
        title_label = main_loop_elements.title_image_func(manager, title_image_path)

        main_sla_timer_label = main_loop_elements.main_sla_timer_label_func(manager)
        caller_profile_tbox = main_loop_elements.caller_profile_tbox_func(manager)

        submit_button = main_loop_elements.submit_button_func(manager)
        threat_entry_title_tbox = main_loop_elements.threat_entry_title_tbox_func(manager)
        threat_entry_slist = main_loop_elements.threat_entry_slist_func(manager, threat_list)
    
        threat_panel, threat_title_tbox, threat_image, threat_description_tbox = main_loop_elements.threat_panel_func(manager)
        ticket_title_tbox = main_loop_elements.ticket_title_tbox_func(manager)
        ticket_entry_tbox = main_loop_elements.ticket_entry_tbox_func(manager)


        return start_shift_loop(connect, cursor, window_surface, clock, background, manager,
                               ticket_ids_list, total_tickets, threat_list, ticket_timer, 
                               randomized_ticket_entry, popup_window_close_timer, popup_window_sla_countdown,
                               main_sla_timer, main_sla_countdown, mid_difficulty_marker, final_difficulty_marker,
                               ticket_presence, caller_popup_window, popup_button_accepted,
                               total_score, missed_calls, missed_tickets, current_ticket_id_index, 
                               back_button, title_label, main_sla_timer_label, caller_profile_tbox, 
                               submit_button, threat_entry_title_tbox, threat_entry_slist,
                               threat_panel, threat_title_tbox, threat_image, threat_description_tbox,
                               ticket_title_tbox, ticket_entry_tbox)
    

    def start_shift_loop(connect, cursor, window_surface, clock, background, manager, 
                        ticket_ids_list, total_tickets, threat_list, ticket_timer, 
                        randomized_ticket_entry, popup_window_close_timer, popup_window_sla_countdown, 
                        main_sla_timer, main_sla_countdown, mid_difficulty_marker, final_difficulty_marker,
                        ticket_presence, caller_popup_window, popup_button_accepted, 
                        total_score, missed_calls, missed_tickets, current_ticket_id_index,  
                        back_button, title_label, main_sla_timer_label, caller_profile_tbox, 
                        submit_button, threat_entry_title_tbox, threat_entry_slist, 
                        threat_panel, threat_title_tbox, threat_image, threat_description_tbox, 
                        ticket_title_tbox, ticket_entry_tbox):
        
        incoming_call_music_path, incoming_call_channel, background_music_path, background_music_channel, \
            list_click_music_path, list_click_music_channel, incorrect_submit_music_path, incorrect_submit_music_channel, \
                correct_submit_music_path, correct_submit_music_channel = music_init()

        ticket_transcript_channel = None
        background_music_channel.play(pygame.mixer.Sound(background_music_path), loops=-1)

        back_button_music_path = "assets/sounds/back_button.mp3"
        pygame.mixer.music.load(back_button_music_path)
        back_button_music_channel = pygame.mixer.Channel(4)
        back_button_music_channel.set_volume(0.2)
        
        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0
            ticket_timer += time_delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == threat_entry_slist:

                        selected_threat = event.text
                        print(selected_threat)

                        list_click_music_channel.play(pygame.mixer.Sound(list_click_music_path))

                        cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
                        description, indicators, countermeasures, image_file = cursor.fetchone()
                        image_path = f"assets/images/threats/{image_file}"
                        threat_title_tbox.set_text(f'<b>{selected_threat.upper()}</b>')
                        
                        try:
                            threat_image_load = pygame.image.load(image_path)
                            threat_image.set_image(new_image=threat_image_load)
                            threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')
                        except:
                            threat_image_load = pygame.image.load("assets/images/threats/default.png")
                            threat_image.set_image(new_image=threat_image_load)
                            threat_description_tbox.set_text(f'<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')

                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == back_button:
                        back_button_music_channel.play(pygame.mixer.Sound(back_button_music_path))
                        background_music_channel.stop()
                        if ticket_transcript_channel:
                            ticket_transcript_channel.stop()
                        pygame.mixer.music.unload()
                        running = False
                    
                    if event.ui_element == submit_button and ticket_presence and selected_threat is not None:

                        ticket_title_tbox.set_text("")
                        ticket_entry_tbox.set_text("AWAITING TICKET...")
                        caller_profile_image.kill()
                        caller_profile_tbox.set_text("NO CALLER")
                        ticket_presence = False
                        ticket_timer = 0

                        main_sla_timer_label.set_text("SLA: ")

                        if selected_threat == answer:
                            correct_submit_music_channel.play(pygame.mixer.Sound(correct_submit_music_path))
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Correct")
                            total_score += 1
                        else:
                            incorrect_submit_music_channel.play(pygame.mixer.Sound(incorrect_submit_music_path))
                            print(f"Selected: {selected_threat}, Correct: {answer}, Answer: Wrong")

                        #background_music_channel.unpause()
                        ticket_transcript_channel.stop()
                        pygame.mixer.music.unload()
                        
                manager.process_events(event)
            
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))

            if ticket_timer >= randomized_ticket_entry and not ticket_presence and caller_popup_window is None:

                caller_popup_window, accept_button, popup_window_countdown = main_loop_elements.caller_popup_window_func(manager)
                popup_window_close_timer = 0

                #background_music_channel.pause()
                incoming_call_channel.set_volume(0.3)
                incoming_call_channel.play(pygame.mixer.Sound(incoming_call_music_path), loops=-1)
                

            if not ticket_ids_list and not ticket_presence:

                background_music_channel.stop()
                shift_report_init(window_surface, clock, background, manager,
                             total_score, total_tickets, missed_calls, missed_tickets)
                running = False
            
            else:

                if caller_popup_window:
                    caller_popup_window.show()
                    manager.draw_ui(window_surface)
                    popup_window_sla_countdown_difference = popup_window_sla_countdown - popup_window_close_timer

                    popup_window_countdown.set_text("SLA: {:.1f}".format(max(0, popup_window_sla_countdown_difference)))
                    popup_window_close_timer += time_delta

                    if popup_window_sla_countdown_difference <= 0:
                        caller_popup_window.hide()
                        caller_popup_window = None
                        selected_id = random.choice(ticket_ids_list)
                        ticket_ids_list.remove(selected_id)
                        ticket_timer = 0
                        missed_calls += 1

                        incoming_call_channel.stop()
                        #background_music_channel.unpause()

                    for event in pygame.event.get():
                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == accept_button:

                                incoming_call_channel.stop()

                                main_sla_timer = 0

                                selected_id = ticket_ids_list[0]
                                cursor.execute('SELECT t.title, t.entry, t.answer, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?',
                                               [selected_id])
                                title, current_ticket, answer, caller_name, caller_org, caller_email, caller_contact, caller_picture_file = cursor.fetchone()
                                caller_picture = f"assets/images/accounts/{caller_picture_file}"
                                selected_threat = None

                                ticket_title_text = f"<b>ID#{selected_id} | {title}</b>"
                                ticket_title_tbox.set_text(ticket_title_text)

                                ticket_entry_tbox.set_text(current_ticket)
                                caller_profile_image = main_loop_elements.caller_profile_image_func(manager, caller_picture)

                                caller_profile_text = f"Name: {caller_name}\nOrganization: {caller_org}\nEmail: {caller_email}\nContact: {caller_contact}"
                                caller_profile_tbox.set_text(caller_profile_text)
                                
                                ticket_presence = True
                                ticket_ids_list.remove(selected_id)

                                caller_popup_window.hide()
                                caller_popup_window = None

                                        
                                cursor.execute('SELECT transcript_path FROM tickets WHERE id=?', [selected_id])
                                ticket_transcript_path = cursor.fetchone()[0]
                                pygame.mixer.music.load(ticket_transcript_path)
                                ticket_transcript_channel = pygame.mixer.Channel(5)
                                ticket_transcript_channel.play(pygame.mixer.Sound(ticket_transcript_path))
                        
                        manager.process_events(event)

                else:
                    manager.draw_ui(window_surface)

                if len(ticket_ids_list) <= final_difficulty_marker:
                    main_sla_countdown = 60
                elif len(ticket_ids_list) <= mid_difficulty_marker:
                    main_sla_countdown = 120

                if ticket_presence and caller_popup_window is None:

                    main_sla_countdown_difference = main_sla_countdown - main_sla_timer
                    main_sla_timer_label.set_text("SLA: {:.1f}".format(max(0, main_sla_countdown_difference)))

                    main_sla_timer += time_delta

                    if main_sla_countdown_difference <= 0:
                        
                        ticket_title_tbox.set_text("")
                        ticket_entry_tbox.set_text("AWAITING TICKET...")
                        caller_profile_image.kill()
                        caller_profile_tbox.set_text("NO CALLER")
                        ticket_presence = False
                        ticket_timer = 0
                        missed_tickets += 1

                        main_sla_timer_label.set_text("SLA: ")

            manager.draw_ui(window_surface)
            pygame.display.update()


    def shift_report_init(window_surface, clock, background, manager, 
                          total_score, total_tickets, missed_calls, missed_tickets):
        
        assessment_percentage = (total_score / total_tickets) * 100
        if assessment_percentage >= 80:
            assessment_result = "PASS"
        else:
            assessment_result = "FAIL"
        
        manager.clear_and_reset()
        shift_report_tbox = main_loop_elements.shift_report_tbox_func(manager, total_score, total_tickets, 
                                                                      missed_calls, missed_tickets, 
                                                                      assessment_result)
        end_shift_title_label = main_loop_elements.end_shift_title_label_func(manager)
        end_shift_button = main_loop_elements.end_shift_button_func(manager)

        return shift_report(window_surface, clock, background, manager, 
                            shift_report_tbox, end_shift_title_label, end_shift_button, 
                            assessment_result)

    
    def shift_report(window_surface, clock, background, manager, 
                     shift_report_tbox, end_shift_title_label, end_shift_button, 
                     assessment_result):
        
        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == end_shift_button:
                        running = False

                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    start_shift_init(connect, cursor)