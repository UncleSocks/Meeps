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
    ticket_transcript_filepath = engine.save_to_file(ticket, ticket_transcript_filename)

    engine.runAndWait()

    return ticket_transcript_filename


class TicketManagement():

    def __init__(self, connect, cursor):

        self.connect = connect
        self.cursor = cursor

    def _init_pygame(self):

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

    def _init_gameplay_elements(self):

        self.ticket_id_list, self.ticket_title_list = SqliteQueries(self.cursor).ticket_ids_titles_query()

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

        self.ticket_confirm_window = False

    def _init_music(self):

        self.menu_button_music = pygame.mixer.music.load(constants.LIST_CLICK_MUSIC_PATH)
        self.create_button_music = pygame.mixer.music.load(constants.CREATE_BUTTON_MUSIC_PATH)
        self.delete_button_music = pygame.mixer.music.load(constants.DELETE_BUTTON__MUSIC_PATH)
        self.back_button_music = pygame.mixer.music.load(constants.BACK_BUTTON_MUSIC_PATH)

        self.menu_button_music_channel = pygame.mixer.Channel(0)
        self.create_button_music_channel = pygame.mixer.Channel(1)
        self.delete_button_music_channel = pygame.mixer.Channel(2)
        self.back_button_music_channel = pygame.mixer.Channel(3)