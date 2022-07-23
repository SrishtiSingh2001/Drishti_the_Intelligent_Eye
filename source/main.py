import cv2
import os
import modules.functions as function
import modules.speech as speech
import modules.getIntent as Intent
import modules.detect as detect

# create an object from speech module
engine = speech.Speech()
listening = False
intent = None


while True:
    cam = cv2.VideoCapture(0)
    # if above statement does not work, try cam = cv2.VideoCapture(0)

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
                detect.describeScene(cam=cam)

            elif(intent == 'read'):
                detect.read(cam=cam)

            elif(intent == 'play'):
                function.play_file("audio_files/sound.mp3")

            elif(intent == 'brightness'):
                function.get_brightness(cam=cam)

            elif(intent == 'time'):
                function.get_time()

            elif(intent == 'color'):
                detect.color(cam=cam)

            elif(intent == 'receipt'):
                detect.analyzeReceipt()

            elif(intent == 'weather'):
                function.weatherForecaste()

            elif intent == 'stop':
                listening = False
                engine.text_to_speech(
                    "OK Quitting now, Please tell me if you need my assistance again.")

            elif resp != None:
                # no intent matched
                engine.text_to_speech(
                    "Sorry, I did not understood. Can you say it again?")

    cam.release()
fs
