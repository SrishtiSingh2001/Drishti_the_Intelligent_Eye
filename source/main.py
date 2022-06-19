import cv2
import os
import datetime
# import functions
import modules.speech as speech
import modules.getIntent as Intent
# import modules.detect as detect

# create an object from speech module
engine = speech.Speech()
listening = False
intent = None

while True:
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not listening:
        resp = engine.recognize_speech()
        if(resp != None):
            intent = Intent.get_intent(resp)
        if(intent == 'drishti' and resp != None):
            listening = True

    else:
        engine.text_to_speech("What can I help you with?")
        intent = ''
        engine.text_to_speech("Listening")
        resp = engine.recognize_speech()
        engine.text_to_speech("Processing")

        if(resp != None):
            intent = Intent.get_intent(resp)
            intent = intent.lower()

            if(intent == 'describe'):
                print("description of the scene")

            elif(intent == 'read'):
                print("read the text")

            elif(intent == 'play'):
                print("play audio")

            elif(intent == 'brightness'):
                print("brightness outside")

            elif(intent == 'form'):
                print("Help me fill the form")

            elif(intent == 'time'):
                print("time right now")

            else:
                # no intent matched
                engine.text_to_speech(
                    "Sorry, I did not understood. Can you say it again?")

cam.release()
