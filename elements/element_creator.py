from collections import namedtuple
from typing import ClassVar, Optional, Callable, \
    Union, Dict
from enum import Enum

import pygame
import pygame_gui



Position = namedtuple('Position', ['x', 'y', 'w', 'h'])
Offset = namedtuple('Offset', ['x', 'y'])


class AnchorConfig(Enum):
    BOTTOMLEFT = 'bottomleft'
    BOTTOMRIGHT = 'bottomright'
    TOPLEFT = 'topleft'
    TOPRIGHT = 'topright'


class DrawElement:
    POS: ClassVar[Position]
    INPUT: ClassVar[Optional[Union[str, list[str]]]] = None
    ANCHOR: ClassVar[Optional[Dict[str, str]]] = None
    ANCHOR_CONFIG: ClassVar[Optional[AnchorConfig]] = None
    ANCHOR_POS: ClassVar[Optional[Offset]] = None
    CONTAINER: ClassVar[Optional[pygame_gui.core.UIContainer]] = None
    OBJECT_ID: ClassVar[Optional[pygame_gui.core.ObjectID]] = None
    STARTING_POINT: ClassVar[Optional[str]] = None

    def __init__(self, manager):
        self.manager = manager
        self.dimension = pygame.Rect(*self.POS)
        if self.ANCHOR_CONFIG and self.ANCHOR_POS \
            and isinstance(self.ANCHOR_CONFIG, AnchorConfig):
            setattr(self.dimension, self.ANCHOR_CONFIG.value, self.ANCHOR_POS)

    def draw_window(self):
        return pygame_gui.elements.UIWindow(
            manager=self.manager,
            rect=self.dimension,
            window_display_title=self.INPUT,
            object_id=self.OBJECT_ID
        )
    
    def draw_button(self):
        return pygame_gui.elements.UIButton(
            manager=self.manager,
            relative_rect=self.dimension,
            text=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )
    
    def draw_textbox(self):
        return pygame_gui.elements.UITextBox(
            manager=self.manager,
            relative_rect=self.dimension,
            html_text=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )
    
    def draw_textentrybox(self):
        return pygame_gui.elements.UITextEntryBox(
            manager=self.manager,
            relative_rect=self.dimension,
            placeholder_text=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )
    
    def draw_label(self):
        return pygame_gui.elements.UILabel(
            manager=self.manager,
            relative_rect=self.dimension,
            text=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )
    
    def draw_selectionlist(self):
        return pygame_gui.elements.UISelectionList(
            manager=self.manager,
            relative_rect=self.dimension,
            item_list=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )
    
    def draw_dropdown(self):
        return pygame_gui.elements.UIDropDownMenu(
            manager=self.manager,
            relative_rect=self.dimension,
            options_list=self.INPUT,
            starting_option=self.STARTING_POINT,
            anchors=self.ANCHOR,
            container=self.CONTAINER
        )
    
    def draw_image(self):
        return pygame_gui.elements.UIImage(
            manager=self.manager,
            relative_rect=self.dimension,
            image_surface=self.INPUT,
            anchors=self.ANCHOR,
            container=self.CONTAINER,
            object_id=self.OBJECT_ID
        )