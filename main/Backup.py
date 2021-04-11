"""Ryerson University ELE 70A Capstone Design Project Fall 2020:
Title: XF06-UV-C BASED GERMS DISINFECTING MACHINE
Group Members: Christopher Jarvis, Alexis Ostrowski, Daniel Ounjankov, Haider Riaz Bosal
"""
import subprocess
import os

filename = os.path.abspath("uvc.py")
while True: #creates an infinite loop to continuously check if the script is running.
    p = subprocess.Popen('python '+filename, shell=True).wait() #Opens a python shell and waits.
    if p != 0: #If the process is not running, then start the process in the python shell we just opened
        continue