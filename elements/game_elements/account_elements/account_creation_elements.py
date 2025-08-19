from elements.element_creator import DrawElement, Position




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