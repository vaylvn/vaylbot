from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from discord_webhook import DiscordWebhook, DiscordEmbed
from twitchAPI.object.eventsub import ChannelFollowEvent, StreamOnlineEvent, StreamOfflineEvent, ChannelPollBeginEvent, ChannelPollEndEvent, ChannelPredictionEvent, ChannelPredictionEndEvent, HypeTrainEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, ChannelAdBreakBeginEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from datetime import datetime, timedelta, date
from twitchAPI.pubsub import PubSub
from collections import OrderedDict
from twitchAPI.helper import first
from multiprocessing import Pool
from contextlib import suppress
from colorama import Fore, init

from playsound3 import playsound
from colorama import Fore, init
from num2words import num2words

from bs4 import BeautifulSoup

from textwrap import wrap
import tldextract
import subprocess
import traceback
import threading
import requests
import win32gui
import requests
import logging
import asyncio
import random
import yaml
import time
import json
import uuid
import pytz
import sys
import os
import re

from pyt2s.services import stream_elements
from pyt2s.services import voice_forge
from pyt2s.services import streamlabs
from pyt2s.services import ibm_watson
from pyt2s.services import cepstral
from pyt2s.services import acapela
from pyt2s.services import oddcast

import obsws_python as obs

twitch = None
streamer = None
chat = None
live = False

bot_id = "1020563705"

# cmd = 'mode 100,20'
# os.system(cmd)

# APP_ID = 'tglr18k2kmbpq7y1k8a2y4376iau1c'
# APP_SECRET = 'yx01kqkx0yp5rvz5pvjyyba2f7aksx'

## YOUTUBE API = AIzaSyAMNLa-bMX81Dh2Hk1UyGBFS7Z2eDnzayw


init(convert=True)
hwnd = win32gui.GetForegroundWindow()
win32gui.MoveWindow(hwnd, 30, 30, 850, 400, True)

vayl_version = "1.3.26"

APP_ID = 'xfc4596ekgo4ewkag6wn01hgs4hfbl'
APP_SECRET = 'p8wl2zzuk3sgjmbdrlxe9l65xno8wk'

USER_SCOPE = [AuthScope.USER_READ_SUBSCRIPTIONS, AuthScope.MODERATION_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, 
              AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS, AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
              AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.MODERATOR_READ_FOLLOWERS, 
              AuthScope.WHISPERS_READ, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_POLLS, AuthScope.CHANNEL_MANAGE_POLLS, AuthScope.CHANNEL_READ_ADS,
              AuthScope.MODERATOR_MANAGE_SHOUTOUTS, AuthScope.MODERATOR_READ_SHOUTOUTS, AuthScope.CHANNEL_READ_PREDICTIONS, AuthScope.CHANNEL_MANAGE_PREDICTIONS,
              AuthScope.CHANNEL_READ_HYPE_TRAIN, AuthScope.CHANNEL_MANAGE_VIPS, AuthScope.CHANNEL_MANAGE_BROADCAST, AuthScope.ANALYTICS_READ_GAMES, AuthScope.MODERATOR_MANAGE_BANNED_USERS,
              AuthScope.MODERATOR_READ_CHATTERS]
TARGET_CHANNEL = ''

with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
    data = yaml.safe_load(file)
    TARGET_CHANNEL = data["connected-account"]


data_directory = os.getcwd() + "\\data\\"



## Variables
########################################
sfx = {}
##
commands = {}
alert_queue = []
##
phrase_cooldown = {}
########################################


## Moderation ######################################################################
moderation = {}
####################################################################################


## TTS #############################################################################
tts_voicepack = {"cepstral":cepstral, "ibmwatson":ibm_watson, "oddcast":oddcast, "streamelements":stream_elements, "streamlabs":streamlabs, "voiceforge":voice_forge }
tts_voice = { "cepstral"        : ["Allison", "Amy", "Belle", "Callie", "Charlie", "Dallas", "Damien", "David", "Diane", "Duchess", "Emily", "Linda", "Robin", "Shouty", "Walter", "William", "Whispery", "Lawrence", "Millie", "Duncan", "Vittoria", "Katrin", "Matthias", "Isabelle", "Jean-Pierre", "Alejandra", "Miguel"],
              "imbwatson"       : ["en-GB_CharlotteV3Voice", "en-GB_JamesV3Voice", "en-GB_KateV3Voice", "en-AU_JackExpressive", "en-AU_HeidiExpressive", "en-US_AllisonV3Voice", "en-US_AllisonExpressive", "en-US_EmilyV3Voice", "en-US_EmmaExpressive", "en-US_HenryV3Voice", "en-US_KevinV3Voice", "en-US_LisaV3Voice", "en-US_LisaExpressive", "en-US_MichaelV3Voice", "en-US_MichaelExpressive", "en-US_OliviaV3Voice", "nl-NL_MerelV3Voice", "fr-FR_NicolasV3Voice", "fr-FR_ReneeV3Voice", "fr-CA_LouiseV3Voice", "de-DE_BirgitV3Voice", "de-DE_DieterV3Voice", "de-DE_ErikaV3Voice", "it-IT_FrancescaV3Voice", "ja-JP_EmiV3Voice", "ko-KR_JinV3Voice", "pt-BR_IsabelaV3Voice", "es-ES_EnriqueV3Voice", "es-ES_LauraV3Voice", "es-LA_SofiaV3Voice", "es-US_SofiaV3Voice"],
              "oddcast"         : ["4-3-1", "6-2-1", "5-4-1", "4-2-1", "5-3-1", "2-7-1", "1-7-1", "7-4-1", "5-2-1", "12-4-1", "8-4-1", "9-2-1", "10-2-1", "4-7-1", "4-4-1", "10-4-1", "3-7-1", "13-4-1", "5-7-1", "6-7-1", "9-4-1", "11-2-1", "7-2-1", "6-3-1", "8-3-1", "7-7-1", "3-1-1", "1-1-1", "2-2-1", "7-3-1", "2-4-1", "3-3-1", "1-3-1", "2-1-1", "2-3-1", "4-1-1", "11-4-1", "8-2-1", "1-2-1", "3-4-1", "8-7-1", "1-7-27", "2-7-27", "2-2-27", "1-4-27", "1-2-27", "1-4-22", "3-2-5", "2-2-5", "1-2-5", "1-4-5", "3-3-10", "5-3-10", "4-3-10", "1-2-10", "2-2-10", "4-4-10", "4-7-10", "6-3-10", "7-3-10", "1-4-10", "3-7-10", "2-7-10", "1-7-10", "2-4-10", "8-3-10", "1-7-18", "1-4-18", "1-7-19", "2-7-19", "1-2-19", "1-4-19", "2-2-19", "2-4-11", "2-7-11", "1-7-11", "2-2-11", "1-2-11", "4-4-11", "1-4-11", "1-2-31", "2-7-32", "1-7-32", "2-2-23", "1-4-23", "1-2-23", "1-7-23", "2-1-4", "2-7-4", "1-7-4", "2-2-4", "4-2-4", "3-2-4", "1-1-4", "4-3-4", "3-3-4", "3-4-4", "5-4-4", "4-4-4", "5-2-4", "1-3-4", "1-4-4", "4-7-4", "2-4-4", "2-3-4", "3-7-4", "6-2-4", "3-1-4", "1-2-15", "3-4-3", "2-7-3", "1-7-3", "3-2-3", "1-1-3", "1-3-3", "2-1-3", "2-2-3", "1-4-3", "2-3-3", "2-4-3", "1-2-8", "1-4-8", "1-7-8", "2-7-8", "3-2-8", "2-7-24", "1-4-24", "1-7-24", "1-4-29", "1-7-29", "2-7-28", "1-4-28", "1-7-28", "2-7-7", "1-7-7", "1-3-7", "10-2-7", "9-2-7", "5-2-7", "6-2-7", "8-2-7", "1-2-7", "1-4-7", "7-2-7", "2-3-7", "2-2-7", "2-4-7", "3-2-7", "6-3-12", "5-3-12", "1-7-12", "2-7-12", "1-4-12", "3-3-12", "7-3-12", "4-3-12", "2-3-12", "8-3-12", "7-3-13", "4-3-13", "8-3-13", "10-3-13", "5-3-13", "2-3-13", "1-4-13", "6-3-13", "1-3-13", "9-3-13", "1-7-20", "2-2-20", "2-7-20", "2-4-20", "1-2-20", "1-4-14", "1-7-14", "2-2-14", "2-7-14", "1-2-14", "2-7-6", "3-4-6", "3-7-6", "4-7-6", "1-7-6", "1-3-6", "2-3-6", "2-4-6", "1-2-30", "1-4-30", "2-2-21", "2-4-21", "1-2-21", "1-7-37", "3-4-37", "1-2-2", "6-2-2", "2-2-2", "9-2-2", "4-3-2", "5-3-2", "1-4-2", "3-4-2", "7-2-2", "8-2-2", "10-2-2", "4-2-2", "3-2-2", "2-1-2", "5-2-2", "2-3-2", "3-3-2", "5-4-2", "4-4-2", "1-1-2", "1-3-2", "1-4-9", "1-2-9", "1-7-9", "2-7-9", "3-4-9", "2-2-9", "1-4-26", "1-3-26", "2-3-26", "1-4-16", "2-7-16", "1-2-16", "3-2-16", "1-7-16", "2-2-16", "1-7-40"],
              "streamelements"  : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Mia", "Miguel", "Penelope", "Astrid", "Filiz", "Gwyneth", "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E", "en-US-Wavenet-F", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D", "en-AU-Standard-C", "en-AU-Standard-D", "en-IN-Wavenet-A", "en-IN-Wavenet-B", "en-IN-Wavenet-C", "af-ZA-Standard-A", "ar-XA-Wavenet-A", "ar-XA-Wavenet-B", "ar-XA-Wavenet-C", "bg-bg-Standard-A", "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-B", "cmn-CN-Wavenet-C", "cmn-CN-Wavenet-D", "cs-CZ-Wavenet-A", "da-DK-Wavenet-A", "nl-NL-Standard-A", "nl-NL-Wavenet-A", "nl-NL-Wavenet-B", "nl-NL-Wavenet-C", "nl-NL-Wavenet-D", "nl-NL-Wavenet-E", "fil-PH-Wavenet-A", "fi-FI-Wavenet-A", "fr-FR-Standard-C", "fr-FR-Standard-D", "fr-FR-Wavenet-A", "fr-FR-Wavenet-B", "fr-FR-Wavenet-C", "fr-FR-Wavenet-D", "fr-CA-Standard-A", "fr-CA-Standard-B", "fr-CA-Standard-C", "fr-CA-Standard-D", "de-DE-Standard-A", "de-DE-Standard-B", "de-DE-Wavenet-A", "de-DE-Wavenet-B", "de-DE-Wavenet-C", "de-DE-Wavenet-D", "el-GR-Wavenet-A", "hi-IN-Wavenet-A", "hi-IN-Wavenet-B", "hi-IN-Wavenet-C", "hu-HU-Wavenet-A", "is-is-Standard-A", "id-ID-Wavenet-A", "id-ID-Wavenet-B", "id-ID-Wavenet-C", "it-IT-Standard-A", "it-IT-Wavenet-A", "it-IT-Wavenet-B", "it-IT-Wavenet-C", "it-IT-Wavenet-D", "ja-JP-Standard-A", "ja-JP-Wavenet-A", "ja-JP-Wavenet-B", "ja-JP-Wavenet-C", "ja-JP-Wavenet-D", "ko-KR-Standard-A", "ko-KR-Wavenet-A", "lv-lv-Standard-A", "nb-no-Wavenet-E", "nb-no-Wavenet-A", "nb-no-Wavenet-B", "nb-no-Wavenet-C", "nb-no-Wavenet-D", "pl-PL-Wavenet-A", "pl-PL-Wavenet-B", "pl-PL-Wavenet-C", "pl-PL-Wavenet-D", "pt-PT-Wavenet-A", "pt-PT-Wavenet-B", "pt-PT-Wavenet-C", "pt-PT-Wavenet-D", "pt-BR-Standard-A", "ru-RU-Wavenet-A", "ru-RU-Wavenet-B", "ru-RU-Wavenet-C", "ru-RU-Wavenet-D", "sr-rs-Standard-A", "sk-SK-Wavenet-A", "es-ES-Standard-A", "sv-SE-Standard-A", "tr-TR-Standard-A", "tr-TR-Wavenet-A", "tr-TR-Wavenet-B", "tr-TR-Wavenet-C", "tr-TR-Wavenet-D", "tr-TR-Wavenet-E", "uk-UA-Wavenet-A", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "Linda", "Heather", "Sean", "Hoda", "Naayf", "Ivan", "Herena", "Tracy", "Danny", "Huihui", "Yaoyao", "Kangkang", "HanHan", "Zhiwei", "Matej", "Jakub", "Guillaume", "Michael", "Karsten", "Stefanos", "Szabolcs", "Andika", "Heidi", "Kalpana", "Hemant", "Rizwan", "Filip", "Lado", "Valluvar", "Pattara", "An"],
              "streamlabs"      : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zeina", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Lea", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Camila", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Lucia", "Mia", "Miguel", "Lupe", "Penelope", "Astrid", "Filiz", "Gwyneth"],
              "voiceforge"      : ["Conrad", "Designer", "Diesel", "Dog", "Evilgenius", "Frank", "French-fry", "Gregory", "Jerkface", "JerseyGirl", "Kayla", "Kevin", "Kidaroo", "Princess", "RansomNote", "Robot", "Shygirl", "Susan", "Tamika", "TopHat", "Vixen", "Vlad", "Warren", "Wiseguy", "Zach", "Obama"]}
# "acapela"         : ["graham22k", "harry22k", "lucy22k", "lucy_nt22k", "peter22k", "peter_nt22k", "queenelizabeth22k", "queenelizabeth_nt22k", "rachel22k", "rachel_nt22k", "rosie22k", "sophiabtob22k", "sophiabtob_nt22k", "rhona22k", "rhona_nt22k", "liam22k", "lisa22k", "lisa_nt22k", "olivia22k", "tyler22k", "tyler_nt22k", "deepa22k", "deepa_nt22k", "nizareng22k", "nizareng_nt22k", "darius22k", "darius_nt22k", "ella22k", "emilioenglish22k", "josh22k", "karen22k", "karen_nt22k", "laura22k", "laura_nt22k", "lily22k", "lily_nt22k", "micah22k", "rod22k", "rod_nt22k", "ryan22k", "ryan_nt22k", "saul22k", "saul_nt22k", "scott22k", "sharon22k", "sharon_nt22k", "tamira22k", "tamira_nt22k", "taylor22k", "taylor_nt22k", "tracy22k", "tracy_nt22k", "valeriaenglish22k", "will22k", "will_nt22k", "leila22k", "leila_nt22k", "jalal22k", "jalal_nt22k", "mehdi22k", "mehdi_nt22k", "nizar22k", "nizar_nt22k", "salma22k", "salma_nt22k", "laia22k", "laia_nt22k", "lulu22k", "lulu_nt22k", "eliska22k", "eliska_nt22k", "mette22k", "mette_nt22k", "rasmus22k", "rasmus_nt22k", "rikke22k", "rikke_nt22k", "daan22k", "daan_nt22k", "femke22k", "femke_nt22k", "jasmijn22k", "jasmijn_nt22k", "max22k", "max_nt22k", "tessabtob22k", "tessabtob_nt22k", "christinabtob22k", "christinabtob_nt22k", "jeroen22k", "jeroen_nt22k", "sofie22k", "sofie_nt22k", "zoe22k", "zoe_nt22k", "hanna22k", "hanna_nt22k", "hanus22k", "hanus_nt22k", "sanna22k", "sanna_nt22k", "alice22k", "alice_nt22k", "anais22k", "anais_nt22k", "anaisbtob22k", "anaisbtob_nt22k", "antoine22k", "antoine_nt22k", "bruno22k", "bruno_nt22k", "claire22k", "claire_nt22k", "constance22k", "constance_nt22k", "elise22k", "julie22k", "julie_nt22k", "manon22k", "manon_nt22k", "margaux22k", "margaux_nt22k", "valentin22k", "anthony22k", "anthony_nt22k", "louise22k", "louise_nt22k", "alice-be22k", "alice-be_nt22k", "anais-be22k", "anais-be_nt22k", "antoine-be22k", "antoine-be_nt22k", "bruno-be22k", "bruno-be_nt22k", "claire-be22k", "claire-be_nt22k", "elise-be22k", "julie-be22k", "julie-be_nt22k", "manon-be22k", "manon-be_nt22k", "margaux-be22k", "margaux-be_nt22k", "valentin-be22k", "andreas22k", "andreas_nt22k", "ankebtob22k", "ankebtob_nt22k", "claudia22k", "claudia_nt22k", "jonas22k", "julia22k", "julia_nt22k", "klaus22k", "klaus_nt22k", "lea22k", "sarah22k", "sarah_nt22k", "dimitris22k", "dimitris_nt22k", "alessio22k", "aurora22k", "barbarabtob22k", "barbarabtob_nt22k", "chiara22k", "chiara_nt22k", "fabiana22k", "fabiana_nt22k", "vittorio22k", "vittorio_nt22k", "sakura22k", "sakura_nt22k", "minji22k", "minji_nt22k", "bente22k", "bente_nt22k", "elias22k", "emilie22k", "ida22k", "ida_nt22k", "kari22k", "kari_nt22k", "olav22k", "olav_nt22k", "ania22k", "ania_nt22k", "gosia22k", "gosia_nt22k", "isabel22k", "isabel_nt22k", "gabriela22k", "gabriela_nt22k", "marcia22k", "marcia_nt22k", "sergio22k", "sergio_nt22k", "alyona22k", "alyona_nt22k", "lena22k", "lena_nt22k", "biera_hmm_22k", "elle_hmm_22k", "anabtob22k", "anabtob_nt22k", "antonio22k", "antonio_nt22k", "elenabtob22k", "elenabtob_nt22k", "ines22k", "ines_nt22k", "maria22k", "maria_nt22k", "emilio22k", "rodrigo22k", "rodrigo_nt22k", "rosa22k", "rosa_nt22k", "valeria22k", "elin22k", "elin_nt22k", "emil22k", "emil_nt22k", "emma22k", "emma_nt22k", "erik22k", "erik_nt22k", "filip22k", "freja22k", "kal22k", "kal_nt22k", "mia22k", "mia_nt22k", "samuel22k", "samuel_nt22k", "ipek22k", "ipek_nt22k", "zeynep22k", "zeynep_nt22k"],                                                                  
####################################################################################

users_spoken = []


## Version Check ################################################################################
async def versionCheck():

    latest = ""
    latest_split = []
    
    url = "https://drive.google.com/drive/u/0/folders/10YHHjNOO5j7cS-LZDdTHWzWaxSwGUx6A"
    response = requests.get(url) 
    html = response.text 
    
    soup = BeautifulSoup(html, 'html.parser') 
    
    for v in soup.findAll("div", attrs={"class": "KL4NAf"}):
        latest = v.text.replace("Vayl ","").replace(".zip","")
    
    if vayl_version != latest:
        spacing = " " * 39
        # print (spacing + "New Version Available")
        # print (spacing + " " + vayl_version + " ----> " + latest)
        # print (" ")
#################################################################################################
    
    
    
    
    
    
    
    
    
    

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    # print (" ")
    # print ("                                          Welcome to Vayl")
    # print (" ")
    await ready_event.chat.join_room(TARGET_CHANNEL)
    await reload(False)
    
  
async def updateVaylVariable (name, value):
    try:
        with open(os.getcwd() + "\\data\\variables\\vayl\\" + name + ".txt", 'w', encoding = "utf-8") as file:
            file.write(value)    
    except:
        pass
  
  
  
## Console ##############################################################################
async def clearConsole():
    try:
        with open(os.getcwd() + "\\data\\console.txt", 'w', encoding = "utf-8") as file:
            pass
    except:
        pass

async def sendToConsole (text):
    try:
        with open(os.getcwd() + "\\data\\console.txt", 'a', encoding = "utf-8") as file:
            file.write("\n" + text)
    except:
        pass
#########################################################################################
  
  
  
async def logError (info, reference):

    global TARGET_CHANNEL
    global vayl_version
    
    await sendToConsole("Error Occured regarding '" + reference + "'")
    
    isExist = os.path.exists(os.getcwd() + "\\data\\logs\\")
    if not isExist:
        os.makedirs(os.getcwd() + "\\data\\logs\\")
    
    timestamp = str(time.time())
    with open (os.getcwd() + "\\data\\logs\\" + timestamp + ".txt", 'w') as log_file:
        log_file.write("User: " + TARGET_CHANNEL + "\n" "Version: " + vayl_version + "\n")
        
        if info:
            log_file.write("Info:" + "\n")  
            for line in info:
                log_file.write("- " + line + "\n") 
        
        log_file.write(traceback.format_exc())
        
        
    try:    
        with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            if "bug-auto-report" in data and data["bug-auto-report"]:
                with open (os.getcwd() + "\\data\\logs\\" + timestamp + ".txt", 'r') as log_file:
                    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/1257675918957351013/wiIdAeOQBaXdhzyLrPRhplWz2mBbfZrTbch--c-5wMYDu1YYk2gUexBj6AUMTahnPlZs", username = "Bug Report", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png")
                    webhook.add_file(file = log_file.read(), filename= timestamp + ".txt")
                    response = webhook.execute()
    except Exception as e:
        pass
        # print (e)
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
    
    # print (symbol[type] + " " + message) 



# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):

    global phrase_cooldown
    global alert_queue
    global moderation
    global live

    try:
        
        message = msg.text
        name = msg.user.name
        
        ## Moderation ###################################################################################

        if name.lower() != "vaylbot":

            flagged = []
            if len(moderation["link"]["whitelist"]) > 0:
                for word in message.split(" "):
                    info = tldextract.extract(word)
                
                    if "http" in word or "www." in word or info.suffix != "":
                        allowed = False
                        for whitelist in moderation["link"]["whitelist"]:
                            if whitelist in word:
                                allowed = True
                        if not allowed:
                            flagged.append(word)

            else:
                for blacklist in moderation["link"]["blacklist"]:
                    if blacklist in message:
                        flagged.append(word)
                        
            if len(flagged) > 0:
                is_mod = await isModerator(name)
                is_streamer = await isStreamer(name)
                if not is_mod and not is_streamer and name.lower() not in moderation["link"]["permitted-users"]:
                    
                    
                    if name not in moderation["link"]["warnings"]:
                        moderation["link"]["warnings"][name] = 0
                        
                    moderation["link"]["warnings"][name] += 1
                    if moderation["link"]["warnings"][name] >= int(moderation["link"]["warning"]["limit"]):
                        ## timeout user
                        
                        duration = int(moderation["link"]["timeout"]["duration"])
                        
                        if len(moderation["link"]["timeout"]["message"]) > 0:
                            await chat.send_message(TARGET_CHANNEL, moderation["link"]["timeout"]["message"].replace("%user%",name).replace("%duration%",str(duration)))
                            await chat.send_message(TARGET_CHANNEL, "Warning " + str(moderation["link"]["warnings"][name]) + " of " + str(moderation["link"]["warning"]["limit"]))
                    
                        async for u in twitch.get_users(logins = [name]):
                            await twitch.ban_user(streamer.id, streamer.id, u.id, "Vayl Moderation (Link)", duration)
                    
                    else:
                        if len(moderation["link"]["warning"]["message"]) > 0:
                            await chat.send_message(TARGET_CHANNEL, moderation["link"]["warning"]["message"].replace("%user%",name))

                    await twitch.delete_chat_message(streamer.id, streamer.id, msg.id)


        #################################################################################################
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        with open(os.getcwd() + "\\configuration\\phrases.yml", 'r', encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            
            for phrase, info in data["phrase"].items():
                caught = True if (info["type"] == "contains" and phrase.lower() in message.lower()) or (info["type"] == "matches" and phrase.lower() == message.lower()) else False
                
                if caught:
                    
                    cooldown = phrase_cooldown[phrase.lower()] if phrase.lower() in phrase_cooldown else 0
                    if time.time() - cooldown >= info["cooldown"]:
                        actions = info["actions"]
                        variables = {"user":msg.user.name}
                        await runActions(info["actions"], variables)
                        phrase_cooldown[phrase.lower()] = time.time()
                    

            
        
        ## First Chat
        if not live:
            async for streams in twitch.get_streams(user_id = streamer.id):
                live = True

        if live:
        
            global users_spoken
            name = msg.user.name
            if name not in users_spoken:
                users_spoken.append(name)
                alert = {}
                alert["type"] = "firstsessionchat"
                alert["user"] = name
                alert_queue.insert(0, alert)
                
            
            first_time_chat = True if msg.__dict__["_parsed"]["tags"]["first-msg"] == "1" else False
            if first_time_chat:
                alert = {}
                alert["type"] = "firsttimechat"
                alert["user"] = name
                alert_queue.insert(0, alert)
            
                        
        if "!addquote" in message:
            try:
                    
           
                if msg.reply_parent_msg_body:
            
                    quote_message = " ".join(msg.reply_parent_msg_body.split("\s"))
                    quote_author = msg.reply_thread_parent_user_login
                    
                    line = '"' + quote_message + '" - ' + quote_author + ", " + str(datetime.now().year)
                    total = 0
                    with open(os.getcwd() + "\\data\\resources\\quotes.yml", 'a+', encoding="utf-8") as file:
                        total = len(file.readlines())
                        file.write("\n" + line)
                    await chat.send_message(TARGET_CHANNEL, "Quote #" + str(total) + " Added: " + line)
                else:
                    await chat.send_message(TARGET_CHANNEL, "!addquote must be used as a reply.")
                    
                    
            except:
                prompt ("error", "Error creating quote.")
                await logError()
            

                    
    except Exception as e:
        # print (f"[{Fore.RED}♦{Fore.WHITE}]] Error handling MessageEvent.")
        await logError()
   
    # # print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')

async def on_raid (raid: dict):
    try:
    
        alert = {}
        alert["type"] = "raid"
        alert["user"] = raid["tags"]["display-name"]
        alert["viewercount"] = str(raid["tags"]["msg-param-viewerCount"])
                
        await updateVaylVariable("latest-raid-raider", raid["tags"]["display-name"])
        await updateVaylVariable("latest-raid-amount", raid["tags"]["msg-param-viewerCount"])
                
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
        
        # # print (cmd.user.badges)
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

## Convert Command ##################################################

convert_confirmation = False
async def convert_command (cmd: ChatCommand):
    
    global convert_confirmation
    is_streamer = await isStreamer(cmd.user.name)
    if is_streamer:
        
        if convert_confirmation:
            
            for filename in os.listdir(os.getcwd() + "\\configuration2"):
                if ".yml" in filename:
                    lines = []
                    with open(os.getcwd() + "\\configuration2\\" + filename, 'r', encoding = "utf-8") as file:
                        for line in file.readlines():
                            lines.append(line)
                    with open(os.getcwd() + "\\configuration2\\" + filename, 'w', encoding = "utf-8") as file:
                        try:
                            for line in lines:
                            
                                newline = ""
                            
                                spacing = 0
                                for s in line:
                                    if s == " ":
                                        spacing += 1
                                    else:
                                        break
                            
                                
                                args = line.split(" ; ")[1:]
                                if "obs:scene" in line:
                                    newline = "obs:scene ; scene=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:show" in line:
                                    newline = "obs:show ; source=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:hide" in line:
                                    newline = "obs:hide ; source=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:toggle" in line:
                                    newline = "obs:toggle ; source=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:label" in line:
                                    newline = "obs:label ; source=" + args[0] + ", text=" + args[2]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:mediafile" in line:
                                    newline = "obs:mediafile ; source=" + args[0] + ", filepath=" + args[1] 
                                    file.write((" " * spacing) + "- " + newline)
                                elif "obs:slideshow" in line:
                                    newline = "obs:slideshow ; source=" + args[0] + ", state=" + args[1]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "playsound" in line:
                                    newline = "playsound ; sound=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "wait" in line:
                                    newline = "wait ; time=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "chat" in line:
                                    newline = "chat ; message=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "editfile" in line:
                                    newline = "editfile ; filepath=" + args[0] + ", action=overwrite, text=" + args[1]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "variable" in line:
                                    newline = "variable ; name=" + args[0] + ", text=" + args[1]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "tts" in line:
                                    newline = "tts ; voice=" + args[0] + ", message=" + args[1] + ", halt=" + args[2] + ", limit=" + args[3]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "cmd" in line:
                                    newline = "cmd ; command=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "announce" in line:
                                    newline = "announce ; message=" + args[0] + ", color=" + args[1]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "counter:increase" in line:
                                    newline = "counter ; name=" + args[0] + ", modifier=increase, amount=" + args[1] + ", limit=9999999"
                                    file.write((" " * spacing) + "- " + newline)
                                elif "counter:decrease" in line:
                                    newline = "counter ; name=" + args[0] + ", modifier=decrease, amount=" + args[1] + ", limit=0"
                                    file.write((" " * spacing) + "- " + newline)
                                elif "counter:set" in line:
                                    newline = "counter ; name=" + args[0] + ", modifier=set, amount=" + args[1] + ", limit=0"
                                    file.write((" " * spacing) + "- " + newline)
                                elif "vip:add" in line:
                                    newline = "vip ; modifier=add, username=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "vip:remove" in line:
                                    newline = "vip ; modifier=remove, username=" + args[0]
                                    file.write((" " * spacing) + "- " + newline)
                                elif "timeout" in line:
                                    newline = "timeout ; username=" + args[0] + ", time=" + args[0] + ", reason=vayl"
                                    file.write((" " * spacing) + "- " + newline)
                                else:
                                    file.write(line)
                            
                                
                        
                        except:
                            continue
            
        else:
            convert_confirmation = True
            await chat.send_message(TARGET_CHANNEL, "IMPORTANT")
            await chat.send_message(TARGET_CHANNEL, "PLEASE ensure you have a backup of your vayl directory before proceeding.")
            await chat.send_message(TARGET_CHANNEL, "--")
            await chat.send_message(TARGET_CHANNEL, "To confirm, retype !convert")

#####################################################################





## FollowAge Command ################################################
async def followage_command (cmd: ChatCommand):

    global chat
    global twitch
    global streamer
    
    try:
    
        # # print (len(cmd.parameter))
        try:
            name = cmd.user.name
            # # print ("length: " + str(len(cmd.parameter)))
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
                    # years = int(followed.days / 365)

                    years, remainder = divmod(followed.total_seconds(), 31536000)
                    days, remainder = divmod(remainder, 86400)
                    hours, remainder = divmod(remainder, 3600)
                    minutes, remainder = divmod(remainder, 60)
                    
                    
                    
                    '''
                    days, remainder) = divmod(seconds, 86400)
                    (hours, remainder) = divmod(remainder, 3600)
                    (minutes, seconds) = divmod(remainder, 60)
                                    
                    
                    seconds = followed.days * 24 * 3600 + followed.seconds
                    minutes, seconds = divmod(seconds, 60)
                    hours, minutes = divmod(minutes, 60)
                    days, hours = divmod(hours, 24)
                    '''
                    
                    await chat.send_message(TARGET_CHANNEL, name + " has been following for " + str(int(years)) + " Years, " + str(int(days)) + " Days, " + str(int(hours)) + " Hours, " + str(int(minutes)) + " Minutes, " + str(int(remainder)) + " Seconds.")

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
    
    f = open(os.getcwd() + "\\data\\resources\\quotes.yml", 'a+', encoding = "utf-8")
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
    f = open(os.getcwd() + "\\data\\resources\\quotes.yml", 'r', encoding = "utf-8")
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
                            sfxname = sound_data["sound"]
                            threading.Thread(target=playsound, args=(os.getcwd() + "\\data\\resources\\sounds\\" + sound_data["sound"],), daemon=True).start()
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
        
        global alert_queue
        
        variables = {}
        variables["userid"] = data["data"]["redemption"]["user"]["id"]
        variables["user"] = data["data"]["redemption"]["user"]["display_name"]
        
        await updateVaylVariable("latest-redeem-user", data["data"]["redemption"]["user"]["display_name"])
        await updateVaylVariable("latest-redeem-name", data["data"]["redemption"]["reward"]["title"])
        
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

    except Exception as e:
        prompt ("error", "Error handling RedeemEvent.")
        await logError()
#####################################################################






        
## Actions ##########################################################
async def runActions (actions, variables):
    
    cl = None
    obs_scenes = []
    obs_groups = []
    
    global twitch
    global streamer

    for a in actions:
        
        action = a.split(" ; ")[0]
        argument_list = a.split(" ; ")[1].split(", ")
        arguments = {}
        
        obs_actions = ["obs:scene","obs:show","obs:hide","obs:toggle","obs:label","obs:image","obs:mediafile","obs:slideshow"]
        try:
            if cl is None:
                if action in obs_actions:
                     with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
                        data = yaml.safe_load(file)
                        cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
                        
                        for scene in cl.get_scene_list().__dict__["scenes"]:
                            obs_scenes.append(scene["sceneName"])
                        for group in cl.get_group_list().__dict__["groups"]:
                            obs_groups.append(group) 
                            
        except Exception as e:
            await logError()
        
        
        ## Should probably make default dictionary here, add default for each action.
        ## Should I add additinal list of "required arguments" and notify user if missing?
        ## Some are optional (such as tts cutoff)

        default = { "obs:scene"      : { "scene":"" },
                    "obs:show"       : { "source":"" },
                    "obs:hide"       : { "source":"" },
                    "obs:toggle"     : { "source":"" },
                    "obs:label"      : { "source":"", "text":"", "color":"" },
                    "obs:mediafile"  : { "source":"", "filepath":"" },
                    "obs:slideshow"  : { "source":"", "state":"" },
                    "playsound"      : { "sound":"" },
                    "wait"           : { "time":0 },
                    "chat"           : { "message":"" },
                    "editfile"       : { "filepath":"", "action":"", "text":"" },
                    "variable"       : { "name":"", "text":"" },
                    "counter"        : { "name":"", "modifier":"", "amount":0 },
                    "list"           : { "name":"", "modifier":"", "text":"" },
                    "conditional"    : { "name":"" },
                    "tts"            : { "voice":"", "message":"", "halt":True, "cutoff":99999999 },
                    "cmd"            : { "command":"" },
                    "announce"       : { "message":"", "color":"default" },
                    "vip"            : { "modifier":"", "username":"" },
                    "webhook"        : { "name":"" }}
        
        required = { "obs:scene"     : ["scene"],
                     "obs:show"      : ["source"],
                     "obs:hide"      : ["source"],
                     "obs:toggle"    : ["source"],
                     "obs:label"     : ["source","text"],
                     "obs:mediafile" : ["source","filepath"],
                     "obs:slideshow" : ["source","state"],
                     "playsound"     : ["sound"],
                     "wait"          : ["time"],
                     "chat"          : ["message"],
                     "editfile"      : ["filepath","action","text"],
                     "variable"      : ["name","text"],
                     "counter"       : ["name","modifier","amount"],
                     "list"          : ["name","modifier","text"],
                     "conditional"   : ["name"],
                     "tts"           : ["voice","message"],
                     "cmd"           : ["command"],
                     "announce"      : ["message"],
                     "vip"           : ["modifier","username"],
                     "webhook"       : ["name"]}
        
        
        ## Global Modifiers
        for argument in argument_list:
            arguments[argument.split("=")[0]] = argument.split("=")[1]
        
        
        for key, value in arguments.items():
        
            default[key] = value
            
            for variable in variables:
                default[key] = default[key].replace("%" + variable + "%", str(variables[variable]))
                    
            for type in ["counter","variable","list"]:
                if "%" + type + ":" in default[key]:
                    type = type.replace("variable","text")
                    name = default[key].split("%" + type + ":")[1].split("%")[0]
                    try:
                        with open(os.getcwd() + "\\data\\variables\\" + type + "\\" + name + ".txt", "r", encoding = "utf-8") as f:
                            list = []
                            for line in f.readlines():
                                list.append(line.rstrip())
                            default[key] = default[key].replace("%" + type + ":" + name + "%", ", ".join(list))
                    except Exception as e:
                        pass
                        # print (e)
            
            if "%rnumber" in default[key]:
                min = int(default[key].split("%rnumber:")[1].split("-")[0])
                max = int(default[key].split("%rnumber:")[1].split("-")[1].split("%")[0])
                rstring = "%rnumber:" + str(min) + "-" + str(max) + "%"
                default[key] = default[key].replace(rstring, str(random.randint(min, max)))
                
            if "%rfollower%" in default[key]:
                followers = []
                async for follower in await twitch.get_channel_followers(broadcaster_id=streamer.id):
                    followers.append(follower.user_name)
                followers.remove("VaylBot")
                default[key] = default[key].replace("%rfollower%", random.choice(followers))
    
            if "%ruser%" in default[key]:
                chatters = []
                async for chatter in await twitch.get_chatters(streamer.id, streamer.id):
                    chatters.append(chatter.user_name)
                chatters.remove("VaylBot")
                default[key] = default[key].replace("%ruser%", random.choice(chatters))

            if "%rlist" in default[key]:
                name = default[key].replace("%","").split(":")[1].split("%")[0]
                with open(os.getcwd() + "\\data\\variables\\list\\" + name + ".txt", 'r', encoding = "utf-8") as f:
                    data = f.read().splitlines()
                    default[key] = default[key].replace("%rlist:" + name + "%", random.choice(data))
    
            if "%system:dateus%" in default[key]:
                today = date.today()
                d3 = today.strftime("%m/%d/%y")
                default[key] = default[key].replace("%system:dateus%", d3)
                
            if "%system:dateuk%" in default[key]:
                today = date.today()
                d3 = today.strftime("%d/%m/%y")
                default[key] = default[key].replace("%system:dateuk%", d3)
                
            if "%system:time%" in default[key]:
                now = datetime.now()
                default[key] = default[key].replace("%system:time%", now.strftime("%H:%M:%S"))
                
            if "%xstring:" in default[key]:
                string = default[key].split(":")[1]
                amount = default[key].split(":")[2].split("%")[0]
                default[key] = default[key].replace("%xstring:" + string + ":" + amount + "%", string * int(amount))
        
        ## Check if requires have been given
        
        missing = []
        for require in required[action]:
            if require not in arguments:
                missing.append("'" + require + "'")

        if len(missing) > 0:
            prompt("misc", "Unable to run '" + action + "' action.")
            prompt("misc", "Missing variables: " + ",".join(missing))
            continue

           
        ###################
        
        
        ## Defaults
        ##  LIST ACTIONS AND THEIR REQUIREMENTS (AND DEFAULTS)
        ##  I SHOULD IN THEORY BE ABLE TO THEN LOOP THROUGH THE ARGUMENTS AND UPDATE THE DEFAULTS
        ##  SAVES HAVING TO LOOP THROUGH AND ASSIGN THE DEFAULTS EVERY TIME.
        ## ########
        

        ## obs:scene
        if action == "obs:scene":
            try:
                found = False
                for scene in cl.get_scene_list().__dict__["scenes"]:
                    if default["scene"] == scene["sceneName"]:
                        cl.set_current_program_scene(default["scene"])
                        found = True
                        break
                if not found:
                    prompt ("error", "Scene not found: " + default["scene"])
            except:
                await logError()

        ## obs:show
        if action == "obs:show":
            try:
                found = False
                for scene in obs_scenes:
                    for item in cl.get_scene_item_list(scene).__dict__["scene_items"]:
                        if default["source"] == item["sourceName"]:
                            id = cl.get_scene_item_id(scene, default["source"], offset = None).__dict__["scene_item_id"] 
                            cl.set_scene_item_enabled(scene, id, True)
                            found = True
                if not found:
                    for group in obs_groups:
                        for item in cl.get_group_scene_item_list(group).__dict__["scene_items"]:
                            if default["source"] in item["sourceName"]:
                                id = cl.get_scene_item_id(group, default["source"], offset = None).__dict__["scene_item_id"] 
                                cl.set_scene_item_enabled(group, id, True)
                                found = True
                if not found:
                    prompt ("misc", "Unable to find source: " + default["source"])
            except:
                await logError()
                
         
        ## obs:hide
        if action == "obs:hide":
            try:
                found = False
                for scene in obs_scenes:
                    for item in cl.get_scene_item_list(scene).__dict__["scene_items"]:
                        if default["source"] == item["sourceName"]:
                            id = cl.get_scene_item_id(scene, default["source"], offset = None).__dict__["scene_item_id"] 
                            cl.set_scene_item_enabled(scene, id, False)
                            found = True
                if not found:
                    for group in obs_groups:
                        for item in cl.get_group_scene_item_list(group).__dict__["scene_items"]:
                            if default["source"] in item["sourceName"]:
                                id = cl.get_scene_item_id(group, default["source"], offset = None).__dict__["scene_item_id"] 
                                cl.set_scene_item_enabled(group, id, False)
                                found = True
                if not found:
                    prompt ("misc", "Unable to find source: " + default["source"])
            except:
                await logError()

        ## obs:toggle
        if action == "obs:toggle":
            try:
                found = False
                for scene in obs_scenes:
                    for item in cl.get_scene_item_list(scene).__dict__["scene_items"]:
                        if default["source"] == item["sourceName"]:
                            id = cl.get_scene_item_id(scene, default["source"], offset = None).__dict__["scene_item_id"] 
                            enabled = bool(cl.get_scene_item_enabled(scene, source_id).__dict__["scene_item_enabled"])
                            cl.set_scene_item_enabled(scene, id, not enabled)
                            found = True
                if not found:
                    for group in obs_groups:
                        for item in cl.get_group_scene_item_list(group).__dict__["scene_items"]:
                            if default["source"] in item["sourceName"]:
                                id = cl.get_scene_item_id(group, default["source"], offset = None).__dict__["scene_item_id"] 
                                enabled = bool(cl.get_scene_item_enabled(group, source_id).__dict__["scene_item_enabled"])
                                cl.set_scene_item_enabled(group, id, not enabled)
                                found = True
                if not found:
                    prompt ("misc", "Unable to find source: " + default["source"])
            except:
                await logError()

        ## obs:label
        if action == "obs:label":
            try:
                label = cl.get_input_settings(default["source"]).__dict__
                data = dict(label["input_settings"])
                if "color" in default and default["color"] != "":
                    color_string = str(default["color"]).replace("0x","")
                    wcs = wrap(color_string, 2)
                    default["color"] = "0x" + wcs[2] + wcs[1] + wcs[0]
                    data["color"] = int(default["color"], 0)
                data["text"] = default["text"]
                cl.set_input_settings(default["source"], data, True)
            except:
                await logError()
                
        ## obs:image
        if action == "obs:image":
            try:
                image = cl.get_input_settings(default["source"]).__dict__
                data = dict(image["input_settings"])
                data["file"] = default["filepath"]
                cl.set_input_settings(default["source"], data, True)
            except:
                await logError()

        ## obs:mediafile
        if action == "obs:mediafile":
            try:
                mediafile = cl.get_input_settings(default["source"]).__dict__
                data = dict(mediafile["input_settings"])
                data["local_file"] = default["filepath"]
                cl.set_input_settings(default["source"], data, True)
            except:
                await logError()

        ## obs:slideshow
        if action == "obs:slideshow":
            try:
                if "play" == default["state"]:
                    cl.trigger_media_input_action(default["source"], "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY")
                elif "pause" == default["state"]:
                    cl.trigger_media_input_action(default["source"], "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE")
            except:
                await logError()

        ## wait
        if action == "wait":
            try:
                await asyncio.sleep(float(default["time"]))
            except:
                await logError()
                
        ## chat
        if action == "chat":
            try:
                await chat.send_message(TARGET_CHANNEL, default["message"])
            except:
                await logError()

        ## editfile
        if action == "editfile":

            try:
                with open(default["path"], 'r', encoding = "utf-8") as f:
                    data = f.read()
                    if default["action"] == "overwrite":
                        try:
                            with open(default["path"], 'w', encoding = "utf-8") as file:
                                file.write(default["text"])
                        except:
                            with open(default["path"], 'w', encoding = "utf-8") as file:
                                file.write(data)
                    elif default["action"] == "overwrite":
                        try:
                            with open(default["path"], 'a', encoding = "utf-8") as file:
                                file.write(default["text"])
                        except:
                            with open(default["path"], 'w', encoding = "utf-8") as file:
                                file.write(data)

            except:
                await logError()

        ## variable
        if action == "variable":
            try:
                with open(os.getcwd() + "\\data\\variables\\text\\" + default["name"], 'r', encoding = "utf-8") as f:
                    data = f.read()
                    try:
                        with open(os.getcwd() + "\\data\\variables\\text\\" + default["name"], 'w', encoding = "utf-8") as file:
                            file.write(default["text"])
                    except:
                        with open(os.getcwd() + "\\data\\variables\\text\\" + default["name"], 'w', encoding = "utf-8") as file:
                            file.write(data)
            except:
                await logError()

        ## counter
        if action == "counter":
            try:
            
                counter = 0
                try:
                    with open(os.getcwd() + "\\data\\variables\\counter\\" + default["name"] + ".txt", 'r', encoding = "utf-8") as file:
                        counter = int(file.read())
                except Exception as e:
                    pass
                         
                default["limit"] = int(default["limit"])         
                default["amount"] = int(default["amount"])
                if default["modifier"] == "increase":
                    counter = (counter + default["amount"]) if (counter + default["amount"]) <= default["limit"] else default["limit"]
                elif default["modifier"] == "decrease":
                    counter = (counter - default["amount"]) if (counter - default["amount"]) >= default["limit"] else default["limit"]
                elif default["modifier"] == "set":
                    counter = default["amount"]
                   
                with open(os.getcwd() + "\\data\\variables\\counter\\" + default["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(counter))
                    
            except:
                await logError()
                
        ## list
        if action == "list":
            try:
            
                list = []
                try:
                    with open(os.getcwd() + "\\data\\variables\\list\\" + default["name"] + ".txt", 'r', encoding = "utf-8") as file:
                        list = file.read().splitlines()
                except Exception as e:
                    pass
                    
                if default["modifier"] == "add":
                    list.append(default["text"])
                elif default["modifier"] == "remove":
                    list.append(default["text"])
                elif default["modifier"] == "clear":
                    list = []
                    
                with open(os.getcwd() + "\\data\\variables\\list\\" + default["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    for line in list:
                        if len(line) > 0:
                            file.write(line + "\n")
            
            except:
                await logError()

        ## announce
        if action == "announce":
            try:
                await twitch.send_chat_announcement(streamer.id, streamer.id, default["message"], default["color"])
            except:
                await logError()
                
        ## vip
        if action == "vip":
            try:
                if default["modifier"] == "add":
                    await twitch.add_channel_vip(streamer.id, default["username"])
                elif default["modifier"] == "remove":
                    await twitch.remove_channel_vip(streamer.id, default["username"])
            except:
                await logError()

        ## cmd
        if action == "cmd":
            try:
                subprocess.run(default["command"], shell = False)
            except:
                await logError()

        ## playsound
        if action == "playsound":
            try:
                contains = False
                for type in [".mp3",".wav"]:
                    if os.path.exists(os.getcwd() + "\\data\\resources\\sounds\\" + arguments["sound"] + type):
                        playsound(os.getcwd() + "\\data\\resources\\sounds\\" + arguments["sound"] + type, block = False)
                        contains = True
                if not contains:
                    prompt ("misc", "Unable to find audio file: " + arguments["sound"])
            except:
                await logError()
        
        ## timeout
        if action == "timeout":
            try:
                async for u in twitch.get_users(logins = [default["username"]]):
                    await twitch.ban_user(streamer.id, streamer.id, u.id, default["reason"], int(default["time"]))
            except:
                await logError()
                
        ## conditional
        if action == "conditional":
            try:
                
                with open(os.getcwd() + "\\configuration\\conditional-actions.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    
                    if default["name"] in data["conditionals"]:
                        
                        outcome = False
                        condition = data["conditionals"][default["name"]]["condition"]
                        variable = data["conditionals"][default["name"]]["variable"]
                        
                        for tag in variables:
                            variable = variable.replace("%" + tag + "%", str(variables[tag]))
                  
                        value = data["conditionals"][default["name"]]["value"]
                        
                        datavalue = ""
                        options = { "Counter":"counter", "Variable":"text", "List":"list" }
                        
                        for option, tag in options.items():
                            if option in condition:
                                with open(os.getcwd() + "\\data\\variables\\" + tag + "\\" + variable + ".txt", 'r', encoding = "utf-8") as file:
                                    datavalue = file.read()
                        
                        result = None
                        
                        if condition == "Counter less than value":
                            value = int(value)
                            datavalue = int(datavalue)
                            result = (datavalue < value)

                        elif condition == "Counter less than or equals value":
                            value = int(value)
                            datavalue = int(datavalue)
                            result = (datavalue <= value)
                            
                        elif condition == "Counter equals value":
                            value = int(value)
                            datavalue = int(datavalue)
                            result = (datavalue == value)

                        elif condition == "Counter more than or equals value":
                            value = int(value)
                            datavalue = int(datavalue)
                            result = (datavalue >= value)

                        elif condition == "Counter more than value":
                            value = int(value)
                            datavalue = int(datavalue)
                            result = (datavalue > value)
                            
                        elif condition == "Variable equals value":
                            value = str(value)
                            result =(datavalue == value)
                        
                        elif condition == "Variable contains value":
                            value = str(value)
                            result = (value in datavalue)
                            
                        elif condition == "List contains value":
                            value = str(value)
                            datavalue = datavalue.splitlines()
                            result = (value in datavalue)
                        
                        if result is not None:
                            await runActions(data["conditionals"][default["name"]][result], variables)
                
            except:
                await logError()
              
        ## webhook
        if action == "webhook":
            try:
                with open(os.getcwd() + "\\configuration\\webhook\\" + default["name"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    
                    webhook = DiscordWebhook(url = data["url"], content = "\n".join(data["message"]), username = "Vayl", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png")
                    
                    info = await twitch.get_channel_information(streamer.id)
                    info = info[0]
                    directory = {"%game%":info.game_name, "%title%":info.title, "%name%":info.broadcaster_name, "%link%":"https://twitch.tv/" + TARGET_CHANNEL.lower()}
                    
                    description = "\n".join(data["embed"]["description"])
                    title = data["embed"]["title"]
                    image_url = data["embed"]["image-url"]
                    thumbnail_url = data["embed"]["thumbnail-url"]
                    
                    for d,r in directory.items():
                        title = title.replace(d,r)
                        description = description.replace(d, r)
    
                    embed = DiscordEmbed(title = "", description = "", color = "C14844")
                    embed.set_description(description = description)
                    embed.set_image(url = image_url)
                    embed.set_thumbnail(url = thumbnail_url)
                    embed.set_author(name=title, url="", icon_url="https://i.ibb.co/mHgBcY2/icon.png")
                
                    for k,v in data["embed"]["fields"].items():
                        for d,r in directory.items():
                            v["name"] = v["name"].replace(d,r)
                            v["value"] = v["value"].replace(d,r)
                        embed.add_embed_field (name = v["name"], value = v["value"])
                    
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    
                '''
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
                        # # print ("Game:  " + info.game_name)

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
                '''
            except:
                await logError()
              
        ## tts
        if action == "tts":
            try:
                
                global tts_voicepack
                if len(default["message"]) <= int(default["limit"]):

                    for voicepack in tts_voice.values():
                        if default["voice"] in voicepack:
                            
                            data = None
                                
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
                                
                            if data is not None:
                            
                                try:
                                    os.remove(os.getcwd() + "\\tts.wav")
                                except:
                                    pass
                            
                                with open(os.getcwd() + "\\tts.wav", "+wb") as file:
                                    file.write(data)
                                    
                                await asyncio.sleep(1)
                                
                                playsound(os.getcwd() + "\\" + filename, block = True if default["halt"] == "true" else False)
                                
                            
                            break
                    
                else:
                    await chat.send_message(TARGET_CHANNEL, "Unable to play TTS, message length exceeds limit of " + default["limit"] + " characters. (" + str(len(default["message"])) + ")")
                    prompt("misc", "Unable to play TTS, message length exceeds limit of " + default["limit"] + " characters. (" + str(len(default["message"])) + ")")

                
            except:
                await logError()
        
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
    
    # swa - 72913836
    
    found = False
    async for streams in twitch.get_streams(user_id = streamer.id):
        
        uptime = streams.started_at.replace(tzinfo=pytz.UTC) + timedelta(hours=1)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        
        t = now - uptime
        days, remainder = divmod(t.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, remainder = divmod(remainder, 60)
        
        '''
        seconds = followed.days * 24 * 3600 + followed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        '''
        
        found = True
        await chat.send_message(TARGET_CHANNEL, "Uptime: " + str(int(days)) + " Days, " + str(int(hours)) + " Hours, " + str(int(minutes)) + " Minutes, " + str(int(remainder)) + " Seconds.")

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
            
                basic_event = ["ad-break", "vayl-load", "stream-online", "stream-offline"]
                if arguments[0] in basic_event:
                    alert_queue.append ({"type":arguments[0]})

            if len(arguments) == 2:
            
                if "hypetrain" in arguments[0]:
                    if arguments[1].isnumeric():
                        alert_queue.append({"type":"hypetrain","level":int(arguments[1])})
            
            if len(arguments) >= 3:
            
                if "bits" in arguments[0]:
                    if arguments[1].isalnum() and arguments[2].isnumeric():
                        if len(arguments) > 3:
                            alert_queue.append({"type":"bits","user":arguments[1],"amount":int(arguments[2]),"message": " ".join(arguments[3:])})
                        else:
                            alert_queue.append({"type":"bits","user":arguments[1],"amount":int(arguments[2])})

            if len(arguments) >= 3:
            
                if "sub" == arguments[0]:
                    if arguments[1].isalnum() and arguments[2].isnumeric() and arguments[3].isnumeric():
                        tiers = ["1","2","3","prime"]
                        tier = arguments[2].lower() if arguments[2].lower() in tiers else "1"
                        message = " ".join(arguments[4:]) if len(arguments) > 4 else ""
                        alert_queue.append({"type":"sub","tier":tier,"user":arguments[1],"total-months":arguments[3],"sub-message":message})
            
            if len(arguments) == 4:
                if "giftsub" == arguments[0]:
                    if arguments[1].isalnum() and arguments[2].isalnum() and arguments[3].isnumeric():
                        for i in range (0, int(arguments[3])):
                            alert_queue.append({"type":"giftsub", "gifter":arguments[1], "tier":arguments[2], "gifted":"ExampleUsername"})

            if len(arguments) == 2:
                if "first-time-chat" == arguments[0]:
                    if arguments[1].isalnum():
                        alert_queue.append({"type":"first-time-chat", "user":arguments[1]})
                elif "first-session-chat" == arguments[0]:
                    if arguments[1].isalnum():
                        alert_queue.append({"type":"first-session-chat", "user":arguments[1]})
                elif "follow" == arguments[0]:
                    if arguments[1].isalnum():
                        alert_queue.append({"type":"follow", "user":arguments[1]})
           
            if len(arguments) >= 2:
                if "shoutout-give" == arguments[0] and len(arguments) == 3:
                    if arguments[1].isalnum() and arguments[2].isnumeric():
                        alert_queue.append({"type":"shoutout-created", "user":arguments[1], "viewercount":int(arguments[2])})
                if "shoutout-receive" == arguments[0] and len(arguments) == 3:
                    if arguments[1].isalnum() and arguments[2].isnumeric():
                        alert_queue.append({"type":"shoutout-receive", "user":arguments[1], "viewercount":int(arguments[2])})
                elif "raid" == arguments[0]:
                    if arguments[1].isalnum():
                        viewercount = int(arguments[2]) if len(arguments) > 2 and arguments[2].isnumeric() else 1
                        alert_queue.append({"type":"raid", "user":arguments[1], "viewercount":viewercount})
           
    except Exception as e:
        pass
        # print (e)
    
#####################################################################
    
    
## 8 Ball ###########################################################

'''
async def run8ball (cmd: ChatCommand):
    arguments = cmd.parameter.split(" ")
    if len(arguments) > 0 and cmd.parameter.endswith("?"):
        await chat.send_message(TARGET_CHANNEL, "(づ◡﹏◡)づ ◯")
        
        options = ["It is certain.","It is decidedly so.", "Without a doubt.", "You may rely on it.", "Most likely.", "Outlook is good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Best not to say.", "The spirits do not respond.", "Don't count on it", "The spirits say no.", "My sources say no", "Outlook is bleak", "Very doubtful"]
        for i in range(0, 5):
            random.shuffle(options)
            
        
        
        await chat.send_message(TARGET_CHANNEL, "(づ◡﹏◡)づ ◯ '" + random.choice(options) + "'")
'''

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
                
            # # print (f"[{Fore.GREEN}♦{Fore.WHITE}] SFX Configuration loaded. (" + str(len(data["sounds"].keys())) + ")")
            
            prompt ("success", "SFX Configuration loaded. (" + str(len(data["sounds"].keys())) + ")")
                
    except Exception as e:
        prompt ("error","Error loading SFX configuration.")
        # # print ("[!] Error loading SFX Configuration.")
        await logError()
    
        
    ############################################################

    
    ## Timed Actions ###########################################
    
    global timed_actions
    timed_actions = []
    
    try:
        with open(os.getcwd() + "\\configuration\\timed-actions.yml", "r", encoding = "utf-8") as file:
            data = yaml.full_load(file)
            for info in data["actions"].values():
                action = {}
                action["counter"] = 0
                action["frequency"] = info["frequency"]
                action["iterations"] = 0
                action["maxiterations"] = info["max-iterations"]
                action["actions"] = info["actions"]
                timed_actions.append(action)
            prompt ("success", "Timed Actions loaded. (" + str(len(data["actions"])) + ")")
    except:
        await logError()
    
    ############################################################


    ## Moderation ##############################################
    
    global moderation
    
    # Link
    try:
        with open(os.getcwd() + "\\configuration\\moderation\\links.yml", "r", encoding = "utf-8") as file:
            data = yaml.full_load(file)
            link_moderation = dict(data)
            link_moderation["warnings"] = {}
            moderation["link"] = link_moderation
    except:
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
    '''
    commands["pp"] = {}
    commands["pp"]["cooldown"] = 0
    commands["pp"]["user-cooldown"] = {}
    chat.register_command("pp", pp_command)
    '''
    
    chat.register_command("redeemon", redeemon)
    chat.register_command("redeemoff", redeemoff)
    
    # SFX
    chat.register_command("sfxon", sfxtoggle_command)
    chat.register_command("sfxoff", sfxtoggle_command)
    
    # 8Ball
    # chat.register_command ("8ball", run8ball)
    
    # Convert
    chat.register_command("convert", convert_command)
    
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

    alert = {}
    alert["type"] = "ad-break"
    
    global alert_queue
    alert_queue.insert(0, alert)

#####################################################################
  
   
## Shoutout Given ###################################################
async def on_shoutout_give(data: ChannelShoutoutCreateEvent):

    alert = {}
    alert["type"] = "shoutout-created"
    alert["user"] = data.event.to_broadcaster_user_name
    
    await updateVaylVariable("latest-shoutout-given", data.event.to_broadcaster_user_name)
        
    global alert_queue
    alert_queue.insert(0, alert)

#####################################################################  

## Shoutout Received#################################################
async def on_shoutout_receive(data: ChannelShoutoutReceiveEvent):

    alert = {}
    alert["type"] = "shoutout-receive"
    alert["user"] = data.event.from_broadcaster_user_name
    alert["viewers"] = str(data.event.viewer_count)
    
    await updateVaylVariable("latest-shoutout-received", data.event.from_broadcaster_user_name)
        
    global alert_queue
    alert_queue.appen(alert)
        
#####################################################################    
    
## Poll Created #####################################################
async def on_poll_create (data: ChannelPollBeginEvent):

    event = data.event.__dict__

    alert = {}
    alert["type"] = "poll-create"
    alert["title"] = data.event.title
    
    option_id = 1
    for choice in event["choices"]:
        alert["option" + str(option_id)] = choice.__dict__["title"]
        option_id += 1

    await updateVaylVariable("latest-poll", data.event.title)

    global alert_queue
    alert_queue.insert(0, alert)
    
#####################################################################    


## Poll Ended #######################################################
async def on_poll_ended (data: ChannelPollEndEvent):
    
    event = data.event.__dict__
    if event["status"] == "completed":
    
        alert = {}
        alert["type"] = "poll-end"
        alert["title"] = data.event.title
        
        option_id = 1
        for choice in event["choices"]:
            alert["option" + str(option_id)] = choice.__dict__["title"]
            alert["option" + str(option_id) + "bits"] = str(choice.__dict__["bits_votes"])
            alert["option" + str(option_id) + "points"] = str(choice.__dict__["channel_points_votes"])
            alert["option" + str(option_id) + "votes"] = str(choice.__dict__["votes"])
            option_id += 1

        global alert_queue
        alert_queue.insert(0, alert)
                        
#####################################################################    
    
    
## Prediction Start #################################################
async def on_prediction_start (data: ChannelPredictionEvent):

    alert = {}
    alert["type"] = "prediction-start"
    alert["title"] = data.event.title

    value = 1
    for option in data.event.outcomes:
        alert["option" + str(value)] = option.title
        value += 1
        
    await updateVaylVariable("latest-prediction", data.event.title)    

    global alert_queue
    alert_queue.insert(0, alert)
                
#####################################################################


## Prediction Start #################################################
async def on_prediction_lock (data: ChannelPredictionEvent):

    alert = {}
    alert["type"] = "prediction-locked"
    alert["title"] = data.event.title

    value = 1
    for option in data.event.outcomes:
        alert["option" + str(value)] = option.title
        alert["option" + str(value) + "points"] = option.channel_points
        value += 1

    global alert_queue
    alert_queue.insert(0, alert)
               
#####################################################################



## Prediction End ###################################################
async def on_prediction_end (data: ChannelPredictionEndEvent):

    alert = {}
    alert["type"] = "prediction-ended"
    alert["title"] = data.event.title

    value = 1
    for option in data.event.outcomes:
        alert["option" + str(value)] = option.title
        alert["option" + str(value) + "points"] = option.channel_points
        value += 1
        
        if option.id == data.event.winning_outcome_id:
            alert["winner"] = option.title
    
    await updateVaylVariable("latest-prediction-winner", alert["winner"])  

    global alert_queue
    alert_queue.insert(0, alert)
                
#####################################################################    



## Hype Train #######################################################
async def on_hype_train (data: HypeTrainEvent):

    contributors = data.event.top_contributions
    trainlevel = data.event.level
    
    alert = {}
    alert["type"] = "hypetrain"
    alert["level"] = trainlevel
    alert["conductor:bits"] = data.event.top_contributions[0].user_name
    alert["conductor:subs"] = data.event.top_contributions[1].user_name
    
    global alert_queue
    alert_queue.insert(0, alert)
            
#####################################################################


    
## Live Check #######################################################
async def on_offline (data: StreamOfflineEvent):
    global live
    live = False
    
    global alert_queue
    alert_queue.insert(0, {"type":"stream-offline"})

async def on_live(data: StreamOnlineEvent):
    global live
    live = True
    
    global alert_queue
    alert_queue.insert(0, {"type":"stream-online"})
#####################################################################    
    
## Follow ###########################################################
async def on_follow(data: ChannelFollowEvent):
    # our event happend, lets do things with the data we got!
    try:
        follower = data.event.user_name
        
        await updateVaylVariable("latest-follower", follower)  

        alert = {}
        alert["type"] = "follow"
        alert["user"] = follower
        alert_queue.append(alert)
        
        prompt ("follow", "Follow: " + alert["user"]) 
        
    except Exception as e:
        prompt ("error", "Error handling FollowEvent.")
        await logError()
#####################################################################
    
    
    
## Timed Actions ####################################################

timed_actions = []

def timedActions():
    asyncio.run(timedActionsAsync())
    
async def timedActionsAsync():
    while True:
    
        global timed_actions
        for action in timed_actions:
            action["counter"] += 1
            if action["counter"] >= action["frequency"]:
                if action["maxiterations"] == -1 or action["iterations"] < action["maxiterations"]:
                    await runActions(action["actions"], {})
                    action["iterations"] += 1
                action["counter"] = 0
                
        
        await asyncio.sleep(1)

#####################################################################    

 
    

## Alert Queue ######################################################

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
                
                
            ## GENERIC EVENT ###############################################################################
            generic_event = ["vayl-load", "ad-break", "prediction-create", "prediction-locked", "prediction-ended", "poll-created", "poll-ended", "first-time-chat", "stream-online", "stream-offline"]
            if alert["type"] in generic_event:
                with open(os.getcwd() + "\\configuration\\event\\" + alert["type"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        actions = data["actions"]
            ################################################################################################
            
            
            
            ## FIRST SESSION CHAT ##########################################################################
            
            elif "firstsessionchat" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\first-session-chat.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User sends first message of session":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
            
            ################################################################################################
            


            ## HYPE TRAIN ##################################################################################
            
            elif "hypetrain" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\hype-train.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific level
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "HypeTrain reaches level ...":
                                    if str(condition["value"]) == str(alert["level"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                           
                        ## at least level
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "HypeTrain reaches at least level ...":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["level"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
            
                        ## specific level
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "HypeTrain reaches level ...":
                                    if str(condition["value"]) == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
            
            ################################################################################################
            
          
            
            
            ## SHOUTOUT GIVEN ##############################################################################
    
            elif "shoutout-created" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\shoutout-created.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        ## priority
                        ## specific user
                        ## specific viewercount
                        ## at least viewercount
                        ## any
                        
                        complete = False

                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Given shoutout to user":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                       
                        ## specific viewercount
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains ... viewers":
                                    if str(condition["value"]).lower() == str(alert["viewercount"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                           
                        ## at least viewercount
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains at least ... viewers":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["viewercount"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                                    
                        ## any
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Given shoutout to user":
                                    if str(condition["value"]).lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
            
            ################################################################################################


   
            ## SHOUTOUT GIVEN ##############################################################################
    
            elif "shoutout-receive" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\shoutout-receieved.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        ## priority
                        ## specific user
                        ## specific viewercount
                        ## at least viewercount
                        ## any
                        
                        complete = False

                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Received shoutout from user":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                       
                        ## specific viewercount
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains ... viewers":
                                    if str(condition["value"]) == str(alert["viewercount"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                           
                        ## at least viewercount
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains at least ... viewers":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["viewercount"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                                    
                        ## any
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Received shoutout from user":
                                    if str(condition["value"]).lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
            
            ################################################################################################
   
            
   
            ## SUB #########################################################################################
            
            elif "sub" == alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\sub.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        ## priority
                        ## specific user
                        ## specific sub month streak
                        ## specific sub month total
                        ## any
                        
                        complete = False
                        
                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User subs":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                            
                        ## specific sub month streak
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... month sub streak":
                                    if str(condition["value"]) == str(alert["streak"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                            
                        ## at least sub month streak
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on at least ... month sub streak":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["streak"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                                    
                        ## any sub month streak
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... month sub streak":
                                    if str(condition["value"]) == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                    
                        ## specific sub month total
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... total sub months":
                                    if str(condition["value"]) == str(alert["total-months"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                        
                        ## at least sub month total
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on at least ... total sub months":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["total-months"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                                    
                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User subs":
                                    if condition["value"].lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
            
            ################################################################################################
            
            
                        
            ## GIFT SUB ####################################################################################
            
            elif "giftsub" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\gift-sub.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                        
                    if "enabled" in data and data["enabled"]:
                        
                        amount = 1
                        for a in alert_queue[1:]:
                            if a["type"] == "giftsub":
                                if a["gifter"] == alert["gifter"]:
                                    amount += 1
                        alert["amount"] = amount

                        complete = False
                        
                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts subs":
                                    if condition["value"].lower() == alert["gifter"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                        
                        ## specific sub amount
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts ... subs":
                                    if str(condition["value"]) == str(amount):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                        
                        ## more than sub amount
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts at least ... subs":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if amount >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                        
                        ## any user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts subs":
                                    if condition["value"].lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
                        
                        ## giftsub was tier x
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts tier ... sub":
                                    if str(condition["value"]) == str(alert["tier"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                            
                        ## any
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts subs":
                                    if condition["value"].lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
                        
                        new_alert_queue = []
                        for i in range(0, len(alert_queue)):
                            if alert_queue[i]["type"] == "giftsub":
                                if alert_queue[i]["gifter"] != alert["gifter"]:
                                    new_alert_queue.append(alert_queue[i])
                            else:
                                new_alert_queue.append(alert_queue[i])
                        alert_queue = new_alert_queue
                        await runActions(actions, alert)
                        
                        continue
            
            ################################################################################################
            

            
            ## BITS ########################################################################################
            
            elif "bits" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\bits.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        ## priority
                        ## specific user
                        ## specific bit amount
                        ## more than bit amount
                        ## any
                        
                        complete = False
                        
                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts bits":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                    
                        ## specific bit amount
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts ... bits":
                                    if str(condition["value"]) == str(alert["amount"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                    
                        ## more than bit amount
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts at least ... bits":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["amount"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                            
                        ## any
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts bits":
                                    if condition["value"].lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break

            ################################################################################################
            
    
            
            ## RAIDS #######################################################################################
            
            elif "raid" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\raid.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        ## priority
                        ## specific user
                        ## specific viewercount
                        ## more than viewercount
                        ## any
                        
                        complete = False
                        
                        
                        ## specific user
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User raids the channel":
                                    if condition["value"].lower() == alert["user"].lower():
                                        actions = condition["actions"]
                                        complete = True
                                        break
                                    
                        ## specific viewercount
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Raid contains ... viewers":
                                    if str(condition["value"]) == str(alert["viewercount"]):
                                        actions = condition["actions"]
                                        complete = True
                                        break
                    
                        ## more than viewercount
                        if not complete:
                            organise = {}
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Raid contains at least ... viewers":
                                    organise[conditional] = int(condition["value"])
                            organised = sorted(organise.items(), key=lambda x:x[1])
                            
                            if len (organised) > 0:
                                marker = None
                                for c in organised:
                                    if int(alert["viewercount"]) >= c[1]:
                                        marker = c
                                if marker is not None:
                                    actions = data["conditionals"][marker[0]]["actions"]
                                    complete = True
                            
                        ## any
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User raids the channel":
                                    if condition["value"].lower() == "any":
                                        actions = condition["actions"]
                                        complete = True
                                        break
             
            ################################################################################################
            
            else:
                pass
            
            await runActions(actions, alert)

            for i in range(0, pop_amount):
                alert_queue.pop(0)
            
        await asyncio.sleep(buffer)
    

    




async def callback_sub(d, data):
    # # print (data) - This is literally just their UUID
    try:
    
        
        alert = {}
        

        
        
        sub_tier = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}
        alert["tier"] = sub_tier[data["sub_plan"]]
        
        
        alert["sub-message"] = data["sub_message"]["message"]
        
        
        if data["is_gift"]:
        
            
        
            alert["type"] = "giftsub"
            alert["gifter"] = data["display_name"]
            alert["gifted"] = data["recipient_display_name"]
            
            await updateVaylVariable("latest-giftsub-gifter", data["display_name"])  
            await updateVaylVariable("latest-giftsub-gifted", data["recipient_display_name"])  
            
            prompt ("sub", "Gift Subscription: " + alert["gifter"] + " > " + alert["gifted"] + " [" + sub_tier[data["sub_plan"]] + "]") 
            # print ("    Message: " + alert["sub-message"]) 
            
        else:
            alert["type"] = "sub"
            alert["user"] = data["display_name"]
            alert["total-months"] = data["cumulative_months"]

            if "streak_months" in data:
                alert["streak"] = data["streak_months"]
            else:
                alert["streak"] = 1

            await updateVaylVariable("latest-subscriber", data["display_name"])  
            
            prompt ("sub", "Subscription: " + alert["user"] + " [" + sub_tier[data["sub_plan"]] + "]") 
            # print ("    Message: " + alert["sub-message"]) 
        
        
        
        
        global alert_queue
        alert_queue.append(alert)
    
    except Exception as e:
        prompt ("error", "Error handling SubscriptionEvent.")
        await logError()
    

async def callback_whisper(data, data2):
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
        # print ("    Message: " + alert["message"])
        
        await updateVaylVariable("latest-bits-donator", data["data"]["user_name"])  
        await updateVaylVariable("latest-bits-amount", data["data"]["bits_used"])

    except Exception as e:
        prompt ("error", "Error handling BitEvent.")
        await logError()





# this is where we set up the bot
async def run():

    # access = y9blozsq7qm2v8d2qw9i9sktyoc8nj
    # refresh = qqwfvwzcifss9e9hl8ewcdb10t8hpn0iuw4710kn3ggigquexi

    # set up twitch api instance and add user authentication with some scopes
    
    # print_spacing = 28 * " "
    
    await sendToConsole("Loading Authentication")
    
    # # print (# print_spacing + "Loading Authentication              ....", end = "\r")
    
    global twitch    
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify = False)
    token, refresh = await auth.authenticate()
    
    await twitch.set_user_authentication(token, USER_SCOPE, refresh)
    
    
    
    # # print (# print_spacing + "Loading Authentication              DONE", end = "\n")
    
    # await twitch.set_user_authentication("a8g7wnqh495gckgmoo4mwgcuggjjx9", USER_SCOPE, "2fag6conscq5y260jo14rkar8plo8bw462oemqqpb5xaqojorm")
    
    await sendToConsole("Fetching Twitch User")
    
    # # print (# print_spacing + " Grabbing Twitch User               ....", end = "\r")

    global streamer
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
    streamer = user
    
    await sendToConsole("Registering EventSub")
    
    # # print (# print_spacing + " Grabbing Twitch User               DONE", end = "\n")
    # # print (# print_spacing + " Registering EventSub               ....", end = "\r")
    
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    
    await eventsub.listen_channel_follow_v2(streamer.id, streamer.id, on_follow)
    await eventsub.listen_stream_online(streamer.id, on_live)
    await eventsub.listen_stream_offline(streamer.id, on_offline)
    await eventsub.listen_channel_ad_break_begin(streamer.id, on_ad)
    await eventsub.listen_channel_poll_begin(streamer.id, on_poll_create)
    await eventsub.listen_channel_poll_end(streamer.id, on_poll_ended)
    await eventsub.listen_channel_prediction_begin(streamer.id, on_prediction_start)    
    await eventsub.listen_channel_prediction_lock(streamer.id, on_prediction_lock)   
    await eventsub.listen_channel_prediction_end(streamer.id, on_prediction_end)   
    await eventsub.listen_hype_train_begin(streamer.id, on_hype_train)   
    
    await eventsub.listen_channel_shoutout_create(streamer.id, streamer.id, on_shoutout_give)
    await eventsub.listen_channel_shoutout_receive(streamer.id, streamer.id, on_shoutout_receive)

    await sendToConsole("Registering PubSub")

    # # print (# print_spacing + " Registering EventSub               DONE", end = "\n")
    # # print (# print_spacing + "  Registering PubSub                ....", end = "\r")
    

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
    
    await sendToConsole("Connecting to Chat")
    
    # # print (# print_spacing + "  Registering PubSub                DONE", end = "\n")
    # # print (# print_spacing + "    Establish Chat                  ....", end = "\r")
    

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
    
    # # print (# print_spacing + "    Establish Chat                  DONE", end = "\n")
    ###################################################
    

    thread2 = threading.Thread(target= manageAlerts)
    thread2.start()
    
    threadactions = threading.Thread(target = timedActions)
    threadactions.start()
    
    
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
    
    await updateVaylVariable("latest-follower", newest_follower)
    await updateVaylVariable("oldest-follower", oldest_follower)

    ###########################################################
    
    
    global alert_queue
    alert = {}
    alert["type"] = "vayl-load"
    alert_queue.insert(0, alert)
    
   
    
    input('')
    
 
    
 
    
# os.startfile("vaylui.py")

# print (" ")                                             
# print ("                                             :@@@@@@@:      ")
# print ("                                           @@@@@@@@@@@@@    ")
# print ("                                         :@@@%+%@@@#*%@@@:  ")
# print (f"                                         @@@@@-:@@@{Fore.LIGHTRED_EX}#{Fore.WHITE}-@@@@@  ")
# print (f"                                        :@@@@@@::@{Fore.LIGHTRED_EX}##{Fore.WHITE}@@@@@@: ")
# print ("                                         @@@@@@@:::@@@@@@@  ")
# print ("                                         :@@@@@@@:@@@@@@@:  ")
# print ("                                           @@@@@@@@@@@@@    ")
# print ("                                             :@@@@@@@:      ")                                          
# print (" ")
## print ("                                              LOADING", end = "\r")
## print ("                                              LOADING")
  


asyncio.run(clearConsole())
asyncio.run(versionCheck())
asyncio.run(run())

