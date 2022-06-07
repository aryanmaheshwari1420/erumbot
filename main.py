import datetime
from distutils.command.config import config
import pyttsx3
import pyaudio
import speech_recognition as sr
from py_console import console
import json
import wikipedia
import webbrowser
import os
import smtplib
import random
import platform 
import subprocess
import sys

class Initilize:
    '''
    Attributes will be taken from the config.json file
    initilizing the listining and speak function 
    '''

    config = open('config.json', 'r')
    # print(config.read())
    jsondata = json.loads(config.read())
    config.close()
    email = jsondata['userConfidentials']['email']
    username = jsondata['userConfidentials']['password']
    wakeup_word = 'alexa'

    def main(self):
        # music,video keys can have multiple paths
        self.wishme()
        while(True):
            flag = False
            if(self.email == '' or self.username == ''):
                self.config_setup()
            query = self.takeCommand()
            if(self.wakeup_word in query.lower()):
            
                command = query.lower().split('alexa')[1]
                console.success(f"Command {command}")
                # self.local_call_pic(command)
                # sys.exit() 
                calling_video = self.local_call_video(command)
                if(not calling_video):
                    flag = True
                    calling_music = self.local_call_music(command)
                if(flag):
                    flag = True
                    calling_browser = self.browser_call(command)
                    if(flag):
                        flag = False
                # pass # various taks
            if(flag):
                self.speak("Couldn't find the result for the given input!")
                
    def config_setup(self):
        self.jsondata['userConfidentials']['email'] = input('Email: ')
        self.jsondata['userConfidentials']['username'] = input('Username: ')
        self.jsondata['userConfidentials']['password'] = input('Password: ')
        config = open('config.json', 'w')
        config.write(json.dumps(self.jsondata))
        config.close()
        return

    def speak(self, audio):
        engine  = pyttsx3.init() 
        voices  = engine.getProperty('voices')
        engine.setProperty('voices',voices[0].id) # various voices
        engine.setProperty('rate', 170) # voice speed
        engine.say(audio) # it will speak the main method speak statement
        engine.runAndWait()

    def wishme(self):
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            self.speak("Good Morning! ")
        elif hour>=12 and hour<18:
            self.speak("Good afternoon! ")
        elif hour>=18 and hour<24:
            self.speak('a') #("Hey! what the FUCK is WRONG with you, its fucking night!")    
        # self.speak("Hi there!") 
    
    def takeCommand(self):
        # It takes microphone input from the user and return string output
        recog = sr.Recognizer()
        with sr.Microphone() as source:
            console.log("Listening...")
            recog.pause_threshold = 0.5
            audio = recog.listen(source)
        try:
            console.log("Recognition...")
            query = recog.recognize_google(audio, language='en-in') # using recognize_google for recognize our language 
            console.success(f"User said: {query}\n") 
        except Exception as e:
            console.warn(f"{e}")
            return "None" # if any problem occur then it return none
        return query

    def sendEmail(self, to,content):
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(email,password)
        server.sendmail(email,to,content)
        server.close()

    def browser_call(self,command):
        commands_delim = ["search","open","goto","browse", "google"]
        space_sep_command = command.split(' ')
        print(len(space_sep_command))
        if(len(space_sep_command) ==  1 or len(space_sep_command) == 2):
            return
        flag = True
        ddelim_word = ""
        for delim_word in space_sep_command:
            if(delim_word in commands_delim):
                ddelim_word = delim_word
                flag = False
                break
        # for delim in space_sep_command:
        if(flag):
            return
        index_delim = space_sep_command.index(delim_word)
        url_query = ''.join(space_sep_command[index_delim+1:])
        if('.com' not in url_query):
            url_query = 'https://google.com/search?q='+url_query
        webbrowser.open_new_tab(url_query)
        return
    
    def local_call_music(self, command):
        '''
        Load the music from local system
        '''
        music_path = self.jsondata['MusicPath']
        if(music_path == ''):
            self.jsondata['MusicPath'] = input('MusicPath: ')
            config = open('./config.json', 'w')
            config.write(json.dumps(self.jsondata))
            config.close()
        list_music = os.listdir(music_path)
        commands_delim = ["open","start","play"]
        space_sep_command = command.split(' ')
        flag = True
        ddelim_word = ""
        for delim_word in space_sep_command:
            if(delim_word in commands_delim):
                ddelim_word = delim_word
                flag = False
                break
        if(flag):
            return
        index_delim = space_sep_command.index(delim_word)
        music_query = ''.join(space_sep_command[index_delim+1:])
        try:
            for music in list_music:
                # print(music_query, music)
                if(music.lower() in music_query.lower()):
                    os.startfile(music_path+'\\'+music)
                    return True
            return False
        except Exception as e:
            console.error(e)
            return False
    
    def local_call_video(self, command):
        '''
        Videos from local path
        '''
        video_path = self.jsondata['VideoPath']
        if(video_path == ''):
            self.jsondata['VideoPath'] = input('VideoPath: ')
            config = open('./config.json', 'w')
            config.write(json.dumps(self.jsondata))
            config.close()
        # print(video_path)
        list_video = os.listdir(video_path)
        commands_delim = ["open","start","play"]
        space_sep_command = command.split(' ')
        flag = True
        ddelim_word = ""
        for delim_word in space_sep_command:
            if(delim_word in commands_delim):
                ddelim_word = delim_word
                flag = False
                break
        if(flag):
            return
        index_delim = space_sep_command.index(delim_word)
        video_query = ''.join(space_sep_command[index_delim+1:])+""
        try:
            for video in list_video:
                # print(video_query, music)
                if(video_query.lower() in video.lower()):
                    os.startfile(video_path + '\\' + video)
                    print(video_path+'\\'+video)
                    return True
            return False
        except Exception as e:
            console.error(e)
            return False
    
    def local_call_pic(self, command):
        picture_path = self.jsondata['PicturesPath']
        if(picture_path == ''):
            self.jsondata['PicturesPath'] = input('PicturesPath: ')
            config = open('./config.json', 'w')
            config.write(json.dumps(self.jsondata))
            config.close()
        # print(picture_path)
        list_picture = os.listdir(picture_path)
        print(list_picture)
        commands_delim = ["open","start","play"]
        space_sep_command = command.split(' ')
        flag = True
        ddelim_word = ""
        for delim_word in space_sep_command:
            if(delim_word in commands_delim):
                ddelim_word = delim_word
                flag = False
                break
        if(flag):
            return
        index_delim = space_sep_command.index(delim_word)
        picture_query = ''.join(space_sep_command[index_delim+1:])+""
        try:
            for picture in list_picture:
                print(picture_query.lower() , picture.lower())

                if(picture_query.lower() in picture.lower()):
                    os.startfile(picture_path + '\\' + picture)
                    print(picture_path+'\\'+picture)
                    return True
            return False
        except Exception as e:
            console.error(e)
            return False
def main():
    bot = Initilize()
    bot.main()
    # bot.local_call_music('start excuses')
    
if __name__ == '__main__':
    
    main()
    




