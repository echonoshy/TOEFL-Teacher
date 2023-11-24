import os
import azure.cognitiveservices.speech as speechsdk
import yaml


class AzureASR:
    def __init__(self):
        self.config = self.__init_config()
        SPEECH_KEY = self.config.get("speech").get("SPEECH_KEY")
        SPEECH_REGION = self.config.get("speech").get("SPEECH_REGION")

        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_recognition_language="en-US"
        
        # 默认使用本地麦克风
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    def __init_config(self):
        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
    def recorder(self):
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
        
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # print("Recognized: {}".format(speech_recognition_result.text))

            return speech_recognition_result.text
        
        

if __name__ == "__main__":
    listener = AzureASR().recorder
    listener()
    print("Done")
        