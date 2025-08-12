from enum import Enum

import pygame
import pygame_gui

from .element_creator import Position, Offset



class BackButton(Enum):
    POS = Position(5, 5, 30, 30)
    ANCHOR = Offset(10, -610)
    TEXT = "<"


class CreateButton(Enum):
    POS = Position(0, 0, 45, 30)
    ANCHOR = Offset(320, -470)
    TEXT = "+"


#Done
def back_button_func(manager):
    
    back_button_rect = pygame.Rect(*BackButton.POS.value)
    back_button_rect.bottomleft = (BackButton.ANCHOR.value)
    #back_button = ElementCreator(manager).create_button_element(back_button_rect, None, BackButton.TEXT.value)
    #back_button = pygame_gui.elements.UIButton(relative_rect=back_button_rect,
    #                                             text="<", manager=manager)
    #return back_button


def account_manager_image_func(manager, image_path):

    account_manager_image_rect = pygame.Rect(20, 35, 345, 70)
    account_manager_image_load = pygame.image.load(image_path)
    account_manager_image = pygame_gui.elements.UIImage(relative_rect=account_manager_image_rect,
                                                       image_surface=account_manager_image_load,
                                                       manager=manager)
    return account_manager_image


def create_button_func(manager):

    create_button_rect = pygame.Rect(*CreateButton.POS.value)
    create_button_rect.bottomleft = (CreateButton.ANCHOR.value)
    create_button = pygame_gui.elements.UIButton(relative_rect=create_button_rect,
                                                 text="+", manager=manager,
                                                 anchors={'bottom':'bottom', 'left':'left'})
    
    return create_button


def delete_button_fun(manager):
    
    delete_button_rect = pygame.Rect(0, 0, 45, 30)
    delete_button_rect.bottomleft = (280, -470)
    delete_button = pygame_gui.elements.UIButton(relative_rect=delete_button_rect,
                                                 text="-", manager=manager,
                                                 anchors={'bottom':'bottom', 'left':'left'})
    
    return delete_button


def account_entry_slist_misc_func(manager):

    account_entry_title_tbox_rect = pygame.Rect(0, 0, 265, 30)
    account_entry_title_tbox_rect.bottomleft = (15, -470)
    account_entry_title_tbox = pygame_gui.elements.UITextBox(relative_rect=account_entry_title_tbox_rect, 
                                                             html_text="ACCOUNT LIST", manager=manager,
                                                             anchors={'left':'left', 'bottom':'bottom'})
    return account_entry_title_tbox


def account_entry_slist_func(manager, account_list):

    account_entry_slist_rect = pygame.Rect(0, 0, 350, 460)
    account_entry_slist_rect.bottomleft = (15, -10)
    account_entry_slist = pygame_gui.elements.UISelectionList(item_list=account_list,
                                                              relative_rect=account_entry_slist_rect,
                                                              manager=manager,
                                                              anchors={'left':'left', 'bottom':'bottom'})

    return account_entry_slist


def account_details(manager):

    account_details_label_rect = pygame.Rect(360, 10, 150, 30)
    account_details_label = pygame_gui.elements.UILabel(relative_rect=account_details_label_rect,
                                                           text="ACCOUNT DETAILS", manager=manager)
    
    selected_account_description_tbox_rect = pygame.Rect(375, 40, 405, 160)
    selected_account_description_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_account_description_tbox_rect,
                                                                     html_text="SELECT AN ACCOUNT", manager=manager)
    
    return account_details_label, selected_account_description_tbox


def assigned_ticket_label_func(manager):

    assigned_ticket_label_rect = pygame.Rect(365, 220, 150, 30)
    assigned_ticket_label = pygame_gui.elements.UILabel(relative_rect=assigned_ticket_label_rect,
                                                        text="ASSIGNED TICKETS", manager=manager)
    
    return assigned_ticket_label


def assigned_tickets(manager, ticket_list):
    
    assigned_ticket_slist_rect = pygame.Rect(375, 250, 405, 390)
    assigned_ticket_slist = pygame_gui.elements.UISelectionList(item_list=ticket_list, 
                                                                relative_rect=assigned_ticket_slist_rect,
                                                                manager=manager)
    return assigned_ticket_slist


def add_account_image_func(manager, image_path):

    add_account_image_rect = pygame.Rect(50, 15, 375, 75)
    add_account_image_load = pygame.image.load(image_path)
    add_account_image = pygame_gui.elements.UIImage(relative_rect=add_account_image_rect,
                                                       image_surface=add_account_image_load,
                                                       manager=manager)
    
    return add_account_image


def new_account_name_tentry_func(manager):

    account_name_label_rect = pygame.Rect(20, 100, 100, 30)
    account_name_label = pygame_gui.elements.UILabel(relative_rect=account_name_label_rect,
                                                     text="ACCOUNT NAME", manager=manager)
    
    new_account_name_tentry_rect = pygame.Rect(15, 125, 765, 30)
    new_account_name_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=new_account_name_tentry_rect,
                                                                 manager=manager)
    return account_name_label, new_account_name_tentry

def new_account_organization_func(manager):

    organization_label_rect = pygame.Rect(20, 170, 100, 30)
    organization_label = pygame_gui.elements.UILabel(relative_rect=organization_label_rect,
                                                     text="ORGANIZATION NAME", manager=manager)
    
    organization_tentry_rect = pygame.Rect(15, 195, 765, 30)
    organization_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=organization_tentry_rect, 
                                                             manager=manager)
    
    return organization_label, organization_tentry


def new_account_email_func(manager):

    account_email_rect = pygame.Rect(20, 240, 50, 30)
    account_email = pygame_gui.elements.UILabel(relative_rect=account_email_rect,
                                                text="EMAIL", manager=manager)
    
    account_email_tentry_rect = pygame.Rect(15, 265, 765, 30)
    account_email_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=account_email_tentry_rect,
                                                              manager=manager)
    
    return account_email, account_email_tentry


def new_account_contact_func(manager):

    account_contact_rect = pygame.Rect(20, 310, 65, 30)
    account_contact = pygame_gui.elements.UILabel(relative_rect=account_contact_rect,
                                                  text="CONTACT", manager=manager)
    
    account_contact_tentry_rect = pygame.Rect(15, 335, 765, 30)
    account_contact_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=account_contact_tentry_rect,
                                                                manager=manager)
    
    return account_contact, account_contact_tentry


def new_account_picture_path_func(manager):

    account_picture_path_label_rect = pygame.Rect(10, 380, 150, 30)
    account_picture_path_label = pygame_gui.elements.UILabel(relative_rect=account_picture_path_label_rect,
                                                             text="PICTURE FILENAME", manager=manager)
    
    account_picture_path_tentry_rect = pygame.Rect(15, 405, 475, 30)
    account_picture_path_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=account_picture_path_tentry_rect,
                                                                     manager=manager)
    
    return account_picture_path_label, account_picture_path_tentry


def new_account_image_border_func(manager):
    new_account_image_border_rect = pygame.Rect(545, 405, 190, 190)
    new_account_image_border = pygame_gui.elements.UITextEntryBox(relative_rect=new_account_image_border_rect,
                                                                  manager=manager)
    return new_account_image_border


def new_account_image_func(manager, image_path):

    new_account_image_rect = pygame.Rect(550, 410, 180, 180)
    try:
        new_account_image_load = pygame.image.load(f"assets/images/accounts/{image_path}")
    except:
        new_account_image_load = pygame.image.load("assets/images/accounts/guest.png")
    new_account_profile_image = pygame_gui.elements.UIImage(relative_rect=new_account_image_rect,
                                                       image_surface=new_account_image_load,
                                                       manager=manager)
    return new_account_profile_image


def add_new_account_button_func(manager):

    add_account_button_rect = pygame.Rect(15, 455, 120, 40)
    add_account_button = pygame_gui.elements.UIButton(relative_rect=add_account_button_rect, 
                                                      text="ADD ACCOUNT", manager=manager)
    return add_account_button


def account_confirm_window_func(manager):
    
    account_confirm_window_rect = pygame.Rect(0, 0, 400, 200)
    account_confirm_window = pygame_gui.elements.UIWindow(rect=account_confirm_window_rect,
                                                 window_display_title="MEEPS SECURITY: New Account",
                                                 manager=manager)
    
    account_confirm_window_label_rect = pygame.Rect(0, -10, 300, 200)
    account_confirm_window_label = pygame_gui.elements.UILabel(relative_rect=account_confirm_window_label_rect, 
                                                            text="ACCOUNT SUCCESSFULLY CREATED", 
                                                            manager=manager,
                                                            container=account_confirm_window,
                                                            anchors={'center':'center'})
    
    account_confirm_close_button_rect = pygame.Rect(10, 10, 200, 40)
    account_confirm_close_button_rect.bottomright = (285, -10)
    account_confirm_close_button = pygame_gui.elements.UIButton(relative_rect=account_confirm_close_button_rect, 
                                                                     text="OK", manager=manager,container=account_confirm_window,
                                                                     anchors={'left':'left', 'bottom':'bottom'})
    
    return account_confirm_window, account_confirm_close_button

def account_delete_warning_window(manager):
    
    account_delete_warning_rect = pygame.Rect(0, 0, 400, 200)
    account_delete_warning = pygame_gui.elements.UIWindow(rect=account_delete_warning_rect,
                                                 window_display_title="MEEPS SECURITY: Delete Threat",
                                                 manager=manager)
    
    account_delete_warning_label_rect = pygame.Rect(0, -10, 300, 200)
    account_delete_warning_label = pygame_gui.elements.UILabel(relative_rect=account_delete_warning_label_rect, 
                                                            text="GUEST ACCNOUNT CANNOT BE DELETED", 
                                                            manager=manager,
                                                            container=account_delete_warning,
                                                            anchors={'center':'center'})
    
    account_warning_close_button_rect = pygame.Rect(10, 10, 200, 40)
    account_warning_close_button_rect.bottomright = (285, -10)
    account_warning_close_button = pygame_gui.elements.UIButton(relative_rect=account_warning_close_button_rect, 
                                                                     text="OK", manager=manager,container=account_delete_warning,
                                                                     anchors={'left':'left', 'bottom':'bottom'})
    
    return account_delete_warning, account_warning_close_button


def account_delete_confirm_window_func(manager):

    account_delete_confirm_window_rect = pygame.Rect(0, 0, 400, 200)
    account_delete_confirm_window = pygame_gui.elements.UIWindow(rect=account_delete_confirm_window_rect, 
                                                                window_display_title="Meeps Security: Delete Threat",
                                                                manager=manager)
    
    
    account_delete_confirm_window_label_rect = pygame.Rect(0, -10, 300, 200)
    account_delete_confirm_window_label = pygame_gui.elements.UILabel(relative_rect=account_delete_confirm_window_label_rect,
                                                                     text="Delete selected account?",
                                                                     manager=manager,
                                                                     container=account_delete_confirm_window,
                                                                     anchors={'center':'center'})
    
    account_delete_confirm_window_warning_label_rect = pygame.Rect(0, -40, 350, 200)
    account_delete_confirm_window_warning_label = pygame_gui.elements.UILabel(relative_rect=account_delete_confirm_window_warning_label_rect,
                                                                     text="[!] This will delete associated tickets.",
                                                                     manager=manager,
                                                                     container=account_delete_confirm_window,
                                                                     anchors={'center':'center'})
    
    account_delete_confirm_yes_button_rect = pygame.Rect(10, 10, 100, 40)
    account_delete_confirm_yes_button_rect.bottomright = (185, -10)
    account_delete_confirm_yes_button = pygame_gui.elements.UIButton(relative_rect=account_delete_confirm_yes_button_rect,
                                                                    text="YES", manager=manager, container=account_delete_confirm_window,
                                                                    anchors={'left':'left', 'bottom':'bottom'})
    
    account_delete_confirm_no_button_rect = pygame.Rect(10, 10, 100, 40)
    account_delete_confirm_no_button_rect.bottomright = (285, -10)
    account_delete_confirm_no_button = pygame_gui.elements.UIButton(relative_rect=account_delete_confirm_no_button_rect, 
                                                                   text="NO", manager=manager, container=account_delete_confirm_window,
                                                                   anchors={'left':'left', 'bottom':'bottom'})

    return account_delete_confirm_window, account_delete_confirm_yes_button, account_delete_confirm_no_button