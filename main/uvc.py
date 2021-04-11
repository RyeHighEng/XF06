"""Ryerson University ELE 70A Capstone Design Project Fall 2020:
Title: XF06-UV-C BASED GERMS DISINFECTING MACHINE
Group Members: Christopher Jarvis, Alexis Ostrowski, Daniel Ounjankov, Haider Riaz Bosal
Github Repo: https://github.com/RyeHighEng/Capstone-Project---UVC-Disinfecting-Machine.git
NOTE: GITHUB repo is outdated and needs to be merged with local changes.
"""
import tkinter as tk
from PIL import Image,ImageTk
import speech_recognition as sr
import datetime, time
import sys,os
import re
# import RPi.GPIO as GPIO
''' This section of the code creates the "GUI" which will display all of the information on the screen.
Unfortunately Tkinter doesn't like to be run in an infinite loop, so if I wanted to move this to a separate class to
clean up the code, it would require threadings. In python there is no real threading due to GIL (global interpreter lock)
so instead it would involve creating subprocesses to circumvent GIL. It is easier to just have everything in the main file.'''
root = tk.Tk()
root.title("UV-C Disinfecting Machine")
root.configure(bg ='#364156' )
root.attributes('-fullscreen', False) # On running the program will maximize (user unable to exit while code is running)
img_dir = os.path.dirname(__file__)
rel_path = "uvc.png"
abs_file_path = os.path.join(img_dir, rel_path)
image = Image.open(abs_file_path) #GUI Background Images.
#TODO: If theres time update the GUI to cycle through a slideshow of helpful tips/ information on COVID.
tk_image = ImageTk.PhotoImage(image)
label_var = tk.StringVar()
my_label = tk.Label(root, textvariable=label_var,image =tk_image, compound='center')
my_label.configure(background='#364156', foreground='white',font=('calibri',36,'bold'))
label_var.set('Welcome!')
my_label.pack(pady=100)

def EmergencyShutdown():
    label_var.set("Shutdown Initiated.")
    root.update()
    # GPIO.output(8, True)
    # GPIO.output(10, True)
    # GPIO.output(12, True)
    # time.sleep(1)
    # GPIO.output(8, False)
    # GPIO.output(10, False)
    # GPIO.output(12, False)
    time.sleep(1)
    os._exit(1)
def timer():
    set_time = 1
    for i in range(0, 11):
        usr_inpt = speech_rec("Please select a disinfectant time in minutes or say \"skip\" to disinfect for default time.")
        if usr_inpt.isdigit() == True:
            label_var.set("Timer set for {0} minutes.".format(usr_inpt))
            root.update()
            temp = re.findall("\d+", usr_inpt)
            set_time = int(temp[0])
            break
        elif i == 10:
            label_var.set("Timeout. Default timer set.")
            root.update()
            break
        elif usr_inpt == "skip":
            label_var.set("Default timer set.")
            root.update()
            break
        else:
            label_var.set("Google detected you said {0}. Please say a number in minutes to set the timer.".format(usr_inpt))
            root.update()
            time.sleep(1)
    return set_time
def speech_rec(command):
    r = sr.Recognizer() # set the variable r to recognize speech input from the mic.
    with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) #Takes a sample of the background noise levels to get a baseline. This makes the voice recognition more accurate.
            label_var.set(command)
            root.update()
            audio = r.listen(source, phrase_time_limit= 3) #Listen for audio. Will wait until audio is detected. Once speech input is recognized, it will record audio for 3 seconds.
            try:
                return r.recognize_google(audio) # Tries to send the audio clip to Google's API, if a response is recieved then return the textual representation of the speech command.
            except sr.UnknownValueError: # Error handling for unknown values (i.e. unrecognizable speech)
                label_var.set("Did not understand. Try again.")
                root.update()
                return 'none'
            except sr.RequestError as e: # Error handling for request errors (i.e. no response from Google's API)
                label_var.set("Could not request results from Google Speech Recognition service; {0}".format(e))
                root.update()
                return 'none'
def callback(Recognizer, audio): #will listen in background and kill the script is key word "stop" is said. Not ideal to use in main program due to the delay time between the two threads
    try:
        if Recognizer.recognize_google(audio) == "stop" or Recognizer.recognize_google(audio) == "quit" or Recognizer.recognize_google(audio) == "kill": #if key is said then exit the program
            EmergencyShutdown()
    except sr.UnknownValueError:
        return
    except sr.RequestError as e:
        return
class Control:
    def __init__(self):
        # Sets GPIO mode (board or
        # GPIO.setmode(GPIO.BOARD)
        # # Set the GPIO Pins to output, input or both
        # GPIO.setup(8, GPIO.OUT)
        # GPIO.setup(10, GPIO.OUT)
        # GPIO.setup(12, GPIO.OUT)
        # GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.PinState(False,False,False) # Null state
        print("init")
    def PinState(self, bool1, bool2, bool3):
        print("pinstate")
        # GPIO.output(8, bool1)
        # GPIO.output(10, bool2)
        # GPIO.output(12, bool3)
    def MotorDir(self, bool1, bool2, bool3, txt):
        label_var.set(txt)
        root.update()
        for i in range(0,3):
            print("motor dir")
            # GPIO.output(8, bool1)
            # GPIO.output(10, bool2)
            # GPIO.output(12, bool3)
            time.sleep(1)
            i = i + 1
        self.PinState(True, False, False) # motor off
        self.PinState(False, False, False) # Null state
    def cooldown(self):
        label_var.set("WARNING: Overheating detected.\nCooldown sequence started.")
        root.update()
        self.MotorDir(False, True, False, "WARNING: Overheating detected.\nCooldown sequence started." )
        self.PinState(True, False, True)
        # while GPIO.input(11):
        #     sleep(1)
        label_var.set("Temperature has reached normal levels.\nCooldown sequence complete.")
        root.update()
        self.PinState(True, True, False)
        time.sleep(1)
        self.MotorDir(False, True, True, "Door is now closing")
        time.sleep(1)
    def waitToClose(self, txt):
        for i in range(0,21):
            usr_inpt = speech_rec("When you are ready to close the door please say \"Close\".")
            if usr_inpt == "stop" or usr_inpt == "quit":
                EmergencyShutdown()
            if usr_inpt == "close":
                break
            elif i == 20:
                label_var.set("Input timeout. Door will now close.")
                root.update()
                break
            else:
                label_var.set("Google detected you said {0}. Please say \"Close\" to Close the door.".format(usr_inpt))
                root.update()
            time.sleep(1)
        self.MotorDir(False, True, True, txt)
    def start_machine(self, end_time):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source) #calibrate background noise.
        stop_listening = r.listen_in_background(m, callback) #spawns a new thread to listen in the background. This will allow the main thread to be terminated by the second thread.
        label_var.set("Starting Machine...Countdown will now begin.")
        root.update()
        countdown = end_time *60
        clock = end_time * 60
        self.PinState(False, False, True)
        while countdown:
            # tempHigh = GPIO.input(11)
            tempHigh = False
            if stop_listening == "stop":
                EmergencyShutdown()
            if tempHigh == True:
                self.cooldown()
                break
            mins, secs = divmod(clock, 60) #returns a tuple of the quotient and the remainder ex: divmod(8,3) returns (2,2). This funtion will get us minutes and seconds.
            timeformat = "{:02d}:{:02d}".format(mins, secs)
            label_var.set(f"Time Remaining: {timeformat}\nTemperature: Normal")
            root.update()
            time.sleep(1)
            #check temp and exit if PI becomes too hot. Arduino will have a temperature monitor for the circuit
            clock -=1
            countdown -= 1
        if tempHigh == False:
            label_var.set("Sterilization complete.")
            root.update()
        stop_listening()

def main():
    control = Control()
    x = True
    while  x == True: # Disinfectant machine will run on an infinite loop.
        # reseting the overheat function in case it was triggered.
        global overheat
        overheat = False
        usr_inpt = speech_rec("Please Say \"Start\" to start uv-c machine.")
        try:
            if usr_inpt == "start": # Key word detected. Start the disinfectant process.
                label_var.set("Google detected you said {0}. Start Command initialized. Please say stop at any point to turn off the machine.".format(usr_inpt))
                root.update()
                control.MotorDir(False, True, False, "Door Opening...Please Wait.")
                control.waitToClose("Door is now closing...Please Wait.")
                time = timer()
                control.start_machine(time)
                control.MotorDir(False, True, False, "Door Opening...Please Wait.")
                control.waitToClose("Door is now Closing...Please Wait.")
            else: # Key word not detected. Try again.
                label_var.set("Google detected you said {0}. Please say \"Start\" to start the machine.".format(usr_inpt))
                root.update()

        except AttributeError as e:
            label_var.set("Attribute Error. None Type {0}".format(e))
            root.update()

if __name__ == '__main__':
    root.after(100,main)
    root.mainloop()
