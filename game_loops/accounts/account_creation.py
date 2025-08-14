import pygame
import pygame_gui
from dataclasses import dataclass

import init
from sound_manager import ButtonSoundManager
import constants
from constants import ButtonAction
import elements.accounts_elements as account_elements
import elements.account_elements_s as ae
from queries import SqliteQueries



@dataclass
class AccountDetails:
    id: int = 0
    name: str = ""
    organization: str = ""
    email: str = ""
    contact: str = ""
    picture_file: str = ""


class AccountCreationStateManager():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor
        self.query = SqliteQueries(self.cursor)
        self.account = AccountDetails()
        self.account_confirm_window = False

    def fetch_account_names(self):
        account_name_list = self.query.account_name_list_query()
        return account_name_list
    
    def _generate_new_account_id(self):
        max_id = self.query.max_account_id_query()
        account_id = max_id + 1
        return account_id
    
    def add_new_account(self):
        self.account.id = self._generate_new_account_id()
        new_account_entry = (self.account.id,
                             self.account.name,
                             self.account.organization,
                             self.account.email,
                             self.account.contact,
                             self.account.picture_file)
        
        self.cursor.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)', new_account_entry)
        self.connect.commit()


class AccountCreationUIManager():

    def __init__(self, pygame_manager, state_manager: AccountCreationStateManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.draw_account_creation_ui()

    def draw_account_creation_ui(self):
        self._draw_images()
        self._draw_buttons()
        self._draw_account_creation_elements()
        
    def _draw_images(self):
        add_account_image = ae.NewAccountImage(self.manager)
        load_add_account_image = pygame.image.load(constants.ADD_ACCOUNT_IMAGE_PATH)
        add_account_image.INPUT = load_add_account_image
        self.add_account_image = add_account_image.draw_image()

    def _draw_buttons(self):
        self.back_button = ae.BackButton(self.manager).draw_button()
        self.add_account_button = ae.AddAccountButton(self.manager).draw_button()

    def _draw_account_creation_elements(self):
        self.account_name_label = ae.NewAccountNameLabel(self.manager).draw_label()
        self.account_name_entry = ae.NewAccountNameTextEntry(self.manager).draw_textentrybox()
        
        self.account_organization_label = ae.NewAccountOrganizationLabel(self.manager).draw_label()
        self.account_organization_entry = ae.NewAccountOrganizationTextEntry(self.manager).draw_textentrybox()

        self.account_email_label = ae.NewAccountEmailLabel(self.manager).draw_label()
        self.account_email_entry = ae.NewAccountEmailTextEntry(self.manager).draw_textentrybox()

        self.account_contact_label = ae.NewAccountContactLabel(self.manager).draw_label()
        self.account_contact_entry = ae.NewAccountContactTextEntry(self.manager).draw_textentrybox()

        self.account_picture_file_label = ae.NewAccountPictureFileLabel(self.manager).draw_label()
        self.account_picture_file = ae.NewAccountPictureFileTextEntry(self.manager).draw_textentrybox()

        self.account_picture_border = ae.NewAccountPictureBorder(self.manager).draw_textentrybox()

    def capture_new_account_details(self):
        self.state.account.name = self.account_name_entry.get_text()
        self.state.account.organization = self.account_organization_entry.get_text()
        self.state.account.email = self.account_email_entry.get_text()
        self.state.account.contact = self.account_contact_entry.get_text()
        self._set_new_account_image()

    def _set_new_account_image(self):
        self.state.account.picture_file = self.account_picture_file.get_text()
        account_picture_path = "".join([constants.ACCOUNT_ASSETS_PATH, self.state.account.picture_file])
        account_picture = ae.NewAccountPicture(self.manager)

        try:
            account_picture_load = pygame.image.load(account_picture_path)
        except (pygame.error, FileNotFoundError):
            account_picture_load = pygame.image.load(constants.GUEST_ACCOUNT_IMAGE_PATH)

        account_picture.INPUT = account_picture_load
        self.account_picture = account_picture.draw_image()

    def display_confirm_window(self):
        self.state.account_confirm_window, \
            self.account_confirm_close_button = account_elements.account_confirm_window_func(self.manager)

    def refresh_creation_page(self):
        self.account_name_entry.set_text("")
        self.account_organization_entry.set_text("")
        self.account_email_entry.set_text("")
        self.account_contact_entry.set_text("")
        self.account_picture_file.set_text("")


class AccountCreationEventHandler():

    def __init__(self, pygame_manager, state_manager: AccountCreationStateManager, ui_manager: AccountCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return ButtonAction.EXIT

        if event.ui_element == self.ui.add_account_button:
            return ButtonAction.CREATE

        if self.state.account_confirm_window \
            and event.ui_element == self.ui.account_confirm_close_button:
            return ButtonAction.CONFIRM_CREATE


class AccountCreationController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface  = self.pygame_renderer.window_surface
        self.button_sfx = ButtonSoundManager()

        self.state = AccountCreationStateManager(self.connect, self.cursor)
        self.ui = AccountCreationUIManager(self.manager, self.state)
        self.event_handler = AccountCreationEventHandler(self.manager, self.state, self.ui)

    def account_creation_loop(self):
        running = True
        while running:
            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND
            events = pygame.event.get()
            
            for event in events:
                if self._handle_events(event) == ButtonAction.EXIT:
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)

        updated_account_list = self.state.fetch_account_names()
        return updated_account_list

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

        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.add_new_account()
        self.ui.display_confirm_window()

    def _handle_confirm_button(self) -> None:
        self.ui.refresh_creation_page()
        self.state.account_confirm_window.kill()
        self.state.account = AccountDetails()

    def _handle_exit_action(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return ButtonAction.EXIT