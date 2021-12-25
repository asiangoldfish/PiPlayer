# Audio Downloader

Audio Downloader is a cross-platform application and is also compatible with a vast range of [sites](http://online.verypdf.com/app/youtube-downloader/supported-video-sites.php) and provides a simple way to download your favourite songs, podcasts and other audio tracks. It utilizes [youtube_dl](https://github.com/ytdl-org/youtube-dl/tree/2021.12.17) to perform the download, and [FFmpeg](https://ffmpeg.org/) for converting to audio files. Other features include:
- Batch download
- Search with the command line interface

## Contents
- [Setup Guide](#how-to-use)
- [How to Use](#how-to-use)

## Setup Guide
Setting up the Audio Downloader is a simple and straight forward task. Below you can pick the guide for your operating system:
- [Debian](./docs/debian)

## How to Use
Once you've setup the application, simply run the `python3 main.py` command to begin. You can either search a song using a URI that starts with "http" or "www", or directly make a youtube search. The application has two modes.

### Batch Requests
Create a new file called "songs.txt". Each line represents one request. Example:
```
1. Hello - Some Random Artist
2. World - A Music Group (ft. Bye)
3. https://requests.audiodownloader.com
```
Once you run the command `python3 main.py`, enter "y" to fetch the requests.

### Command Line Interface Requests
When prompted after starting the application, enter "n". Then search for the song to download.
