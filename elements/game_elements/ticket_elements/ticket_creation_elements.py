from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig




class NewTicketImage(DrawElement):
    POS = Position(50, 5, 250, 75)


class NewTicketTitle(DrawElement):  
    POS = Position(15, 125, 765, 30)
    INPUT = "ENTER TICKET TITLE"


class NewTicketDescription(DrawElement):
    POS = Position(15, 160, 765, 200)
    INPUT = "ENTER TICKET DESCRIPTION"


class AccountDropDownLabel(DrawElement):
    POS = Position(60, 78, 285, 45)
    INPUT = "SELECT TICKET CALLER ACCOUNT"


class AccountDropDown(DrawElement):
    POS = Position(325, 85, 455, 30)
    STARTING_POINT = "Guest"


class AddTicketButton(DrawElement):
    POS = Position(600, 30, 180, 45)
    INPUT = "CREATE TICKET"


class ThreatListTextBox(DrawElement):
    POS = Position(0, 0, 300, 30)
    INPUT = "TICKET RESOLUTION"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -250)


class ThreatList(DrawElement):
    POS = Position(0, 0, 300, 240)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class ThreatDescription(DrawElement):
    POS = Position(325, 370, 455, 270)
    INPUT = "SELECT A THREAT"


class ConfirmWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: New Account"


class ConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "TICKET CREATED SUCCESSFULLY"
    ANCHOR = {'center':'center'}