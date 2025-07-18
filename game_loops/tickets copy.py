import pygame
import pygame_gui
import pyttsx3
import init
import queries
import elements.ticket_elements as ticket_elements


def ticket_transcript_generator(id, ticket):

    
    engine = pyttsx3.init()
    filename = f"assets/sounds/{id}_transcript.wav"
    ticket_transcript_path = engine.save_to_file(ticket, filename)
    engine.runAndWait()

    return filename



def ticket_management_init_values():

    selected_threat = None
    ticket_title = None
    ticket_entry = None
    ticket_confirm_window = None

    return selected_threat, ticket_title, ticket_entry, ticket_confirm_window


def ticket_management(connect, cursor):

    
    def music_init():

        menu_button_music_path = "assets/sounds/list_click2.mp3"
        pygame.mixer.music.load(menu_button_music_path)
        menu_button_music_channel = pygame.mixer.Channel(0)

        delete_button_music_path = "assets/sounds/delete_button.mp3"
        pygame.mixer.music.load(delete_button_music_path)
        delete_button_music_channel = pygame.mixer.Channel(1)

        add_button_music_path = "assets/sounds/add_button.mp3"
        pygame.mixer.music.load(add_button_music_path)
        add_button_music_channel = pygame.mixer.Channel(2)

        return menu_button_music_path, menu_button_music_channel, delete_button_music_path, delete_button_music_channel, add_button_music_path, add_button_music_channel
    
    
    def ticket_management_init(connect, cursor):

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        id_list, ticket_list = queries.tickets(cursor)

        back_button = ticket_elements.back_button_func(manager)
        ticket_manager_image = ticket_elements.ticket_manager_image_func(manager, "assets/images/general/ticket_mngr.png")
        ticket_information_label = ticket_elements.ticket_information_label_func(manager)

        create_button = ticket_elements.create_ticket_button_func(manager)
        delete_button = ticket_elements.delete_ticket_button_func(manager)
        ticket_entry_title_tbox = ticket_elements.ticket_entry_slist_misc_func(manager)
        ticket_entry_slist = ticket_elements.ticket_entry_slist_func(manager, ticket_list)
        selected_ticket_title_tbox, selected_ticket_description_tbox = ticket_elements.selected_ticket_tbox_func(manager)
        
        account_details_label = ticket_elements.account_details_label_func(manager)
        selected_ticket_account_tbox = ticket_elements.selected_ticket_account_func(manager)

        selected_ticket_id = None
        selected_threat, ticket_title, ticket_entry, ticket_confirm_window = ticket_management_init_values()
        

        return ticket_management_loop(connect, cursor, window_surface, clock, background, manager,
                                id_list, ticket_list, back_button, ticket_manager_image, 
                                ticket_information_label, create_button, delete_button, 
                                ticket_entry_title_tbox, ticket_entry_slist, 
                                selected_ticket_title_tbox, selected_ticket_description_tbox, 
                                account_details_label, selected_ticket_account_tbox, selected_threat, 
                                ticket_title, ticket_entry, ticket_confirm_window, 
                                selected_ticket_id)


    def ticket_management_loop(connect, cursor, window_surface, clock, background, manager,
                                id_list, ticket_list, back_button, ticket_manager_image, 
                                ticket_information_label, create_button, delete_button, 
                                ticket_entry_title_tbox, ticket_entry_slist, 
                                selected_ticket_title_tbox, selected_ticket_description_tbox, 
                                account_details_label, selected_ticket_account_tbox, selected_threat, 
                                ticket_title, ticket_entry, ticket_confirm_window, 
                                selected_ticket_id):
        
        menu_button_music_path, menu_button_music_channel, delete_button_music_path, delete_button_music_channel, add_button_music_path, add_button_music_channel = music_init()

        back_button_music_path = "assets/sounds/back_button.mp3"
        pygame.mixer.music.load(back_button_music_path)
        back_button_music_channel = pygame.mixer.Channel(4)
        back_button_music_channel.set_volume(0.2)
        
        
        running = True
        while running:
            
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        back_button_music_channel.play(pygame.mixer.Sound(back_button_music_path))
                        pygame.mixer.music.unload()
                        running = False
                    
                    if event.ui_element == create_button:
                        
                        add_button_music_channel.play(pygame.mixer.Sound(add_button_music_path))
                        
                        id_list, ticket_list = ticket_creation_init(connect, cursor)
                        ticket_entry_slist.kill()
                        ticket_entry_slist = ticket_elements.ticket_entry_slist_func(manager, ticket_list)

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == ticket_entry_slist:

                        menu_button_music_channel.play(pygame.mixer.Sound(menu_button_music_path))
                        selected_ticket = event.text
                        
                        id_index_find = ticket_list.index(selected_ticket)
                        selected_ticket_id = id_list[id_index_find]
                        
                        cursor.execute('SELECT t.title, t.entry, a.name, a.organization, a.email, a.contact FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?', [selected_ticket_id])
                        title, entry, name, organization, email, contact = cursor.fetchone()
                        selected_ticket_title_tbox.set_text(f"<b>{title}</b>")
                        selected_ticket_description_tbox.set_text(f"{entry}")
                        selected_ticket_account_tbox.set_text(f"<b>Name:</b> {name}\n<b>Organization:</b> {organization}\n<b>Email:</b> {email}\n<b>Contact:</b> {contact}")

                if selected_ticket_id is not None:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == delete_button:
                            
                            delete_button_music_channel.play(pygame.mixer.Sound(delete_button_music_path))

                            cursor.execute('DELETE FROM tickets WHERE id=?', [selected_ticket_id])
                            connect.commit()

                            id_list, ticket_list = queries.tickets(cursor)
                            ticket_entry_slist.kill()
                            ticket_entry_slist = ticket_elements.ticket_entry_slist_func(manager, ticket_list)


                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    def ticket_creation_init(connect, cursor):

        window_surface, clock, background = init.pygame_init()
        manager = init.pygame_gui_init()

        threat_list = queries.threats(cursor)
        id_list, account_list = queries.accounts(cursor)

        ticket_image_path = "assets/images/general/new_ticket.png"
        new_ticket_image = ticket_elements.new_ticket_image_func(manager, ticket_image_path)

        back_button = ticket_elements.back_button_func(manager)
        title_text_entry = ticket_elements.title_text_entry_func(manager)

        ticket_text_entry = ticket_elements.ticket_text_entry_func(manager)
        caller_dropdown_label, caller_dropdown = ticket_elements.caller_dropdown_func(manager, account_list)

        create_button, threat_entry_title_tbox, threat_entry_slist = ticket_elements.threat_entry_slist_func(manager, threat_list)
        threat_description_tbox = ticket_elements.threat_description_tbox_func(manager)

        selected_threat, ticket_title, ticket_entry, ticket_confirm_window = ticket_management_init_values()

        return ticket_creation(connect, cursor, window_surface, clock, background, manager, 
                               threat_list, new_ticket_image, back_button, title_text_entry,
                               ticket_text_entry, caller_dropdown_label, caller_dropdown, create_button, threat_entry_title_tbox, threat_entry_slist, 
                               threat_description_tbox, selected_threat, ticket_title, ticket_entry, 
                               ticket_confirm_window)
    
        
    def ticket_creation(connect, cursor, window_surface, clock, background, manager, 
                        threat_list, new_ticket_image, back_button, title_text_entry, 
                        ticket_text_entry, caller_dropdown_label, caller_dropdown, create_button, 
                        threat_entry_title_tbox, threat_entry_slist, 
                        threat_description_tbox, selected_threat, ticket_title, ticket_entry,
                        ticket_confirm_window):

        menu_button_music_path = "assets/sounds/list_click2.mp3"
        pygame.mixer.music.load(menu_button_music_path)
        menu_button_music_channel = pygame.mixer.Channel(0)

        create_button_music_path = "assets/sounds/create_button.mp3"
        pygame.mixer.music.load(create_button_music_path)
        create_button_music_channel = pygame.mixer.Channel(3)

        back_button_music_path = "assets/sounds/back_button.mp3"
        pygame.mixer.music.load(back_button_music_path)
        back_button_music_channel = pygame.mixer.Channel(4)
        back_button_music_channel.set_volume(0.2)

        selected_caller = None
        
        
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        back_button_music_channel.play(pygame.mixer.Sound(back_button_music_path))
                        updated_id_list, updated_ticket_list = queries.tickets(cursor)
                        return updated_id_list, updated_ticket_list

                if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == threat_entry_slist:
                        
                        menu_button_music_channel.play(pygame.mixer.Sound(menu_button_music_path))

                        selected_threat = event.text
                        print(selected_threat)

                        cursor.execute('SELECT description, indicators, countermeasures FROM threats WHERE name=?', [selected_threat])
                        description, indicators, countermeasures = cursor.fetchone()
                        threat_description_tbox.set_text(f'<b>{selected_threat.upper()}</b>\n<b>Description</b>:\n{description}\n<b>Indicators:\n</b>{indicators}\n<b>Countermeasures:</b>\n{countermeasures}')

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == caller_dropdown:
                        selected_caller = event.text
                
                ticket_title = title_text_entry.get_text()
                ticket_entry = ticket_text_entry.get_text()
                
                if selected_threat is not None and ticket_title is not None and ticket_entry is not None and ticket_confirm_window is None:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == create_button:

                            
                            if selected_caller is None:
                                selected_caller_id = 1
                            else:
                                cursor.execute('SELECT id FROM accounts WHERE name=?', [selected_caller])
                                selected_caller_id = int(cursor.fetchone()[0])
                            
                            create_button_music_channel.play(pygame.mixer.Sound(create_button_music_path))

                            cursor.execute('SELECT MAX(id) FROM tickets')
                            last_id = cursor.fetchone()[0]
                            new_id = last_id + 1

                            transcript_path = ticket_transcript_generator(new_id, ticket_entry)
                            print(transcript_path)

                            new_ticket = (new_id, ticket_title, ticket_entry, selected_threat, selected_caller_id, transcript_path)
                            cursor.execute('INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)', new_ticket)
                            connect.commit()

                            ticket_confirm_window, ticket_confirm_close_button = ticket_elements.ticket_confirm_window_func(manager)
            
                manager.process_events(event)

            manager.update(time_delta)
            window_surface.blit(background, (0, 0))

            if ticket_confirm_window:
                ticket_confirm_window.show()
                manager.draw_ui(window_surface)
                
                for event in pygame.event.get():
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == ticket_confirm_close_button:

                            title_text_entry.set_text("")
                            ticket_text_entry.set_text("")
                            threat_description_tbox.set_text("SELECT A THREAT")

                            ticket_confirm_window.hide()
                            selected_threat, ticket_title, ticket_entry, ticket_confirm_window = ticket_management_init_values()

                    manager.process_events(event)


            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    ticket_management_init(connect, cursor)