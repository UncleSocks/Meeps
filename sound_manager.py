import pygame
import constants



MENU_BUTTON_SFX_CHANNEL = 0
BACK_BUTTON_SFX_CHANNEL = 1
MODIFY_BUTTON_SFX_CHANNEL = 2
DELETE_BUTTON_SFX_CHANNEL = 2
LIST_BUTTON_SFX_CHANNEL = 2
CORRECT_SUBMIT_SFX_CHANNEL = 3
INCORRECT_SUBMIT_SFX_CHANNEL = 3

BACKGROUND_MUSIC_CHANNEL = 4
INCOMMING_CALL_CHANNEL = 5


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
    

class LoopingSoundManager():

    def __init__(self, sound_path, channel):

        self.looping_sound = pygame.mixer.Sound(sound_path)
        self.looping_channel = pygame.mixer.Channel(channel)

    def play_loop(self):
        return self.looping_channel.play(self.looping_sound, loops=-1)
    
    def stop_loop(self):
        return self.looping_channel.stop()
    
    def adjust_loop_volume(self, volume):
        return self.looping_channel.set_volume(volume)


class BackgroundMusicManager():

    def __init__(self, music_path):

        self.music_path = music_path

    def load_music(self):
        return pygame.mixer.music.load(self.music_path)

    def play_music(self):
        return pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        return pygame.mixer.music.stop()
    
    def adjust_music_volue(self, volume):
        return pygame.mixer.music.set_volume(volume) 
    

class TicketTranscriptManager():

    def __init__(self, transcript_path):

        self.transcript_path = transcript_path

    def load_transcript(self):
        return pygame.mixer.music.load(self.transcript_path)

    def play_transcript(self):
        return pygame.mixer.music.play()
    
    def stop_transcript(self):
        return pygame.mixer.music.stop()
    
    def adjust_transcript_volume(self, volume):
        return pygame.mixer.music.set_volume(volume)