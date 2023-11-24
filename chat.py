import requests
import json 
import yaml

from pynput import keyboard
from pynput.keyboard import Key, Listener

import os, sys
sys.path.append(os.getcwd())

from tts import AzureTTS
from asr import AzureASR


speaker = AzureTTS().speaker
recorder = AzureASR().recorder


class ChatBot:
    def __init__(self):
        config = self.__init_config()
        self.openai_url = config.get("chat").get("openai").get("url")
        self.openai_key = config.get("chat").get("openai").get("key")
        self.role_setting = config.get("chat").get("rolePlay").get("roleType").get("ToeflTeacher").get("roleSetting")
        
        self.user_input = ""
    
    def __init_config(self):
        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config


    def get_openai_response(self, history):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": history,
            "temperature": 0.7,
        }
        response = requests.post(self.openai_url, headers=headers, json=data)
        
        # TODO: 这里应该增加请求失败二次请求的功能
        message = json.loads(response.text).get("choices")[0].get("message").get("content")
        return message

    def key_board_on_press(self, key):
        if key == keyboard.Key.shift:
            self.user_input = recorder()

        
    def key_board_on_release(self, key):
        if key == keyboard.Key.shift:
            return False
    

    def chat_termial_client(self):
        # 在终端中的对话演示
        print("Neko: Hi here, welcome to Neko's English course.")
        speaker("Hi here, welcome to Neko's English course.")
        
        # TODO: history manager function
        history = [
            {"role":"system", "content": self.role_setting},
            {"role":"user", "content": "Let's start!"},
            {"role":"assistant", "content": "Understood"}
        ]
            
        while True:
            try:
                with Listener(on_press=self.key_board_on_press, on_release=self.key_board_on_release) as listener:
                    listener.join()
                
                # 空内容不请求
                if self.user_input: 
                    print(f"\nYou: {self.user_input}")  
                    if self.user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                        print("Neko: Goodbye!")
                        speaker("Goodbye!")
                        break    
                    
                    history.append({"role": "user", "content": self.user_input})
                    message = self.get_openai_response(history)
                    print(f"Neko: {message}")
                    speaker(message)
                    
                    history.append({"role": "assistant", "content": message})
                    
                    self.user_input = ""   
                
            except Exception as e:
                pass
                    

if __name__ == "__main__":
    ChatBot().chat_termial_client()