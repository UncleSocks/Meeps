import pygame
import pygame_gui
from pygame_gui.core import ObjectID


def back_button_func(manager):
    
    back_button_rect = pygame.Rect(5, 5, 30, 30)
    back_button = pygame_gui.elements.UIButton(relative_rect=back_button_rect,
                                                 text="<", manager=manager)
    return back_button


def introduction_tbox(manager, introduction_text):

    introduction_tbox_rect = pygame.Rect(0, 0, 450, 300)
    introduction_tbox = pygame_gui.elements.UITextBox(relative_rect=introduction_tbox_rect, 
                                                      manager=manager, html_text=introduction_text,
                                                      anchors={'center':'center'})
    
    continue_button_rect = pygame.Rect(0, 485, 150, 50)
    continue_button = pygame_gui.elements.UIButton(relative_rect=continue_button_rect,
                                                        text="CONTINUE", manager=manager,
                                                        anchors={'centerx':'centerx'})
    return introduction_tbox, continue_button


def introduction_tbox_func(manager, introduction_text):

    introduction_tbox_rect = pygame.Rect(0, 0, 450, 300)
    introduction_tbox = pygame_gui.elements.UITextBox(relative_rect=introduction_tbox_rect, 
                                                      manager=manager, html_text=introduction_text,
                                                      anchors={'center':'center'})

    return introduction_tbox


def continue_button_func(manager):

    continue_button_rect = pygame.Rect(0, 485, 150, 50)
    continue_button = pygame_gui.elements.UIButton(relative_rect=continue_button_rect,
                                                        text="CONTINUE", manager=manager,
                                                        anchors={'centerx':'centerx'})
    return continue_button


def title_image_func(manager, image_path):

    title_image_rect = pygame.Rect(30, 35, 280, 110)
    title_image_load = pygame.image.load(image_path)
    title_image = pygame_gui.elements.UIImage(relative_rect=title_image_rect,
                                                       image_surface=title_image_load,
                                                       manager=manager)
    return title_image


def main_sla_timer_label_func(manager):
    
    main_sla_timer_label_rect = pygame.Rect(210, 140, 100, 60)
    main_sla_timer_label = pygame_gui.elements.UILabel(relative_rect=main_sla_timer_label_rect,
                                                       text="SLA: ", manager=manager)
    return main_sla_timer_label


def caller_profile_tbox_func(manager):

    caller_profile_tbox_rect = pygame.Rect(120, 180, 195, 100)
    caller_profile_tbox = pygame_gui.elements.UITextBox(relative_rect=caller_profile_tbox_rect,
                                                        html_text="NO CALLER",
                                                        manager=manager)
    return caller_profile_tbox

#NOT YET DONE HERE:
def caller_profile_image_func(manager, image_path):

    caller_profile_image_rect = pygame.Rect(18, 180, 98, 98)
    try:
        caller_profile_image_load = pygame.image.load(image_path)
    except:
        caller_profile_image_load = pygame.image.load("assets/images/accounts/guest.png")
    caller_profile_image = pygame_gui.elements.UIImage(relative_rect=caller_profile_image_rect,
                                                       image_surface=caller_profile_image_load,
                                                       manager=manager)
    return caller_profile_image


def submit_button_func(manager):

    submit_button_rect = pygame.Rect(0, 0, 300, 40)
    submit_button_rect.bottomleft = (15, -10)
    submit_button = pygame_gui.elements.UIButton(relative_rect=submit_button_rect,
                                                 text="SUBMIT", manager=manager,
                                                 anchors={'left':'left', 'bottom':'bottom'})
    return submit_button


def threat_entry_title_tbox_func(manager):

    threat_entry_title_tbox_rect = pygame.Rect(15, -360, 300, 30)
    threat_entry_title_tbox = pygame_gui.elements.UITextBox(relative_rect=threat_entry_title_tbox_rect,
                                                            html_text="THREAT ENTRIES", manager=manager,
                                                            anchors = {'bottom':'bottom'})
    return threat_entry_title_tbox


def threat_entry_slist_func(manager, threat_list):

    threat_entry_slist_rect = pygame.Rect(0, 0, 300, 280)
    threat_entry_slist_rect.bottomleft = (15, -50)
    threat_entry_slist = pygame_gui.elements.UISelectionList(item_list=threat_list,
                                                             relative_rect=threat_entry_slist_rect,
                                                             manager=manager,
                                                             anchors={'left':'left', 'bottom':'bottom'})
    return threat_entry_slist


def threat_panel_func(manager):

    threat_panel_rect = pygame.Rect(325, 290, 460, 350)
    threat_panel = pygame_gui.elements.UIPanel(relative_rect=threat_panel_rect,
                                               manager=manager)
    
    threat_title_rect = pygame.Rect(5, 5, 445, 30)
    threat_title_tbox = pygame_gui.elements.UITextBox(relative_rect=threat_title_rect,
                                                 html_text="SELECT THREAT", manager=manager,
                                                 container=threat_panel,
                                                 object_id=ObjectID(object_id='#threat'))
    
    threat_image_rect = pygame.Rect(0, 40, 250, 50)
    threat_image_load = pygame.image.load("assets/images/general/blank.png")
    threat_image = pygame_gui.elements.UIImage(relative_rect=threat_image_rect,
                                               image_surface=threat_image_load, 
                                               container=threat_panel, manager=manager,
                                               anchors={'centerx':'centerx'})


    threat_description_tbox_rect = pygame.Rect(5, 95, 445, 250)
    threat_description_tbox = pygame_gui.elements.UITextBox(relative_rect=threat_description_tbox_rect,
                                                           html_text="", manager=manager, container=threat_panel,
                                                           object_id=ObjectID(object_id='#threat'))
    return threat_panel, threat_title_tbox, threat_image, threat_description_tbox


def ticket_title_tbox_func(manager):

    ticket_title_tbox_rect = pygame.Rect(325, 5, 460, 40)
    ticket_title_tbox = pygame_gui.elements.UITextBox(relative_rect=ticket_title_tbox_rect, 
                                                       html_text="", manager=manager)
    return ticket_title_tbox


def ticket_entry_tbox_func(manager):

    ticket_entry_tbox_rect = pygame.Rect(325, 45, 460, 235)
    ticket_entry_tbox = pygame_gui.elements.UITextBox(relative_rect=ticket_entry_tbox_rect, 
                                                       html_text="AWAITING TICKET...", manager=manager)
    return ticket_entry_tbox


def caller_popup_window_func(manager):
    
    caller_popup_window_rect = pygame.Rect(0, 0, 400, 200)
    caller_popup_window = pygame_gui.elements.UIWindow(rect=caller_popup_window_rect,
                                                 window_display_title="MEEPS SECURITY: New Caller",
                                                 manager=manager)
    
    caller_popup_window_label_rect = pygame.Rect(15, -60, 300, 200)
    caller_popup_window_label = pygame_gui.elements.UILabel(relative_rect=caller_popup_window_label_rect, 
                                                            text="INCOMING CALLER...", 
                                                            manager=manager,
                                                            container=caller_popup_window)

    caller_popup_window_sla_timer_label_rect = pygame.Rect(0, 0, 100, 60)
    caller_popup_window_sla_timer_label_rect.bottomright = (-30, -5)
    caller_popup_window_sla_timer_label = pygame_gui.elements.UILabel(relative_rect=caller_popup_window_sla_timer_label_rect, 
                                                                      text="SLA: ", manager=manager,container=caller_popup_window,
                                                                      anchors={'right':'right', 'bottom':'bottom'})
    
    caller_popup_window_answer_button_rect = pygame.Rect(0, 0, 200, 40)
    caller_popup_window_answer_button_rect.bottomleft = (15, -10)
    caller_popup_window_answer_button = pygame_gui.elements.UIButton(relative_rect=caller_popup_window_answer_button_rect, 
                                                                     text="ANSWER", manager=manager,container=caller_popup_window,
                                                                     anchors={'left':'left', 'bottom':'bottom'})
    
    return caller_popup_window, caller_popup_window_answer_button, caller_popup_window_sla_timer_label


def shift_report_tbox_func(manager, score, ticket_count, missed_calls, missed_tickets, assessment_result):
    
    shift_report_tbox_rect = pygame.Rect(0, 0, 300, 230)
    shift_report_tbox = pygame_gui.elements.UITextBox(relative_rect=shift_report_tbox_rect,
                                                           html_text=f"Employee No: #1361\nTitle: L1 SOC Analyst\nTotal Tickets: {ticket_count}\nAccurate Ticket Resolution: {score}\nMissed Calls: {missed_calls}\nMissed Tickets: {missed_tickets}\n\n<b>ASSESSMENT RESULT:<b> {assessment_result}", 
                                                           manager=manager,
                                                           anchors={'center':'center'})
    return shift_report_tbox


def end_shift_button_func(manager):

    end_shift_button_rect = pygame.Rect(0, -210, 300, 40)
    end_shift_button = pygame_gui.elements.UIButton(relative_rect=end_shift_button_rect,
                                                 text="END SHIFT", manager=manager,
                                                 anchors={'centerx':'centerx', 'bottom':'bottom'})
    return end_shift_button


def end_shift_title_label_func(manager):

    end_shift_title_label_rect = pygame.Rect(0, 170, 100, 60)
    end_shift_title_label = pygame_gui.elements.UILabel(relative_rect=end_shift_title_label_rect,
                                                       text="SHIFT REPORT", manager=manager,
                                                       anchors={'centerx':'centerx'})
    return end_shift_title_label