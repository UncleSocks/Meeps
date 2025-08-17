from constants import Settings
from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig



class MenuImage(DrawElement):
    POS = Position(165, 80, 500, 190)


class TitleSloganLabel(DrawElement):
    POS = Position(150, 180, 500, 190)
    INPUT = "Guarding the Cyberspace"


class ShiftButton(DrawElement):
    POS = Position(0, 30, 300, 40)
    INPUT = "START SHIFT"
    ANCHOR = {'center':'center'}


class TicketButton(DrawElement):
    POS = Position(0, -255, 300, 40)
    INPUT = "MANAGE TICKETS"
    ANCHOR = {'centerx':'centerx', 'bottom':'bottom'}


class AccountButton(DrawElement):
    POS = Position(0, -195, 300, 40)
    INPUT = "MANAGE ACCOUNTS"
    ANCHOR = {'centerx':'centerx', 'bottom':'bottom'}


class ThreatButton(DrawElement):
    POS = Position(0, -135, 300, 40)
    INPUT = "THREAT DATABASE"
    ANCHOR = {'centerx':'centerx', 'bottom':'bottom'}


class LogOffButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "LOG OFF"


class VersionLabel(DrawElement):
    POS = Position(0, 0, 200, 150)
    INPUT = Settings.VERSION.value
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(-35, 60)


class GitHubLabel(DrawElement):
    POS = Position(0, 0, 200, 200)
    INPUT = "GitHub @unclesocks"
    ANCHOR = {'right':'right', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(0, 85)