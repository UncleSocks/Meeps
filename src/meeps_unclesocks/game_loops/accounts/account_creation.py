import os
from dataclasses import dataclass, astuple

import pygame
import pygame_gui

import elements.game_elements.account_elements.account_creation_elements as ace
import elements.game_elements.shared_elements as se
from constants import StateTracker, ButtonAction, \
    AssetBasePath, ImagePaths, DefaultImages, ButtonSFX
from init import PygameRenderer
from managers.sound_manager import ButtonSoundManager
from managers.db_manager import DatabaseQueries, DatabaseModification




@dataclass
class AccountDetails:
    id: int = 0
    name: str = ""
    organization: str = ""
    email: str = ""
    contact: str = ""
    picture_file: str = ""


class AccountCreationStateManager:

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = DatabaseQueries(self.cursor)
        self.modify = DatabaseModification(self.cursor, self.connect)
        self.account = AccountDetails()
        self.confirm_window = False

    def fetch_account_names(self):
        account_name_list = self.query.fetch_account_names()
        return account_name_list
    
    def _generate_new_account_id(self):
        max_id = self.query.fetch_max_id(table='accounts')
        account_id = int(max_id or 0) + 1
        return account_id
    
    def add_new_account(self):
        self.account.id = self._generate_new_account_id()
        new_account_entry = astuple(self.account)
        self.modify.insert_entry(table='accounts', value=new_account_entry)


class AccountCreationUIManager:

    def __init__(self, pygame_manager, state_manager: AccountCreationStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.draw_account_creation_ui()

    def draw_account_creation_ui(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_account_creation_elements()
        
    def _draw_images(self):
        add_account_image = ace.NewAccountImage(self.manager)
        load_add_account_image = pygame.image.load(ImagePaths.ACCOUNT_CREATION.path)
        add_account_image.INPUT = load_add_account_image
        self.add_account_image = add_account_image.draw_image()

    def _draw_buttons(self):
        self.back_button = se.BackButton(self.manager).draw_button()
        self.add_account_button = ace.AddAccountButton(self.manager).draw_button()

    def _draw_account_creation_elements(self):
        self.account_name_label = ace.NewAccountNameLabel(self.manager).draw_label()
        self.account_organization_label = ace.NewAccountOrganizationLabel(self.manager).draw_label()
        self.account_email_label = ace.NewAccountEmailLabel(self.manager).draw_label()
        self.account_contact_label = ace.NewAccountContactLabel(self.manager).draw_label()
        self.account_picture_file_label = ace.NewAccountPictureFileLabel(self.manager).draw_label()

        self.account_name_entry = ace.NewAccountNameTextEntry(self.manager).draw_textentrybox()
        self.account_organization_entry = ace.NewAccountOrganizationTextEntry(self.manager).draw_textentrybox()
        self.account_email_entry = ace.NewAccountEmailTextEntry(self.manager).draw_textentrybox()
        self.account_contact_entry = ace.NewAccountContactTextEntry(self.manager).draw_textentrybox()        
        self.account_picture_file = ace.NewAccountPictureFileTextEntry(self.manager).draw_textentrybox()
        self.account_picture_border = ace.NewAccountPictureBorder(self.manager).draw_textentrybox()

    def text_entry_box_elements(self):
        return [
            self.account_name_entry,
            self.account_organization_entry,
            self.account_email_entry,
            self.account_contact_entry,   
            self.account_picture_file,
            self.account_picture_border
        ]

    def capture_new_account_details(self):
        self.state.account.name = self.account_name_entry.get_text()
        self.state.account.organization = self.account_organization_entry.get_text()
        self.state.account.email = self.account_email_entry.get_text()
        self.state.account.contact = self.account_contact_entry.get_text()
        self._set_new_account_image()

    def _set_new_account_image(self):
        self.state.account.picture_file = self.account_picture_file.get_text()
        account_picture_path = os.path.join(AssetBasePath.ACCOUNT_ASSETS.value, self.state.account.picture_file)
        account_picture = ace.NewAccountPicture(self.manager)

        try:
            account_picture_load = pygame.image.load(account_picture_path)
        except (pygame.error, FileNotFoundError):
            account_picture_load = pygame.image.load(DefaultImages.GUEST_ACCOUNT.path)

        account_picture.INPUT = account_picture_load
        self.account_picture = account_picture.draw_image()

    def display_confirm_window(self):
        self.state.confirm_window = ace.ConfirmWindow(self.manager).draw_window()

        confirm_label = ace.ConfirmLabel(self.manager)
        confirm_label.CONTAINER = self.state.confirm_window
        self.confirm_label = confirm_label.draw_label()

        confirm_button = se.ConfirmButton(self.manager)
        confirm_button.CONTAINER = self.state.confirm_window
        self.confirm_button = confirm_button.draw_button()

    def refresh_creation_page(self):
        for element in self.text_entry_box_elements():
            element.set_text("")
            

class AccountCreationEventHandler:

    def __init__(self, pygame_manager, state_manager: AccountCreationStateManager, ui_manager: AccountCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT

        if event.ui_element == self.ui.add_account_button:
            return ButtonAction.CREATE

        if self.state.confirm_window \
            and event.ui_element == self.ui.confirm_button:
            return ButtonAction.CONFIRM_CREATE


class AccountCreationController:

    def __init__(self, connect, cursor, manager):
        self.connect = connect
        self.cursor = cursor
        self.manager = manager

        self.pygame_renderer = PygameRenderer()
        self.window_surface  = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = AccountCreationStateManager(self.connect, self.cursor)
        self.ui = AccountCreationUIManager(self.manager, self.state)
        self.event_handler = AccountCreationEventHandler(self.manager, self.state, self.ui)

    def game_loop(self, events):            
        for event in events:
            action = self._handle_events(event)
            if action == ButtonAction.EXIT:
                return StateTracker.ACCOUNT_MANAGEMENT

    def _handle_events(self, event):
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                button_event = self.event_handler.handle_button_pressed(event)

                if button_event == ButtonAction.EXIT:
                    return self._handle_exit_action()

                button_action_map = {
                    ButtonAction.CREATE: self._handle_create_button,
                    ButtonAction.CONFIRM_CREATE: self._handle_confirm_button
                }

                button_action = button_action_map.get(button_event)
                if button_action:
                    button_action()
            
            self.manager.process_events(event)
            return True
    
    def _handle_create_button(self) -> None:
        self.ui.capture_new_account_details()

        if not all([
            self.state.account.name,
            self.state.account.organization,
            self.state.account.email,
            self.state.account.contact,
            self.state.account.picture_file
        ]):
            return

        self.button_sfx.play_sfx(ButtonSFX.MODIFY_BUTTON)
        self.state.add_new_account()
        self.ui.display_confirm_window()

    def _handle_confirm_button(self) -> None:
        self.button_sfx.play_sfx(ButtonSFX.CONFIRM_BUTTON)
        self.ui.refresh_creation_page()
        self.state.confirm_window.kill()
        self.state.account = AccountDetails()

    def _handle_exit_action(self):
        self.button_sfx.play_sfx(ButtonSFX.BACK_BUTTON)
        self.manager.clear_and_reset()
        return ButtonAction.EXIT