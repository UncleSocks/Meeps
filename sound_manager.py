import pygame
import constants



MENU_BUTTON_SFX_CHANNEL = 0
BACK_BUTTON_SFX_CHANNEL = 1
MODIFY_BUTTON_SFX_CHANNEL = 2
DELETE_BUTTON_SFX_CHANNEL = 2
LIST_BUTTON_SFX_CHANNEL = 2
CORRECT_SUBMIT_SFX_CHANNEL = 3
INCORRECT_SUBMIT_SFX_CHANNEL = 3


class ButtonSoundManager():

    def __init__(self):    

        self.button_sfx = {

            'menu_button': pygame.mixer.Sound(constants.MENU_BUTTON_MUSIC_PATH), 
            'back_button': pygame.mixer.Sound(constants.BACK_BUTTON_MUSIC_PATH), 
            'modify_button': pygame.mixer.Sound(constants.CREATE_BUTTON_MUSIC_PATH),
            'delete_button': pygame.mixer.Sound(constants.DELETE_BUTTON__MUSIC_PATH),
            'list_button': pygame.mixer.Sound(constants.LIST_CLICK_MUSIC_PATH),
            'correct_submit': pygame.mixer.Sound(constants.CORRECT_SUBMIT_MUSIC_PATH),
            'incorrect_submit': pygame.mixer.Sound(constants.INCORRECT_SUBMIT_MUSIC_PATH)

        }

        self.button_sfx_channels = {

            'menu_button': pygame.mixer.Channel(MENU_BUTTON_SFX_CHANNEL),
            'back_button': pygame.mixer.Channel(BACK_BUTTON_SFX_CHANNEL),
            'modify_button': pygame.mixer.Channel(MODIFY_BUTTON_SFX_CHANNEL),
            'delete_button': pygame.mixer.Channel(DELETE_BUTTON_SFX_CHANNEL),
            'list_button': pygame.mixer.Channel(LIST_BUTTON_SFX_CHANNEL),
            'correct_submit': pygame.mixer.Channel(CORRECT_SUBMIT_SFX_CHANNEL),
            'incorrect_submit': pygame.mixer.Channel(INCORRECT_SUBMIT_SFX_CHANNEL)

        }


    def play_sfx(self, button_pressed: str):
        return self.button_sfx_channels[button_pressed].play(self.button_sfx[button_pressed])


    def stop_sfx(self, button_pressed: str):
        return self.button_sfx_channels[button_pressed].stop()


    def adjust_sfx_volume(self, button_pressed: str, volume: int):
        return self.button_sfx_channels[button_pressed].set_volume(volume)