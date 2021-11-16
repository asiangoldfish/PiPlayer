from sys import stdout, exit, argv
from os import system, chdir, getcwd, path, mkdir

# Managing subprocesses, usually run outside Python's control
from subprocess import run, check_output

# File pattern matching
from glob import glob

# For text wrapping multi line strings
from textwrap import dedent

# For downloading videos
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError


# Downloads videos from URIs or based on youtube search
def downloader():
    system("clear")

    audiodir_path = f"{getcwd()}/audio/"
    print(f"Files will be stored in {audiodir_path}")

    # Looks for directory called audio within the project. If does not exist, create a new audio directory
    if not path.isdir("audio"):
        print("Could not find the audio folder. Creating a new folder")
        mkdir(audiodir_path, 0o777)

    chdir(audiodir_path)

    print("Enter video URIs. Enter without URI to proceed with downloading")
    print('To instead search on YouTube, prefix with "ytsearch:". Example: ytsearch:"Forget you - Cee Lo Green"')

    # Infinite loop to capture all links to donwload
    urls_list = list()
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

        urls_list.append(url)

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
def convert_audio() -> None:
    """Rename and/or convert video files to audio files
    """
    # All supported formats that youtube_dl can download a file as.
    # Excludes mp3 and wav formats
    formats = ["3gp", "aac", "flv", "m4a", "mp4", "ogg", "webm"]
    files = list()

    path_to_search_for = f"{getcwd()}/audio"

    # Searches for all files with the extensions in formats[].
    # Loops through each element in formats, one at a time
    for i, format in enumerate(formats):

        # Searches through all files with specified extension (format[i]),
        # returning a list. Joins this with the existing files[]
        found_files = glob(f"{path_to_search_for}/*.{formats[i]}")

        # Do nothing if files with the specified extensions were not found,
        # else append found files to files[]
        if len(found_files) <= 0:
            continue
        else:
            files += found_files

    # Terminate program if no files were round
    if len(files) <= 0:
        print(f"Directory to search in: {getcwd()}/audio/")
        print(
            f"Attempting to find files with any of the following extensions: ")

        # Print the list of formats the program searches for
        for format in formats:
            print(f"- {format}")

        print(
            f"Could not find any matching files to convert..")
        exit()

    ################################################################################

    # Clear terminal
    system("clear")

    # Prompt user for converting files
    print(f"Attempting to convert files in:", end="\n\n")
    for file in files:
        new_file = file.split(f"{getcwd()}/audio/")
        print(new_file[1])
    # Exit program is user keyboard interrupts
    try:
        prompt = input("\nAre you sure you would like to proceed? [y/N] ")
    except KeyboardInterrupt:
        exit("\nAborting conversion...")

    if prompt.casefold() == "y":
        print("Converting files to mp3 format...")
        pass
    else:
        print("Aborting conversion...")
        exit()

    ################################################################################

    # Convert files in files[] to mp3 format. Documentation: https://pypi.org/project/ffmpy/

    # Store path to unsuccessfully converted files
    failed_files = list()

    for file in files:
        new_path = file.split(f"{getcwd()}")[1]

        # Extracts the file path without extension.
        file_no_ext = new_path.split(".")[0]

        # Adds new extension to the file path
        file_new_ext = f"{file_no_ext}.mp3"

        # Convert file to mp3 formatted file
        try:
            check_output(
                f"ffmpeg -i '.{new_path}' .'{file_new_ext}'", shell=True)
        except Exception:
            # Register full path of unsuccessful files during conversion
            printc("Unable to convert file", "red")
            failed_files.append(file)

    # Success message for converting files
    # Print a list of files that unsuccessfully did not convert, if any.
    if len(failed_files) == 0:
        printc("\nSuccessfully converted all files!", "green")
    else:
        print("\nThe following files were unsuccessful:\n")
        for file in failed_files:
            file = file.split(f"{getcwd()}/audio/")[1]
            print(f"- {file}")

        print("\nThey may have failed because there were \\, \" or \' in the file name.")
        print("You can ignore this if it was because you skipped them.")
        print("Consider remove these and try again.")

    ################################################################################

    # Prompt user to delete old files if they were successful
    # Exit program is user keyboard interrupts
    # Only proceed with deleting old files if any files were converted at all

    # This functionality is not complete yet
    """
    if len(files) > len(failed_files):
        try:
            prompt = input(
                "\nDelete old files that were successfully converted (this cannot be undone!)? [y/N] ")
        except KeyboardInterrupt:
            exit("\nAborting deletion of fold files...")

        # Deletes old files one by one if user says yes
        if prompt.casefold() == "y":
            print("Deleting old files...")
            system(f"rm {file}")
    """


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
    -c, --converter             convert video/audio files to mp3 files
    """)

    # Print the help page
    print(help_string)


# Rename files
def rename_files(dirpath: str = None) -> None:
    """Rename all files

    Args:
        dirpath (str, optional): [description]. Defaults to None.
    """

    # Default filepath
    if dirpath is None:
        dirpath = f"{getcwd()}/audio/"

    # Error handle if there is no audio directory
    try:
        chdir(dirpath)
    except FileNotFoundError:
        print(
            f"Searching for audio directory...\nCould not find {dirpath}")
        exit()


# Main function of the program
def main():
    """Main function in the program. Same functionality as main in C language,
    but without argc and argv parameters.
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
        "-c": convert_audio,
        "--converter": convert_audio,
    }

    try:
        key = argv[1]
    except IndexError:
        print(missing_cmd)
        exit()

    # Warn user if too many commands have been passed
    if len(argv) > 2:
        print("Too many arguments have been passed")
        exit()

    value = switcher.get(key, invalid_cmd)

    # Raise error if wrong command was given
    try:
        value()
    except TypeError:
        print("Command not found. Use -h or --help for a list of commands")


# Print stuff to terminal with colours
def printc(string: str, code: str,) -> None:
    """Class for generating strings with colours on terminal. Uses ANSI Escape Codes to generate them.
    A coloured string must be escaped with RESET, otherwise the chosen colour will persist.

    Args:
    -----
        print_string (str): String to print to terminal.

        code (str): Available arguments: OK/Green, WARNING/Yellow, FAIL/Red
    """
    OK = "\033[92m"  # Green
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOUR

    testvar = "OK".casefold

    if code.casefold() == "ok" or code.casefold() == "green":
        colour = OK
    elif code.casefold() == "warning" or code.casefold() == "yellow":
        colour = WARNING
    elif code.casefold() == "fail" or code.casefold() == "red":
        colour = FAIL
    else:
        raise ValueError(
            "Code arg not valid. Check the printc docstring for help.")

    print("%s%s%s" % (colour, (string), RESET))


if __name__ == "__main__":
    main()
