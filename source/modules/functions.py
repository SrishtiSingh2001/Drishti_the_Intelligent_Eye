import cv2
import numpy as np
import os
import modules.speech as speech
import time
import datetime

engine = speech.Speech()


def get_brightness(cam):
    ret, frame = cam.read()
    if ret == None:
        engine.text_to_speech("Not getting any frame. Quitting now...")
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg = np.sum(frame) / (frame.shape[0] * frame.shape[1])
        avg = avg / 255
        brightness = None
        if(avg > 0.6):
            brightness = "Very bright"
        elif(0.4 < avg <= 0.6):
            brightness = "Bright"
        elif(0.2 < avg <= 0.4):
            brightness = "Dim"
        else:
            brightness = "Dark"

        engine.text_to_speech("It is {} outside".format((brightness)))

    return


def play_file(fname):
    os.system("start " + fname)
    time.sleep(4)
    return


def get_time():

    currentDT = datetime.datetime.now()

    engine.text_to_speech("The time is {} hours and {} minutes".format(
        currentDT.hour, currentDT.minute))

    return
