from pygame_gui.core import ObjectID

from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig




class IntroductionText(DrawElement):
    POS = (0, 0, 450, 300)
    INPUT = "INTRODUCTION TEXT"
    ANCHOR = {'center':'center'}


class ContinueButton(DrawElement):
    POS = (0, 485, 150, 50)
    INPUT = "CONTINUE"
    ANCHOR = {'centerx':'centerx'}


class ShiftTitleImage(DrawElement):
    POS = Position(30, 35, 280, 110)


class SubmitButton(DrawElement):
    POS = Position(0, 0, 300, 40)
    INPUT = "SUBMIT"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class TicketSLATimerLabel(DrawElement):
    POS = Position(210, 140, 100, 60)
    INPUT = "SLA: "


class CallerInformation(DrawElement):
    POS = (120, 180, 195, 100)
    INPUT = "NO CALLER"


class TicketTitle(DrawElement):
    POS = Position(325, 5, 460, 40)
    INPUT = ""


class TicketInformation(DrawElement):
    POS = Position(325, 45, 460, 235)
    INPUT = "AWAITING TICKET..."


class ThreatListTitle(DrawElement):
    POS = Position(15, -360, 300, 30)
    INPUT = "THREAT ENTRIES"
    ANCHOR = {'bottom':'bottom'}


class ThreatList(DrawElement):
    POS = Position(0, 0, 300, 280)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -50)


class ThreatPanel(DrawElement):
    POS = Position(325, 290, 460, 350)


class ThreatTitle(DrawElement):
    POS = Position(5, 5, 445, 30)
    INPUT = "SELECT THREAT"
    OBJECT_ID = ObjectID(object_id='#threat')


class ThreatImage(DrawElement):
    POS = Position(0, 40, 250, 50)
    ANCHOR = {'centerx':'centerx'}


class ThreatInformation(DrawElement):
    POS = Position(5, 95, 445, 250)
    INPUT = ""
    OBJECT_ID = ObjectID(object_id='#threat')


class CallerProfileImagee(DrawElement):
    POS = Position(18, 180, 98, 98)


class CallerPopupWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: New Caller"


class CallerPopupWindowLabel(DrawElement):
    POS = Position(15, -60, 300, 200)
    INPUT = "INCOMING CALLER..."


class CallerPopupWindowSLA(DrawElement):
    POS = Position(0, 0, 100, 60)
    INPUT = "SLA: "
    ANCHOR = {'right':'right', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(-30, -5)


class AnswerButton(DrawElement):
    POS = Position(0, 0, 200, 40)
    INPUT = "ANSWER"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class EndShiftLabel(DrawElement):
    POS = Position(0, 170, 100, 60)
    INPUT = "SHIFT REPORT"
    ANCHOR = {'centerx':'centerx'}


class EndShiftTextBox(DrawElement):
    POS = Position(0, 0, 300, 230)
    ANCHOR = {'center':'center'}


class EndShiftButton(DrawElement):
    POS = Position(0, -210, 300, 40)
    INPUT = "END SHIFT"
    ANCHOR = {'centerx':'centerx', 'bottom':'bottom'}