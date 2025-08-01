import pygame
import pygame_gui
from dataclasses import dataclass

import constants
import init
import sound_manager
from queries import SqliteQueries
from .account_creation import AccountCreationController
import elements.accounts_elements as account_elements



@dataclass
class AccountDetails:
    name: str = ""
    organization: str = ""
    email: str = ""
    contact: str = ""
    picture_path: str = ""


class AccountStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.account_variables()

    def account_variables(self):
        self.account_name_list = self.fetch_account_names()
        self.account_id_name_map = self.account_id_name_mapper()
        self.assigned_ticket_list = []
        self.selected_account = None
        self.account_delete_confirm_window = False

    def account_id_name_mapper(self):
        account_id_name_list = self.query.account_id_name_list()
        account_id_name_map = {account[1]: account[0] for account in account_id_name_list}
        return account_id_name_map

    def fetch_account_names(self):
        account_name_list = self.query.account_name_list_query()
        return account_name_list

    def fetch_account_details(self):
        selected_account_id = self.account_id_name_map[self.selected_account]
        account_details = self.query.account_details_query(selected_account_id)
        account = AccountDetails(*account_details)
        return account
    
    def fetch_assigned_tickets(self):
        selected_account_id = self.account_id_name_map[self.selected_account]
        assigned_tickets_list = self.query.ticket_title_caller_id_query(selected_account_id)
        return assigned_tickets_list
    
    def delete_selected_account(self):
        selected_account_id = self.account_id_name_map[self.selected_account]
        self.cursor.execute('DELETE FROM accounts WHERE id=?', [selected_account_id])        
        self.cursor.execute('DELETE FROM tickets WHERE caller_id=?', [selected_account_id])
        self.connect.commit()
        return
    

class AccountUIManager():

    def __init__(self, manager, state_manager: AccountStateManager):
        self.manager = manager
        self.state = state_manager
        self.account_name_list = self.state.account_name_list
        self.assigned_ticket_list = self.state.assigned_ticket_list
        self.build_ui(self.account_name_list, self.assigned_ticket_list)

    def build_ui(self, account_name_list, assigned_ticket_list):
        self.back_button = account_elements.back_button_func(self.manager)
        self.create_button = account_elements.create_button_func(self.manager)
        self.delete_button = account_elements.delete_button_fun(self.manager)

        self.account_entry_title_tbox = account_elements.account_entry_slist_misc_func(self.manager)
        self.account_entry_slist = account_elements.account_entry_slist_func(self.manager, account_name_list)

        self.assigned_ticket_label = account_elements.assigned_ticket_label_func(self.manager)
        self.assigned_ticket_slist = account_elements.assigned_tickets(self.manager, assigned_ticket_list)

        self.account_manager_image = account_elements.account_manager_image_func(self.manager, constants.ACCOUNT_MANAGEMENT_IMAGE_PATH)
        self.account_details_label, self.selected_account_description_tbox = account_elements.account_details(self.manager)

    def display_confirm_window(self):
        self.state.account_delete_confirm_window, self.confirm_delete_yes_button, \
            self.confirm_delete_no_button = account_elements.account_delete_confirm_window_func(self.manager)

    def refresh_account_list(self, updated_account_list):
        self.account_entry_slist.set_item_list(updated_account_list)

    def refresh_assigned_tickets(self, assigned_ticket_list):
        self.assigned_ticket_slist.set_item_list(assigned_ticket_list)


class AccountEventHandler():

    def __init__(self, pygame_manager, state_manager: AccountStateManager, ui_manager: AccountUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_account_selection(self, selected_account):
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        self.state.selected_account = selected_account
        self._update_account_textbox()

    def _update_account_textbox(self):
        account = self.state.fetch_account_details()
        
        self.ui.selected_account_description_tbox.set_text(
            f"<b>Name:</b> {account.name}\n"
            f"<b>Organization:</b> {account.organization}\n"
            f"<b>Email:</b> {account.email}\n"
            f"<b>Contact:</b> {account.contact}\n"
            f"<b>Picture Filename:</b> {account.picture_path}"
        )

        self.state.assigned_ticket_list = self.state.fetch_assigned_tickets()
        self.ui.refresh_assigned_tickets(self.state.assigned_ticket_list)

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()

        if event.ui_element == self.ui.create_button:
            self._handle_create_button()

        if event.ui_element == self.ui.delete_button and self.state.selected_account is not None:
            self._handle_delete_button()

        if self.state.account_delete_confirm_window and event.ui_element == self.ui.confirm_delete_yes_button:
            self._handle_confirm_yes_button()

        if self.state.account_delete_confirm_window and event.ui_element == self.ui.confirm_delete_no_button:
            self._handle_confirm_no_button()

    def _handle_back_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION
    
    def _handle_create_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.account_name_list = AccountCreationController(self.state.connect, self.state.cursor).account_creation_loop()
        self.ui.refresh_account_list(self.state.account_name_list)
        self.state.account_id_name_map = self.state.account_id_name_mapper()

    def _handle_delete_button(self):
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.ui.display_confirm_window()
        
    def _handle_confirm_yes_button(self):
        self.button_sfx.play_sfx(constants.DELETE_BUTTON_SFX)
        self.state.delete_selected_account()
        self.state.account_name_list = self.state.fetch_account_names()
        self.ui.refresh_account_list(self.state.account_name_list)
        self.state.account_id_name_map = self.state.account_id_name_mapper()

        self.state.account_delete_confirm_window.kill()

    def _handle_confirm_no_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.state.account_delete_confirm_window.kill()

    
class AccountManagementController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface  = self.pygame_renderer.window_surface

        self.state = AccountStateManager(self.connect, self.cursor)
        self.ui = AccountUIManager(self.manager, self.state)
        self.event_handler = AccountEventHandler(self.manager, self.state, self.ui)

    def account_management_loop(self):
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
            and event.ui_element == self.ui.account_entry_slist:
            selected_account = event.text
            self.event_handler.handle_account_selection(selected_account)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_action = self.event_handler.handle_button_pressed(event)

            if button_action == constants.EXIT_ACTION:
                return False
            
        self.manager.process_events(event)
        return True