import pygame
import pygame_gui
from typing import Optional
from dataclasses import dataclass

import elements.game_elements.account_elements.account_management_elements as ame
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, \
    ImagePaths, ButtonSFX
from init import PygameRenderer
from managers.sound_manager import ButtonSoundManager
from managers.db_manager import DatabaseQueries, DatabaseRemovals




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
        self.query = DatabaseQueries(self.cursor)
        self.delete = DatabaseRemovals(self.cursor, self.connect)
        self.account_variables()

    def account_variables(self) -> None:
        self.account_name_list = self.fetch_account_names()
        self.account_id_name_map = self.account_id_name_mapper()
        self.assigned_ticket_list = []
        self.selected_account = None
        self.account_delete_confirm_window = None
        self.account_delete_warning_window = None

    def account_id_name_mapper(self) -> dict:
        account_id_name_list = self.query.fetch_account_names_ids()
        account_id_name_map = {account[1]: account[0] for account in account_id_name_list}
        return account_id_name_map

    def fetch_account_names(self) -> list:
        account_name_list = self.query.fetch_account_names()
        return account_name_list

    def fetch_account_details(self) -> tuple:
        selected_account_id = self.account_id_name_map[self.selected_account]
        print(type(selected_account_id))
        account_details = self.query.fetch_account_details(selected_account_id)
        account = AccountDetails(*account_details)
        return account
    
    def fetch_assigned_tickets(self) -> list:
        selected_account_id = self.account_id_name_map[self.selected_account]
        assigned_tickets_list = self.query.fetch_assigned_tickets(selected_account_id)
        return assigned_tickets_list
    
    def delete_selected_account(self) -> None:
        selected_account_id = self.account_id_name_map[self.selected_account]
        self.delete.delete_account(selected_account_id)
    

class AccountUIManager:

    def __init__(self, manager, state_manager: AccountStateManager):
        self.manager = manager
        self.state = state_manager
        self.draw_ui_elements()

    def draw_ui_elements(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_account_elements()
        self._draw_ticket_elements()

    def _draw_images(self):
        account_manager_image = ame.TitleImage(self.manager)
        load_account_manager_image = pygame.image.load(ImagePaths.ACCOUNT_MANAGEMENT.value)
        account_manager_image.INPUT = load_account_manager_image
        self.account_manager_image = account_manager_image.draw_image()
        
    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.create_button = se.CreateButton(self.manager).draw_button()
        self.delete_button = se.DeleteButton(self.manager).draw_button()

    def _draw_account_elements(self):
        self.account_entry_title_tbox = ame.AccountListTitle(self.manager).draw_textbox()

        account_selection_list = ame.AccountList(self.manager)
        account_selection_list.INPUT = self.state.account_name_list
        self.account_selection_list = account_selection_list.draw_selectionlist()
        
        self.account_details_label = ame.AccountLabel(self.manager).draw_label()
        self.selected_account_description = ame.AccountDescriptionTextBox(self.manager).draw_textbox()

    def _draw_ticket_elements(self):
        self.assigned_ticket_label = ame.AssignedTicketLabel(self.manager).draw_label()

        ticket_selection_list = ame.AssignedTicketList(self.manager)
        ticket_selection_list.INPUT = self.state.assigned_ticket_list
        self.ticket_selection_list = ticket_selection_list.draw_selectionlist()

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
        self.state.account_delete_confirm_window = ame.DeleteConfirmWindow(self.manager).draw_window()

        confirm_delete_label = ame.DeleteConfirmLabel(self.manager)
        confirm_delete_label.CONTAINER = self.state.account_delete_confirm_window
        self.confirm_delete_label = confirm_delete_label.draw_label()

        confirm_delete_warning_label = ame.DeleteConfirmWarningLabel(self.manager)
        confirm_delete_warning_label.CONTAINER = self.state.account_delete_confirm_window
        self.confirm_delete_warning_label = confirm_delete_warning_label.draw_label()

        confirm_delete_yes_button = se.DeleteYesButton(self.manager)
        confirm_delete_yes_button.CONTAINER = self.state.account_delete_confirm_window
        self.confirm_delete_yes_button = confirm_delete_yes_button.draw_button()

        confirm_delete_no_button = se.DeleteNoButton(self.manager)
        confirm_delete_no_button.CONTAINER = self.state.account_delete_confirm_window
        self.confirm_delete_no_button = confirm_delete_no_button.draw_button()
        
    def display_warning_window(self) -> None:
        self.state.account_delete_warning_window = ame.DeleteWarningWindow(self.manager).draw_window()

        delete_warning_label = ame.DeleteWarningLabel(self.manager)
        delete_warning_label.CONTAINER = self.state.account_delete_warning_window
        self.delete_warning_label = delete_warning_label.draw_label()

        warning_continue_button = ame.DeleteWarningButton(self.manager)
        warning_continue_button.CONTAINER = self.state.account_delete_warning_window
        self.warning_continue_button = warning_continue_button.draw_button()

    def refresh_account_list(self, updated_account_list) -> None:
        self.account_selection_list.set_item_list(updated_account_list)
        self.state.account_id_name_map = self.state.account_id_name_mapper()

    def refresh_assigned_tickets(self, assigned_ticket_list) -> None:
        self.ticket_selection_list.set_item_list(assigned_ticket_list)


class AccountEventHandler:

    def __init__(self, pygame_manager, state_manager: AccountStateManager, ui_manager: AccountUIManager, 
                 sound_manager: ButtonSoundManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager
        
    def handle_account_selection(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.LIST_BUTTON)
        self._update_account_textbox()

    def _update_account_textbox(self) -> None:
        account = self.state.fetch_account_details()
        account_details = self.ui.format_account_details(account)
        self.ui.selected_account_description.set_text(account_details)
        self.state.assigned_ticket_list = self.state.fetch_assigned_tickets()
        self.ui.refresh_assigned_tickets(self.state.assigned_ticket_list)

    def handle_button_pressed(self, event) -> Optional[ButtonAction]:
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT
        
        if event.ui_element == self.ui.create_button:
            return ButtonAction.CREATE
        
        if event.ui_element == self.ui.delete_button \
            and self.state.selected_account is not None:
            return ButtonAction.DELETE
        
        if self.state.account_delete_confirm_window \
            and event.ui_element == self.ui.confirm_delete_yes_button:
            return ButtonAction.CONFIRM_DELETE
        
        if self.state.account_delete_confirm_window \
            and event.ui_element == self.ui.confirm_delete_no_button:
            return ButtonAction.CANCEL_DELETE

        if self.state.account_delete_warning_window \
            and event.ui_element == self.ui.warning_continue_button:
            return ButtonAction.CONTINUE     

    
class AccountManagementController:

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
        self.window_surface  = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = AccountStateManager(self.connect, self.cursor)
        self.ui = AccountUIManager(self.manager, self.state)
        self.event_handler = AccountEventHandler(self.manager, self.state, self.ui, self.button_sfx)
    
    def game_loop(self, events) -> None:
        for event in events:
            action = self._handle_events(event)

            if action == ButtonAction.EXIT:
                return StateTracker.MAIN_MENU
            if action == ButtonAction.CREATE:
                return StateTracker.ACCOUNT_CREATION

    def _handle_events(self, event) -> bool:
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION \
            and event.ui_element == self.ui.account_selection_list:
            self.state.selected_account = event.text
            self.event_handler.handle_account_selection()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_event = self.event_handler.handle_button_pressed(event)

            if button_event == ButtonAction.EXIT:
                return self._handle_exit_action()
            
            if button_event == ButtonAction.CREATE:
                return self._handle_create_action()

            button_action_map = {
                ButtonAction.DELETE: self._handle_delete_action,
                ButtonAction.CONFIRM_DELETE: self._handle_confirm_delete_action,
                ButtonAction.CANCEL_DELETE: self._handle_cancel_delete_action,
                ButtonAction.CONTINUE: self._handle_continue_action
            }    

            button_action = button_action_map.get(button_event)
            if button_action:
                button_action()

        self.manager.process_events(event)
        return True
    
    def _handle_create_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.CREATE
    
    def _handle_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        if self.state.selected_account == 'Guest':
            self.ui.display_warning_window()
        else:
            self.ui.display_confirm_window()

    def _handle_confirm_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.DELETE_BUTTON)
        self.state.account_delete_confirm_window.kill()
        self.state.delete_selected_account()
        self.state.account_name_list = self.state.fetch_account_names()
        self.ui.refresh_account_list(self.state.account_name_list)

    def _handle_cancel_delete_action(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.state.account_delete_confirm_window.kill()

    def _handle_continue_action(self) -> None:
        self.state.account_delete_warning_window.kill()

    def _handle_exit_action(self) -> False:
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT