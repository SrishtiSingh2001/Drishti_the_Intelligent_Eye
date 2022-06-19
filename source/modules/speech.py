import azure.cognitiveservices.speech as speechsdk
from modules.keys import keys


class Speech():
    def __init__(self):
        speech_config = speechsdk.SpeechConfig(
            subscription=keys['speech_key'], region=keys['speech_region'])

        audio_config_output = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True)

        audio_config_input = speechsdk.audio.AudioConfig(
            use_default_microphone=True)

        # The language of the voice that speaks.
        # speech_config.speech_synthesis_voice_name = 'hi-IN-SwaraNeural'
        speech_config.speech_recognition_language = "en-US"

        # The language of the voice that inputs
        speech_config.speech_recognition_language = "en-US"

        # create an instance to convert texts to speech
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config_output)

        # create an instance to recognize speech
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config_input)

        # custom training
        phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(
            self.speech_recognizer)
        phrase_list_grammar.addPhrase("Drishti")
        phrase_list_grammar.clear()

    def recognize_speech(self):
        print("Speak into your microphone.")

        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
            return speech_recognition_result.text

        return None

    def text_to_speech(self, text):

        speech_synthesis_result = self.speech_synthesizer.speak_text_async(
            text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(
                        cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
