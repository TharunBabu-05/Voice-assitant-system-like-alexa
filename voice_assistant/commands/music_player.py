import pygame
import os

def handle(text):
    if "play music" in text.lower():
        pygame.mixer.init()
        music_folder = "music/"
        for file in os.listdir(music_folder):
            if file.endswith(".mp3"):
                pygame.mixer.music.load(os.path.join(music_folder, file))
                pygame.mixer.music.play()
                return f"Playing {file}"
        return "No music files found."
    return None
