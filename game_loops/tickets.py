import pygame
import pygame_gui
import pyttsx3

import init
import constants
import elements.ticket_elements as ticket_elements
from queries import SqliteQueries



def ticket_transcript_generator(id, ticket):

    engine = pyttsx3.init()
    ticket_transcript_filename = f'assets/sounds/{id}_transcript.wav'
    engine.save_to_file(ticket, ticket_transcript_filename)

    engine.runAndWait()

    return ticket_transcript_filename


class TicketManagement():

    def __init__(self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self._init_pygame()
        self._init_gameplay_elements()
        self._init_ui_elements()
        self._init_state_variables()
        self._init_music()

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

    def _init_gameplay_elements(self):

        self.ticket_title_list = SqliteQueries(self.cursor).ticket_titles_query()
        self.ticket_id_list = SqliteQueries(self.cursor).ticket_ids_query()

    def _init_ui_elements(self):

        self.back_button = ticket_elements.back_button_func(self.manager)
        self.ticket_management_image = ticket_elements.ticket_manager_image_func(self.manager, constants.TICKET_MANAGEMENT_IMAGE_PATH)
        self.ticket_information_label = ticket_elements.ticket_information_label_func(self.manager)

        self.create_button = ticket_elements.create_ticket_button_func(self.manager)
        self.delete_button = ticket_elements.delete_ticket_button_func(self.manager)

        self.ticket_entry_title_tbox = ticket_elements.ticket_entry_slist_misc_func(self.manager)
        self.ticket_entry_slist = ticket_elements.ticket_entry_slist_func(self.manager, self.ticket_title_list)
        self.selected_ticket_title_tbox, self.selected_ticket_description_tbox = ticket_elements.selected_ticket_tbox_func(self.manager)

        self.account_details_label = ticket_elements.account_details_label_func(self.manager)
        self.selected_ticket_account_tbox = ticket_elements.selected_ticket_account_func(self.manager)

    def _init_state_variables(self):

        self.selected_ticket_id = None
        self.selected_ticket = None

        self.ticket_title = None
        self.ticket_entry = None

        self.ticket_delete_confirm_window = False

    def _init_music(self):

        self.menu_button_music = pygame.mixer.music.load(constants.LIST_CLICK_MUSIC_PATH)
        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.delete_button_music = pygame.mixer.music.load(constants.DELETE_BUTTON__MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.menu_button_music_channel = pygame.mixer.Channel(0)
        self.create_button_music_channel = pygame.mixer.Channel(1)
        self.delete_button_music_channel = pygame.mixer.Channel(2)
        self.back_button_music_channel = pygame.mixer.Channel(3)


    def ticket_management_loop(self):

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.time_delta)



    def _handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.ticket_entry_slist:

                self.selected_ticket = event.text
                self._handle_ticket_selection()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self.manager.process_events(event)


    def _handle_ticket_selection(self):

        self.menu_button_music_channel.play(pygame.mixer.Sound(constants.MENU_BUTTON_MUSIC_PATH))

        id_index_find = self.ticket_title_list.index(self.selected_ticket)
        self.selected_ticket_id = self.ticket_id_list[id_index_find]

        ticket_title, ticket_entry, account_name, account_organization, account_email, account_contact = SqliteQueries(self.cursor).ticket_account_query(self.selected_ticket_id)
        
        self.selected_ticket_title_tbox.set_text(f"<b>{ticket_title}</b>")
        self.selected_ticket_description_tbox.set_text(f"{ticket_entry}")

        self.selected_ticket_account_tbox.set_text(f"<b>Name:</b> {account_name}\n<b>Organization:</b> {account_organization}\n<b>Email:</b> {account_email}\n<b>Contact:</b> {account_contact}")

    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            pygame.mixer.music.unload()
            
            self.running = False

        if event.ui_element == self.create_button:

            self.create_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))
            
            ticket_create = TicketCreation(self.connect, self.cursor)
            self.ticket_title_list = ticket_create.ticket_creation_loop()

            self.ticket_entry_slist.kill()
            self.ticket_entry_slist = ticket_elements.ticket_entry_slist_func(self.manager, self.ticket_title_list)

            self.ticket_id_list = SqliteQueries(self.cursor).ticket_ids_query()

        if event.ui_element == self.delete_button and self.selected_ticket is not None:

            self.delete_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))
            self.ticket_delete_confirm_window, self.ticket_delete_confirm_yes_button, self.ticket_delete_confirm_no_window = ticket_elements.ticket_delete_confirm_window_func(self.manager)

        if self.ticket_delete_confirm_window:

            self.ticket_delete_confirm_window.show()

            if event.ui_element == self.ticket_delete_confirm_yes_button:

                self.delete_button_music_channel.play(pygame.mixer.Sound(constants.DELETE_BUTTON__MUSIC_PATH))

                self.ticket_title_list = self._delete_tickets()
                self.ticket_entry_slist.kill()
                self.ticket_entry_slist = ticket_elements.ticket_entry_slist_func(self.manager, self.ticket_title_list)

                self.ticket_delete_confirm_window.kill()

            if event.ui_element == self.ticket_delete_confirm_no_window:

                self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
                self.ticket_delete_confirm_window.kill()


    def _delete_tickets(self):

        self.cursor.execute('DELETE FROM tickets WHERE id=?', [self.selected_ticket_id])
        self.connect.commit()

        updated_ticket_title_list = SqliteQueries(self.cursor).ticket_titles_query()

        return updated_ticket_title_list



class TicketCreation():

    def __init__(self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self._init_pygame()
        self._init_gameplay_elements()
        self._init_ui_elements()
        self._init_state_variables()
        self._init_music()

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

    def _init_gameplay_elements(self):

        self.threat_list = SqliteQueries(self.cursor).threat_list_query()
        self.account_name_list = SqliteQueries(self.cursor).account_name_list_query()
        self.account_id_list = SqliteQueries(self.cursor).account_id_query()

    def _init_ui_elements(self):

        self.new_ticket_image = ticket_elements.new_ticket_image_func(self.manager, constants.NEW_TICKET_IMAGE_PATH)

        self.back_button = ticket_elements.back_button_func(self.manager)

        self.ticket_title_text_entry = ticket_elements.title_text_entry_func(self.manager)
        self.ticket_text_entry = ticket_elements.ticket_text_entry_func(self.manager)
        self.caller_dropdown_label, self.caller_dropdown = ticket_elements.caller_dropdown_func(self.manager, self.account_name_list)

        self.threat_description_tbox = ticket_elements.threat_description_tbox_func(self.manager)
        self.create_button, self.threat_entry_title_tbox, self.threat_entry_slist = ticket_elements.threat_entry_slist_func(self.manager, self.threat_list)

    def _init_state_variables(self):

        self.selected_caller = None
        self.selected_ticket = None
        self.selected_threat = None

        self.ticket_title = None
        self.ticket_entry = None

        self.new_ticket_confirm_window = False

    def _init_music(self):

        self.menu_button_music = pygame.mixer.music.load(constants.MENU_BUTTON_MUSIC_PATH)
        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.menu_button_music_channel = pygame.mixer.Channel(0)
        self.create_button_music_channel = pygame.mixer.Channel(1)
        self.back_button_music_channel = pygame.mixer.Channel(2)

    
    def ticket_creation_loop(self):

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.time_delta)

        return self.updated_ticket_title_list


    def _handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.threat_entry_slist:

                self.selected_threat = event.text
                self._handle_threat_selection()

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.caller_dropdown:
                self.selected_caller = event.text

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self._get_ticket_entry_content()
            self.manager.process_events(event)

        
    def _handle_threat_selection(self):

        self.menu_button_music_channel.play(pygame.mixer.Sound(constants.MENU_BUTTON_MUSIC_PATH))
        print(self.selected_threat)
        threat_description, threat_indicators, threat_countermeasures = SqliteQueries(self.cursor).threat_ticket_selection_query(self.selected_threat)
        self.threat_description_tbox.set_text(f'<b>{self.selected_threat.upper()}</b>\n<b>Description</b>:\n{threat_description}\n<b>Indicators:\n</b>{threat_indicators}\n<b>Countermeasures:</b>\n{threat_countermeasures}')


    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            self.updated_ticket_title_list = SqliteQueries(self.cursor).ticket_titles_query()
            
            self.running = False
        
        if event.ui_element == self.create_button and all([
            self.selected_threat,
            self.ticket_title,
            self.ticket_entry,
        ]):
            
            selected_caller_id = 1 if self.selected_caller is None else SqliteQueries(self.cursor).ticket_caller_id_query(self.selected_caller)

            self.create_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))

            self.cursor.execute('SELECT MAX(id) FROM tickets')
            last_ticket_id = self.cursor.fetchone()[0]
            new_ticket_id = last_ticket_id + 1

            ticket_transcript_path = ticket_transcript_generator(new_ticket_id, self.ticket_entry)

            new_ticket = (new_ticket_id, self.ticket_title, self.ticket_entry, self.selected_threat, selected_caller_id, ticket_transcript_path)
            self.cursor.execute('INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)', new_ticket)
            self.connect.commit()

            self.new_ticket_confirm_window, self.new_ticket_close_button = ticket_elements.ticket_confirm_window_func(self.manager)

        if self.new_ticket_confirm_window:

            self.new_ticket_confirm_window.show()
            self.manager.draw_ui(self.window_surface)

            if event.ui_element == self.new_ticket_close_button:

                self._reset_ticket_entry_content()
                self.new_ticket_confirm_window.kill()
                self._init_state_variables()


    def _get_ticket_entry_content(self):

        self.ticket_title = self.ticket_title_text_entry.get_text()
        self.ticket_entry = self.ticket_text_entry.get_text()

    def _reset_ticket_entry_content(self):

        self.ticket_title_text_entry.set_text("")
        self.ticket_text_entry.set_text("")
        self.threat_description_tbox.set_text("SELECT A THREAT")