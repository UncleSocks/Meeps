import pygame
import pygame_gui

import init
import constants
import elements.accounts_elements as account_elements
from queries import SqliteQueries



class AccountManagement:

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

        self.account_name_list = SqliteQueries(self.cursor).account_name_list_query()
        self.account_id_list = SqliteQueries(self.cursor).account_id_query()
        self.assigned_ticket_list = []

    def _init_ui_elements(self):

        self.back_button = account_elements.back_button_func(self.manager)
        self.create_button = account_elements.create_button_func(self.manager)
        self.delete_button = account_elements.delete_button_fun(self.manager)

        self.account_entry_title_tbox = account_elements.account_entry_slist_misc_func(self.manager)
        self.account_entry_slist = account_elements.account_entry_slist_func(self.manager, self.account_name_list)

        self.assigned_ticket_label = account_elements.assigned_ticket_label_func(self.manager)
        self.assigned_ticket_slist = account_elements.assigned_tickets(self.manager, self.assigned_ticket_list)

        self.account_manager_image = account_elements.account_manager_image_func(self.manager, constants.ACCOUNT_MANAGEMENT_IMAGE_PATH)
        self.account_details_label, self.selected_account_description_tbox = account_elements.account_details(self.manager)

    def _init_state_variables(self):

        self.selected_account = None
        self.account_delete_confirm_window = False

    def _init_music(self):

        self.menu_button_music = pygame.mixer.music.load(constants.MENU_BUTTON_MUSIC_PATH)
        self.delete_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.add_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.menu_button_music_channel = pygame.mixer.Channel(0)
        self.delete_button_music_channel = pygame.mixer.Channel(1)
        self.add_button_music_channel = pygame.mixer.Channel(2)
        self.back_button_music_channel = pygame.mixer.Channel(3)


    def account_management_loop(self):

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

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.account_entry_slist:

                self.selected_account = event.text
                self._handle_account_selection()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self.manager.process_events(event)


    def _handle_account_selection(self):

        self.menu_button_music_channel.play(pygame.mixer.Sound(constants.MENU_BUTTON_MUSIC_PATH))

        id_index_find = self.account_name_list.index(self.selected_account)
        self.selected_account_id = self.account_id_list[id_index_find]

        account_name, account_organization, account_email, account_contact, account_picture_path = SqliteQueries(self.cursor).account_details_query(self.selected_account_id)
        self.selected_account_description_tbox.set_text(f"<b>Name:</b> {account_name}\n<b>Organization:</b> {account_organization}\n<b>Email:</b> {account_email}\n<b>Contact:</b> {account_contact}\n<b>Picture Filename:</b> {account_picture_path}")

        self.assigned_ticket_list = SqliteQueries(self.cursor).ticket_title_caller_id_query(self.selected_account_id)
        self.assigned_ticket_slist = account_elements.assigned_tickets(self.manager, self.assigned_ticket_list)


    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            pygame.mixer.music.unload()

            self.running = False

        if event.ui_element == self.create_button:

            self.add_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))

            account_create = AccountCreation(self.connect, self.cursor)
            self.account_name_list = account_create.account_creation_loop()

            self.account_entry_slist.kill()
            self.account_entry_slist = account_elements.account_entry_slist_func(self.manager, self.account_name_list)

            self.account_id_list = SqliteQueries(self.cursor).account_id_query()

        if event.ui_element == self.delete_button and self.selected_account is not None:

            self.delete_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))
            self.account_delete_confirm_window, self.account_delete_confirm_yes_button, self.account_delete_no_button = account_elements.account_delete_confirm_window_func(self.manager)


        if self.account_delete_confirm_window:

            self.account_delete_confirm_window.show()

            if event.ui_element == self.account_delete_confirm_yes_button:

                self.delete_button_music_channel.play(pygame.mixer.Sound(constants.DELETE_BUTTON__MUSIC_PATH))

                self.account_name_list = self._delete_account()
                self.account_entry_slist.kill()
                self.account_entry_slist = account_elements.account_entry_slist_func(self.manager, self.account_name_list)

                self.account_delete_confirm_window.kill()

            if event.ui_element == self.account_delete_no_button:

                self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
                self.account_delete_confirm_window.kill()


    def _delete_account(self):

        self.cursor.execute('DELETE FROM accounts WHERE id=?', [self.selected_account_id])
        self.connect.commit()
        
        self.cursor.execute('DELETE FROM tickets WHERE caller_id=?', [self.selected_account_id])
        self.connect.commit()

        updated_account_name_list = SqliteQueries(self.cursor).account_name_list_query()

        return updated_account_name_list


class AccountCreation():

    def __init__(self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self._init_pygame()
        self._init_ui_elements()
        self._init_state_variables()
        self._init_music()

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

    def _init_ui_elements(self):

        self.back_button = account_elements.back_button_func(self.manager)
        self.add_account_image = account_elements.add_account_image_func(self.manager, constants.ADD_ACCOUNT_IMAGE_PATH)

        self.account_name_label, self.new_account_name_tentry = account_elements.new_account_name_tentry_func(self.manager)
        self.account_organization_label, self.new_account_organization_tentry = account_elements.new_account_organization_func(self.manager)
        self.account_email_label, self.new_account_email_tentry = account_elements.new_account_email_func(self.manager)
        self.account_contact_label, self.new_account_contact_tentry = account_elements.new_account_contact_func(self.manager)
        self.account_picture_path_label, self.new_account_picture_path_tentry = account_elements.new_account_picture_path_func(self.manager)
        
        self.new_account_image_border = account_elements.new_account_image_border_func(self.manager)

        self.add_account_button = account_elements.add_new_account_button_func(self.manager)

    def _init_state_variables(self):

        self.new_account_name = None
        self.new_account_organization = None
        self.new_account_email = None
        self.new_account_contact = None
        self.new_account_picture_path = None

        self.account_confirm_window = False

    def _init_music(self):

        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)
        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)

        self.back_button_music_channel = pygame.mixer.Channel(3)
        self.create_button_music_channel = pygame.mixer.Channel(4)


    def account_creation_loop(self):

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.time_delta)

        return self.updated_account_name_list


    def _handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self._get_new_account_content()
            self.manager.process_events(event)


    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            self.updated_account_name_list = SqliteQueries(self.cursor).account_name_list_query()

            self.running = False

        if event.ui_element == self.add_account_button and all([
            self.new_account_name,
            self.new_account_organization,
            self.new_account_email,
            self.new_account_contact, 
            self.new_account_picture_path
        ]):
            
            self.create_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))

            self.cursor.execute('SELECT MAX(id) FROM accounts')
            last_account_id = self.cursor.fetchone()[0]
            new_account_id = last_account_id + 1

            new_account_entry = (new_account_id, self.new_account_name, self.new_account_organization, 
                                 self.new_account_email, self.new_account_contact, self.new_account_picture_path)
            
            self.cursor.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)', new_account_entry)
            self.connect.commit()

            self.account_confirm_window, self.account_confirm_close_button = account_elements.account_confirm_window_func(self.manager)


        if self.account_confirm_window:

            self.account_confirm_window.show()
            self.manager.draw_ui(self.window_surface)

            if event.ui_element == self.account_confirm_close_button:
                
                self._reset_account_content()
                self.account_confirm_window.kill()
                self._init_state_variables()


    def _get_new_account_content(self):

        self.new_account_name = self.new_account_name_tentry.get_text()
        self.new_account_organization = self.new_account_organization_tentry.get_text()
        self.new_account_email = self.new_account_email_tentry.get_text()
        self.new_account_contact = self.new_account_contact_tentry.get_text()

        self.new_account_picture_path = self.new_account_picture_path_tentry.get_text()
        account_elements.new_account_image_func(self.manager, self.new_account_picture_path)

    def _reset_account_content(self):

        self.new_account_name_tentry.set_text("")
        self.new_account_organization_tentry.set_text("")
        self.new_account_email_tentry.set_text("")
        self.new_account_contact_tentry.set_text("")
        self.new_account_picture_path_tentry.set_text("")
