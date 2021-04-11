import speech_recognition as sr
# In order to use a microphone connected to a computer port we need to install a few dependencies: pyaudio, portaudio...
#To use offline speech recognition we need to also install pocketsphynx
import datetime, time
import sys,os
import re

def start_seq():
    door()
    time = timer()
    start_machine(time)
    door()
def door():
    print("Opening Door. Please wait...")
    # Do some commands to control the servo/motor and open the door.
    time.sleep(1) # Waits for 1 seconds after opening door before...tried 3 seconds and it felt too long. Can change this later.
    for i in range(0,21):
        usr_inpt = speech_rec("When you are ready to close the door please say \"Close\".")
        if usr_inpt == "stop" or usr_inpt == "quit": 
            kill()
        if usr_inpt == "close":
            break
        elif i == 20:
            print("Input timeout. Door will now close.")
            break
        else:
            print("Google detected you said {0}. Please say \"Close\" to Close the door.".format(usr_inpt))
        time.sleep(1)
    # Do some commands to control the servo/motor and close the door.
def timer():
    set_time = 1
    for i in range(0, 10):
        usr_inpt = speech_rec("Please select a disinfectant time in minutes or say \"skip\" to disinfect for default time.")
        if usr_inpt.isdigit() == True:
            print("Timer set for {0} minutes.".format(usr_inpt))
            temp = re.findall("\d+", usr_inpt)
            set_time = int(temp[0])
            break
        elif i == 4:
            print("Timeout. Default timer set.")
            break
        elif usr_inpt == "skip":
            print("Default timer set.")
            break
        else:
            print("Google detected you said {0}. Please say a number in minutes to set the timer.".format(usr_inpt))
            time.sleep(1)
    return set_time
def start_machine(end_time):
    r = sr.Recognizer()
    m = sr.Microphone()

    with m as source:
        r.adjust_for_ambient_noise(source) #calibrate background noise.
    stop_listening = r.listen_in_background(m, callback) #spawns a new thread to listen in the background.
    print("Starting Machine...Countdown will now begin.")
    # Do commands to control the relay circuit to start the uv-c lights
    countdown = end_time *60
    clock = end_time * 60 # don't really need this variable...
    
    while countdown: # TODO: Add temperature sensor once set up on rpi. Additional parameter will break loop if temperature is too high.
        if stop_listening == "stop":
            kill()
        mins, secs = divmod(clock, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)
        print(timeformat,"\r", end="")
        #TODO: Find a way to use the listen in background function OR just kill the program with the physical kill button.
        time.sleep(1)
        #check temp and set value.
        clock -=1
        countdown -= 1
    # Do commands to control the relay circuits and stop the uv-c lights 
    print("Sterilization complete.")
    stop_listening() #kills thread.

def kill():
    #Code to turn off relays and open emergency door
    sys.exit() # Kills the script completely. Backup script will re-start script automatically.

def speech_rec(command):
    r = sr.Recognizer() 
    with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print(command)
            audio = r.listen(source, phrase_time_limit= 3)
            try:
                # print("Google Detected you said " + r.recognize_google(audio))
                return r.recognize_google(audio)
            except sr.UnknownValueError:
                print("Did not understand. Try again.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def callback(Recognizer, audio): #will listen in background and kill the script is key word "stop" is said.
#TODO: See if we can use this to "talk" to the main thread to simplify the code.
    try:
        if Recognizer.recognize_google(audio) == "stop" or Recognizer.recognize_google(audio) == "quit" or Recognizer.recognize_google(audio) == "kill":
            os._exit(1)
    except sr.UnknownValueError:
        return
    except sr.RequestError as e:
        return
def main():
    x = True
    while  x == True:
        usr_inpt = speech_rec("Please Say \"Start\" to start uv-c machine.")
        try:
            if usr_inpt == "start":
                print("Google detected you said {0}. Start Command initialized. Please say stop at any point to turn off the machine.".format(usr_inpt))
                start_seq()
            else:
                print("Google detected you said {0}. Please say \"Start\" to start the machine.".format(usr_inpt))
        except AttributeError as e:
            print("Attribute Error. None Type {0}".format(e))
if __name__ == '__main__':
    main()
