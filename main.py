import pygame
import tkinter as tk
from tkinter.filedialog import askdirectory
import os

# TODOS
# - Filter out anything that is not an audio file for var song_list

# Fonts used throughout the program
helvetica = "Helvetica 12 bold"

music_player = tk.Tk()
music_player.title("PiPlayer")
music_player.geometry("1280x720")

# Select directory where audio files are stored
directory = askdirectory()
os.chdir(directory)  # Change directory
song_list = os.listdir()  # Return list of audio files

# Store all audio files in an array represented in a Listbox
play_list = tk.Listbox(music_player, font=helvetica,
                       bg="yellow", selectmode=tk.SINGLE)

"""CHECK THIS CODE. MAY BE BUGGED
"""
pos = 0

for item in song_list:
    play_list.insert(pos, item)
    pos += 1

# For loading and playing sounds
pygame.init()
pygame.mixer.init()

# Music player functionalities


def play(current_song) -> None:
    """Loads a song and plays it
    """
    pygame.mixer.music.load(play_list.get(tk.ACTIVE))
    current_song.set(play_list.get(tk.ACTIVE))
    pygame.mixer.music.play()


def stop() -> None:
    """Stops the currently played song
    """
    pygame.mixer.music.stop()


def pause() -> None:
    """Pause the currently played song
    """


def unpause() -> None:
    """Unpause the currently paused song
    """
    pygame.mixer.music.unpause()


# Currently played song variable
current_song_var = tk.StringVar()
song_title = tk.Label(music_player, font=helvetica,
                      textvariable=current_song_var)

# Buttons for each of the functionalities
button_play = tk.Button(music_player, width=5, height=3, font=helvetica,
                        text="Play", command=lambda: play(current_song=current_song_var), bg="blue", fg="white")
button_stop = tk.Button(music_player, width=5, height=3,
                        font=helvetica, text="STOP", command=stop, bg="red", fg="white")
button_pause = tk.Button(music_player, width=5, height=3, font=helvetica,
                         text="PAUSE", command=pause, bg="purple", fg="white")
button_unpause = tk.Button(music_player, width=5, height=3, font=helvetica,
                           text="UNPAUSE", command=unpause, bg="orange", fg="white")


# Widgets layout
song_title.pack()
button_play.pack()
button_stop.pack()
button_pause.pack()
button_unpause.pack()
play_list.pack()

music_player.mainloop()
