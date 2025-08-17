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


class DeleteYesButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "Yes"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(185, -10)


class DeleteNoButton(DrawElement):
    POS = Position(10, 10, 100, 40)
    INPUT = "No"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)


class ConfirmButton(DrawElement):
    POS = Position(10, 10, 200, 40)
    INPUT = "OK"
    ANCHOR = {'left':'left', 'bottom':'bottom'}
    ANCHOR_CONFIG = AnchorConfig.BOTTOMRIGHT
    ANCHOR_POS = Offset(285, -10)