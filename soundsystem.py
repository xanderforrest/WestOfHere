import pygame


class SoundSystem:
    def __init__(self):
        self.global_volume = 1.0
        pass  # create sound groups so volume can be controlled

    def play_sound(self, sound):
        channel = pygame.mixer.find_channel()
        if channel:
            sound.set_volume(self.global_volume)
            channel.play(sound)
        else:
            print("No channels available")
