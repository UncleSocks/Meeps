import pygame
import pygame_gui


def back_button_func(manager):
    
    back_button_rect = pygame.Rect(5, 5, 30, 30)
    back_button = pygame_gui.elements.UIButton(relative_rect=back_button_rect,
                                                 text="<", manager=manager)
    return back_button


def threat_database_image_func(manager, image_path):

    threat_database_image_rect = pygame.Rect(20, 35, 320, 80)
    threat_database_image_load = pygame.image.load(image_path)
    threat_database_image = pygame_gui.elements.UIImage(relative_rect=threat_database_image_rect,
                                                       image_surface=threat_database_image_load,
                                                       manager=manager)
    return threat_database_image


def create_button_func(manager):

    create_button_rect = pygame.Rect(0, 0, 45, 30)
    create_button_rect.bottomleft = (320, -470)
    create_button = pygame_gui.elements.UIButton(relative_rect=create_button_rect,
                                                 text="+", manager=manager,
                                                 anchors={'bottom':'bottom', 'left':'left'})
    
    return create_button
    

def delete_button_func(manager):
    
    delete_button_rect = pygame.Rect(0, 0, 45, 30)
    delete_button_rect.bottomleft = (280, -470)
    delete_button = pygame_gui.elements.UIButton(relative_rect=delete_button_rect,
                                                 text="-", manager=manager,
                                                 anchors={'bottom':'bottom', 'left':'left'})
    
    return delete_button


def threat_entry_slist_misc_func(manager):
    
    threat_entry_title_tbox_rect = pygame.Rect(0, 0, 265, 30)
    threat_entry_title_tbox_rect.bottomleft = (15, -470)
    threat_entry_title_tbox = pygame_gui.elements.UITextBox(relative_rect=threat_entry_title_tbox_rect,
                                                            html_text="THREAT ENTRIES", manager=manager,
                                                            anchors={'left':'left', 'bottom':'bottom'})
    
    return threat_entry_title_tbox


def threat_entry_slist_func(manager, threat_list):
    
    threat_entry_slist_rect = pygame.Rect(0, 0, 350, 460)
    threat_entry_slist_rect.bottomleft = (15, -10)
    threat_entry_slist = pygame_gui.elements.UISelectionList(item_list=threat_list,
                                                             relative_rect=threat_entry_slist_rect,
                                                             manager=manager,
                                                             anchors={'left':'left', 'bottom':'bottom'})
    
    return threat_entry_slist


def threat_details_func(manager):

    threat_details_label_rect = pygame.Rect(360, 10, 150, 30)
    threat_details_label = pygame_gui.elements.UILabel(relative_rect=threat_details_label_rect,
                                                           text="THREAT DETAILS", manager=manager)
    
    selected_threat_title_tbox_rect = pygame.Rect(375, 35, 405, 30)
    selected_threat_title_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_threat_title_tbox_rect,
                                                               html_text="", manager=manager)
    
    selected_threat_description_tbox_rect = pygame.Rect(375, 70, 405, 175)
    selected_threat_description_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_threat_description_tbox_rect,
                                                                     html_text="THREAT DESCRIPTION", manager=manager)
    
    selected_threat_indicators_tbox_rect = pygame.Rect(375, 250, 405, 175)
    selected_threat_indicators_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_threat_indicators_tbox_rect,
                                                                     html_text="THREAT INDICATORS", manager=manager)
    
    selected_threat_countermeasures_tbox_rect = pygame.Rect(375, 430, 405, 175)
    selected_threat_countermeasures_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_threat_countermeasures_tbox_rect,
                                                                     html_text="THREAT COUNTERMEASURES", manager=manager)
    
    selected_threat_image_path_tbox_rect = pygame.Rect(375, 610, 405, 30)
    selected_threat_image_path_tbox = pygame_gui.elements.UITextBox(relative_rect=selected_threat_image_path_tbox_rect,
                                                                    html_text="THREAT IMAGE PATH", manager=manager)
    
    return threat_details_label, selected_threat_title_tbox, selected_threat_description_tbox, selected_threat_indicators_tbox, selected_threat_countermeasures_tbox, selected_threat_image_path_tbox


def add_threat_image_func(manager, image_path):

    add_threat_image_rect = pygame.Rect(20, 10, 350, 75)
    add_threat_image_load = pygame.image.load(image_path)
    add_threat_image = pygame_gui.elements.UIImage(relative_rect=add_threat_image_rect,
                                                       image_surface=add_threat_image_load,
                                                       manager=manager)
    
    return add_threat_image


def threat_entry_func(manager):

    threat_entry_name_tentry_rect = pygame.Rect(180, 90, 600, 30)
    threat_entry_name_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=threat_entry_name_tentry_rect,
                                                                   placeholder_text="ENTER THREAT TITLE",
                                                                   initial_text="ENTER THREAT TITLE",
                                                                   manager=manager)
    
    threat_entry_description_tentry_rect = pygame.Rect(15, 130, 765, 150)
    threat_entry_description_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=threat_entry_description_tentry_rect,
                                                                         placeholder_text="ENTER THREAT DESCRIPTION",
                                                                         initial_text="ENTER THREAT DESCRIPTION",
                                                                         manager=manager)
    
    threat_entry_indicators_tentry_rect = pygame.Rect(15, 290, 765, 150)
    threat_entry_indicators_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=threat_entry_indicators_tentry_rect,
                                                                        placeholder_text="ENTER THREAT INDICATORS",
                                                                        initial_text="ENTER THREAT INDICATORS",
                                                                        manager=manager)
    
    threat_entry_countermeasures_tentry_rect = pygame.Rect(15, 450, 765, 150)
    threat_entry_countermeasures_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=threat_entry_countermeasures_tentry_rect,
                                                                             placeholder_text="ENTER THREAT COUNTERMEASURES",
                                                                             initial_text="ENTER THREAT COUNTERMEASURES",
                                                                             manager=manager)
    
    threat_entry_image_path_tentry_rect = pygame.Rect(15, 610, 765, 30)
    threat_entry_image_path_tentry = pygame_gui.elements.UITextEntryBox(relative_rect=threat_entry_image_path_tentry_rect,
                                                                        placeholder_text="ENTER THREAT IMAGE FILENAME",
                                                                        initial_text="ENTER THREAT IMAGE FILENAME",
                                                                        manager=manager)
    
    return threat_entry_name_tentry, threat_entry_description_tentry, threat_entry_indicators_tentry, threat_entry_countermeasures_tentry, threat_entry_image_path_tentry


def threat_entry_add_button_func(manager):

    add_button_rect = pygame.Rect(600, 30, 180, 45)
    add_button = pygame_gui.elements.UIButton(relative_rect=add_button_rect,
                                                 text="ADD THREAT", manager=manager)
    
    return add_button


def threat_confirm_window_func(manager):
    
    threat_confirm_window_rect = pygame.Rect(0, 0, 400, 200)
    threat_confirm_window = pygame_gui.elements.UIWindow(rect=threat_confirm_window_rect,
                                                 window_display_title="MEEPS SECURITY: New Threat",
                                                 manager=manager)
    
    threat_confirm_window_label_rect = pygame.Rect(0, -10, 300, 200)
    threat_confirm_window_label = pygame_gui.elements.UILabel(relative_rect=threat_confirm_window_label_rect, 
                                                            text="THRAT SUCCESSFULLY ADDED", 
                                                            manager=manager,
                                                            container=threat_confirm_window,
                                                            anchors={'center':'center'})
    
    threat_confirm_close_button_rect = pygame.Rect(10, 10, 200, 40)
    threat_confirm_close_button_rect.bottomright = (285, -10)
    threat_confirm_close_button = pygame_gui.elements.UIButton(relative_rect=threat_confirm_close_button_rect, 
                                                                     text="OK", manager=manager,container=threat_confirm_window,
                                                                     anchors={'left':'left', 'bottom':'bottom'})
    
    return threat_confirm_window, threat_confirm_close_button


def threat_delete_confirm_window_func(manager):

    threat_delete_confirm_window_rect = pygame.Rect(0, 0, 400, 200)
    threat_delete_confirm_window = pygame_gui.elements.UIWindow(rect=threat_delete_confirm_window_rect, 
                                                                window_display_title="Meeps Security: Delete Threat",
                                                                manager=manager)
    
    
    threat_delete_confirm_window_label_rect = pygame.Rect(0, -10, 300, 200)
    threat_delete_confirm_window_label = pygame_gui.elements.UILabel(relative_rect=threat_delete_confirm_window_label_rect,
                                                                     text="Delete selected threat?",
                                                                     manager=manager,
                                                                     container=threat_delete_confirm_window,
                                                                     anchors={'center':'center'})
    
    threat_delete_confirm_window_warning_label_rect = pygame.Rect(0, -40, 350, 200)
    threat_delete_confirm_window_warning_label = pygame_gui.elements.UILabel(relative_rect=threat_delete_confirm_window_warning_label_rect,
                                                                     text="[!] This will delete associated tickets.",
                                                                     manager=manager,
                                                                     container=threat_delete_confirm_window,
                                                                     anchors={'center':'center'})
    
    threat_delete_confirm_yes_button_rect = pygame.Rect(10, 10, 100, 40)
    threat_delete_confirm_yes_button_rect.bottomright = (185, -10)
    threat_delete_confirm_yes_button = pygame_gui.elements.UIButton(relative_rect=threat_delete_confirm_yes_button_rect,
                                                                    text="YES", manager=manager, container=threat_delete_confirm_window,
                                                                    anchors={'left':'left', 'bottom':'bottom'})
    
    threat_delete_confirm_no_button_rect = pygame.Rect(10, 10, 100, 40)
    threat_delete_confirm_no_button_rect.bottomright = (285, -10)
    threat_delete_confirm_no_button = pygame_gui.elements.UIButton(relative_rect=threat_delete_confirm_no_button_rect, 
                                                                   text="NO", manager=manager, container=threat_delete_confirm_window,
                                                                   anchors={'left':'left', 'bottom':'bottom'})

    return threat_delete_confirm_window, threat_delete_confirm_yes_button, threat_delete_confirm_no_button