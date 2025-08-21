import pygame
from constants import SFXPath, MixerChannels, \
    ButtonSFX




class ButtonSoundManager():

    def __init__(self):    

        self.button_sfx = {

            ButtonSFX.MENU_BUTTON: pygame.mixer.Sound(SFXPath.MENU_BUTTON.value), 
            ButtonSFX.BACK_BUTTON: pygame.mixer.Sound(SFXPath.BACK_BUTTON.value), 
            ButtonSFX.MODIFY_BUTTON: pygame.mixer.Sound(SFXPath.MODIFY_BUTTON.value),
            ButtonSFX.DELETE_BUTTON: pygame.mixer.Sound(SFXPath.DELETE_BUTTON.value),
            ButtonSFX.LIST_BUTTON: pygame.mixer.Sound(SFXPath.LIST_BUTTON.value),
            ButtonSFX.CORRECT_SUBMISSION: pygame.mixer.Sound(SFXPath.CORRECT_SUBMISSION.value),
            ButtonSFX.INCORRECT_SUBMISSION: pygame.mixer.Sound(SFXPath.INCORRECT_SUBMISSION.value)

        }

        self.button_sfx_channel = pygame.mixer.Channel(MixerChannels.BUTTON_SFX.value)

    def play_sfx(self, button_pressed: str):
        return self.button_sfx_channel.play(self.button_sfx[button_pressed])

    def stop_sfx(self):
        return self.button_sfx_channel.stop()

    def adjust_sfx_volume(self, volume: int):
        return self.button_sfx_channel.set_volume(volume)
    

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
    
    def adjust_music_volume(self, volume):
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