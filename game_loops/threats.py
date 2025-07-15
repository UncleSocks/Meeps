import pygame
import pygame_gui

import init
import constants
import elements.threats_elements as threat_element
from queries import SqliteQueries




class ThreatManagement():

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

    def _init_ui_elements(self):

        self.back_button = threat_element.back_button_func(self.manager)
        self.create_button = threat_element.create_button_func(self.manager)
        self.delete_button = threat_element.delete_button_func(self.manager)

        self.threat_database_image = threat_element.threat_database_image_func(self.manager, constants.THREAT_DATABASE_IMAGE_PATH)
        self.threat_entry_title_tbox = threat_element.threat_entry_slist_misc_func(self.manager)
        self.threat_entry_slist = threat_element.threat_entry_slist_func(self.manager, self.threat_list)

        self.threat_details_label, self.selected_threat_title_tbox, self.selected_threat_description_tbox, \
            self.selected_threat_indicators_tbox, self.selected_threat_countermeasures_tbox, \
                self.selected_threat_image_path_tbox = threat_element.threat_details_func(self.manager)
        
    def _init_state_variables(self):

        self.selected_threat = None
        self.threat_delete_confirm_window = False
        
    def _init_music(self):

        self.menu_button_music = pygame.mixer.music.load(constants.MENU_BUTTON_MUSIC_PATH)
        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.delete_button_music = pygame.mixer.music.load(constants.DELETE_BUTTON__MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.menu_button_music_channel = pygame.mixer.Channel(0)
        self.create_button_music_channel = pygame.mixer.Channel(1)
        self.delete_button_music_channel = pygame.mixer.Channel(2)
        self.back_button_music_channel = pygame.mixer.Channel(3)

    def threat_management_loop(self):

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.manager, self.time_delta)


    def _handle_events(self, events):

        for event in  events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.threat_entry_slist:

                self.selected_threat = event.text
                self._handle_threat_selection()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self.manager.process_events(event)


    def _handle_threat_selection(self):

        self.menu_button_music_channel.play(pygame.mixer.Sound(constants.MENU_BUTTON_MUSIC_PATH))

        description, indicators, countermeasures, image_path = SqliteQueries(self.cursor).threat_selection_query(self.selected_threat)

        self.selected_threat_title_tbox.set_text(f"<b>{self.selected_threat}</b>")
        self.selected_threat_description_tbox.set_text(f"DESCRIPTION:\n{description}")
        self.selected_threat_indicators_tbox.set_text(f"INDICATORS:\n{indicators}")
        self.selected_threat_countermeasures_tbox.set_text(f"COUNTERMEASURES:\n{countermeasures}")
        self.selected_threat_image_path_tbox.set_text(f"{image_path}")

    
    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            self.back_button_music_channel.set_volume(0.2)
            self.running = False

        if event.ui_element == self.create_button:

            self.create_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))

            threat_create = ThreatCreation(self.connect, self.cursor)
            updated_threat_list = threat_create.threat_creation_loop()
            self.threat_entry_slist.kill()
            self.threat_entry_slist = threat_element.threat_entry_slist_func(self.manager, updated_threat_list)

        if event.ui_element == self.delete_button and self.selected_threat is not None:

            self.delete_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))
            self.threat_delete_confirm_window, self.threat_delete_confirm_yes_button, self.threat_delete_confirm_no_button = threat_element.threat_delete_confirm_window_func(self.manager)
            

        if self.threat_delete_confirm_window:
            
            self.threat_delete_confirm_window.show()

            if event.ui_element == self.threat_delete_confirm_yes_button:

                self.delete_button_music_channel.play(pygame.mixer.Sound(constants.DELETE_BUTTON__MUSIC_PATH))

                updated_threat_list = self._delete_threat()
                self.threat_entry_slist.kill()
                self.threat_entry_slist = threat_element.threat_entry_slist_func(self.manager, updated_threat_list)

                self.threat_delete_confirm_window.kill()

            if event.ui_element == self.threat_delete_confirm_no_button:
                
                self.back_button_music_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
                self.threat_delete_confirm_window.kill()


    def _delete_threat(self):

        self.cursor.execute('DELETE FROM tickets WHERE answer=?', [self.selected_threat])
        self.connect.commit()

        self.cursor.execute('DELETE FROM threats WHERE name=?', [self.selected_threat])
        self.connect.commit()

        updated_threat_list = SqliteQueries(self.cursor).threat_list_query()

        return updated_threat_list



class ThreatCreation():

    def __init__(self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

        self._init_pygame()
        self._init_ui_elements()
        self._init_state_variables()
        self._init_music()
        self._init_threat_entry_variables()


    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

    def _init_ui_elements(self):

        self.threat_create_image = threat_element.add_threat_image_func(self.manager, constants.THREAT_CREATE_IMAGE_PATH)
        
        self.back_button = threat_element.back_button_func(self.manager)
        self.add_button = threat_element.threat_entry_add_button_func(self.manager)

        self.threat_entry_name, self.threat_entry_description, self.threat_entry_indicators, \
            self.threat_entry_countermeasures, self.threat_entry_image_path = threat_element.threat_entry_func(self.manager)
        
    def _init_state_variables(self):

        self.updated_threat_list = None

    def _init_music(self):

        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.create_button_music_channel = pygame.mixer.Channel(3)

        self.back_button_channel = pygame.mixer.Channel(4)
        self.back_button_channel.set_volume(0.2)

            
    def _init_threat_entry_variables(self):

        self.threat_name = None
        self.threat_description = None
        self.threat_indicators = None
        self.threat_countermeasures = None
        self.threat_image_path = None

        self.confirm_window = False


    def threat_creation_loop(self):

        self.running = True
        while self.running:

            self.time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()
            self._handle_events(events)
            self.pygame_renderer.ui_renderer(self.manager, self.time_delta)

        return self.updated_threat_list


    def _handle_events(self, events):
        
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_pressed(event)

            self._handle_threat_entry_content()

            self.manager.process_events(event)



    def _handle_button_pressed(self, event):

        if event.ui_element == self.back_button:

            self.back_button_channel.play(pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH))
            self.updated_threat_list = SqliteQueries(self.cursor).threat_list_query()

            self.running = False
        
        if event.ui_element == self.add_button and self.threat_name is not None and self.threat_description is not None and self.threat_indicators is not None and self.threat_countermeasures is not None:

            self.create_button_music_channel.play(pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH))

            self.cursor.execute('SELECT MAX(id) FROM threats')
            last_id = self.cursor.fetchone()[0]
            new_id = last_id + 1

            new_threat_entry = (new_id, self.threat_name, self.threat_description, self.threat_indicators, self.threat_countermeasures, self.threat_image_path)
            self.cursor.execute('INSERT INTO threats VALUES (?, ?, ?, ?, ?, ?)', new_threat_entry)
            self.connect.commit()

            self.confirm_window, self.confirm_close_button = threat_element.threat_confirm_window_func(self.manager)

        
        if self.confirm_window:

            self.confirm_window.show()
            self.manager.draw_ui(self.window_surface)

            if event.ui_element == self.confirm_close_button:

                self.threat_entry_name.set_text("")
                self.threat_entry_description.set_text("")
                self.threat_entry_indicators.set_text("")
                self.threat_entry_countermeasures.set_text("")
                self.threat_entry_image_path.set_text("")

                self.confirm_window.hide()

                self._init_threat_entry_variables()

    def _handle_threat_entry_content(self):

        self.threat_name = self.threat_entry_name.get_text()
        self.threat_description = self.threat_entry_description.get_text()
        self.threat_indicators = self.threat_entry_indicators.get_text()
        self.threat_countermeasures = self.threat_entry_countermeasures.get_text()
        self.threat_image_path = self.threat_entry_image_path.get_text()
