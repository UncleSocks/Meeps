import pygame
import pygame_gui
from dataclasses import dataclass

import constants
import init
import sound_manager
from queries import SqliteQueries
from .ticket_creation import TicketCreationController
import elements.ticket_elements as ticket_elements



@dataclass
class TicketDetails:
    title: str = ""
    entry: str = ""
    account: str = ""
    account_organization: str = ""
    account_email: str = ""
    account_contact: str = ""


class TicketStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.ticket_variables()

    def ticket_variables(self):
        self.ticket_title_list = self.query.ticket_titles_query()
        self.ticket_title_id_map = self.ticket_id_title_mapper()
        self.selected_ticket = None
        self.ticket_delete_confirm_window = False

    def ticket_id_title_mapper(self):
        ticket_id_title_list = self.query.ticket_id_title_list()
        ticket_id_title_map = {ticket[1]: ticket[0] for ticket in ticket_id_title_list}
        return ticket_id_title_map
    
    def fetch_ticket_titles(self):
        ticket_title_list = self.query.ticket_titles_query()
        return ticket_title_list
    
    def fetch_ticket_details(self):
        selected_ticket_id = self.ticket_title_id_map[self.selected_ticket]
        ticket_details = self.query.ticket_account_query(selected_ticket_id)
        ticket = TicketDetails(*ticket_details)
        return ticket
    
    def delete_selected_ticket(self):
        selected_ticket_id = self.ticket_title_id_map[self.selected_ticket]
        self.cursor.execute('DELETE FROM tickets WHERE id=?', [selected_ticket_id])
        self.connect.commit()
        return
    

class TicketUIManager():

    def __init__(self, pygame_manager, state_manager: TicketStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ticket_list = self.state.ticket_title_list
        self.build_ui(self.ticket_list)

    def build_ui(self, ticket_list):
        self.back_button = ticket_elements.back_button_func(self.manager)
        self.ticket_management_image = ticket_elements.ticket_manager_image_func(self.manager, constants.TICKET_MANAGEMENT_IMAGE_PATH)
        self.ticket_information_label = ticket_elements.ticket_information_label_func(self.manager)

        self.create_button = ticket_elements.create_ticket_button_func(self.manager)
        self.delete_button = ticket_elements.delete_ticket_button_func(self.manager)

        self.ticket_entry_title_tbox = ticket_elements.ticket_entry_slist_misc_func(self.manager)
        self.ticket_entry_slist = ticket_elements.ticket_entry_slist_func(self.manager, ticket_list)
        self.selected_ticket_title_tbox, self.selected_ticket_description_tbox = ticket_elements.selected_ticket_tbox_func(self.manager)

        self.account_details_label = ticket_elements.account_details_label_func(self.manager)
        self.selected_ticket_account_tbox = ticket_elements.selected_ticket_account_func(self.manager)

    def display_confirm_window(self):
        self.state.ticket_delete_confirm_window, self.ticket_delete_confirm_yes_button, \
            self.ticket_delete_confirm_no_button = ticket_elements.ticket_delete_confirm_window_func(self.manager)

    def refresh_ticket_list(self, updated_ticket_list):
        self.ticket_entry_slist.set_item_list(updated_ticket_list)


class TicketEventHandler():

    def __init__(self, pygame_manager, state_manager: TicketStateManager, ui_manager: TicketUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_ticket_selection(self, selected_ticket):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        self.state.selected_ticket = selected_ticket
        self._update_ticket_textbox()

    def _update_ticket_textbox(self):
        ticket = self.state.fetch_ticket_details()

        self.ui.selected_ticket_title_tbox.set_text(f"<b>{ticket.title}</b>")
        self.ui.selected_ticket_description_tbox.set_text(f"{ticket.entry}")
        self.ui.selected_ticket_account_tbox.set_text(
            f"<b>Name:</b> {ticket.account}\n"
            f"<b>Organization:</b> {ticket.account_organization}\n"
            f"<b>Email:</b> {ticket.account_email}\n"
            f"<b>Contact:</b> {ticket.account_contact}"
        )

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()
        
        if event.ui_element == self.ui.create_button:
            return self._handle_create_button()

        if event.ui_element == self.ui.delete_button and self.state.selected_ticket is not None:
            self._handle_delete_button()

        if self.state.ticket_delete_confirm_window and event.ui_element == self.ui.ticket_delete_confirm_yes_button:
            self._handle_confirm_yes_button()

        if self.state.ticket_delete_confirm_window and event.ui_element == self.ui.ticket_delete_confirm_no_button:
            self._handle_confirm_no_button()

    def _handle_back_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    
    def _handle_create_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        return constants.CREATE_ACTION

    def _handle_delete_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.ui.display_confirm_window()
        
    def _handle_confirm_yes_button(self):
        self.button_sfx.play_sfx(constants.DELETE_BUTTON_SFX)
        self.state.delete_selected_ticket()
        self.state.ticket_title_list = self.state.fetch_ticket_titles()
        self.ui.refresh_ticket_list(self.state.ticket_title_list)
        self.state.ticket_title_id_map = self.state.ticket_id_title_mapper()

        self.state.ticket_delete_confirm_window.kill()

    def _handle_confirm_no_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.state.ticket_delete_confirm_window.kill()


class TicketManagementController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface = self.pygame_renderer.window_surface

        self.state = TicketStateManager(self.connect, self.cursor)
        self.ui = TicketUIManager(self.manager, self.state)
        self.event_handler = TicketEventHandler(self.manager, self.state, self.ui)

    def ticket_management_loop(self):
        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()

            for event in events:
                if not self._handle_events(event):
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.ticket_entry_slist:
            selected_ticket = event.text
            self.event_handler.handle_ticket_selection(selected_ticket)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_action = self.event_handler.handle_button_pressed(event)

            if button_action == constants.CREATE_ACTION:
                ticket_creation_page = TicketCreationController(self.state.connect, self.state.cursor)
                self.state.ticket_title_list = ticket_creation_page.ticket_creation_loop()
                self._handle_creation_return()

            elif button_action == constants.EXIT_ACTION:
                return False
            
        self.manager.process_events(event)
        return True
    
    def _handle_creation_return(self):
            self.ui.refresh_ticket_list(self.state.ticket_title_list)
            self.state.ticket_title_id_map = self.state.ticket_id_title_mapper()