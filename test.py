from gtts import gTTS
import os
import pygame

# Create a test speech
tts = gTTS("Hello Captain. This is Flight Bot assisting you.", lang="en")
tts.save("test.mp3")

# Initialize pygame
pygame.mixer.init()
pygame.mixer.music.load("test.mp3")
pygame.mixer.music.play()

# Keep script running until audio finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
