from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from discord_webhook import DiscordWebhook, DiscordEmbed
from twitchAPI.object.eventsub import ChannelFollowEvent, StreamOnlineEvent, ChannelPollBeginEvent, ChannelPollEndEvent, ChannelPredictionEvent, ChannelPredictionEndEvent, HypeTrainEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, ChannelAdBreakBeginEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from twitchAPI.pubsub import PubSub
from collections import OrderedDict
from pytube import YouTube
from contextlib import suppress
import numpy as np
from colorama import Fore, init
from multiprocessing import Pool
from datetime import datetime, timedelta
import win32gui
import pytz
import vlc
from global_hotkeys import *
import logging

from num2words import num2words

import subprocess
import traceback
import requests
import pyttsx3
import threading
import requests
import asyncio
import ffmpeg
import random
import yaml
import time
import json
import uuid
import sys
import os

from pydub import AudioSegment

from pyt2s.services import acapela
from pyt2s.services import cepstral
from pyt2s.services import ibm_watson
from pyt2s.services import oddcast
from pyt2s.services import stream_elements
from pyt2s.services import streamlabs
from pyt2s.services import voice_forge

import pyttsx3


import wave, audioop

import re

# from playsound import playsound
from playsound3 import playsound

import obsws_python as obs
# from obsws_python import ConnectionRefusedError

twitch = None
streamer = None
chat = None
live = False

bot_id = "1020563705"

# cmd = 'mode 100,20'
# os.system(cmd)
init(convert=True)
hwnd = win32gui.GetForegroundWindow()
win32gui.MoveWindow(hwnd, 30, 30, 850, 440, True)

# APP_ID = 'tglr18k2kmbpq7y1k8a2y4376iau1c'
# APP_SECRET = 'yx01kqkx0yp5rvz5pvjyyba2f7aksx'

vayl_version = "1.3.22"

APP_ID = 'xfc4596ekgo4ewkag6wn01hgs4hfbl'
APP_SECRET = 'p8wl2zzuk3sgjmbdrlxe9l65xno8wk'

USER_SCOPE = [AuthScope.USER_READ_SUBSCRIPTIONS, AuthScope.MODERATION_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, 
              AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS, AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
              AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.MODERATOR_READ_FOLLOWERS, 
              AuthScope.WHISPERS_READ, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_POLLS, AuthScope.CHANNEL_MANAGE_POLLS, AuthScope.CHANNEL_READ_ADS,
              AuthScope.MODERATOR_MANAGE_SHOUTOUTS, AuthScope.MODERATOR_READ_SHOUTOUTS, AuthScope.CHANNEL_READ_PREDICTIONS, AuthScope.CHANNEL_MANAGE_PREDICTIONS,
              AuthScope.CHANNEL_READ_HYPE_TRAIN, AuthScope.CHANNEL_MANAGE_VIPS, AuthScope.CHANNEL_MANAGE_BROADCAST, AuthScope.ANALYTICS_READ_GAMES]
TARGET_CHANNEL = ''

with open(os.getcwd() + "\\configuration\\credentials.yml", 'r', encoding = "utf-8") as file:
    data = yaml.safe_load(file)
    TARGET_CHANNEL = data["connected-account"]




## Variables
########################################
sfx = {}
##
commands = {}
alert_queue = []
##
phrase_cooldown = {}
########################################




## TTS #############################################################################
tts_voice = { "cepstral"        : ["Allison", "Amy", "Belle", "Callie", "Charlie", "Dallas", "Damien", "David", "Diane", "Duchess", "Emily", "Linda", "Robin", "Shouty", "Walter", "William", "Whispery", "Lawrence", "Millie", "Duncan", "Vittoria", "Katrin", "Matthias", "Isabelle", "Jean-Pierre", "Alejandra", "Miguel"],
              "imbwatson"       : ["en-GB_CharlotteV3Voice", "en-GB_JamesV3Voice", "en-GB_KateV3Voice", "en-AU_JackExpressive", "en-AU_HeidiExpressive", "en-US_AllisonV3Voice", "en-US_AllisonExpressive", "en-US_EmilyV3Voice", "en-US_EmmaExpressive", "en-US_HenryV3Voice", "en-US_KevinV3Voice", "en-US_LisaV3Voice", "en-US_LisaExpressive", "en-US_MichaelV3Voice", "en-US_MichaelExpressive", "en-US_OliviaV3Voice", "nl-NL_MerelV3Voice", "fr-FR_NicolasV3Voice", "fr-FR_ReneeV3Voice", "fr-CA_LouiseV3Voice", "de-DE_BirgitV3Voice", "de-DE_DieterV3Voice", "de-DE_ErikaV3Voice", "it-IT_FrancescaV3Voice", "ja-JP_EmiV3Voice", "ko-KR_JinV3Voice", "pt-BR_IsabelaV3Voice", "es-ES_EnriqueV3Voice", "es-ES_LauraV3Voice", "es-LA_SofiaV3Voice", "es-US_SofiaV3Voice"],
              "oddcast"         : ["4-3-1", "6-2-1", "5-4-1", "4-2-1", "5-3-1", "2-7-1", "1-7-1", "7-4-1", "5-2-1", "12-4-1", "8-4-1", "9-2-1", "10-2-1", "4-7-1", "4-4-1", "10-4-1", "3-7-1", "13-4-1", "5-7-1", "6-7-1", "9-4-1", "11-2-1", "7-2-1", "6-3-1", "8-3-1", "7-7-1", "3-1-1", "1-1-1", "2-2-1", "7-3-1", "2-4-1", "3-3-1", "1-3-1", "2-1-1", "2-3-1", "4-1-1", "11-4-1", "8-2-1", "1-2-1", "3-4-1", "8-7-1", "1-7-27", "2-7-27", "2-2-27", "1-4-27", "1-2-27", "1-4-22", "3-2-5", "2-2-5", "1-2-5", "1-4-5", "3-3-10", "5-3-10", "4-3-10", "1-2-10", "2-2-10", "4-4-10", "4-7-10", "6-3-10", "7-3-10", "1-4-10", "3-7-10", "2-7-10", "1-7-10", "2-4-10", "8-3-10", "1-7-18", "1-4-18", "1-7-19", "2-7-19", "1-2-19", "1-4-19", "2-2-19", "2-4-11", "2-7-11", "1-7-11", "2-2-11", "1-2-11", "4-4-11", "1-4-11", "1-2-31", "2-7-32", "1-7-32", "2-2-23", "1-4-23", "1-2-23", "1-7-23", "2-1-4", "2-7-4", "1-7-4", "2-2-4", "4-2-4", "3-2-4", "1-1-4", "4-3-4", "3-3-4", "3-4-4", "5-4-4", "4-4-4", "5-2-4", "1-3-4", "1-4-4", "4-7-4", "2-4-4", "2-3-4", "3-7-4", "6-2-4", "3-1-4", "1-2-15", "3-4-3", "2-7-3", "1-7-3", "3-2-3", "1-1-3", "1-3-3", "2-1-3", "2-2-3", "1-4-3", "2-3-3", "2-4-3", "1-2-8", "1-4-8", "1-7-8", "2-7-8", "3-2-8", "2-7-24", "1-4-24", "1-7-24", "1-4-29", "1-7-29", "2-7-28", "1-4-28", "1-7-28", "2-7-7", "1-7-7", "1-3-7", "10-2-7", "9-2-7", "5-2-7", "6-2-7", "8-2-7", "1-2-7", "1-4-7", "7-2-7", "2-3-7", "2-2-7", "2-4-7", "3-2-7", "6-3-12", "5-3-12", "1-7-12", "2-7-12", "1-4-12", "3-3-12", "7-3-12", "4-3-12", "2-3-12", "8-3-12", "7-3-13", "4-3-13", "8-3-13", "10-3-13", "5-3-13", "2-3-13", "1-4-13", "6-3-13", "1-3-13", "9-3-13", "1-7-20", "2-2-20", "2-7-20", "2-4-20", "1-2-20", "1-4-14", "1-7-14", "2-2-14", "2-7-14", "1-2-14", "2-7-6", "3-4-6", "3-7-6", "4-7-6", "1-7-6", "1-3-6", "2-3-6", "2-4-6", "1-2-30", "1-4-30", "2-2-21", "2-4-21", "1-2-21", "1-7-37", "3-4-37", "1-2-2", "6-2-2", "2-2-2", "9-2-2", "4-3-2", "5-3-2", "1-4-2", "3-4-2", "7-2-2", "8-2-2", "10-2-2", "4-2-2", "3-2-2", "2-1-2", "5-2-2", "2-3-2", "3-3-2", "5-4-2", "4-4-2", "1-1-2", "1-3-2", "1-4-9", "1-2-9", "1-7-9", "2-7-9", "3-4-9", "2-2-9", "1-4-26", "1-3-26", "2-3-26", "1-4-16", "2-7-16", "1-2-16", "3-2-16", "1-7-16", "2-2-16", "1-7-40"],
              "streamelements"  : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Mia", "Miguel", "Penelope", "Astrid", "Filiz", "Gwyneth", "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E", "en-US-Wavenet-F", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D", "en-AU-Standard-C", "en-AU-Standard-D", "en-IN-Wavenet-A", "en-IN-Wavenet-B", "en-IN-Wavenet-C", "af-ZA-Standard-A", "ar-XA-Wavenet-A", "ar-XA-Wavenet-B", "ar-XA-Wavenet-C", "bg-bg-Standard-A", "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-B", "cmn-CN-Wavenet-C", "cmn-CN-Wavenet-D", "cs-CZ-Wavenet-A", "da-DK-Wavenet-A", "nl-NL-Standard-A", "nl-NL-Wavenet-A", "nl-NL-Wavenet-B", "nl-NL-Wavenet-C", "nl-NL-Wavenet-D", "nl-NL-Wavenet-E", "fil-PH-Wavenet-A", "fi-FI-Wavenet-A", "fr-FR-Standard-C", "fr-FR-Standard-D", "fr-FR-Wavenet-A", "fr-FR-Wavenet-B", "fr-FR-Wavenet-C", "fr-FR-Wavenet-D", "fr-CA-Standard-A", "fr-CA-Standard-B", "fr-CA-Standard-C", "fr-CA-Standard-D", "de-DE-Standard-A", "de-DE-Standard-B", "de-DE-Wavenet-A", "de-DE-Wavenet-B", "de-DE-Wavenet-C", "de-DE-Wavenet-D", "el-GR-Wavenet-A", "hi-IN-Wavenet-A", "hi-IN-Wavenet-B", "hi-IN-Wavenet-C", "hu-HU-Wavenet-A", "is-is-Standard-A", "id-ID-Wavenet-A", "id-ID-Wavenet-B", "id-ID-Wavenet-C", "it-IT-Standard-A", "it-IT-Wavenet-A", "it-IT-Wavenet-B", "it-IT-Wavenet-C", "it-IT-Wavenet-D", "ja-JP-Standard-A", "ja-JP-Wavenet-A", "ja-JP-Wavenet-B", "ja-JP-Wavenet-C", "ja-JP-Wavenet-D", "ko-KR-Standard-A", "ko-KR-Wavenet-A", "lv-lv-Standard-A", "nb-no-Wavenet-E", "nb-no-Wavenet-A", "nb-no-Wavenet-B", "nb-no-Wavenet-C", "nb-no-Wavenet-D", "pl-PL-Wavenet-A", "pl-PL-Wavenet-B", "pl-PL-Wavenet-C", "pl-PL-Wavenet-D", "pt-PT-Wavenet-A", "pt-PT-Wavenet-B", "pt-PT-Wavenet-C", "pt-PT-Wavenet-D", "pt-BR-Standard-A", "ru-RU-Wavenet-A", "ru-RU-Wavenet-B", "ru-RU-Wavenet-C", "ru-RU-Wavenet-D", "sr-rs-Standard-A", "sk-SK-Wavenet-A", "es-ES-Standard-A", "sv-SE-Standard-A", "tr-TR-Standard-A", "tr-TR-Wavenet-A", "tr-TR-Wavenet-B", "tr-TR-Wavenet-C", "tr-TR-Wavenet-D", "tr-TR-Wavenet-E", "uk-UA-Wavenet-A", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "Linda", "Heather", "Sean", "Hoda", "Naayf", "Ivan", "Herena", "Tracy", "Danny", "Huihui", "Yaoyao", "Kangkang", "HanHan", "Zhiwei", "Matej", "Jakub", "Guillaume", "Michael", "Karsten", "Stefanos", "Szabolcs", "Andika", "Heidi", "Kalpana", "Hemant", "Rizwan", "Filip", "Lado", "Valluvar", "Pattara", "An"],
              "streamlabs"      : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zeina", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Lea", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Camila", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Lucia", "Mia", "Miguel", "Lupe", "Penelope", "Astrid", "Filiz", "Gwyneth"],
              "voiceforge"      : ["Conrad", "Designer", "Diesel", "Dog", "Evilgenius", "Frank", "French-fry", "Gregory", "Jerkface", "JerseyGirl", "Kayla", "Kevin", "Kidaroo", "Princess", "RansomNote", "Robot", "Shygirl", "Susan", "Tamika", "TopHat", "Vixen", "Vlad", "Warren", "Wiseguy", "Zach", "Obama"]}
# "acapela"         : ["graham22k", "harry22k", "lucy22k", "lucy_nt22k", "peter22k", "peter_nt22k", "queenelizabeth22k", "queenelizabeth_nt22k", "rachel22k", "rachel_nt22k", "rosie22k", "sophiabtob22k", "sophiabtob_nt22k", "rhona22k", "rhona_nt22k", "liam22k", "lisa22k", "lisa_nt22k", "olivia22k", "tyler22k", "tyler_nt22k", "deepa22k", "deepa_nt22k", "nizareng22k", "nizareng_nt22k", "darius22k", "darius_nt22k", "ella22k", "emilioenglish22k", "josh22k", "karen22k", "karen_nt22k", "laura22k", "laura_nt22k", "lily22k", "lily_nt22k", "micah22k", "rod22k", "rod_nt22k", "ryan22k", "ryan_nt22k", "saul22k", "saul_nt22k", "scott22k", "sharon22k", "sharon_nt22k", "tamira22k", "tamira_nt22k", "taylor22k", "taylor_nt22k", "tracy22k", "tracy_nt22k", "valeriaenglish22k", "will22k", "will_nt22k", "leila22k", "leila_nt22k", "jalal22k", "jalal_nt22k", "mehdi22k", "mehdi_nt22k", "nizar22k", "nizar_nt22k", "salma22k", "salma_nt22k", "laia22k", "laia_nt22k", "lulu22k", "lulu_nt22k", "eliska22k", "eliska_nt22k", "mette22k", "mette_nt22k", "rasmus22k", "rasmus_nt22k", "rikke22k", "rikke_nt22k", "daan22k", "daan_nt22k", "femke22k", "femke_nt22k", "jasmijn22k", "jasmijn_nt22k", "max22k", "max_nt22k", "tessabtob22k", "tessabtob_nt22k", "christinabtob22k", "christinabtob_nt22k", "jeroen22k", "jeroen_nt22k", "sofie22k", "sofie_nt22k", "zoe22k", "zoe_nt22k", "hanna22k", "hanna_nt22k", "hanus22k", "hanus_nt22k", "sanna22k", "sanna_nt22k", "alice22k", "alice_nt22k", "anais22k", "anais_nt22k", "anaisbtob22k", "anaisbtob_nt22k", "antoine22k", "antoine_nt22k", "bruno22k", "bruno_nt22k", "claire22k", "claire_nt22k", "constance22k", "constance_nt22k", "elise22k", "julie22k", "julie_nt22k", "manon22k", "manon_nt22k", "margaux22k", "margaux_nt22k", "valentin22k", "anthony22k", "anthony_nt22k", "louise22k", "louise_nt22k", "alice-be22k", "alice-be_nt22k", "anais-be22k", "anais-be_nt22k", "antoine-be22k", "antoine-be_nt22k", "bruno-be22k", "bruno-be_nt22k", "claire-be22k", "claire-be_nt22k", "elise-be22k", "julie-be22k", "julie-be_nt22k", "manon-be22k", "manon-be_nt22k", "margaux-be22k", "margaux-be_nt22k", "valentin-be22k", "andreas22k", "andreas_nt22k", "ankebtob22k", "ankebtob_nt22k", "claudia22k", "claudia_nt22k", "jonas22k", "julia22k", "julia_nt22k", "klaus22k", "klaus_nt22k", "lea22k", "sarah22k", "sarah_nt22k", "dimitris22k", "dimitris_nt22k", "alessio22k", "aurora22k", "barbarabtob22k", "barbarabtob_nt22k", "chiara22k", "chiara_nt22k", "fabiana22k", "fabiana_nt22k", "vittorio22k", "vittorio_nt22k", "sakura22k", "sakura_nt22k", "minji22k", "minji_nt22k", "bente22k", "bente_nt22k", "elias22k", "emilie22k", "ida22k", "ida_nt22k", "kari22k", "kari_nt22k", "olav22k", "olav_nt22k", "ania22k", "ania_nt22k", "gosia22k", "gosia_nt22k", "isabel22k", "isabel_nt22k", "gabriela22k", "gabriela_nt22k", "marcia22k", "marcia_nt22k", "sergio22k", "sergio_nt22k", "alyona22k", "alyona_nt22k", "lena22k", "lena_nt22k", "biera_hmm_22k", "elle_hmm_22k", "anabtob22k", "anabtob_nt22k", "antonio22k", "antonio_nt22k", "elenabtob22k", "elenabtob_nt22k", "ines22k", "ines_nt22k", "maria22k", "maria_nt22k", "emilio22k", "rodrigo22k", "rodrigo_nt22k", "rosa22k", "rosa_nt22k", "valeria22k", "elin22k", "elin_nt22k", "emil22k", "emil_nt22k", "emma22k", "emma_nt22k", "erik22k", "erik_nt22k", "filip22k", "freja22k", "kal22k", "kal_nt22k", "mia22k", "mia_nt22k", "samuel22k", "samuel_nt22k", "ipek22k", "ipek_nt22k", "zeynep22k", "zeynep_nt22k"],                                                                  
####################################################################################




# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print (" ")
    print ("                                          Welcome to Vayl")
    print (" ")
    await ready_event.chat.join_room(TARGET_CHANNEL)
    await reload(False)
    
  
async def logError (info = None):

    global TARGET_CHANNEL
    global vayl_version
    
    isExist = os.path.exists(os.getcwd() + "\\logs\\")
    if not isExist:
        os.makedirs(os.getcwd() + "\\logs\\")
    
    timestamp = str(time.time())
    with open (os.getcwd() + "\\logs\\" + timestamp + ".txt", 'w') as log_file:
        log_file.write("User: " + TARGET_CHANNEL + "\n")
        log_file.write("Version: " + vayl_version + "\n")
        
        if info:
            log_file.write("Info:" + "\n")  
            for line in info:
                log_file.write("- " + line + "\n") 
        
        log_file.write(traceback.format_exc())
        
        
    try:    
        with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            if "bug-auto-report" in data:
                if data["bug-auto-report"]:
                    # webhook.add_file(file=f.read(), filename="example.jpg")
                    
                    with open (os.getcwd() + "\\logs\\" + timestamp + ".txt", 'r') as log_file:
                        webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/1257675918957351013/wiIdAeOQBaXdhzyLrPRhplWz2mBbfZrTbch--c-5wMYDu1YYk2gUexBj6AUMTahnPlZs", username = "Bug Report", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png")
                        webhook.add_file(file = log_file.read(), filename= timestamp + ".txt")
                        # webhook.add_embed(embed)
                        response = webhook.execute()

    except Exception as e:
        print (e)
        # prompt ("misc", "Vayl Configuration not found, please download 'configuration.yml' from provided ZIP.")
        
        
def prompt (type, message):
    symbol = {"success": f"[{Fore.GREEN}♦{Fore.WHITE}]",
              "error": f"[{Fore.LIGHTRED_EX}!{Fore.WHITE}]",
              "bits": f"[{Fore.MAGENTA}▲{Fore.WHITE}]",
              "hotkey": f"[{Fore.BLUE}►{Fore.WHITE}]",
              "follow": f"[{Fore.YELLOW}★{Fore.WHITE}]",
              "sub": f"[{Fore.YELLOW}★{Fore.WHITE}]",
              "misc": f"[{Fore.WHITE}♦{Fore.WHITE}]"
              }
    
    print (symbol[type] + " " + message) 



# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    try:
        message = msg.text
        
        with open(os.getcwd() + "\\configuration\\phrases.yml", 'r', encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            
            for phrase in data["phrase"]:
                valid = False
                if data["phrase"][phrase]["exact"] and message == phrase:
                    valid = True
                elif data["phrase"][phrase]["contains"] and phrase in message:
                    valid = True
        
                if valid:
                
                    if phrase not in phrase_cooldown:
                        phrase_cooldown[phrase] = 0
                        
                    if time.time() - phrase_cooldown[phrase] >= data["phrase"][phrase]["cooldown"]:
                    
                        variables = {}
                        variables["user"] = msg.user.name
                        
                        actions = data["phrase"][phrase]["actions"]
                        await runActions(actions, variables)
                        
        if "!addquote" in message:
            try:
                    
           
                if msg.reply_parent_msg_body:
            
                    quote_message = " ".join(msg.reply_parent_msg_body.split("\s"))
                    quote_author = msg.reply_thread_parent_user_login
                    
                    line = '"' + quote_message + '" - ' + quote_author + ", " + str(datetime.now().year)
                    total = 0
                    with open(os.getcwd() + "\\resources\\quotes.yml", 'a+', encoding="utf-8") as file:
                        total = len(file.readlines())
                        file.write("\n" + line)
                    await chat.send_message(TARGET_CHANNEL, "Quote #" + str(total) + " Added: " + line)
                else:
                    await chat.send_message(TARGET_CHANNEL, "!addquote must be used as a reply.")
                    
                    
            except:
                prompt ("error", "Error creating quote.")
                await logError()
            

                    
    except Exception as e:
        print (f"[{Fore.RED}♦{Fore.WHITE}]] Error handling MessageEvent.")
        await logError()
   
    # print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')

async def on_raid (raid: dict):
    try:
    
        alert = {}
        alert["type"] = "raid"
        alert["user"] = raid["tags"]["display-name"]
        alert["viewercount"] = str(raid["tags"]["msg-param-viewerCount"])
                
        with open(os.getcwd() + "\\variables\\latest-raid-raider.txt", 'w', encoding = "utf-8") as file:
            file.write(raid["tags"]["display-name"])          
        with open(os.getcwd() + "\\variables\\latest-raid-amount.txt", 'w', encoding = "utf-8") as file:
            file.write(str(raid["tags"]["msg-param-viewerCount"]))          
                
        alert_queue.append(alert)
          
    except Exception as e:
        prompt ("error", "Error handling RaidEvent.")
        await logError()
                            
        


## Reload Command ###################################################
async def reload_command (cmd: ChatCommand):
    if await isStreamer(cmd.user.name):
        await reload(True)
#####################################################################




## Custom Commands ##################################################
async def custom_command (cmd: ChatCommand):
    
    command = cmd.name
    arguments = cmd.parameter.split(" ")
    
    
    
    try:
        
        user = cmd.user.name
        
        # print (cmd.user.badges)
        global straamer
        
        global commands
        if user not in commands[command]["user-cooldown"]:
            commands[command]["user-cooldown"][user] = 0
        
        with open(os.getcwd() + "\\configuration\\commands.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)

        
            is_streamer = await isStreamer(user)
            if not is_streamer:
            
                if "streamer-only" in data:
                    if data["streamer-only"] == True:
                        return
                
                if "sub-only" in data:
                    if data["sub-only"] == True:
                        subbed = await isSubbed(user)
                        if not subbed:
                            return

                if "mod-only" in data:
                    if data["mod-only"] == True:
                    
                        mod = await isModerator(streamer.id, user)
                        if not mod:
                            return

                if "vip-only" in data:
                    if data["vip-only"] == True:
                        if not "vip" in cmd.user.badges:
                            return
                    
        
            if (time.time() - commands[command]["user-cooldown"][user] >= data["command"][command]["cooldown"]) or is_streamer:
                
                variables = {}
                variables["user"] = user
                variables["cmdtext"] = " ".join(arguments)
                
                for i in range(1, 9999):
                    variables["arg" + str(i)] = ""
                for i in range(0, len(arguments)):
                    if arguments[i].startswith("@"):
                        arguments[i] = arguments[i].replace("@","",1)
                
                    variables["arg" + str(i + 1)] = arguments[i]
                
                actions = data["command"][command]["actions"]
                await runActions(actions, variables)
                
                commands[command]["user-cooldown"][user] = time.time()
    except Exception as e:
        prompt ("error", "Error handling Custom Command. (!" + command + ")")
        await logError()
#####################################################################



## PP Command #######################################################
async def pp_command (cmd: ChatCommand):
    command = cmd.name
    user = cmd.user.name

    if len(cmd.parameter) == 0:
        
        global commands
        if user not in commands[command]["user-cooldown"]:
            commands[command]["user-cooldown"][user] = 0
        
        if time.time() - commands[command]["user-cooldown"][user] >= 10:
            
            length = random.randint(0, 12)
            girth = "=" * length
            dingdong = "8" + girth + "D | " + user + " is rocking a " + str(length) + " inch pp!"
            
            global chat
            await chat.send_message(TARGET_CHANNEL, dingdong)
            
            # 8======D | MowhawkJules is rocking a  inch pp!
            
            commands[command]["user-cooldown"][user] = time.time()
#####################################################################




## FollowAge Command ################################################
async def followage_command (cmd: ChatCommand):

    global chat
    global twitch
    global streamer
    
    try:
    
        # print (len(cmd.parameter))
        try:
            name = cmd.user.name
            # print ("length: " + str(len(cmd.parameter)))
            if len(str(cmd.parameter)) > 0:
                name = cmd.parameter                
                
            found = False
            channel_follower_result = await twitch.get_channel_followers(broadcaster_id=streamer.id)
            async for follower in channel_follower_result:
                if follower.user_name.lower() == name.lower():
                    found = True
                    
                    follow_date = follower.followed_at.replace(tzinfo=pytz.UTC)
                    now = datetime.now().replace(tzinfo=pytz.UTC)
                    
                    followed = now - follow_date
                    seconds = followed.days * 24 * 3600 + followed.seconds
                    minutes, seconds = divmod(seconds, 60)
                    hours, minutes = divmod(minutes, 60)
                    days, hours = divmod(hours, 24)
                    
                    
                    await chat.send_message(TARGET_CHANNEL, name + " has been following for " + str(days) + " Days, " + str(hours) + " Hours, " + str(minutes) + " Minutes, " + str(seconds) + " Seconds.")

            if not found:
                await chat.send_message(TARGET_CHANNEL, "Unable to find " + name)
            
        except:
            await chat.send_message(TARGET_CHANNEL, "Unable to fetch followage.")
            await logError()

    except Exception as e:
        prompt ("error", "Error handling FollowAge Command.")
        await logError()

    
        
#####################################################################


## Quote ############################################################
async def addquote (cmd: ChatCommand):
    pass
    
async def quote (cmd: ChatCommand):
    
    f = open(os.getcwd() + "\\resources\\quotes.yml", 'a+', encoding = "utf-8")
    quotes = f.readlines()
    total = len(quotes)
    
    if total > 0:
        if len(cmd.parameter) == 0:
            # Random
            
            value = random.randint(0, total - 1)
            quote = quotes[value]
            await chat.send_message(TARGET_CHANNEL, "Quote #" + str(value + 1) + ": " + quote)
        else:
            value = 1
            try:
                value = int (cmd.parameter)
            except:
                pass
                
            if value <= 0:
                value = 1
            elif value > total:
                value = total
                
            quote = quotes[value - 1]
            await chat.send_message(TARGET_CHANNEL, "Quote #" + str(value) + ": " + quote)
                
           
    else:
        await chat.send_message(TARGET_CHANNEL, "No quotes added... yet!")
        
async def quotes (cmd: ChatCommand):
    f = open(os.getcwd() + "\\resources\\quotes.yml", 'r', encoding = "utf-8")
    total = len(f.readlines())
    await chat.send_message(TARGET_CHANNEL, str(total) + " Available Quotes.")
        
#####################################################################




## SFX Commands #####################################################
async def sfxtoggle_command (cmd: ChatCommand):

    with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
        data = yaml.safe_load(file)
        
        if cmd.name == "sfxon":
            data["enabled"] = True
        elif cmd.name == "sfxoff":
            data["enabled"] = False
        
        with open(os.getcwd() + "\\configuration\\sfx.yml", 'w', encoding = "utf-8") as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)

async def sfx_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        # await cmd.reply('you did not tell me what to reply with')
        
        command = cmd.name
        
        try:
            global twitch
            global streamer
                    
            command = cmd.name
            user = cmd.user.name

            global sfx
            
            if command in sfx["sounds"]:
                
                t = time.time()
                sound = command
                sound_data = sfx["sounds"][sound]
                

                
                with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
                    s_data = yaml.safe_load(file)
                    if "enabled" in s_data:
                        if not s_data["enabled"]:
                            return
                
                is_streamer = await isStreamer(user)
                if not is_streamer:
                
                    if "streamer-only" in data:
                        if data["streamer-only"] == True:
                            return
                
                    if "sub-only" in sound_data:
                        if sound_data["sub-only"] == True:
                            subbed = await isSubbed(user)
                            if not subbed:
                                return

                    if "mod-only" in sound_data: 
                        if sound_data["mod-only"] == True:
                            mod = await isModerator(streamer.id, user)
                            if not mod:
                                return

                    if "vip-only" in sound_data:
                        if sound_data["vip-only"] == True:
                            if not "vip" in cmd.user.badges:
                                return

                if user not in sfx["global-usage"]:
                    sfx["global-usage"][user] = 0

                if t - sfx["global-usage"][user] >= sfx["global-cooldown"]:
                    if t - sound_data["last-use-time"] >= sound_data["global-cooldown"]:
                        
                        if user not in sound_data["last-use-user"]:
                            sound_data["last-use-user"][user] = 0
                    
                        if t - sound_data["last-use-user"][user] >= sound_data["user-cooldown"]:
                            
                            ## PLAY SOUND
                            ## make sure to update all the right "last-use" variables
                            
                            
                            sfxname = sound_data["sound"]
                            
                            threading.Thread(target=playsound, args=(os.getcwd() + "\\resources\\sounds\\" + sound_data["sound"],), daemon=True).start()

                            
                            sound_data["last-use-user"][user] = t
                            sound_data["last-use-time"] = t
                            sfx["global-usage"][user] = t
                            
                            
        except Exception as e:
            prompt ("error", "Error handling SFX Command. (!" + command + ")")
            await logError()
#####################################################################
        
        
        
## Redeems ##########################################################
async def callback_points(d, data):
    try:
    
        # print (data)
        
        global alert_queue
        
        variables = {}
        variables["userid"] = data["data"]["redemption"]["user"]["id"]
        variables["user"] = data["data"]["redemption"]["user"]["display_name"]
        
        
        with open(os.getcwd() + "\\variables\\latest-redeem-user.txt", 'w', encoding = "utf-8") as file:
            file.write(data["data"]["redemption"]["user"]["display_name"]) 
        with open(os.getcwd() + "\\variables\\latest-redeem-name.txt", 'w', encoding = "utf-8") as file:
            file.write(data["data"]["redemption"]["reward"]["title"]) 
        
        variables["userinput"] = ""
        if "user_input" in data["data"]["redemption"]:
            variables["userinput"] = data["data"]["redemption"]["user_input"]

        with open(os.getcwd() + "\\configuration\\redeems.yml", 'r', encoding = "utf-8") as file:
            redeem_data = yaml.safe_load(file)
        
            title = data["data"]["redemption"]["reward"]["title"].lower()
            for redeem in redeem_data["redeem"].keys():
                if redeem.lower() in title:
                
                    actions = redeem_data["redeem"][redeem]["actions"]
                
                    if redeem_data["redeem"][redeem]["queue"]: 
                        variables["type"] = "redeem"
                        variables["buffer"] = redeem_data["redeem"][redeem]["buffer"]
                        variables["actions"] = actions
                        alert_queue.append(variables)
                    else:
                        await runActions(actions, variables)


        valon = False
        # HydrationStation
        if valon:
            title = data["data"]["redemption"]["reward"]["title"].lower()
            if title == "hydrate":
                subprocess.run(["powershell.exe","-executionpolicy", "bypass","-file","C:\\Users\\joene\\Desktop\\usb\\scripts\\lightON.ps1"])
                await asyncio.sleep(3)
                subprocess.run(["powershell.exe","-executionpolicy", "bypass","-file","C:\\Users\\joene\\Desktop\\usb\\scripts\\lightOFF.ps1"])

    except Exception as e:
        prompt ("error", "Error handling RedeemEvent.")
        await logError()
#####################################################################
        
        
        
## Actions ##########################################################
async def runActions (actions, variables):
    
    cl = None
    
    obs_actions = ["obs:scene","obs:show","obs:hide","obs:toggle","obs:label","obs:image","obs:mediafile","obs:slideshow"]
    try:
        for obs_action in obs_actions:
            for action in actions:
                if obs_action in action:
                
                    with open(os.getcwd() + "\\configuration\\credentials.yml", 'r', encoding = "utf-8") as file:
                        data = yaml.safe_load(file)
                    
                        cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
                        # print (cl)
                        break
    except Exception:
        pass

    
    for action in actions:
        arguments = action.split(" ; ")
        
        obs_actions = ["obs:scene","obs:show","obs:hide","obs:toggle","obs:label","obs:image","obs:mediafile","obs:slideshow"]
        if arguments[0] in obs_actions:
            if cl == None:
                prompt ("error", "Skipped Action - No OBS session found.")
                continue
        
    
        if "playsound" in arguments[0]:
            try:
                
                contains = False
                audio_types = ["mp3","wav"]
                for audio_type in audio_types:
                    if os.path.exists(os.getcwd() + "\\resources\\sounds\\" + arguments[1].replace("." + audio_type, "") + "." + audio_type):
                        playsound(os.getcwd() + "\\resources\\sounds\\" + arguments[1].replace("." + audio_type, "") + "." + audio_type, block = False)
                        contains = True
            
                if not contains:
                    prompt ("misc", "Unable to find audio file: " + str(arguments[1]))
                    
            
            except:
                prompt ("error", "Error occured performing 'playsound' action.", info = ["Attempting to play sound: " + str(arguments[1])])
                await logError(info = ["Attempting to play sound: " + str(arguments[1])])
                
        if "obs:slideshow" in arguments[0]:
            try:
                if "play" == arguments[2].lower():
                    cl.trigger_media_input_action(arguments[1], "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY")
                if "pause" == arguments[2].lower():
                    cl.trigger_media_input_action(arguments[1], "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE")
            except:
                prompt ("error", "Error occured performing 'obs:slideshow' action.")
                await logError(info = ["Attempting to use obs:slideshow", "Using: " + str(arguments[2]).lower()])
                
        
        if "obs:scene" in arguments[0]:
            try:
                
                scenes = cl.get_scene_list().__dict__
                all_scenes = []
                for scene in scenes["scenes"]:
                    all_scenes.append(scene["sceneName"])
                if arguments[1] in all_scenes: 
                    cl.set_current_program_scene(arguments[1])
                else:
                    prompt ("error", "Scene not found: " + arguments[1])
                    
                    
            except:
                prompt ("error", "Error occured performing 'obs:scene' action.")
                await logError(info = ["Attempting to set scene to " + str(arguments[1])])
            
        if "obs:show" in arguments[0]:
            try:

                found = False
                scenes = cl.get_scene_list()
                formatted_scenes = scenes.__dict__["scenes"]
                for scene in formatted_scenes:
                    # print (scene["sceneName"])
                    try:
                        item_list = cl.get_scene_item_list(scene["sceneName"])
                        for item in item_list.__dict__["scene_items"]:
                            
                            if item["sourceName"] == arguments[1]:
                                source_id = cl.get_scene_item_id(scene["sceneName"], arguments[1], offset=None).__dict__["scene_item_id"]
                                cl.set_scene_item_enabled(scene["sceneName"], source_id, True)
                                found = True
                    except Exception as e:
                        continue
                        
                if not found:
                    groups = cl.get_group_list().__dict__
                    for group in groups["groups"]:
                        group_items = cl.get_group_scene_item_list(group).__dict__
                        for item in group_items["scene_items"]:
                            if item["sourceName"] == arguments[1]:
                                source_id = cl.get_scene_item_id(group, arguments[1]).__dict__["scene_item_id"]
                                cl.set_scene_item_enabled(group, source_id, True)
                                found = True
                
                if not found:
                    prompt ("error", "Source not found: " + arguments[1])
                
            except Exception as e:
                prompt ("error", "Error occured performing 'obs:show' action.")
                await logError()
        
            
        if "obs:hide" in arguments[0]:
            try:
                
                
                found = False
                scenes = cl.get_scene_list()
                formatted_scenes = scenes.__dict__["scenes"]

                for scene in formatted_scenes:
                    try:
                    
                        item_list = cl.get_scene_item_list(scene["sceneName"])
                        # print (item_list.__dict__)
                        
                        for item in item_list.__dict__["scene_items"]:
                        
                            # print (item)
                        
                            if item["sourceName"] == arguments[1]:
                    
                                # print ("Looking for " + arguments[1] + " in " + scene["sceneName"])
                                source_id = cl.get_scene_item_id(scene["sceneName"], arguments[1], offset=None).__dict__["scene_item_id"]
                                cl.set_scene_item_enabled(scene["sceneName"], source_id, False)
                                found = True
                    except Exception as e:
                        continue
                        

                if not found:
                    groups = cl.get_group_list().__dict__
                    for group in groups["groups"]:
                        group_items = cl.get_group_scene_item_list(group).__dict__
                        for item in group_items["scene_items"]:
                            if item["sourceName"] == arguments[1]:
                                source_id = cl.get_scene_item_id(group, arguments[1]).__dict__["scene_item_id"]
                                cl.set_scene_item_enabled(group, source_id, False)
                                found = True
                
                if not found:
                    prompt ("error", "Source not found: " + arguments[1])
                        
            except Exception as e:
                prompt ("error", "Error occured performing 'obs:hide' action.")
                await logError()
               
        if "obs:toggle" in arguments[0]:
            try:
            
                found = False
                scenes = cl.get_scene_list()
                formatted_scenes = scenes.__dict__["scenes"]
                
                # print (formatted_scenes)
                
                for scene in formatted_scenes:
                    try:
                    
                        item_list = cl.get_scene_item_list(scene["sceneName"])
                        # print (item_list.__dict__)
                        
                        for item in item_list.__dict__["scene_items"]:
                        
                            # print (item)
                        
                            if item["sourceName"] == arguments[1]:
                                source_id = cl.get_scene_item_id(scene["sceneName"], arguments[1], offset=None).__dict__["scene_item_id"]
                                enabled = bool(cl.get_scene_item_enabled(scene["sceneName"], source_id).__dict__["scene_item_enabled"])
                                cl.set_scene_item_enabled(scene["sceneName"], source_id, not enabled)
                                found = True
                    except:
                        pass
                        

                if not found:
                    groups = cl.get_group_list().__dict__
                    for group in groups["groups"]:
                        group_items = cl.get_group_scene_item_list(group).__dict__
                        for item in group_items["scene_items"]:
                            if item["sourceName"] == arguments[1]:
                                source_id = cl.get_scene_item_id(group, arguments[1]).__dict__["scene_item_id"]
                                enabled = bool(cl.get_scene_item_enabled(group, source_id).__dict__["scene_item_enabled"])
                                cl.set_scene_item_enabled(group, source_id, not enabled)
                                found = True
                
                if not found:
                    prompt ("error", "Source not found: " + arguments[1])
                   
            except Exception as e:    
                prompt ("error", "Error occured performing 'obs:toggle' action.")
                await logError()
                
        if "obs:label" in arguments[0]:
            try:
                dictionary = {}
                
                # print (arguments[1])
                
                label = cl.get_input_settings(arguments[1])
                label_data = label.__dict__
                for key, value in label_data["input_settings"].items():
                    dictionary[key] = value
                    
                if "text" in arguments[2]:
                    text = arguments[3]
                    
                    for variable in variables:
                        text = text.replace("%" + variable + "%", str(variables[variable]))
                    
                    if "counter" in text:
                    
                        try:
                            for file in os.listdir(os.getcwd() + "\\variables\\"):
                                filename = os.fsdecode(file)
                                if "counter_" in filename and filename.endswith(".txt"): 
                                    c = filename.replace("counter_","").replace(".txt","")
                                    with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                        text = text.replace("%counter:" + c + "%", f.read())
                        except Exception as e:
                            pass

                    for word in text.split(" "):
                        if "resource:" in word:
                            resource = word.replace("%","")
                            resource = resource.replace("resource:","")
                            try:
                                with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                    text = text.replace(word, f.read())
                            except Exception as e:
                                pass

                    dictionary["text"] = text
                    cl.set_input_settings(arguments[1], dictionary, True)
            
                elif "file" in arguments[2]:
                    dictionary["file"] = arguments[3]
                    dictionary["read_from_file"] = "True"
                    cl.set_input_settings(arguments[1], dictionary, True)
            except:
                prompt ("error", "Error occured performing 'obs:label' action.")
                await logError()

        if "wait" in arguments[0]:
            try:
                await asyncio.sleep(float(arguments[1]))
            except:
                prompt ("error", "Error occured performing 'wait' action.")
                await logError()
        if "chat" in arguments[0]:
            try:
            
            
                global chat
                text = arguments[1]
                for variable in variables:
                    text = text.replace("%" + variable + "%", str(variables[variable]))
            
                for word in text.split(" "):
                    if "%user:" in word and ":game%" in word:
                        
                        try:
                            
                            name = word.split("%user:")[1].split(":game%")[0]
                            
                            found = 0
                            async for users in twitch.get_users(logins = [name]):
                                infos = await twitch.get_channel_information(users.id)
                                info = infos[0]
                                game = info.game_name
                                if game == "":
                                    game = "nothing"
                                text = text.replace("%user:" + name + ":game%", game)
                                found += 1
                                
                            if found == 0:
                                
                                text = text.replace("%user:" + name + ":game%", "nothing")
                                prompt("misc", "No user found with name: " + name)
                                
                        except:
                            text = text.replace(word, "nothing")
                            prompt ("error", "Issue fetching user info.")
                        
                        pass

                ## Random Number
                words = text.split(" ")
                for i in range(0, len(words)):
                    if "%rnumber" in words[i]:
                        min = words[i].split(":")[1].split("-")[0]
                        max = words[i].split(":")[1].split("-")[1].replace("%","")
                        
                        value = random.randint(int(min), int(max))
                        words[i] = words[i].replace(words[i], str(value))
                text = " ".join(words)
                
                ## Random User
                if "%ruser%" in text:
                    channel_follower_result = await twitch.get_channel_followers(broadcaster_id=streamer.id)
                    followers = []
                    async for follower in channel_follower_result:
                        followers.append(follower.user_name)
                          
                    text = text.replace("%ruser%", random.choice(followers))
                    

                
                if "counter" in text:
                    try:
                        for file in os.listdir(os.getcwd() + "\\variables\\"):
                            filename = os.fsdecode(file)
                            if "counter_" in filename and filename.endswith(".txt"): 
                                c = filename.replace("counter_","").replace(".txt","")
                                with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                    text = text.replace("%counter:" + c + "%", f.read())
                    except Exception as e:
                            pass
                
                for word in text.split(" "):
                    if "resource:" in word:
                        resource = word.replace("%","")
                        resource = resource.replace("resource:","")
                        try:
                            with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                text = text.replace(word, f.read())
                        except Exception as e:
                            pass
                
                # loop through file names in resources folder
                # replace %resource:name% with the text of that file
                directory = os.listdir(os.getcwd() + "\\variables")
                names = [x.split('.')[0] for x in directory]
                
                for name in names:
                    if os.path.exists(os.getcwd() + "\\variables\\" + name + ".txt"):
                        resource = open(os.getcwd() + "\\variables\\" + name + ".txt","r", encoding = "utf-8")
                        text = text.replace("%variable:" + name + "%", resource.read())
                    
                await chat.send_message(TARGET_CHANNEL, text)
            except:
                prompt ("error", "Error occured performing 'chat' action.")
                await logError()
        if "editfile" in arguments[0]:
            try:
                text = arguments[2]
                for variable in variables:
                    text = text.replace("%" + variable + "%", variables[variable])
                    
                if "counter" in text:
                    try:
                        for file in os.listdir(os.getcwd() + "\\variables\\"):
                            filename = os.fsdecode(file)
                            if "counter_" in filename and filename.endswith(".txt"): 
                                c = filename.replace("counter_","").replace(".txt","")
                                with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                    text = text.replace("%counter:" + c + "%", f.read())
                    except Exception as e:
                        pass
                        
                for word in text.split(" "):
                    if "resource:" in word:
                        resource = word.replace("%","")
                        resource = resource.replace("resource:","")
                        try:
                            with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                text = text.replace(word, f.read())
                        except Exception as e:
                            pass
                
                with open(arguments[1], 'w', encoding = "utf-8") as file:
                    file.write(text)
                
                ## open file using filepath given
                ## write to have argument info
            except:
                prompt ("error", "Error occured performing 'editfile' action.")
                await logError()
        if "variable" in arguments[0]:
            try:
                text = arguments[2]
                for variable in variables:
                    text = text.replace("%" + variable + "%", variables[variable])
                    
                if "counter" in text:
                    try:
                        for file in os.listdir(os.getcwd() + "\\variables\\"):
                            filename = os.fsdecode(file)
                            if "counter_" in filename and filename.endswith(".txt"): 
                                c = filename.replace("counter_","").replace(".txt","")
                                with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                    text = text.replace("%counter:" + c + "%", f.read())
                    except Exception as e:
                        pass
                
                for word in text.split(" "):
                    if "resource:" in word:
                        resource = word.replace("%","")
                        resource = resource.replace("resource:","")
                        try:
                            with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                text = text.replace(word, f.read())
                        except Exception as e:
                            pass
                
                with open(os.getcwd() + "\\variables\\" + arguments[1] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(text)
            except:
                prompt ("error", "Error occured performing 'variable' action.")
                await logError()
        if "counter:increase" in arguments[0]:
            try:
            
                counter = 0
                try:
                    with open(os.getcwd() + "\\variables\\counter_" + arguments[1] + ".txt", 'r', encoding = "utf-8") as file:
                        counter = int(file.read())
                except Exception as e:
                    pass
            
                increment = 0
                try:
                    
                    value = arguments[2]
                    for variable in variables:
                        try:
                            value = value.replace("%" + variable + "%", int(variables[variable]))
                        except:
                            continue
                    increment = int(value)

                    

                except Exception as e:
                    print (e)
                                    
                with open(os.getcwd() + "\\variables\\counter_" + arguments[1] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(counter + increment))
            except:
                prompt ("error", "Error occured performing 'counter:increase' action.")
                await logError()
                
        if "counter:decrease" in arguments[0]:
            try:
                counter = 0
                try:
                    with open(os.getcwd() + "\\variables\\counter_" + arguments[1] + ".txt", 'r', encoding = "utf-8") as file:
                        counter = int(file.read())
                except Exception as e:
                    pass
            
                decrement = 0
             
                value = arguments[2]
                for variable in variables:
                    try:
                        value = value.replace("%" + variable + "%", int(variables[variable]))
                    except:
                        continue
                decrement = int(value)
  
                                    
                total = (counter - decrement)
                if total < 0:
                    total = 0
                
                with open(os.getcwd() + "\\variables\\counter_" + arguments[1] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(total))
            except:
                prompt ("error", "Error occured performing 'counter:decrease' action.")
                await logError()
        if "counter:set" in arguments[0]:
            try:
                
                newvalue = arguments[2]
                for variable in variables:
                    try:
                        newvalue = newvalue.replace("%" + variable + "%", int(variables[variable]))
                    except:
                        continue
                
                
                value = int(newvalue)
                
                with open(os.getcwd() + "\\variables\\counter_" + arguments[1] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(value))
            except:
                prompt ("error", "Error occured performing 'counter:set' action.")
                await logError()
        if "obs:image" in arguments[0]:
            try:
                dictionary = {}
                label = cl.get_input_settings(arguments[1])
                label_data = label.__dict__
                for key, value in label_data["input_settings"].items():
                    dictionary[key] = value
                dictionary["file"] = arguments[2]
                cl.set_input_settings(arguments[1], dictionary, True)
            except:
                prompt ("error", "Error occured performing 'obs:image' action.")
                await logError()
        if "obs:mediafile" in arguments[0]:
            try:
                dictionary = {}
                label = cl.get_input_settings(arguments[1])
                label_data = label.__dict__
                for key, value in label_data["input_settings"].items():
                    dictionary[key] = value
                dictionary["local_file"] = arguments[2]
                cl.set_input_settings(arguments[1], dictionary, True)
            except:
                prompt ("error", "Error occured performing 'obs:mediafile' action.")
                await logError()
        if "tts" in arguments[0]:
            
            try:
                
                
                voice = arguments[1]
                text = arguments[2]
                halt = arguments[3]
                cutoff = int(arguments[4])
                
                
                for variable in variables:
                    text = text.replace("%" + variable + "%", str(variables[variable]))
                    
                if "counter" in text:
                    try:
                        for file in os.listdir(os.getcwd() + "\\variables\\"):
                            filename = os.fsdecode(file)
                            if "counter_" in filename and filename.endswith(".txt"): 
                                c = filename.replace("counter_","").replace(".txt","")
                                with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                    text = text.replace("%counter:" + c + "%", f.read())
                    except Exception as e:
                        pass

                for word in text.split(" "):
                    if "resource:" in word:
                        resource = word.replace("%","")
                        resource = resource.replace("resource:","")
                        try:
                            with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                text = text.replace(word, f.read())
                        except Exception as e:
                            pass
                        
                for word in text.split(" "):
                    if word.isnumeric():
                        replacer = "\b" + word + "\b"
                        text = re.sub(replacer, num2words(int(word)), text)
                
                voicetypes = { "acapela"        : acapela,
                               "cepstral"       : cepstral,
                               "ibm_watson"     : ibm_watson,
                               "oddcast"        : oddcast,
                               "streamelements" : stream_elements,
                               "streamlabs"     : streamlabs,
                               "voice_forge"    : voice_forge }
                
                if len(text) <= cutoff:
                
                    data = None
                    is_wav = False
                    
                    found_voicepack = ""
                    found_voice = ""
                    for voicepack in tts_voice:
                        for v in tts_voice[voicepack]:
                            if voice.lower() == v.lower():
                                found_voicepack = voicepack
                                found_voice = v
                    
                    if found_voice != "":  
                        voice = found_voice

                        if voicepack == "acapela":
                            __session__ = requests.session()
                            __url1__ = 'https://www.acapela-group.com/www/static/website/demoOptionsDef_voicedemo.php'
                            __url2__ = 'https://h-ir-ssd-1.acapela-group.com/webservices/1-60-00/UrlMaker.json'
                            __headers__ = {
                                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                                'Referer': 'https://www.acapela-group.com/demos/',
                                'Origin': 'https://www.acapela-group.com/demos/',                             
                            }
                            res = __session__.get(__url1__, headers=__headers__)
                            json_res = res.text.replace('var vaasOptions = ', '').replace('};', '}')
                            json_res = json.loads(json_res)
                            params = {
                                'cl_login': json_res['login'],
                                'cl_app': json_res['app'],
                                'session_start': json_res['session']['start'],
                                'session_time': json_res['session']['time'],
                                'session_key': json_res['session']['key'],
                                'req_voice': voice,
                                'req_text': text
                            }
                            res = __session__.post(__url2__, params=params, headers=__headers__)
                            res = __session__.get(res.json()['snd_url'])
                            data = res.content
                        
                        if voicepack == "cepstral":
                            __session__ = requests.session()
                            __url1__ = 'https://www.cepstral.com/en/demos'
                            __url2__ = 'https://www.cepstral.com/demos/createAudio.php?'
                            
                            params = {
                                'voiceText': text,
                                'voice': voice,
                                'createTime': int(time.time() * 1000),
                                'rate': 170,
                                'pitch': 1,
                                'sfx': 'none'
                            }
                            __session__.get(__url1__)
                            res = __session__.get(__url2__, params=params)
                            mp3_location = 'https://www.cepstral.com' + res.json()['mp3_loc']
                            res = __session__.get(mp3_location)
                            data = res.content
                        
                        if voicepack == "ibmwatson":
                            __session__ = requests.session()
                            __url1__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/session'   
                            __url2__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/store'   
                            __url3__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/newSynthesizer'

                            __headers__ = {
                                'Origin': 'https://www.ibm.com',
                                'Referer': 'https://www.ibm.com/demos/live/tts-demo/self-service/home',
                                'Accept': 'application/json, text/plain, */*',
                            }
                            
                            __session__.post(__url1__, headers=__headers__)
                            id = str(uuid.uuid4())    
                            jsonPayload = {"ssmlText": f"<prosody pitch=\"0%\" rate=\"-0%\">{text}</prosody>", "sessionID": id}   
                            __session__.post(__url2__, data=jsonPayload, headers=__headers__)
                            res = __session__.get(__url3__, params={'voice' : voice,'id': id})
                            data = res.content
                            
                        if voicepack == "oddcast":
                            __url1__ = 'https://cache-a.oddcast.com/tts/genB.php'
                            voiceParts = voice.split('-')
                            voiceId, engineId, languageId = voiceParts
                            params = {
                                'EID': int(engineId),
                                'LID': int(languageId),
                                'VID': int(voiceId),
                                'TXT': text,
                                'EXT': 'mp3',
                                'FNAME': '',
                                'ACC': 15679,
                                'SceneID': 2703396,
                                'HTTP_ERR': '',
                                'cache_flag': 3
                            }
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                                'Sec-Gpc': '1',
                                'Sec-Fetch-Site': 'same-site',
                                'Sec-Fetch-Mode': 'cors',
                                'Sec-Fetch-Dest': 'empty',
                                'Sec-Ch-Ua-Platform': '"Windows"',
                                'Sec-Ch-Ua-Mobile': '?0',
                                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
                                'Referer': 'https://www.oddcast.com/',
                                'Priority': 'u=1, i',
                                'Origin': 'https://www.oddcast.com'
                            }
                            res = requests.get(__url1__, params=params, headers=headers)
                            data = res.content
                        
                        if voicepack == "streamelements":
                            __url1__ = 'https://api.streamelements.com/kappa/v2/speech?'
                            params = {
                                'voice': voice,
                                'text': text
                            }
                            res = requests.get(__url1__, params)
                            data = res.content
                        
                        if voicepack == "streamlabs":
                            __url1__ = 'https://streamlabs.com/polly/speak'
                            __headers__ = {
                                'Referer': 'https://streamlabs.com'
                            }
                            params = {
                                'voice': voice,
                                'text': text
                            }
                            res = requests.post(__url1__, params=params, headers=__headers__)
                            mp3_url = res.json()['speak_url']
                            res = requests.get(mp3_url)
                            data = res.content            
                            
                        if voicepack == "voiceforge":
                            __url1__ = 'https://api.voiceforge.com/swift_engine?'
                            __headers__ = {
                                'HTTP_X_API_KEY': '8b3f76a8539',
                            }
                            params = {
                                'voice': voice,
                                'msg': text,
                                'email': 'null',
                            }
                            res = requests.get(__url1__, params=params, headers=__headers__)
                            
                            data = res.content
                            is_wav = True
                        
                        
                        filename = "tts.wav"
                        if is_wav:
                            filename = "tts.wav"
                        
                        
                        if data:
                        
                            try:
                                os.remove(os.getcwd() + "\\" + filename)
                            except:
                                pass
                            
                            with open(os.getcwd() + "\\" + filename, "+wb") as ttsfile:
                                ttsfile.write(data)
                                
                            while not os.path.exists(os.getcwd() + "\\" + filename):
                                time.sleep(2)

                           
                               
                            if halt.lower() == "true":
                                playsound(os.getcwd() + "\\" + filename, block = True)
                            else:
                                playsound(os.getcwd() + "\\" + filename, block = False) 

                    else:
                        prompt("misc", "Unable to find voice '" + voice + "'.")

                else:
                    await chat.send_message(TARGET_CHANNEL, "Unable to play TTS, message length exceeds limit of " + str(cutoff) + " characters. (" + str(len(text)) + ")")
                    prompt("misc", "Unable to play TTS, message length exceeds limit of " + str(cutoff) + " characters. (" + str(len(text)) + ")")


                
                        # await asyncio.sleep(seconds)
                
            except:
                prompt ("error", "Error occured performing 'tts' action.")
                await logError()
        
        if "cmd" in arguments[0]:
            try:
                text = arguments[1]
                for variable in variables:
                    text = text.replace("%" + variable + "%", variables[variable])
                subprocess.run(text)
            except:
                prompt ("error", "Error occured performing 'cmd' action.")
                await logError()
                
        if "announce" in arguments [0]:
            try:
            
                text = arguments[1]
                for variable in variables:
                    text = text.replace("%" + variable + "%", str(variables[variable]))
                
                if "counter" in text:
                    try:
                        for file in os.listdir(os.getcwd() + "\\variables\\"):
                            filename = os.fsdecode(file)
                            if "counter_" in filename and filename.endswith(".txt"): 
                                c = filename.replace("counter_","").replace(".txt","")
                                with open(os.getcwd() + "\\variables\\" + filename, 'r', encoding = "utf-8") as f:
                                    text = text.replace("%counter:" + c + "%", f.read())
                    except Exception as e:
                        pass
                        
                for word in text.split(" "):
                    if "%user:" in word and ":game%" in word:
                        
                        try:
                            
                            name = word.split("%user:")[1].split(":game%")[0]
                            
                            found = 0
                            async for users in twitch.get_users(logins = [name]):
                                infos = await twitch.get_channel_information(users.id)
                                info = infos[0]
                                game = info.game_name
                                if game == "":
                                    game = "nothing"
                                text = text.replace("%user:" + name + ":game%", game)
                                found += 1
                                
                            if found == 0:
                                
                                text = text.replace("%user:" + name + ":game%", "nothing")
                                prompt("misc", "No user found with name: " + name)
                                
                        except:
                            text = text.replace(word, "nothing")
                            prompt ("error", "Issue fetching user info.")
                        
                        pass
                      
                for word in text.split(" "):
                    if "resource:" in word:
                        resource = word.replace("%","")
                        resource = resource.replace("resource:","")
                        try:
                            with open(os.getcwd() + "\\resources\\" + resource + ".txt", 'r', encoding = "utf-8") as f:
                                text = text.replace(word, f.read())
                        except Exception as e:
                            pass
                
                color = arguments[2]
                colors = ["blue","green","orange","purple","primary"]
                
                if color.lower() in colors:
                    color = color.lower()
                else:
                    color = "primary"
                

                
                await twitch.send_chat_announcement(streamer.id, streamer.id, text, color)
                
            except:
                prompt ("error", "Error occured performing 'announce' action.")
                await logError()
        
        if "vip:add" in arguments[0]:
            try:
                
                user = str(arguments[1])
                for variable in variables:
                    user = user.replace("%" + variable + "%", str(variables[variable]))
                
                
                
                await twitch.add_channel_vip(streamer.id, user)
            except:
                prompt ("error", "Error occured performing 'vip:add' action.")
                await logError()
        
        if "vip:remove" in arguments [0]:
            try:
                user = str(arguments[1])
                for variable in variables:
                    user = user.replace("%" + variable + "%", str(variables[variable]))
                
                await twitch.remove_channel_vip(streamer.id, user)
            except:
                prompt ("error", "Error occured performing 'vip:remove' action.")
                await logError()
        
        # print (action)
#####################################################################



## Is Moderator #####################################################   
async def isModerator (streamer_id, user):
    async for mod in twitch.get_moderators(streamer_id):
        if mod.user_name.lower() == user.lower():
            return True
    return False
#####################################################################
    
## Is Moderator #####################################################   
async def isStreamer (user):
    return (user.lower() == TARGET_CHANNEL.lower())
#####################################################################    
    
## Is Moderator #####################################################   
async def isSubbed (user):
    global streamer
    subs = await twitch.get_broadcaster_subscriptions(streamer.id)
    subbed = user.lower() in [sub.user_name.lower() for sub in subs.data]
    return subbed
#####################################################################  
    
async def redeemon(cmd: ChatCommand):
    global streamer
    await twitch.update_custom_reward(streamer.id, "971b436f-eb1e-4045-9d31-854f644f5fd6", is_enabled=True)

async def redeemoff(cmd: ChatCommand):
    global streamer
    await twitch.update_custom_reward(streamer.id, "971b436f-eb1e-4045-9d31-854f644f5fd6", is_enabled=False)
    

async def getGame (cmd: ChatCommand):
    global twitch
    infos = await twitch.get_channel_information(streamer.id)
    info = infos[0]
    game = info.game_name
    await chat.send_message(TARGET_CHANNEL, "Current Game: " + game)
    
    

async def setGame (cmd: ChatCommand):
    global twitch
    global streamer

    is_mod = await isModerator(streamer.id, cmd.user.name)
    is_streamer = await isStreamer(cmd.user.name)
        
    gameid = ""
    gamename = ""
    if is_mod or is_streamer:
        game = cmd.parameter

        async for games in twitch.get_games(names = [game]):
            gameid = str(games.id)
            gamename = str(games.name)
            break
            
    if gameid != "":
        await twitch.modify_channel_information(streamer.id, game_id = gameid)
        await chat.send_message(TARGET_CHANNEL, "Game has been set to: " + gamename)
    else:
        await chat.send_message(TARGET_CHANNEL, "Unable to find: " + cmd.parameter)


async def setTitle (cmd: ChatCommand):
    global twitch
    global streamer

    is_mod = await isModerator(streamer.id, cmd.user.name)
    is_streamer = await isStreamer(cmd.user.name)
        
    gameid = ""
    gamename = ""
    if is_mod or is_streamer:
        if len(cmd.parameter) > 0:
            await twitch.modify_channel_information(streamer.id, title = cmd.parameter)
            await chat.send_message(TARGET_CHANNEL, "Stream Title has been updated.")
    

async def uptime (cmd: ChatCommand):
    global twitch
    global streamer
    
    found = False
    async for streams in twitch.get_streams(user_id = streamer.id):
        
        uptime = streams.started_at.replace(tzinfo=pytz.UTC) + timedelta(hours = 1)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        
        followed = now - uptime
        seconds = followed.days * 24 * 3600 + followed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        
        found = True
        await chat.send_message(TARGET_CHANNEL, "Uptime: " + str(days) + " Days, " + str(hours) + " Hours, " + str(minutes) + " Minutes, " + str(seconds) + " Seconds.")

    if not found:
        await chat.send_message(TARGET_CHANNEL, "Channel is not live.")


## Debug Command ####################################################
async def debug_command (cmd: ChatCommand):
    
    
    global twitch
    global streamer
    is_streamer = await isStreamer(cmd.user.name)
    arguments = cmd.parameter.split(" ")
    

    
    try:
        if is_streamer:
        
            global alert_queue

            if len(arguments) == 1:
            
                
            
            
                if "live" in arguments[0]:
                                    
                    with open(os.getcwd() + "\\configuration\\live-notification.yml", 'r', encoding = "utf-8") as file:
                        config = yaml.safe_load(file)
                        try:
                        
                            global TARGET_CHANNEL
                            webhook = DiscordWebhook(url = config["webhook"], username = "Vayl", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png")
                            if str(config["ping-everyone"]).lower() == "true":
                                webhook = DiscordWebhook(url = config["webhook"], username = "Vayl", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png", content = "||@everyone||")

                            
                            
                            infos = await twitch.get_channel_information(streamer.id)
                            info = infos[0]
                            # print ("Game:  " + info.game_name)

                            directory = {"%game%":info.game_name, "%title%":info.title, "%name%":info.broadcaster_name, "%link%":"https://twitch.tv/" + TARGET_CHANNEL.lower()}

                            description = "\n".join(config["embed"]["description"])
                            title = config["embed"]["title"]
                            image_url = config["embed"]["image-url"]
                            thumbnail_url = config["embed"]["thumbnail-url"]
                            
                            for d,r in directory.items():
                                title = title.replace(d,r)
                                description = description.replace(d, r)
                            
                            # "‎"
                            
                            embed = DiscordEmbed(title = "", description = "", color = "C14844")
                            

                            
                            # embed.set_title(title = title)
                            embed.set_description(description = description)
                            embed.set_image(url = image_url)
                            embed.set_thumbnail(url = thumbnail_url)
                            embed.set_author(name=title, url="", icon_url="https://i.ibb.co/mHgBcY2/icon.png")
                            # embed.set_footer(text="Powered by Vayl", icon_url="https://i.ibb.co/mHgBcY2/icon.png")
                                
                            if config["embed"]["fields"]["include"]:
                                for fields in config["embed"]["fields"]:
                                    if str(fields).isnumeric():
                                        fname = config["embed"]["fields"][fields]["name"]
                                        fvalue = config["embed"]["fields"][fields]["value"]
                                        for d,r in directory.items():
                                            fname = fname.replace(d,r)
                                            fvalue = fvalue.replace(d, r)
                                    
                                        embed.add_embed_field(name= fname , value = fvalue)
                            
                            webhook.add_embed(embed)
                            response = webhook.execute()
                            
                        except Exception as e:
                            prompt ("error", "Error handling DEBUG Live Notification.")
                            await logError()
                        finally:
                            prompt ("success", "Pushing DEBUG Live Notification to Discord.")
             
            if len(arguments) == 2:
                if "hypetrain" in arguments[0]:
                
                    if arguments[1].isnumeric():
                    
                        with open(os.getcwd() + "\\configuration\\event\\hype-train.yml", 'r', encoding = "utf-8") as file:
                            config = yaml.safe_load(file)
                        
                            trainlevel = str(arguments[1])
                        
                            try:
                            
                            
                                if config["levels"]["any"]["enabled"]:

                                    variables = {}
                                    variables["level"] = str(arguments[1])
                                    actions = config["levels"]["any"]["actions"]
                                    await runActions(actions, variables)
                                else:
                                    
                                    # priority ">="
                                    
                                    for level in reversed(config["levels"]):
                                                                       
                                        if str(level).isnumeric():
                                            if level == int(trainlevel):
                                                if config["levels"][level]["enabled"]:
                                                    variables = {}
                                                    variables["level"] = str(arguments[1])
                                                    actions = config["levels"][level]["actions"]
                                                    await runActions(actions, variables)
                                        elif ">=" in str(level):
                                            checklevel = int(str(level).replace(">=",""))
                                            if int(trainlevel) >= checklevel:
                                                if config["levels"][str(level)]["enabled"]:
                                                    variables = {}
                                                    variables["level"] = str(arguments[1])
                                                    actions = config["levels"][str(level)]["actions"]
                                                    await runActions(actions, variables)
                                                    break
                                    

                            except Exception as e:
                                prompt ("error", "Error handling HypeTrainEvent.")
                                await logError()
             
            if len(arguments) >= 3:
                if "bits" in arguments[0]:
                    if arguments[1].isalnum():
                        if arguments[2].isnumeric():
                       
                            alert = {}
                            alert["type"] = "bits"
                            alert["user"] = arguments[1]
                            alert["amount"] = arguments[2]
                            
                            if len(arguments) > 3:
                                message = " ".join(arguments[3:])
                                alert["message"] = message

                            alert_queue.append(alert)
                
            if len(arguments) >= 3:
            

                if "sub" == arguments[0]:
              
                
                    if arguments[1].isalnum():
                        if arguments[2].isnumeric():
                            if arguments[3].isnumeric():
                                alert = {}
                                alert["type"] = "sub"
                                alert["tier"] = arguments[2] 
                                alert["user"] = arguments[1]
                                alert["total-months"] = arguments[3]
                                
                                tier_found = False
                                tiers = ["1","2","3","Prime"]
                                for tier in tiers:
                                    if arguments[2].lower() == tiers.lower():
                                        alert["tier"] = tier
                                        tier_found = True
                                if not tier_found:
                                    alert["tier"] = "null"
                                    
                                
                                
                                if len(arguments) > 4:
                                    message = " ".join(arguments[4:])
                                    alert["sub-message"] = message
                                    
                                print ("suuuuuub")
                                    
                                alert_queue.append(alert)
            
            if len(arguments) == 4:
                if "giftsub" == arguments[0]:
                    if arguments[1].isalnum():
                        if arguments[2].isnumeric():
                            if arguments[3].isnumeric():
                                
                                
                                for i in range(0, int(arguments[3])):
                                    alert = {}
                                    alert["type"] = "giftsub"
                                    alert["gifter"] = arguments[1]
                                    alert["tier"] = arguments[2]
                                    alert["gifted"] = "ExampleUsername"
                                    alert_queue.append(alert)
                                
            
            if len(arguments) == 2:
                if "follow" == arguments[0]:
                    if arguments[1].isalnum():
                        alert = {}
                        alert["type"] = "follow"
                        alert["user"] = arguments[1]
                        alert_queue.append(alert)
           
            if len(arguments) >= 2:
                if "raid" == arguments[0]:
                    if arguments[1].isalnum():
                    
                        alert = {}
                        alert["type"] = "raid"
                        alert["user"] = arguments[1]
                    
                        if len(arguments) > 2:
                            if arguments[2].isnumeric():
                                alert["viewercount"] = str(int(arguments[2]))
                        else:
                            alert["viewercount"] = 1
                                
                        alert_queue.append(alert)
           
    except Exception as e:
        print (e)
    
#####################################################################
    
    
## 8 Ball ###########################################################

async def run8ball (cmd: ChatCommand):
    arguments = cmd.parameter.split(" ")
    if len(arguments) > 0 and cmd.parameter.endswith("?"):
        await chat.send_message(TARGET_CHANNEL, "(づ◡﹏◡)づ ◯")
        
        options = ["It is certain.","It is decidedly so.", "Without a doubt.", "You may rely on it.", "Most likely.", "Outlook is good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Best not to say.", "The spirits do not respond.", "Don't count on it", "The spirits say no.", "My sources say no", "Outlook is bleak", "Very doubtful"]
        for i in range(0, 5):
            random.shuffle(options)
            
        
        
        await chat.send_message(TARGET_CHANNEL, "(づ◡﹏◡)づ ◯ '" + random.choice(options) + "'")

#####################################################################
    
    
## Reload ###########################################################   
async def reload(reloadInChat):

    ## SoundFX Commands ########################################
    global sfx
    sfx["sounds"] = {}
    
    global chat
    
    try:
        with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)
            
            sfx["global-cooldown"] = data["global-cooldown"]
            sfx["global-usage"] = {}
           
            for sound in data["sounds"].keys():
                
                sound = sound.lower()
                chat.register_command(sound, sfx_command)
                
                sound_data = {}
                sound_data["global-cooldown"] = data["sounds"][sound]["cooldown"]["global"]
                sound_data["user-cooldown"] = data["sounds"][sound]["cooldown"]["global"]
                sound_data["sound"] = data["sounds"][sound]["sound"]
                sound_data["last-use-time"] = 0
                sound_data["last-use-user"] = {}
                sound_data["sub-only"] = str(data["sounds"][sound]["sub-only"]).lower()
                sound_data["mod-only"] = str(data["sounds"][sound]["mod-only"]).lower()
                sound_data["vip-only"] = str(data["sounds"][sound]["vip-only"]).lower()

                
                sfx["sounds"][sound] = sound_data
                
            # print (f"[{Fore.GREEN}♦{Fore.WHITE}] SFX Configuration loaded. (" + str(len(data["sounds"].keys())) + ")")
            
            prompt ("success", "SFX Configuration loaded. (" + str(len(data["sounds"].keys())) + ")")
                
    except Exception as e:
        prompt ("error","Error loading SFX configuration.")
        # print ("[!] Error loading SFX Configuration.")
        await logError()
    
        
    ############################################################



    
    

    ## Timed Messages ##########################################

    global timed_messages
    timed_messages = []
    
    try:
        with open(os.getcwd() + "\\configuration\\timed-messages.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)
            for message in data["messages"].keys():
                
                tmessage = {}
                tmessage["maxiterations"] = data["messages"][message]["iterations"]
                tmessage["iterations"] = 0
                tmessage["frequency"] = data["messages"][message]["frequency"]
                tmessage["counter"] = 0
                tmessage["messages"] = data["messages"][message]["messages"]
                timed_messages.append(tmessage)
                
            prompt ("success", "Timed Messages loaded. (" + str(len(data["messages"].keys())) + ")")
    except Exception as e:
        prompt ("error", "Error loading timed messaged.")
        await logError()
    
    ############################################################



    ## Custom Commands #########################################
    global commands
    
    try:
        with open(os.getcwd() + "\\configuration\\commands.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)
            for command in data["command"].keys():
                chat.register_command(command, custom_command)
                commands[command] = {}
                commands[command]["cooldown"] = data["command"][command]["cooldown"]
                commands[command]["user-cooldown"] = {}
            prompt ("success", "Custom Commands loaded. (" + str(len(data["command"].keys())) + ")")
    except Exception as e:
        prompt ("error", "Error loading Custom Commands.")
        await logError()
            
    # Quote
    # chat.register_command("addquote", addquote) # CAN'T SUE SINCE DOESN'T TRIGGER WHEN REPLY
    chat.register_command("quote", quote)   
    chat.register_command("quotes", quotes)   
            
    # SetGame
    chat.register_command("setgame", setGame)
    chat.register_command("settitle", setTitle)
    chat.register_command("game", getGame)
            
    chat.register_command("uptime", uptime)        
            
    # PP
    commands["pp"] = {}
    commands["pp"]["cooldown"] = 0
    commands["pp"]["user-cooldown"] = {}
    chat.register_command("pp", pp_command)
    
    chat.register_command("redeemon", redeemon)
    chat.register_command("redeemoff", redeemoff)
    
    # SFX
    chat.register_command("sfxon", sfxtoggle_command)
    chat.register_command("sfxoff", sfxtoggle_command)
    
    # 8Ball
    chat.register_command ("8ball", run8ball)
    
    # Counter
    # chat.register_command("counter", counter_command)
    
    # Followage
    chat.register_command("followage", followage_command)
    ############################################################
    
    ## Debug Commands ##########################################
    chat.register_command("debug", debug_command)
    ############################################################

    ## Reload Command ##########################################
    chat.register_command("reloadvayl", reload_command)
    ############################################################
    
    if (reloadInChat == True):
        await chat.send_message(TARGET_CHANNEL, "Vayl Reloaded.")
   
    
#####################################################################  
    
    
## Ad Break #########################################################
async def on_ad (data: ChannelAdBreakBeginEvent):
    with open(os.getcwd() + "\\configuration\\event\\adbreak.yml", 'r', encoding = "utf-8") as file:
        data = yaml.safe_load(file)
        if data["enabled"]:
            try:
            
                variables = {}
                actions = data["actions"]
                await runActions(actions, variables)
                    
            except Exception as e:
                prompt ("error", "Error handling AdEvent.")
                await logError()
#####################################################################
  
   
## Shoutout Given ###################################################
async def on_shoutout_give(data: ChannelShoutoutCreateEvent):
    with open(os.getcwd() + "\\configuration\\event\\shoutout-create.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:

                variables = {}
                variables["user"] = data.event.to_broadcaster_user_name
                
                with open(os.getcwd() + "\\variables\\latest-shoutout-given.txt", 'w', encoding = "utf-8") as file:
                    file.write(data.event.to_broadcaster_user_name)  
                
                actions = config["actions"]
                await runActions(actions, variables)

            except Exception as e:
                prompt ("error", "Error handling ShoutoutGivenEvent.")
                await logError()
#####################################################################  

## Shoutout Received#################################################
async def on_shoutout_receive(data: ChannelShoutoutReceiveEvent):
    with open(os.getcwd() + "\\configuration\\event\\shoutout-receive.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:
            
                variables = {}
                variables["user"] = data.event.from_broadcaster_user_name
                variables["viewers"] = str(data.event.viewer_count)
                
                with open(os.getcwd() + "\\variables\\latest-shoutout-received.txt", 'w', encoding = "utf-8") as file:
                    file.write(data.event.from_broadcaster_user_name) 
                
                actions = config["actions"]
                await runActions(actions, variables)

            except Exception as e:
                prompt ("error", "Error handling ShoutoutReceiveEvent.")
                await logError()
#####################################################################    
    
## Poll Created #####################################################
async def on_poll_create (data: ChannelPollBeginEvent):

    #print (data.event.__dict__)
    event = data.event.__dict__

    with open(os.getcwd() + "\\configuration\\event\\poll-create.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:
            
                with open(os.getcwd() + "\\variables\\latest-poll.txt", 'w', encoding = "utf-8") as file:
                    file.write(data.event.title) 
            
                variables = {}
                variables["title"] = data.event.title

                option_id = 1
                for choice in event["choices"]:
                    variables["option" + str(option_id)] = choice.__dict__["title"]
                    option_id += 1

                actions = config["actions"]
                await runActions(actions, variables)
                    
            except Exception as e:
                prompt ("error", "Error handling PollCreationEvent.")
                await logError()
#####################################################################    

## Poll Ended #######################################################
async def on_poll_ended (data: ChannelPollEndEvent):
    
    event = data.event.__dict__
    if event["status"] == "completed":

        with open(os.getcwd() + "\\configuration\\event\\poll-ended.yml", 'r', encoding = "utf-8") as file:
            config = yaml.safe_load(file)
            if config["enabled"]:
                try:
                
                    variables = {}
                    
                    option_id = 1
                    for choice in event["choices"]:
                        variables["option" + str(option_id)] = choice.__dict__["title"]
                        variables["option" + str(option_id) + "bits"] = str(choice.__dict__["bits_votes"])
                        variables["option" + str(option_id) + "points"] = str(choice.__dict__["channel_points_votes"])
                        variables["option" + str(option_id) + "votes"] = str(choice.__dict__["votes"])
                        option_id += 1
                    
                    actions = config["actions"]
                    await runActions(actions, variables)
                        
                except Exception as e:
                    prompt ("error", "Error handling PollEndedEvent.")
                    await logError()
                    
#####################################################################    
    
## Prediction Start #################################################
async def on_prediction_start (data: ChannelPredictionEvent):
    with open(os.getcwd() + "\\configuration\\event\\prediction-created.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:
            
                with open(os.getcwd() + "\\variables\\latest-prediction.txt", 'w', encoding = "utf-8") as file:
                    file.write(data.event.title) 
            
                variables = {}
                variables["title"] = data.event.title
                
                
                
                value = 1
                for option in data.event.outcomes:
                    variables["option" + str(value)] = option.title
                    value += 1
                
                actions = config["actions"]
                await runActions(actions, variables)
                    
            except Exception as e:
                prompt ("error", "Error handling PredictionStartEvent.")
                await logError()
#####################################################################

## Prediction Start #################################################
async def on_prediction_lock (data: ChannelPredictionEvent):
    with open(os.getcwd() + "\\configuration\\event\\prediction-locked.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:
            
                variables = {}
                variables["title"] = data.event.title
                
                value = 1
                for option in data.event.outcomes:
                    variables["option" + str(value)] = option.title
                    variables["option" + str(value) + "points"] = option.channel_points
                    value += 1
                
                
                actions = config["actions"]
                await runActions(actions, variables)
                    
            except Exception as e:
                prompt ("error", "Error handling PredictionLockEvent.")
                await logError()
#####################################################################

## Prediction End ###################################################
async def on_prediction_end (data: ChannelPredictionEndEvent):
    with open(os.getcwd() + "\\configuration\\event\\prediction-ended.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        if config["enabled"]:
            try:
            
                variables = {}
                variables["title"] = data.event.title
                
                win = data.event.winning_outcome_id
                winner = ""
                
                value = 1
                for option in data.event.outcomes:
                    variables["option" + str(value)] = option.title
                    variables["option" + str(value) + "points"] = option.channel_points
                    value += 1
                    
                    if option.id == win:
                        variables["winner"] = option.title
                
                with open(os.getcwd() + "\\variables\\latest-prediction-winner.txt", 'w', encoding = "utf-8") as file:
                    file.write(variables["winner"]) 
                
                actions = config["actions"]
                await runActions(actions, variables)
                    
            except Exception as e:
                prompt ("error", "Error handling PredictionEndEvent.")
                await logError()
#####################################################################    

## Hype Train #######################################################
async def on_hype_train (data: HypeTrainEvent):

    contributors = data.event.top_contributions
    trainlevel = data.event.level
    
    
    

    with open(os.getcwd() + "\\configuration\\event\\hype-train.yml", 'r',  encoding = "utf-8") as file:
        config = yaml.safe_load(file)
    
        try:
            
            variables = {}
            try:
                conductor_bits = data.event.top_contributions[0].user_name
                conductor_subs = data.event.top_contributions[1].user_name
                variables["conductor:bits"] = conductor_bits
                variables["conductor:subs"] = conductor_subs
            except:
                pass
            
            if config["levels"]["any"]["enabled"]:

                
                variables["level"] = str(arguments[1])
                actions = config["levels"]["any"]["actions"]
                await runActions(actions, variables)
                
            else:
                
                # priority ">="
                
                for level in reversed(config["levels"]):
                                                   
                    if str(level).isnumeric():
                        if int(level) == trainlevel:
                            if config["levels"][level]["enabled"]:
                                variables = {}
                                variables["level"] = str(trainlevel)
                                actions = config["levels"][level]["actions"]
                                await runActions(actions, variables)
                    elif ">=" in str(level):
                        checklevel = int(str(level).replace(">=",""))
                        if trainlevel >= checklevel:
                            if config["levels"][str(level)]["enabled"]:
                                variables = {}
                                variables["level"] = str(trainlevel)
                                actions = config["levels"][str(level)]["actions"]
                                await runActions(actions, variables)
                                break
                

        except Exception as e:
            prompt ("error", "Error handling HypeTrainEvent.")
            await logError()
#####################################################################
    
## Live Check #######################################################
async def on_live(data: StreamOnlineEvent):

    # print (str(data.to_dict()))
    # stream_data = data.to_dict()
    
    

    with open(os.getcwd() + "\\configuration\\live-notification.yml", 'r', encoding = "utf-8") as file:
        config = yaml.safe_load(file)
        try:
        
            global TARGET_CHANNEL
            webhook = DiscordWebhook(url = config["webhook"], content = "")
            if str(config["ping-everyone"]).lower() == "true":
                webhook = DiscordWebhook(url = config["webhook"], content = "||@everyone||")

            global twitch
            global streamer
            infos = await twitch.get_channel_information(streamer.id)
            info = infos[0]
            # print ("Game:  " + info.game_name)

            directory = {"%game%":info.game_name, "%title%":info.title, "%name%":info.broadcaster_name, "%link%":"https://twitch.tv/" + TARGET_CHANNEL.lower()}

            description = "\n".join(config["embed"]["description"])
            title = config["embed"]["title"]
            image_url = config["embed"]["image-url"]
            thumbnail_url = config["embed"]["thumbnail-url"]
            
            for d,r in directory.items():
                title = title.replace(d,r)
                description = description.replace(d, r)
            
            # "‎"
            
            embed = DiscordEmbed(title = "", description = "", color = "C14844")
            # embed.set_title(title = title)
            embed.set_description(description = description)
            embed.set_image(url = image_url)
            embed.set_thumbnail(url = thumbnail_url)
            embed.set_author(name=title, url="", icon_url="https://i.ibb.co/mHgBcY2/icon.png")
            # embed.set_footer(text="Powered by Vayl", icon_url="https://i.ibb.co/mHgBcY2/icon.png")
                
            if config["embed"]["fields"]["include"]:
                for fields in config["embed"]["fields"]:
                    if str(fields).isnumeric():
                        fname = config["embed"]["fields"][fields]["name"]
                        fvalue = config["embed"]["fields"][fields]["value"]
                        for d,r in directory.items():
                            fname = fname.replace(d,r)
                            fvalue = fvalue.replace(d, r)
                    
                        embed.add_embed_field(name= fname , value = fvalue)
            
            webhook.add_embed(embed)
            response = webhook.execute()
            
            
        
        except Exception as e:
            prompt ("error", "Error handling Live Notification.")
            await logError()
        finally:
            prompt ("success", "Pushing Live Notification to Discord.")
            
 
#####################################################################    
    
## Follow ###########################################################
async def on_follow(data: ChannelFollowEvent):
    # our event happend, lets do things with the data we got!
    try:
        follower = data.event.user_name
        
        with open(os.getcwd() + "\\variables\\latest-follower.txt", 'w', encoding = "utf-8") as file:
            file.write(follower)  
        
        alert = {}
        alert["type"] = "follow"
        alert["user"] = follower
        alert_queue.append(alert)
        
        prompt ("follow", "Follow: " + alert["user"]) 
        
    except Exception as e:
        prompt ("error", "Error handling FollowEvent.")
        await logError()
#####################################################################
    
    

 
    

## Alert Queue ######################################################



test = {}
test["type"] = "follow"
test["user"] = "TestingUsername1"
# alert_queue.append(test)

test = {}
test["type"] = "sub"
test["sub-message"] = "Testing Message to see how it looks"
test["user"] = "Valon"
test["total-months"] = "5"
# alert_queue.append(test)


timed_messages = []

def manageTimedMessages():
    asyncio.run(manageTimedMessagesAsync())

async def manageTimedMessagesAsync():
    while True:
        global chat
        global timed_messages
        for tmessage in timed_messages:
            if tmessage["maxiterations"] != -1:
                if tmessage["iterations"] >= tmessage["maxiterations"]:
                    continue
            
            tmessage["counter"] += 1
            if tmessage["counter"] >= tmessage["frequency"]:
                for message in tmessage["messages"]:
                    await chat.send_message(TARGET_CHANNEL, message)
                
                tmessage["iterations"] += 1
                tmessage["counter"] = 0
        await asyncio.sleep(1)




def manageAlerts():
    asyncio.run(manageAlertsAsync())
    
async def manageAlertsAsync():

    global alert_queue

    while True:
        
        
        
        buffer = 1
        pop_amount = 1


        if len(alert_queue) > 0:
            
            alert = alert_queue[0]
            actions = []
            
            if "redeem" in alert["type"]:
                actions = alert["actions"]
                buffer = alert["buffer"]
            
            elif "giftsub" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\giftsub.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.full_load(file)
                    
                    if data["single"]["enabled"] or data["multiple"]["enabled"]:
                    
                        
                        duplicate = 0
                        gifter = alert["gifter"]
                        for a in alert_queue[1:]:
                            if a["type"] == "giftsub":
                                if a["gifter"] == gifter:
                                    duplicate += 1

 
                        # print ("Duplicates: " + str(duplicate))
                            
                        total = (duplicate + 1)    
                            
                        if total == 1:
                            if data["single"]["enabled"]:
                                actions = data["single"]["actions"]
                                buffer = data["single"]["buffer"]
                            
                            alert["sub-amount"] = "1"
                        
                        else:

                            selected_option = ""
                            alert["sub-amount"] = str(total)

                            if data["multiple"]["enabled"]:
                                for options in reversed(data["multiple"]):
                                    if str(options) != "enabled":
                                        if str(options).isnumeric():
                                            if total >= options:
                                                buffer = data["multiple"][options]["buffer"]
                                                actions = data["multiple"][options]["actions"]
                                                selected_option = str(options)
                                                pop_amount = total
                                                break
                            
                            if selected_option == "":
                                if data["single"]["enabled"]:
                                    actions = data["single"]["actions"]
                                    buffer = data["single"]["buffer"]
                                    pop_amount = 1
                            
                            
                            ## loop through queue and remove all instances of same gifter

                            new_alert_queue = []
                            for i in range(0, len(alert_queue)):
                                if alert_queue[i]["type"] == "giftsub":
                                    if alert_queue[i]["gifter"] != gifter:
                                        new_alert_queue.append(alert_queue[i])
                                else:
                                    new_alert_queue.append(alert_queue[i])
                            alert_queue = new_alert_queue
                            
                            
                            await runActions(actions, alert)
                            await asyncio.sleep(buffer)
                            
                            continue
                            
                            
                        
            
            elif "bits" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\bits.yml", 'r', encoding = "utf-8") as file:
                    
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        amount = int(alert["amount"])
                      
                        for option in data:
                            if "enabled" != option:
                        
                                requirement = data[option]["requirement"]
                                min = -1
                                max = -1

                                if "<" in requirement:
                                    min = 0
                                    max = int(requirement.split("<")[1]) - 1
                                elif "<=" in requirement:
                                    min = 0
                                    max = int(requirement.split("<=")[1])
                                elif ">=" in requirement:
                                    min = int(requirement.split(">=")[1])
                                    max = 99999999999
                                elif ">" in requirement:
                                    min = int(requirement.split(">")[1]) + 1
                                    max = 99999999999
                                elif "=" in requirement:
                                    min = int(requirement.split("=")[1])
                                    max = int(requirement.split("=")[1])
                                elif "-" in requirement:
                                    min = int(requirement.split("-")[0])
                                    max = int(requirement.split("-")[1])
                            
                                if min != -1 and max != -1:
                                    if amount >= min and amount <= max:
                                        buffer = data[option]["buffer"]
                                        actions = data[option]["actions"]
               
            elif "raid" in alert["type"]:
                
                with open(os.getcwd() + "\\configuration\\event\\raid.yml", 'r', encoding = "utf-8") as file:
                    
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        specific_user = "default"
                        
                        amount = alert["viewercount"]
                        
                        for option in data["variations"]:
                            if "user" in data["variations"][option] and data["variations"][option]["user"] == alert["user"]:
                                # Specifc User
                                specific_user = option
                                break
                        
                        if specific_user == "default":
                            for option in data["variations"]:
                                if data["variations"][option]["user"] == "any":
                                    requirement = str(data["variations"][option]["viewers"])
                                    min = -1
                                    max = -1

                                    if "<" in requirement:
                                        min = 0
                                        max = int(requirement.split("<")[1]) - 1
                                    elif "<=" in requirement:
                                        min = 0
                                        max = int(requirement.split("<=")[1])
                                    elif ">=" in requirement:
                                        min = int(requirement.split(">=")[1])
                                        max = 99999999999
                                    elif ">" in requirement:
                                        min = int(requirement.split(">")[1]) + 1
                                        max = 99999999999
                                    elif "=" in requirement:
                                        min = int(requirement.split("=")[1])
                                        max = int(requirement.split("=")[1])
                                    elif "-" in requirement:
                                        min = int(requirement.split("-")[0])
                                        max = int(requirement.split("-")[1])
                                
                                    if min != -1 and max != -1:
                                        if int(amount) >= min and int(amount) <= max:
                                            buffer = data["variations"][option]["buffer"]
                                            actions = data["variations"][option]["actions"]
                      
                        if specific_user != "default":
                            buffer = data["variations"][specific_user]["buffer"]
                            actions = data["variations"][specific_user]["actions"]
                            
                        
             
               
            else:
                with open(os.getcwd() + "\\configuration\\event\\" + alert["type"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        buffer = data["buffer"]
                        actions = data["actions"]
            
            await runActions(actions, alert)

            for i in range(0, pop_amount):
                alert_queue.pop(0)
            
        await asyncio.sleep(buffer)
    

    




async def callback_sub(d, data):
    # print (data) - This is literally just their UUID
    try:
    
        
        alert = {}
        

        
        
        sub_tier = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}
        alert["tier"] = sub_tier[data["sub_plan"]]
        
        
        alert["sub-message"] = data["sub_message"]["message"]
        
        
        if data["is_gift"]:
        
            
        
            alert["type"] = "giftsub"
            alert["gifter"] = data["display_name"]
            alert["gifted"] = data["recipient_display_name"]
            
            with open(os.getcwd() + "\\variables\\latest-gifsub-gifter.txt", 'w', encoding = "utf-8") as file:
                file.write(data["display_name"]) 
            with open(os.getcwd() + "\\variables\\latest-gifsub-gifted.txt", 'w', encoding = "utf-8") as file:
                file.write(data["recipient_display_name"]) 
        
            prompt ("sub", "Gift Subscription: " + alert["gifter"] + " > " + alert["gifted"] + " [" + sub_tier[data["sub_plan"]] + "]") 
            print ("    Message: " + alert["sub-message"]) 
            
        else:
            alert["type"] = "sub"
            alert["user"] = data["display_name"]
            alert["total-months"] = data["cumulative_months"]

            if "streak_months" in data:
                alert["streak"] = data["streak_months"]

            with open(os.getcwd() + "\\variables\\latest-subscriber.txt", 'w', encoding = "utf-8") as file:
                file.write(data["display_name"]) 
            
            prompt ("sub", "Subscription: " + alert["user"] + " [" + sub_tier[data["sub_plan"]] + "]") 
            print ("    Message: " + alert["sub-message"]) 
        
        
        
        
        global alert_queue
        alert_queue.append(alert)
    
    except Exception as e:
        prompt ("error", "Error handling SubscriptionEvent.")
        await logError()
    
    # TODO - Make sure I set the latest-subscriber file to the user that has the sub
    # Note, it may be a regular sub or a gifted sub so need to check this.
    
    # print (data2)

async def callback_whisper(data, data2):
    # print (data)
    # print (data2)
    pass
      
async def callback_bits (d, data):
    try:
    
        global alert_queue
        alert = {}
        alert["type"] = "bits"
        alert["user"] = data["data"]["user_name"]
        alert["amount"] = str(data["data"]["bits_used"])
        
        message = data["data"]["chat_message"]
        words = message.split(" ")
        for word in words:
            if "cheer" in word and len(word) > 5:
                message = message.replace(word,"")
        alert["message"] = message
        alert_queue.append(alert)

        prompt ("bits", "Bits: " + str(alert["amount"]) + " from " + alert["user"])
        print ("    Message: " + alert["message"])
        
        with open(os.getcwd() + "\\variables\\latest-bits-donator.txt", 'w', encoding = "utf-8") as file:
            file.write(data["data"]["user_name"])
        with open(os.getcwd() + "\\variables\\latest-bits-amount.txt", 'w', encoding = "utf-8") as file:
            file.write(str(data["data"]["bits_used"]))

    except Exception as e:
        prompt ("error", "Error handling BitEvent.")
        await logError()





# this is where we set up the bot
async def run():

    # access = y9blozsq7qm2v8d2qw9i9sktyoc8nj
    # refresh = qqwfvwzcifss9e9hl8ewcdb10t8hpn0iuw4710kn3ggigquexi

    # set up twitch api instance and add user authentication with some scopes
    
    print_spacing = 28 * " "
    
    print (print_spacing + "Loading Authentication              ....", end = "\r")
    
    global twitch    
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify = False)
    token, refresh = await auth.authenticate()
    
    await twitch.set_user_authentication(token, USER_SCOPE, refresh)
    
    print (print_spacing + "Loading Authentication              DONE", end = "\n")
    
    # await twitch.set_user_authentication("a8g7wnqh495gckgmoo4mwgcuggjjx9", USER_SCOPE, "2fag6conscq5y260jo14rkar8plo8bw462oemqqpb5xaqojorm")
    
    print (print_spacing + " Grabbing Twitch User               ....", end = "\r")

    global streamer
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
    streamer = user
    
    print (print_spacing + " Grabbing Twitch User               DONE", end = "\n")
    print (print_spacing + " Registering EventSub               ....", end = "\r")
    
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    await eventsub.listen_channel_follow_v2(streamer.id, streamer.id, on_follow)
    await eventsub.listen_stream_online(streamer.id, on_live)
    await eventsub.listen_channel_ad_break_begin(streamer.id, on_ad)
    await eventsub.listen_channel_poll_begin(streamer.id, on_poll_create)
    await eventsub.listen_channel_poll_end(streamer.id, on_poll_ended)
    await eventsub.listen_channel_prediction_begin(streamer.id, on_prediction_start)    
    await eventsub.listen_channel_prediction_lock(streamer.id, on_prediction_lock)   
    await eventsub.listen_channel_prediction_end(streamer.id, on_prediction_end)   
    await eventsub.listen_hype_train_begin(streamer.id, on_hype_train)   
    
    await eventsub.listen_channel_shoutout_create(streamer.id, streamer.id, on_shoutout_give)
    await eventsub.listen_channel_shoutout_receive(streamer.id, streamer.id, on_shoutout_receive)

    print (print_spacing + " Registering EventSub               DONE", end = "\n")
    print (print_spacing + "  Registering PubSub                ....", end = "\r")
    

    pubsub = PubSub(twitch)
    pubsub.start()

    ## Redeems ########################################
    redeem_event = await pubsub.listen_channel_points(user.id, callback_points)
    ###################################################
    
    ## Subs ###########################################
    sub_event = await pubsub.listen_channel_subscriptions(user.id, callback_sub)
    ###################################################
    
    ## Whisper ########################################
    whisper_event = await pubsub.listen_whispers(user.id, callback_whisper)
    ###################################################
    
    ## Bits ###########################################
    bit_event = await pubsub.listen_bits(user.id, callback_bits)
    ###################################################
    
    print (print_spacing + "  Registering PubSub                DONE", end = "\n")
    print (print_spacing + "    Establish Chat                  ....", end = "\r")
    

    ## Chat ###########################################
    btwitch = await Twitch(APP_ID, APP_SECRET)    
    #await btwitch.set_user_authentication("lss7obc7j3nw9a5eiaikjukh38sid8", USER_SCOPE, "55x1ugaicpvo4etji11duth5nki0kloin0gh3ntnzcf0sru3jp")

    await btwitch.set_user_authentication("fi7d5m18fm1zmcgfabax16xssvvddc", USER_SCOPE, "qudyvazycvc2ef557n0m4prkg84zbpafgbxkq1u2uxh2fck7jm")

    global chat
    chat = await Chat(btwitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.RAID, on_raid)
    chat.start()
    
    print (print_spacing + "    Establish Chat                  DONE", end = "\n")
    ###################################################
    

    
    
    thread1 = threading.Thread(target= manageTimedMessages)
    thread1.start()
    
    thread2 = threading.Thread(target= manageAlerts)
    thread2.start()
    
    
    ############################################################
    newest_follower = ""
    newest_follower_time = 0
    oldest_follower = ""
    oldest_follower_time = 0
    
    channel_follower_result = await twitch.get_channel_followers(broadcaster_id=streamer.id)
    async for follower in channel_follower_result:


        follow_date = follower.followed_at.replace(tzinfo=pytz.UTC)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        followed = now - follow_date
        seconds = followed.days * 24 * 3600 + followed.seconds
        
        if newest_follower == "":
            newest_follower = follower.user_name
            newest_follower_time = seconds
        else:
            if seconds < newest_follower_time:
                newest_follower = follower.user_name
                newest_follower_time = seconds
        
        if oldest_follower == "":
            oldest_follower = follower.user_name
            oldest_follower_time = seconds
        else:
            if seconds > oldest_follower_time:
                oldest_follower = follower.user_name
                oldest_follower_time = seconds
    
    with open(os.getcwd() + "\\variables\\latest-follower.txt", 'w', encoding = "utf-8") as file:
        file.write(newest_follower) 
    
    with open(os.getcwd() + "\\variables\\oldest-follower.txt", 'w', encoding = "utf-8") as file:
        file.write(oldest_follower) 
    ###########################################################
    
    
    
   
    
    input('')
    
 
    
 
    
# os.startfile("vaylui.py")

print (" ")                                             
print ("                                             :@@@@@@@:      ")
print ("                                           @@@@@@@@@@@@@    ")
print ("                                         :@@@%+%@@@#*%@@@:  ")
print (f"                                         @@@@@-:@@@{Fore.LIGHTRED_EX}#{Fore.WHITE}-@@@@@  ")
print (f"                                        :@@@@@@::@{Fore.LIGHTRED_EX}##{Fore.WHITE}@@@@@@: ")
print ("                                         @@@@@@@:::@@@@@@@  ")
print ("                                         :@@@@@@@:@@@@@@@:  ")
print ("                                           @@@@@@@@@@@@@    ")
print ("                                             :@@@@@@@:      ")                                          
print (" ")
#print ("                                              LOADING", end = "\r")
#print ("                                              LOADING")
  


       
      


asyncio.run(run())

