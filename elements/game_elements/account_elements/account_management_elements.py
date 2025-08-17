from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig



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
    INPUT = "Meeps Security: Delete Account"


class DeleteConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "Delete selected account?"
    ANCHOR = {'center':'center'}


class DeleteConfirmWarningLabel(DrawElement):
    POS = Position(0, -40, 350, 200)
    INPUT = "[!] This will delete associated tickets."
    ANCHOR = {'center':'center'}