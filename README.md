# XF06
This repository contains the code for Ryerson Department of Electrical, Computer and Biomedical Engineering Capston Project XF06 - UVC Based Disinfecting Machine control system.
This code is intended to be used on the Raspberry Pi in conjunction with an Arduino which interprets the control signals to physically control the circuit components.
The main program is written entirely in Python, and uses the Speech Recognition library to connect to Google's Deep Learning/AI powered Speech Recognition API.

Before running any of the programs in this repository there are a few dependencies which needs to be installed which are outlined below. The easiest way to install thee libraries
is by using "pip install <package name>", however the .whl files can downloaded from  https://pypi.org/ and then installed using "pip install <directory>/package.whl".
Packages can also be downloaded and unzipped directly into the python path. If you don't know where your python is installed you can create a python file an import sys and
use print(sys.path) to find the installation location.

Dependencies:

1. Python 3 (Testing and work was completed on Python 3.8.3)
2. If not installed with python, install pip.
3. pip install SpeechRecognition, Pillow, pyaudio, RPi.GPIO
4. install portaudio from http://www.portaudio.com/ (pyaudio is a binding for PortAudio v19)


After the installation is complete you can test the functionality of the of the speech recognition and control of the RPi's GPIO pins by using the files included in the test folder.