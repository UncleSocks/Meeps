import pygame
import pygame_gui
from typing import Optional
from dataclasses import dataclass

import constants
from constants import ManagementButtonAction, ManagementButtonSfx
import init
from sound_manager import ButtonSoundManager
from queries import SqliteQueries
from .account_creation import AccountCreationController
import elements.accounts_elements as ae



@dataclass
class AccountDetails:
    name: str = ""
    organization: str = ""
    email: str = ""
    contact: str = ""
    picture_path: str = ""


class AccountStateManager:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.account_variables()

    def account_variables(self) -> None:
        self.account_name_list = self.fetch_account_names()
        self.account_id_name_map = self.account_id_name_mapper()
        self.assigned_ticket_list = []
        self.selected_account = None
        self.account_delete_confirm_window = None

    def account_id_name_mapper(self) -> dict:
        account_id_name_list = self.query.account_id_name_list()
        account_id_name_map = {account[1]: account[0] for account in account_id_name_list}
        return account_id_name_map

    def fetch_account_names(self) -> list:
        account_name_list = self.query.account_name_list_query()
        return account_name_list

    def fetch_account_details(self):
        selected_account_id = self.account_id_name_map[self.selected_account]
        account_details = self.query.account_details_query(selected_account_id)
        account = AccountDetails(*account_details)
        return account
    
    def fetch_assigned_tickets(self) -> list:
        selected_account_id = self.account_id_name_map[self.selected_account]
        assigned_tickets_list = self.query.ticket_title_caller_id_query(selected_account_id)
        return assigned_tickets_list
    
    def delete_selected_account(self) -> None:
        selected_account_id = self.account_id_name_map[self.selected_account]
        self.cursor.execute('DELETE FROM accounts WHERE id=?', [selected_account_id])        
        self.cursor.execute('DELETE FROM tickets WHERE caller_id=?', [selected_account_id])
        self.connect.commit()
    

class AccountUIManager:

    def __init__(self, manager, state_manager: AccountStateManager):
        self.manager = manager
        self.state = state_manager
        self.draw_management_ui()

    def draw_management_ui(self):
        self.account_manager_image = ae.account_manager_image_func(self.manager, 
                                                                   constants.ACCOUNT_MANAGEMENT_IMAGE_PATH)
        self._draw_buttons()
        self._draw_account_elements()
        self._draw_ticket_elements()

    def _draw_buttons(self):
        self.back_button = ae.back_button_func(self.manager)
        self.create_button = ae.create_button_func(self.manager)
        self.delete_button = ae.delete_button_fun(self.manager)

    def _draw_account_elements(self):
        self.account_entry_title_tbox = ae.account_entry_slist_misc_func(self.manager)
        self.account_entry_slist = ae.account_entry_slist_func(self.manager, 
                                                               self.state.account_name_list)
        self.account_details_label, \
            self.selected_account_description_tbox = ae.account_details(self.manager)

    def _draw_ticket_elements(self):
        self.assigned_ticket_label = ae.assigned_ticket_label_func(self.manager)
        self.assigned_ticket_slist = ae.assigned_tickets(self.manager, 
                                                         self.state.assigned_ticket_list)

    def format_account_details(self, account: AccountDetails) -> str:
        formatted_account_details = (
            f"<b>Name:</b> {account.name}\n"
            f"<b>Organization:</b> {account.organization}\n"
            f"<b>Email:</b> {account.email}\n"
            f"<b>Contact:</b> {account.contact}\n"
            f"<b>Picture Filename:</b> {account.picture_path}"
        )
        return formatted_account_details

    def display_confirm_window(self) -> None:
        self.state.account_delete_confirm_window, self.confirm_delete_yes_button, \
            self.confirm_delete_no_button = ae.account_delete_confirm_window_func(self.manager)

    def refresh_account_list(self, updated_account_list) -> None:
        self.account_entry_slist.set_item_list(updated_account_list)
        self.state.account_id_name_map = self.state.account_id_name_mapper()

    def refresh_assigned_tickets(self, assigned_ticket_list) -> None:
        self.assigned_ticket_slist.set_item_list(assigned_ticket_list)


class AccountEventHandler:

    def __init__(self, pygame_manager, state_manager: AccountStateManager, ui_manager: AccountUIManager, 
                 sound_manager: ButtonSoundManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager
        
    def handle_account_selection(self) -> None:
        self.button_sfx.play_sfx(constants.MENU_BUTTON_SFX)
        self._update_account_textbox()

    def _update_account_textbox(self) -> None:
        account = self.state.fetch_account_details()
        account_details = self.ui.format_account_details(account)
        self.ui.selected_account_description_tbox.set_text(account_details)
        self.state.assigned_ticket_list = self.state.fetch_assigned_tickets()
        self.ui.refresh_assigned_tickets(self.state.assigned_ticket_list)

    def handle_button_pressed(self, event) -> Optional[ManagementButtonAction]:
        if event.ui_element == self.ui.back_button:
            return ManagementButtonAction.EXIT
        
        if event.ui_element == self.ui.create_button:
            return ManagementButtonAction.CREATE
        
        if event.ui_element == self.ui.delete_button and \
            self.state.selected_account is not None:
            return ManagementButtonAction.DELETE
        
        if self.state.account_delete_confirm_window and \
            event.ui_element == self.ui.confirm_delete_yes_button:
            return ManagementButtonAction.CONFIRM_DELETE
        
        if self.state.account_delete_confirm_window and \
            event.ui_element == self.ui.confirm_delete_no_button:
            return ManagementButtonAction.CANCEL_DELETE      

    
class AccountManagementController:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface  = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = AccountStateManager(self.connect, self.cursor)
        self.ui = AccountUIManager(self.manager, self.state)
        self.event_handler = AccountEventHandler(self.manager, self.state, self.ui, self.button_sfx)
    
    def account_management_loop(self) -> None:
        running = True
        while running:
            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()

            for event in events:
                if not self._handle_events(event):
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)

    def _handle_events(self, event) -> bool:
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.account_entry_slist:
            self.state.selected_account = event.text
            self.event_handler.handle_account_selection()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)
            
            if button_event == ManagementButtonAction.EXIT:
                return self._handle_exit_action()

            button_action_map = {
                ManagementButtonAction.CREATE: self._handle_create_action,
                ManagementButtonAction.DELETE: self._handle_delete_action,
                ManagementButtonAction.CONFIRM_DELETE: self._handle_confirm_delete_action,
                ManagementButtonAction.CANCEL_DELETE: self._handle_cancel_delete_action,
            }    

            button_action = button_action_map.get(button_event)
            if button_action:
                button_action()

        self.manager.process_events(event)
        return True
    
    def _handle_create_action(self) -> None:
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        account_creation_page = AccountCreationController(self.state.connect, self.state.cursor)
        self.state.account_name_list = account_creation_page.account_creation_loop()
        self.ui.refresh_account_list(self.state.account_name_list)

    def _handle_delete_action(self) -> None:
        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.ui.display_confirm_window()

    def _handle_confirm_delete_action(self) -> None:
        self.button_sfx.play_sfx(constants.DELETE_BUTTON_SFX)
        self.state.account_delete_confirm_window.kill()
        self.state.delete_selected_account()
        self.state.account_name_list = self.state.fetch_account_names()
        self.ui.refresh_account_list(self.state.account_name_list)

    def _handle_cancel_delete_action(self) -> None:
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        self.state.account_delete_confirm_window.kill()

    def _handle_exit_action(self) -> False:
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return False