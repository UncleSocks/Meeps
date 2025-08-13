import constants
from .element_creator import DrawElement, \
    Position, Offset, AnchorConfig



class BackButton(DrawElement):
    POS = Position(5, 5, 30, 30)
    INPUT = "<"
    ANCHOR = {'bottom':'bottom', 'left':'left'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(10, -610)


class CreateButton(DrawElement):
    POS = Position(0, 0, 45, 30)
    INPUT = "+"
    ANCHOR = {'bottom':'bottom', 'left':'left'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(320, -470)


class DeleteButton(DrawElement):
    POS = Position(0, 0, 45, 30)
    INPUT = "-"
    ANCHOR = {'bottom':'bottom', 'left':'left'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(280, -470)
    

class TitleImage(DrawElement):
    POS = Position(20, 35, 345, 70)
    INPUT = constants.ACCOUNT_MANAGEMENT_IMAGE_PATH


class AccountListTitle(DrawElement):
    POS = Position(0, 0, 265, 30)
    INPUT = "ACCOUNT LIST"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -470)


class AccountList(DrawElement):
    POS = (0, 0, 350, 460)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class AccountLabel(DrawElement):
    POS = (360, 10, 150, 30)
    INPUT = "ACCOUNT DETAILS"


class AccountDescriptionTextBox(DrawElement):
    POS = (375, 40, 405, 160)
    INPUT = "SELECT AN ACCOUNT"


class AssignedTicketLabel(DrawElement):
    POS = (365, 220, 150, 30)
    INPUT = "ASSIGNED TICKETS"


class AssignedTicketList(DrawElement):
    POS = (375, 250, 405, 390)


class DeleteWarningWindow(DrawElement):
    POS = (0, 0, 400, 200)
    INPUT = "Meeps Security: Delete Threat"


class DeleteWarningLabel(DrawElement):
    POS = (0, -10, 300, 200)
    INPUT = "Guest account cannot be delete."
    ANCHOR = {'center':'center'}


class DeleteWarningButton(DrawElement):
    POS = (10, 10, 200, 40)
    INPUT = "OK"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)


class DeleteConfirmWindow(DrawElement):
    POS = (0, 0, 400, 200)
    INPUT = "Meeps Security: Delete Threat"


class DeleteConfirmLabel(DrawElement):
    POS = (0, -10, 300, 200)
    INPUT = "Delete selected account?"
    ANCHOR = {'center':'center'}


class DeleteConfirmWarningLabel(DrawElement):
    POS = (0, -40, 350, 200)
    INPUT = "[!] This will delete associated tickets."
    ANCHOR = {'center':'center'}


class DeleteNoButton(DrawElement):
    POS = (10, 10, 100, 40)
    INPUT = "No"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)


class DeleteYesButton(DrawElement):
    POS = (10, 10, 100, 40)
    INPUT = "Yes"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(185, -10)


class NewAccountImage(DrawElement):
    POS = (50, 15, 375, 75)
    INPUT = constants.ADD_ACCOUNT_IMAGE_PATH