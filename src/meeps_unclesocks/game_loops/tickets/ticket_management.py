import pygame
import pygame_gui
from dataclasses import dataclass

import elements.game_elements.ticket_elements.ticket_management_elements as tme
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, \
    ImagePaths, ButtonSFX
from init import PygameRenderer
from sound_manager import ButtonSoundManager
from queries import SqliteQueries




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
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_ticket_elements()

    def _draw_images(self):
        ticket_manager_image = tme.TitleImage(self.manager)
        load_ticket_manager_image = pygame.image.load(ImagePaths.TICKET_MANAGEMENT.value)
        ticket_manager_image.INPUT = load_ticket_manager_image
        self.ticket_manager_image = ticket_manager_image.draw_image()

    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.create_button = se.CreateButton(self.manager).draw_button()
        self.delete_button = se.DeleteButton(self.manager).draw_button()

    def _draw_ticket_elements(self):
        self.ticket_entry_title_tbox = tme.TicketListTitle(self.manager).draw_textbox()

        ticket_selection_list = tme.TicketList(self.manager)
        ticket_selection_list.INPUT = self.state.ticket_title_list
        self.ticket_selection_list = ticket_selection_list.draw_selectionlist()

        self.ticket_details_label = tme.TicketLabel(self.manager).draw_label()
        self.ticket_title = tme.TicketTitleTextBox(self.manager).draw_textbox()
        self.ticket_description = tme.TicketDescriptionTextBox(self.manager).draw_textbox()
        self.account_details_label = tme.AccountLabel(self.manager).draw_label()
        self.account_description = tme.AccountDescriptionTextBox(self.manager).draw_textbox()

    def display_confirm_window(self):
        self.state.ticket_delete_confirm_window = tme.DeleteConfirmWindow(self.manager).draw_window()

        delete_confirm_label = tme.DeleteConfirmLabel(self.manager)
        delete_confirm_label.CONTAINER = self.state.ticket_delete_confirm_window
        self.delete_confirm_label = delete_confirm_label.draw_label()
        
        ticket_delete_confirm_yes_button = se.DeleteYesButton(self.manager)
        ticket_delete_confirm_yes_button.CONTAINER = self.state.ticket_delete_confirm_window
        self.ticket_delete_confirm_yes_button = ticket_delete_confirm_yes_button.draw_button()

        ticket_delete_confirm_no_button = se.DeleteNoButton(self.manager)
        ticket_delete_confirm_no_button.CONTAINER = self.state.ticket_delete_confirm_window
        self.ticket_delete_confirm_no_button = ticket_delete_confirm_no_button.draw_button()

    def refresh_ticket_list(self, updated_ticket_list):
        self.ticket_selection_list.set_item_list(updated_ticket_list)
        self.state.ticket_title_id_map = self.state.ticket_id_title_mapper()


class TicketEventHandler():

    def __init__(self, pygame_manager, state_manager: TicketStateManager, ui_manager: TicketUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = ButtonSoundManager()

    def handle_ticket_selection(self, selected_ticket):
        self.button_sfx.play_sfx(ButtonSFX.LIST_BUTTON)
        self.state.selected_ticket = selected_ticket
        self._update_ticket_textbox()

    def _update_ticket_textbox(self):
        ticket = self.state.fetch_ticket_details()

        self.ui.ticket_title.set_text(f"<b>{ticket.title}</b>")
        self.ui.ticket_description.set_text(f"{ticket.entry}")
        self.ui.account_description.set_text(
            f"<b>Name:</b> {ticket.account}\n"
            f"<b>Organization:</b> {ticket.account_organization}\n"
            f"<b>Email:</b> {ticket.account_email}\n"
            f"<b>Contact:</b> {ticket.account_contact}"
        )

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if event.ui_element == self.ui.create_button:
            return ButtonAction.CREATE

        if event.ui_element == self.ui.delete_button \
            and self.state.selected_ticket is not None:
            return ButtonAction.DELETE

        if self.state.ticket_delete_confirm_window \
            and event.ui_element == self.ui.ticket_delete_confirm_yes_button:
            return ButtonAction.CONFIRM_DELETE

        if self.state.ticket_delete_confirm_window \
            and event.ui_element == self.ui.ticket_delete_confirm_no_button:
            return ButtonAction.CANCEL_DELETE


class TicketManagementController():

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
        self.window_surface = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = TicketStateManager(self.connect, self.cursor)
        self.ui = TicketUIManager(self.manager, self.state)
        self.event_handler = TicketEventHandler(self.manager, self.state, self.ui)

    def game_loop(self, events):
        for event in events:
            action = self._handle_events(event)
            
            if action == ButtonAction.EXIT:
                return StateTracker.MAIN_MENU
            if action == ButtonAction.CREATE:
                return StateTracker.TICKET_CREATION

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.ticket_selection_list:
            selected_ticket = event.text
            self.event_handler.handle_ticket_selection(selected_ticket)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == ButtonAction.EXIT:
                return self._handle_exit_action()
            
            if button_event == ButtonAction.CREATE:
                return self._handle_create_action()

            button_action_map = {
                ButtonAction.DELETE: self._handle_delete_action,
                ButtonAction.CONFIRM_DELETE: self._handle_confirm_delete_action,
                ButtonAction.CANCEL_DELETE: self._handle_cancel_delete_action
            }

            button_action = button_action_map.get(button_event)
            if button_action:
                button_action()

        self.manager.process_events(event)
        return True
    
    def _handle_create_action(self):
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.CREATE

    def _handle_delete_action(self):
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.ui.display_confirm_window()

    def _handle_confirm_delete_action(self):
        self.button_sfx.play_sfx(ButtonSFX.DELETE_BUTTON)
        self.state.ticket_delete_confirm_window.kill()
        self.state.delete_selected_ticket()
        self.state.ticket_title_list = self.state.fetch_ticket_titles()
        self.ui.refresh_ticket_list(self.state.ticket_title_list)

    def _handle_cancel_delete_action(self):
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.state.ticket_delete_confirm_window.kill()

    def _handle_exit_action(self):
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT