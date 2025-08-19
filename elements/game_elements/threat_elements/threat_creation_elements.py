from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig



class NewThreatImage(DrawElement):
    POS = Position(20, 10, 350, 75)


class AddThreatButton(DrawElement):
    POS = Position(600, 30, 180, 45)
    INPUT = "ADD THREAT"


class NewThreatName(DrawElement):
    POS = Position(180, 90, 600, 30)
    INPUT = "ENTER THREAT NAME"


class NewThreatDescription(DrawElement):
    POS = Position(15, 130, 765, 150)
    INPUT = "ENTER THREAT DESCRIPTION"


class NewThreatIndicators(DrawElement):
    POS = Position(15, 290, 765, 150)
    INPUT = "ENTER THREAT INDICATORS"


class NewThreatCountermeasures(DrawElement):
    POS = Position(15, 450, 765, 150)
    INPUT = "ENTER THREAT COUNTERMEASURES"


class NewThreatImageFileName(DrawElement):
    POS = Position(15, 610, 765, 30)
    INPUT = "ENTER THREAT FILENAME"


class ConfirmWindow(DrawElement):
    POS = Position(0, 0, 400, 200)
    INPUT = "Meeps Security: New Threat"


class ConfirmLabel(DrawElement):
    POS = Position(0, -10, 300, 200)
    INPUT = "THREAT ADDED SUCCESSFULLY"
    ANCHOR = {'center':'center'}