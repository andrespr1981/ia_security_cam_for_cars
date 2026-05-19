import pygame

pygame.mixer.init()

def play_sound():

    if not pygame.mixer.music.get_busy():

        pygame.mixer.music.load("sounds/alarm.mp3")
        pygame.mixer.music.play()