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
    POS = Position(40, 35, 315, 75)


class TicketListTitle(DrawElement):
    POS = Position(0, 0, 265, 30)
    INPUT = "TICKET LIST"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -470)


class TicketList(DrawElement):
    POS = Position(0, 0, 350, 460)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class TicketLabel(DrawElement):
    POS = Position(360, 10, 150, 30)
    INPUT = "TICKET DETAILS"


class TicketTitleTextBox(DrawElement):
    POS = Position(375, 35, 405, 30)
    INPUT = ""


class TicketDescriptionTextBox(DrawElement):
    POS = Position(375, 70, 405, 400)
    INPUT = "SELECT A TICKET"


class AccountLabel(DrawElement):
    POS = Position(370, 480, 195, 35)
    INPUT = "CALLER ACCOUNT DETAILS"


class AccountDescriptionTextBox(DrawElement):
    POS = Position(375, 510, 405, 130)
    INPUT = ""


class DeleteConfirmWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: Delete Ticket"


class DeleteConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "Delete selected ticket?"
    ANCHOR = {'center':'center'}


class DeleteYesButton(DrawElement):
    POS = (10, 10, 100, 40)
    INPUT = "YES"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(185, -10)


class DeleteNoButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "NO"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)