from enum import Enum




class Settings(Enum):
    VERSION = 'v2025.1.0 BETA'
    DATABASE = 'data/data.db'
    FPS = 60
    MS_PER_SECOND = 1000


class WindowConfig(Enum):
    WIDTH = 800
    HEIGHT = 650
    CAPTION = "Meeps_Security_Responder.exe"
    ICON = 'assets/images/static/icon.png'
    THEME = 'theme.json'
    BACKGROUND = 0,0,0 #RGB values for black.


class StateTracker(Enum):
    MAIN_MENU = 'main_menu'
    SHIFT = 'shift'
    SHIFT_REPORT = 'shift_report'
    TICKET_MANAGEMENT = 'ticket_management'
    TICKET_CREATION = 'ticket_creation'
    ACCOUNT_MANAGEMENT = 'account_management'
    ACCOUNT_CREATION = 'account_creation'
    THREAT_MANAGEMENT = 'threat_management'
    THREAT_CREATION = 'threat_creation'
    EXIT = 'exit'


class ButtonAction(Enum):
    EXIT = 'exit'
    SHIFT = 'shift'
    TICKET = 'ticket'
    ACCOUNT = 'account'
    THREAT = 'threat'
    SUBMIT = 'submit'
    ANSWER = 'answer'
    CREATE = 'create'
    CONFIRM_CREATE = 'confirm_create'
    DELETE = 'delete'
    CONFIRM_DELETE = 'confirm_delete'
    CANCEL_DELETE = 'cancel_delete'
    CONTINUE = 'continue'
    SHIFT_REPORT = 'shift_report'


class Timers(Enum):
    MIN_CALL_INTERVAL = 5
    MAX_CALL_INTERVAL = 12


class AssetBasePath(Enum):
    THREAT_ASSETS = 'data/images/threats/'
    ACCOUNT_ASSETS = 'data/images/accounts/'


class ImagePaths(Enum):
    TITLE = 'assets/images/static/title.png'
    TICKET_MANAGEMENT = 'assets/images/static/ticket_mngr.png'
    TICKET_CREATION = 'assets/images/static/new_ticket.png'
    THREAT_MANAGEMENT = 'assets/images/static/threat_database.png'
    THREAT_CREATION = 'assets/images/static/add_threat.png'
    ACCOUNT_MANAGEMENT = 'assets/images/static/account_manager.png'
    ACCOUNT_CREATION = 'assets/images/static/add_account.png'


class DefaultImages(Enum):
    THREAT = 'assets/images/default/threat.png'
    GUEST_ACCOUNT = 'assets/images/default/guest.png'
    BLANK = 'assets/images/static/blank.png'


class MusicPaths(Enum):
    BACKGROUND_MUSIC = 'assets/sounds/music/background.mp3'
    INCOMING_CALL = 'assets/sounds/music/incoming_call.mp3'


class SFXPath(Enum):
    BACK_BUTTON = 'assets/sounds/sfx/back_button.mp3'
    MENU_BUTTON = 'assets/sounds/sfx/menu_button.mp3'
    MODIFY_BUTTON = 'assets/sounds/sfx/modify_button.mp3'
    DELETE_BUTTON = 'assets/sounds/sfx/delete_button.mp3'
    CONFIRM_BUTTON = 'assets/sounds/sfx/confirm_button.mp3'
    LIST_BUTTON = 'assets/sounds/sfx/list_click.mp3'
    CORRECT_SUBMISSION = 'assets/sounds/sfx/correct_submit.mp3'
    INCORRECT_SUBMISSION = 'assets/sounds/sfx/incorrect_submit.mp3'


class MixerChannels(Enum):
    BUTTON_SFX = 0
    INCOMING_CALL = 1


class ButtonSFX(Enum):
    BACK_BUTTON = 'back_button'
    MENU_BUTTON = 'menu_button'
    MODIFY_BUTTON = 'modify_button'
    DELETE_BUTTON = 'delete_button'
    CONFIRM_BUTTON = 'confirm_button'
    LIST_BUTTON = 'list_button'
    CORRECT_SUBMISSION = 'correct_submission'
    INCORRECT_SUBMISSION = 'incorrect_submission'