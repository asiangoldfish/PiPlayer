from sys import stdout, exit, argv
from os import system, chdir, getcwd, path, mkdir

# Managing subprocesses, usually run outside Python's control
from subprocess import run, SubprocessError

# File pattern matching
from glob import glob

# For text wrapping multi line strings
from textwrap import dedent

# For downloading videos
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

import config

# Downloads videos from URIs or based on youtube search
def download(working_dir: str = getcwd(), songsfile: str = "songs.txt"):
    """Downloads online videos to local disk

    Takes song or url requests, prompting the user to use requests from the
    file songs.txt, or as invidivual requests from the command line interface.
    Each line in the filerepresents one request. URI validations are simple
    and considers any requests starting with "http" or "www" as valid. Any
    other requests are considered a YouTube search.

    The download destination by default is targeted at /present/working/
    directory/audio/.
    """

    def default_search(request, urls_list = None):
        """Defaults youtube_dl's search option to youtube search

        Args:
            request (str): URI or YouTube search request
        """
        # Default the request to youtube search, unless "http", "www" or similar has been entered.
        subdomains = ["http", "www"]
        if request[0:3] or request[0:2] not in subdomains:
            request = f"ytsearch: {request}"

        urls_list.append(request)

    # Stores all new audio files in audio directory within this project folder. If this folder doesn't exist,
    # then creates a new audio directory. Lastly, changes present directory to this directory.
    audiodir_path = f"{working_dir}/audio/"
    urls_list = list()

    # Keyboard interrupt
    try:
        prompt = input(f"Fetch requests automatically from {songsfile}? [Y/n] ")
    except:
        print("")
        exit(0)

    ###############################
    # If-statement branch 1 start #
    ###############################
    if prompt == "" or prompt == "y" or prompt == "Y":
        """Fetches requests from file with song requests

        The file's name defaults to songs.txt and appends each line to the
        urls_list variable.
        """
        # Opens the songsfile, read each line as request and appends them to
        # the url_listvariable
        try:
            read_songfile = open(songsfile, "r")
        except FileNotFoundError:
            exit(f"File {songsfile} was not found at {getcwd()}/")

        request = read_songfile.readline()

        # Loops through each line and appends each request to the urls_list
        while request:
            request = request.strip("\n")
            default_search(request, urls_list)
            request = read_songfile.readline()

        read_songfile.close()

    ###############################
    # If-statement branch 2 start #
    ###############################
    else:
        """Prompts user to enter a URI or perform a youtube search. A URI must
        begin with either "http", "www" or similar to be considered a valid
        URI. Otherwise it defaults to a youtube search.
        Cancel with CTRL+D, and additionally allows multiple requests at
        the same time.
        """

        print("Enter video URIs. Enter without URI to proceed with downloading")
        print('To instead search on YouTube, prefix with "ytsearch:"')

        # Perform an infinite loop to capture all requests.
        while True:
            try:
                url = input(f"Link: ")
            except KeyboardInterrupt:
                exit("")
            except EOFError:
                exit("")

            if url == "":
                stdout.write("\033[F")  # back to previous line
                stdout.write("\033[K")  # clear line
                break

            # Appends request to urls_list
            default_search(url, urls_list)

    # Terminate program if no input has been provided
    if len(urls_list) <= 0:
        if prompt == "" or prompt == "y" or prompt == "Y":
            exit(f"No URIs were provided in {songsfile}")
        else:
            exit(f"No URIs were provided.")

    # Change directory to audio, so all new files are stored here
    if not path.isdir("audio"):
        mkdir(audiodir_path, 0o777)
    chdir(audiodir_path)

    # Downloads audios
    print("Downloading videos...")
    audio_downloader = YoutubeDL({"format": "bestaudio",
                                  "restrictfilenames": True,
                                  "ignoreerrors": True,
                                  "outtmpl": '%(title)s.%(ext)s'
                                  })

    # Error handle if download uri is invalid
    try:
        audio_downloader.download()
    except DownloadError as e:
        print(e)
        exit("An error occurred the downloads were aborted")
    
    if (config.enable_audio_converter):
        convert_audio()


# Converts video or incompatible audio files to audio file format
def convert_audio() -> None:
    """Rename and/or convert video files to audio files
    """
    # All supported formats that youtube_dl can download a file as.
    # Excludes mp3 and wav formats
    formats = ["3gp", "aac", "flv", "m4a", "mp4", "ogg", "webm"]
    files = list()

    # Searches for all files with the extensions in formats[].
    # Loops through each element in formats, one at a time
    for i, format in enumerate(formats):

        # Searches through all files with specified extension (format[i]),
        # returning a list. Joins this with the existing files[]
        found_files = glob(f"*.{formats[i]}")

        # Do nothing if files with the specified extensions were not found,
        # else append found files to files[]
        if len(found_files) <= 0:
            continue
        else:
            files += found_files

    # Terminate program if no files were round
    if len(files) <= 0:
        print(
            f"Attempting to find files with any of the following extensions: ")

        # Print the list of formats the program searches for
        for format in formats:
            print(f"- {format}")

        exit(
            f"Could not find any matching files to convert..")

    ################################################################################

    print(f"Attempting to convert files in:", end="\n\n")
    for file in files:
        new_file = file.split(f"{getcwd()}")
        print(new_file[0])

    """ # Exit program is user keyboard interrupts
    try:
        prompt = input("\nAre you sure you would like to proceed? [y/N] ")
    except KeyboardInterrupt:1
        exit("\nAborting conversion...")

    if prompt.casefold() == "y":
        print("Converting files to mp3 format...")
    else:
        exit("Aborting conversion...") """

    ################################################################################

    # Convert files in files[] to mp3 format. Documentation: https://pypi.org/project/ffmpy/

    # Store path to unsuccessfully converted files
    failed_files = list()

    for file in files:
        new_path = f"{getcwd()}/{file}"

        # Extracts the file path without extension.
        file_no_ext = new_path.split(".")[0]

        # Adds new extension to the file path
        file_new_ext = f"{file_no_ext}.mp3"

        # Convert file to mp3 formatted file
        try:
            run(
                f"ffmpeg -i '{new_path}' '{file_new_ext}'", shell=True, check=True)
        except Exception as conv_e:
            # All other errors unrelated to the subprocess module
            # Register full path of unsuccessful files during conversion
            print(conv_e)
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

    # If an error happened during the conversion, assume that it's either missing
    # ffmpeg installed on the system or there's an error in the file name
    if len(failed_files) == len(files):
        print("\nErrors were found while attempting to convert files.")
        print("Ensure that ffmpeg is installed on the system: ffmpeg --version")
        print("If not, then there may be special cases in the file name(s)")
        exit()

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
            exit("\nAborting deletion of old files...")
    """

    # Deletes old files one by one if user says yes
    # if prompt.casefold() == "y":

    #print("Deleting old files...")
    for file in files:
        system(f"rm '{file}'")


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
def rename_files(filename: str) -> None:
    """Rename files

    Args:
        filename (str, optional): [description]. Defaults to None.
    """

    # Default filepath
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
        "-d": download,
        "--downloader": download,
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
    # main()
    download()
