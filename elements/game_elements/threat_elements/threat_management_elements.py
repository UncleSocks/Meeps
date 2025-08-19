from elements.element_creator import DrawElement, \
    Position, Offset, AnchorConfig



class TitleImage(DrawElement):
    POS = Position(20, 35, 345, 70)


class ThreatListTitle(DrawElement):
    POS = Position(0, 0, 265, 30)
    INPUT = "THREAT ENTRIES"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -470)


class ThreatList(DrawElement):
    POS = Position(0, 0, 350, 460)
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMLEFT
    ANCHOR_POS = Offset(15, -10)


class ThreatDetailLabel(DrawElement):
    POS = Position(360, 10, 150, 30)
    INPUT = "THREAT DETAILS"


class ThreatTitle(DrawElement):
    POS = Position(375, 35, 405, 30)
    INPUT = ""


class ThreatDescription(DrawElement):
    POS = Position(375, 70, 405, 175)
    INPUT = "THREAT DESCRIPTION"


class ThreatIndicators(DrawElement):
    POS = Position(375, 250, 405, 175)
    INPUT = "THREAT INDICATORS"


class ThreatCountermeasures(DrawElement):
    POS = Position(375, 430, 405, 175)
    INPUT = "THREAT COUNTERMEASURES"


class ThreatImageFileName(DrawElement):
    POS = Position(375, 610, 405, 30)
    INPUT = "THREAT IMAGE FILENAME"