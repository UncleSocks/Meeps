import pygame
import pygame_gui
from dataclasses import dataclass

import init
import sound_manager
import constants
import elements.accounts_elements as account_elements
from queries import SqliteQueries



@dataclass
class AccountDetails:
    id: int = 0
    name: str = ""
    organization: str = ""
    email: str = ""
    contact: str = ""
    picture_path: str = ""


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
                             self.account.picture_path)
        
        self.cursor.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)', new_account_entry)
        self.connect.commit()


class AccountCreationUIManager():

    def __init__(self, manager):
        self.manager = manager
        self.build_ui()

    def build_ui(self):
        self.back_button = account_elements.back_button_func(self.manager)
        self.add_account_button = account_elements.add_new_account_button_func(self.manager)
        
        self.account_name_label, self.new_account_name_tentry = account_elements.new_account_name_tentry_func(self.manager)
        self.account_organization_label, self.new_account_organization_tentry = account_elements.new_account_organization_func(self.manager)
        self.account_email_label, self.new_account_email_tentry = account_elements.new_account_email_func(self.manager)
        self.account_contact_label, self.new_account_contact_tentry = account_elements.new_account_contact_func(self.manager)
        self.account_picture_path_label, self.new_account_picture_path_tentry = account_elements.new_account_picture_path_func(self.manager)
        
        self.add_account_image = account_elements.add_account_image_func(self.manager, constants.ADD_ACCOUNT_IMAGE_PATH)
        self.new_account_image_border = account_elements.new_account_image_border_func(self.manager)

    def refresh_creation_page(self):
        self.new_account_name_tentry.set_text("")
        self.new_account_organization_tentry.set_text("")
        self.new_account_email_tentry.set_text("")
        self.new_account_contact_tentry.set_text("")
        self.new_account_picture_path_tentry.set_text("")


class AccountCreationEventHandler():

    def __init__(self, pygame_manager, state_manager: AccountCreationStateManager, ui_manager: AccountCreationUIManager):
        self.manager = pygame_manager
        self.state = state_manager
        self.ui = ui_manager
        self.button_sfx = sound_manager.ButtonSoundManager()

    def handle_button_pressed(self, event):
        if event.ui_element == self.ui.back_button:
            return self._handle_back_button()

        if event.ui_element == self.ui.add_account_button:
            self._handle_add_button()

        if self.state.account_confirm_window and event.ui_element == self.account_confirm_close_button:
            self.ui.refresh_creation_page()
            self.state.account_confirm_window.kill()
            self.state.account = AccountDetails()

    def _handle_back_button(self):
        self.button_sfx.play_sfx(constants.BACK_BUTTON_SFX)
        return constants.EXIT_ACTION

    def _handle_add_button(self):
        self._get_new_account_details()

        if not all([
            self.state.account.name,
            self.state.account.organization,
            self.state.account.email,
            self.state.account.contact,
            self.state.account.picture_path
        ]):
            return

        self.button_sfx.play_sfx(constants.MODIFY_BUTTON_SFX)
        self.state.add_new_account()

        self.state.account_confirm_window, self.account_confirm_close_button = account_elements.account_confirm_window_func(self.manager)
        self.state.account_confirm_window.show()

    def _get_new_account_details(self):
        self.state.account.name = self.ui.new_account_name_tentry.get_text()
        self.state.account.organization = self.ui.new_account_organization_tentry.get_text()
        self.state.account.email = self.ui.new_account_email_tentry.get_text()
        self.state.account.contact = self.ui.new_account_contact_tentry.get_text()

        self.state.account.picture_path = self.ui.new_account_picture_path_tentry.get_text()
        account_elements.new_account_image_func(self.manager, self.state.account.picture_path)


class AccountCreationController():

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        self.pygame_renderer = init.PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.window_surface  = self.pygame_renderer.window_surface

        self.state = AccountCreationStateManager(self.connect, self.cursor)
        self.ui = AccountCreationUIManager(self.manager)
        self.event_handler = AccountCreationEventHandler(self.manager, self.state, self.ui)

    def account_creation_loop(self):
        running = True
        while running:

            time_delta = self.pygame_renderer.clock.tick(constants.FPS) / constants.MILLISECOND_PER_SECOND

            events = pygame.event.get()
            for event in events:
                if not self._handle_events(event):
                    running = False

            self.pygame_renderer.ui_renderer(time_delta)

        updated_account_list = self.state.fetch_account_names()
        return updated_account_list

    def _handle_events(self, event):
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                button_action = self.event_handler.handle_button_pressed(event)

                if button_action == constants.EXIT_ACTION:
                    return False
            
            self.manager.process_events(event)
            return True