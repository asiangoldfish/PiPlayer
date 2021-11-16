from youtube_dl import YoutubeDL
from sys import stdout, exit, argv
from os import system, chdir, getcwd, path, mkdir

# File pattern matching
from glob import glob

# For text wrapping multi line strings
from textwrap import dedent

# File system
# Tk is imported to fix the bug with askdirectory not closing
try:
    import tkinter as tk
except ImportError:
    print("Failed to import required module: tkinter.\nInstall package using 'pip install tkinter'.")
    exit()
from tkinter.filedialog import askdirectory

from youtube_dl.utils import DownloadError


# Manual
def helper():
    """Help menu with list of commands
    """
    help_string = dedent("""
    PiPlayer version: Development
    Usage: python3 downloader.py [OPTION]
    This is a downloader for online videos. For a list of supported sites,
    please read youtube_dl's documentation.

    -d, --downloader            download audio files from the world wide web
    -h, --help                  help page for downloader.py
    """)

    # Print the help page
    print(help_string)


# Downloads videos from URIs or based on youtube search
def downloader():
    system("clear")

    audiodir_path = f"{getcwd()}/audio/"
    print(f"Files will be stored in {audiodir_path}")

    if not path.isdir("audio"):
        print("Could not find the audio folder. Creating a new folder")
        mkdir(audiodir_path, 0o777)

    chdir(audiodir_path)

    print("Enter video URIs. Enter without URI to proceed with downloading")
    print('To instead search on YouTube, prefix with "ytsearch:". Example: ytsearch:"Forget you - Cee Lo Green"')

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

    # Error handle if download uri is invalid
    try:
        audio_downloader.download(urls_list)
    except DownloadError as e:
        print(e)
        exit()

    # Convert video to audio files
    print(glob("./audio/*.webm", ))


# Converts video or incompatible audio files to audio file format
def convert_audio():
    """Rename and/or convert video files to audio files
    """


# Main function of the program
def __main():
    """Main function in the program. Same functionality as main in C language,
    but without argc argv.
    """
    # String in cases where user did not provide a command
    missing_cmd = "Missing command. Use -h or --help."
    invalid_cmd = "Invalid command. Use -h or --help"

    # Dictionary with all available flags
    switcher = {
        "-d": downloader,
        "--downloader": downloader,
        "-h": helper,
        "--helper": helper,
    }

    try:
        key = argv[1]
    except IndexError:
        print(missing_cmd)
        exit()

    value = switcher.get(key, invalid_cmd)
    value()


if __name__ == "__main__":
    __main()
