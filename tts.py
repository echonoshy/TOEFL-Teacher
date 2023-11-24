import os
import azure.cognitiveservices.speech as speechsdk
import yaml



class AzureTTS:
    def __init__(self):
        self.config = self.__init_config()
        SPEECH_KEY = self.config.get("speech").get("SPEECH_KEY")
        SPEECH_REGION = self.config.get("speech").get("SPEECH_REGION")
        voice_name = self.config.get("chat").get("rolePlay").get("roleType").get("ToeflTeacher").get("voiceName")
        
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        
        speech_config.speech_synthesis_voice_name = voice_name
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        
    def __init_config(self):
        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    
    def speaker(self, text):
        assert isinstance(text, str)

        # 配置嗓音、角色和情感
        content = f"""  
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
                <voice name="en-US-JennyNeural">
                    <mstts:express-as role="Girl" style="cheerful">
                        <prosody rate="+10.00%">
                            {text}
                        </prosody>  
                    </mstts:express-as>

                </voice>
            </speak>
            
            """
        
        # 发音
        # speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()
        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(ssml=content).get()
 
 
 
if __name__ == "__main__":
    speaker = AzureTTS().speaker 
    speaker("Nice to meet you sir.")