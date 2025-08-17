from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig



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