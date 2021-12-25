# **PiPlayer**

MP3 player for Raspberry Pi
---
## **Contents**
- [How To Use](#how-to-use)
- [Development](#development)

## **How to Use**
PiPlayer is currently in development, but there's nothing stopping you from trying out its not-so-broken features!

1. The program is meant to run on a Raspberry Pi with a display. It's therefore advisable to test out its features on a Debian based Linux distribution. The programs may break if run on a Windows based system without WSL (Windows Subsystem for Linux).

2. Install git:
```
sudo apt-get update
sudo apt-get install git
```
3. Clone the repository and change to the new directory:
```
git clone https://github.com/asiangoldfish/PiPlayer.git
cd PiPlayer
```
4. The project has a branch for an updated stable version and an unstable, but the most up-to-date version:
```
# Stable version
git checkout main
# Unstable, but most up-to-date version
git checkout main-dev
```
5. Activate Python virtual environment:
```
# Install venv if you don't have it
sudo apt install python3-venv

python3 -m venv venv
source venv/bin/activate
```
6. Install all required packages with pip:
```
# Install pip if you don't have it
sudo apt-get install python3-pip

pip3 install -r requirements.txt
```
6a. Tkinter can be tricky to install. Try the following methods (if one of them works, then skip the others):
Note: Use the last option to install tkinter on Raspberry Pi
```
pip3 install tkinter
sudo apt install python3-tkinter
sudo apt install python-tk
```
7. The video downloader application is able to convert video and incompatible audio formats to the MP3 format. Therefore, install FFmpeg to utilize this application:
```
sudo apt-get install ffmpeg
```

The program comes with two seperate applications: video downloader and mp3 player. To use the video downloader:
```
python3 downloader.py -h
```
To use the mp3 player (this program may or may not work for your setup as it's a GUI application):
```
python3 main.py
```

To install a video to your local disk using [downloader.py](./downloader.py), provide it with a URI or simply search on YouTube using `ytsearch:"[SEARCH KEYWORD]"`. For the most accurate result, use the following format: `[SONG NAME]-[ARTIST]`. Quotation marks are needed in the youtube search to avoid producing errors.

## **Development**
To setup the development environment, follow the [How to Use](#how-to-use) instructions up to the part where you execute the applications.

PiPlayer comes with two applications. One of them, [downloader.py](./downloader.py), is adding songs to the playlist convinient. The other application, [main.py](./main.py), runs the GUI mp3 application. The GUI and its functionalities are powered by tkinter,
