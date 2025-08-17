from elements.element_creator import DrawElement, \
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


class AccountListTitle(DrawElement):
    POS = Position(0, 0, 265, 30)
    INPUT = "ACCOUNT LIST"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -470)


class AccountList(DrawElement):
    POS = Position(0, 0, 350, 460)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class AccountLabel(DrawElement):
    POS = Position(360, 10, 150, 30)
    INPUT = "ACCOUNT DETAILS"


class AccountDescriptionTextBox(DrawElement):
    POS = Position(375, 40, 405, 160)
    INPUT = "SELECT AN ACCOUNT"


class AssignedTicketLabel(DrawElement):
    POS = Position(365, 220, 150, 30)
    INPUT = "ASSIGNED TICKETS"


class AssignedTicketList(DrawElement):
    POS = Position(375, 250, 405, 390)


class DeleteWarningWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: Delete Threat"


class DeleteWarningLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "Guest account cannot be delete."
    ANCHOR = {'center':'center'}


class DeleteWarningButton(DrawElement):
    POS = Position(10, 10, 200, 40)
    INPUT = "OK"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)


class DeleteConfirmWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: Delete Threat"


class DeleteConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "Delete selected account?"
    ANCHOR = {'center':'center'}


class DeleteConfirmWarningLabel(DrawElement):
    POS = Position(0, -40, 350, 200)
    INPUT = "[!] This will delete associated tickets."
    ANCHOR = {'center':'center'}


class DeleteNoButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "No"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)


class DeleteYesButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "Yes"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(185, -10)


class NewAccountImage(DrawElement):
    POS = Position(50, 15, 375, 75)


class NewAccountNameLabel(DrawElement):
    POS = Position(20, 100, 100, 30)
    INPUT = "ACCOUNT NAME"


class NewAccountNameTextEntry(DrawElement):
    POS = Position(15, 125, 765, 30)


class NewAccountOrganizationLabel(DrawElement):
    POS = Position(20, 170, 100, 30)
    INPUT = "ORGANIZATION NAME"


class NewAccountOrganizationTextEntry(DrawElement):
    POS = Position(15, 195, 765, 30)


class NewAccountEmailLabel(DrawElement):
    POS = Position(20, 240, 50, 30)
    INPUT = "EMAIL"


class NewAccountEmailTextEntry(DrawElement):
    POS = Position(15, 265, 765, 30)


class NewAccountContactLabel(DrawElement):
    POS = Position(20, 310, 65, 30)
    INPUT = "CONTACT DETAILS"


class NewAccountContactTextEntry(DrawElement):
    POS = Position(15, 335, 765, 30)


class NewAccountPictureFileLabel(DrawElement):
    POS = Position(10, 380, 150, 30)
    INPUT = "PROFILE PICTURE"


class NewAccountPictureFileTextEntry(DrawElement):
    POS = Position(15, 405, 475, 30)


class NewAccountPictureBorder(DrawElement):
    POS = Position(545, 405, 190, 190)


class NewAccountPicture(DrawElement):
    POS = Position(550, 410, 180, 180)


class AddAccountButton(DrawElement):
    POS = Position(15, 455, 120, 40)
    INPUT = "ADD ACCOUNT"


class ConfirmWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: New Account"


class ConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "ACCOUNT CREATED SUCCESSFULLY"
    ANCHOR = {'center':'center'}


class ConfirmButton(DrawElement):
    POS = Position(10, 10, 200, 40)
    INPUT = "OK"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)