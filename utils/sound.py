import random
from playsound import playsound 

def sound():
    sounds = ['sounds/alarm.mp3','sounds/fart.mp3','sounds/oof.mp3']
    choice = random.choice(sounds)
    playsound(choice)