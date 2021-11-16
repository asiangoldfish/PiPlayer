from youtube_dl import YoutubeDL
from sys import stdout, exit
from os import system, chdir, getcwd
from os.path import dirname

# File system
# Tk is imported to fix the bug with askdirectory not closing
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Clear terminal
system("clear")

print("YouTube Downloader")


# Prompt user for changing directory
print(f"Current directory: {getcwd()}")
chdir_prompt = input("Would you like to change directory? [y/N] ")

if chdir_prompt.lower() == "y":
    # Create tk window only so the file prompt can close
    tk = Tk()
    # tk.geometry("100x100")

    # Prompt user to choose a directory
    directory = askdirectory()
    if len(directory):
        # Change directory
        chdir(directory)

    tk.destroy()


print("Pass video URIs. Press enter without a URI to proceed with downloading")

# Infinite loop to capture all links to donwload
urls_list = set()
while True:
    # Exit program with CTRL+C
    try:
        url = input(f"Link: ")
    except KeyboardInterrupt:
        exit("")  # Print prompt on new line

    if url == "":
        stdout.write("\033[F")  # back to previous line
        stdout.write("\033[K")  # clear line
        break

    urls_list.add(url)


# Terminate program if no input has been provided
if len(urls_list) <= 0:
    print("No URIs have been provided. Terminating program")
    exit()


# Clears terminal and downloads audios
print("Downloading videos...")
audio_downloader = YoutubeDL({"format": "bestaudio"})
# audio_downloader.extract_info(urls_list)
audio_downloader.download(urls_list)
