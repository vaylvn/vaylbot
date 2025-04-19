__version__ = "beta0042"

## Imports =========================================================================
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from discord_webhook import DiscordWebhook, DiscordEmbed
from twitchAPI.object.eventsub import ChannelFollowEvent, StreamOnlineEvent, StreamOfflineEvent, ChannelPollBeginEvent, ChannelPollEndEvent, ChannelPredictionEvent, ChannelPredictionEndEvent, HypeTrainEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, ChannelAdBreakBeginEvent, ChannelSubscribeEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelCheerEvent, ChannelPointsCustomRewardRedemptionAddEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from datetime import datetime, timedelta, date
from twitchAPI.pubsub import PubSub
from collections import OrderedDict
from twitchAPI.helper import first
from playsound3 import playsound
from colorama import Fore, Back, Style, init
from num2words import num2words
from collections import deque

from textwrap import wrap
import tldextract
import subprocess
import traceback
import threading
import requests
import requests
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
## =================================================================================


## TTS =============================================================================
tts_voicepack = {"cepstral":cepstral, "ibmwatson":ibm_watson, "oddcast":oddcast, "streamelements":stream_elements, "streamlabs":streamlabs, "voiceforge":voice_forge }
tts_voice = { "cepstral"        : ["Allison", "Amy", "Belle", "Callie", "Charlie", "Dallas", "Damien", "David", "Diane", "Duchess", "Emily", "Linda", "Robin", "Shouty", "Walter", "William", "Whispery", "Lawrence", "Millie", "Duncan", "Vittoria", "Katrin", "Matthias", "Isabelle", "Jean-Pierre", "Alejandra", "Miguel"],
              "imbwatson"       : ["en-GB_CharlotteV3Voice", "en-GB_JamesV3Voice", "en-GB_KateV3Voice", "en-AU_JackExpressive", "en-AU_HeidiExpressive", "en-US_AllisonV3Voice", "en-US_AllisonExpressive", "en-US_EmilyV3Voice", "en-US_EmmaExpressive", "en-US_HenryV3Voice", "en-US_KevinV3Voice", "en-US_LisaV3Voice", "en-US_LisaExpressive", "en-US_MichaelV3Voice", "en-US_MichaelExpressive", "en-US_OliviaV3Voice", "nl-NL_MerelV3Voice", "fr-FR_NicolasV3Voice", "fr-FR_ReneeV3Voice", "fr-CA_LouiseV3Voice", "de-DE_BirgitV3Voice", "de-DE_DieterV3Voice", "de-DE_ErikaV3Voice", "it-IT_FrancescaV3Voice", "ja-JP_EmiV3Voice", "ko-KR_JinV3Voice", "pt-BR_IsabelaV3Voice", "es-ES_EnriqueV3Voice", "es-ES_LauraV3Voice", "es-LA_SofiaV3Voice", "es-US_SofiaV3Voice"],
              "oddcast"         : ["4-3-1", "6-2-1", "5-4-1", "4-2-1", "5-3-1", "2-7-1", "1-7-1", "7-4-1", "5-2-1", "12-4-1", "8-4-1", "9-2-1", "10-2-1", "4-7-1", "4-4-1", "10-4-1", "3-7-1", "13-4-1", "5-7-1", "6-7-1", "9-4-1", "11-2-1", "7-2-1", "6-3-1", "8-3-1", "7-7-1", "3-1-1", "1-1-1", "2-2-1", "7-3-1", "2-4-1", "3-3-1", "1-3-1", "2-1-1", "2-3-1", "4-1-1", "11-4-1", "8-2-1", "1-2-1", "3-4-1", "8-7-1", "1-7-27", "2-7-27", "2-2-27", "1-4-27", "1-2-27", "1-4-22", "3-2-5", "2-2-5", "1-2-5", "1-4-5", "3-3-10", "5-3-10", "4-3-10", "1-2-10", "2-2-10", "4-4-10", "4-7-10", "6-3-10", "7-3-10", "1-4-10", "3-7-10", "2-7-10", "1-7-10", "2-4-10", "8-3-10", "1-7-18", "1-4-18", "1-7-19", "2-7-19", "1-2-19", "1-4-19", "2-2-19", "2-4-11", "2-7-11", "1-7-11", "2-2-11", "1-2-11", "4-4-11", "1-4-11", "1-2-31", "2-7-32", "1-7-32", "2-2-23", "1-4-23", "1-2-23", "1-7-23", "2-1-4", "2-7-4", "1-7-4", "2-2-4", "4-2-4", "3-2-4", "1-1-4", "4-3-4", "3-3-4", "3-4-4", "5-4-4", "4-4-4", "5-2-4", "1-3-4", "1-4-4", "4-7-4", "2-4-4", "2-3-4", "3-7-4", "6-2-4", "3-1-4", "1-2-15", "3-4-3", "2-7-3", "1-7-3", "3-2-3", "1-1-3", "1-3-3", "2-1-3", "2-2-3", "1-4-3", "2-3-3", "2-4-3", "1-2-8", "1-4-8", "1-7-8", "2-7-8", "3-2-8", "2-7-24", "1-4-24", "1-7-24", "1-4-29", "1-7-29", "2-7-28", "1-4-28", "1-7-28", "2-7-7", "1-7-7", "1-3-7", "10-2-7", "9-2-7", "5-2-7", "6-2-7", "8-2-7", "1-2-7", "1-4-7", "7-2-7", "2-3-7", "2-2-7", "2-4-7", "3-2-7", "6-3-12", "5-3-12", "1-7-12", "2-7-12", "1-4-12", "3-3-12", "7-3-12", "4-3-12", "2-3-12", "8-3-12", "7-3-13", "4-3-13", "8-3-13", "10-3-13", "5-3-13", "2-3-13", "1-4-13", "6-3-13", "1-3-13", "9-3-13", "1-7-20", "2-2-20", "2-7-20", "2-4-20", "1-2-20", "1-4-14", "1-7-14", "2-2-14", "2-7-14", "1-2-14", "2-7-6", "3-4-6", "3-7-6", "4-7-6", "1-7-6", "1-3-6", "2-3-6", "2-4-6", "1-2-30", "1-4-30", "2-2-21", "2-4-21", "1-2-21", "1-7-37", "3-4-37", "1-2-2", "6-2-2", "2-2-2", "9-2-2", "4-3-2", "5-3-2", "1-4-2", "3-4-2", "7-2-2", "8-2-2", "10-2-2", "4-2-2", "3-2-2", "2-1-2", "5-2-2", "2-3-2", "3-3-2", "5-4-2", "4-4-2", "1-1-2", "1-3-2", "1-4-9", "1-2-9", "1-7-9", "2-7-9", "3-4-9", "2-2-9", "1-4-26", "1-3-26", "2-3-26", "1-4-16", "2-7-16", "1-2-16", "3-2-16", "1-7-16", "2-2-16", "1-7-40"],
              "streamelements"  : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Mia", "Miguel", "Penelope", "Astrid", "Filiz", "Gwyneth", "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E", "en-US-Wavenet-F", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D", "en-AU-Standard-C", "en-AU-Standard-D", "en-IN-Wavenet-A", "en-IN-Wavenet-B", "en-IN-Wavenet-C", "af-ZA-Standard-A", "ar-XA-Wavenet-A", "ar-XA-Wavenet-B", "ar-XA-Wavenet-C", "bg-bg-Standard-A", "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-B", "cmn-CN-Wavenet-C", "cmn-CN-Wavenet-D", "cs-CZ-Wavenet-A", "da-DK-Wavenet-A", "nl-NL-Standard-A", "nl-NL-Wavenet-A", "nl-NL-Wavenet-B", "nl-NL-Wavenet-C", "nl-NL-Wavenet-D", "nl-NL-Wavenet-E", "fil-PH-Wavenet-A", "fi-FI-Wavenet-A", "fr-FR-Standard-C", "fr-FR-Standard-D", "fr-FR-Wavenet-A", "fr-FR-Wavenet-B", "fr-FR-Wavenet-C", "fr-FR-Wavenet-D", "fr-CA-Standard-A", "fr-CA-Standard-B", "fr-CA-Standard-C", "fr-CA-Standard-D", "de-DE-Standard-A", "de-DE-Standard-B", "de-DE-Wavenet-A", "de-DE-Wavenet-B", "de-DE-Wavenet-C", "de-DE-Wavenet-D", "el-GR-Wavenet-A", "hi-IN-Wavenet-A", "hi-IN-Wavenet-B", "hi-IN-Wavenet-C", "hu-HU-Wavenet-A", "is-is-Standard-A", "id-ID-Wavenet-A", "id-ID-Wavenet-B", "id-ID-Wavenet-C", "it-IT-Standard-A", "it-IT-Wavenet-A", "it-IT-Wavenet-B", "it-IT-Wavenet-C", "it-IT-Wavenet-D", "ja-JP-Standard-A", "ja-JP-Wavenet-A", "ja-JP-Wavenet-B", "ja-JP-Wavenet-C", "ja-JP-Wavenet-D", "ko-KR-Standard-A", "ko-KR-Wavenet-A", "lv-lv-Standard-A", "nb-no-Wavenet-E", "nb-no-Wavenet-A", "nb-no-Wavenet-B", "nb-no-Wavenet-C", "nb-no-Wavenet-D", "pl-PL-Wavenet-A", "pl-PL-Wavenet-B", "pl-PL-Wavenet-C", "pl-PL-Wavenet-D", "pt-PT-Wavenet-A", "pt-PT-Wavenet-B", "pt-PT-Wavenet-C", "pt-PT-Wavenet-D", "pt-BR-Standard-A", "ru-RU-Wavenet-A", "ru-RU-Wavenet-B", "ru-RU-Wavenet-C", "ru-RU-Wavenet-D", "sr-rs-Standard-A", "sk-SK-Wavenet-A", "es-ES-Standard-A", "sv-SE-Standard-A", "tr-TR-Standard-A", "tr-TR-Wavenet-A", "tr-TR-Wavenet-B", "tr-TR-Wavenet-C", "tr-TR-Wavenet-D", "tr-TR-Wavenet-E", "uk-UA-Wavenet-A", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "Linda", "Heather", "Sean", "Hoda", "Naayf", "Ivan", "Herena", "Tracy", "Danny", "Huihui", "Yaoyao", "Kangkang", "HanHan", "Zhiwei", "Matej", "Jakub", "Guillaume", "Michael", "Karsten", "Stefanos", "Szabolcs", "Andika", "Heidi", "Kalpana", "Hemant", "Rizwan", "Filip", "Lado", "Valluvar", "Pattara", "An"],
              "streamlabs"      : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zeina", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Lea", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Camila", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Lucia", "Mia", "Miguel", "Lupe", "Penelope", "Astrid", "Filiz", "Gwyneth"],
              "voiceforge"      : ["Conrad", "Designer", "Diesel", "Dog", "Evilgenius", "Frank", "French-fry", "Gregory", "Jerkface", "JerseyGirl", "Kayla", "Kevin", "Kidaroo", "Princess", "RansomNote", "Robot", "Shygirl", "Susan", "Tamika", "TopHat", "Vixen", "Vlad", "Warren", "Wiseguy", "Zach", "Obama"]}
## =================================================================================

## Directory =======================================================================
vdir = {"home" : os.getcwd()}
vdir["data"] = os.path.join(vdir["home"], "data")
for path in ["logs","resources","variables"]:
    vdir[path] = os.path.join(vdir["data"], path)
for path in ["sounds"]:
    vdir[path] = os.path.join(vdir["resources"], path)
for path in ["boolean","counter","list","text","vayl"]:
    vdir[path] = os.path.join(vdir["variables"], path)
vdir["configuration"] = os.path.join(vdir["home"], "configuration")
for path in ["conditionals","event","webhook"]:
    vdir[path] = os.path.join(vdir["configuration"], path)
## =================================================================================

## Bot Variables ===================================================================
sv = { "id" : "xfc4596ekgo4ewkag6wn01hgs4hfbl", "secret" : "p8wl2zzuk3sgjmbdrlxe9l65xno8wk",
       "version" : "", "twitch" : None, "streamer" : None, "channel" : None, "chat" : None, "live" : False,
       "alerts" : deque(), "actions" : [], "commands" : {}, "sfx" : {}, "phrases" : {}, "spoken" : [] }
## =================================================================================


## UserScope =======================================================================
USER_SCOPE = [AuthScope.USER_READ_SUBSCRIPTIONS, AuthScope.MODERATION_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, 
              AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS, AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
              AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.MODERATOR_READ_FOLLOWERS, 
              AuthScope.WHISPERS_READ, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_POLLS, AuthScope.CHANNEL_MANAGE_POLLS, AuthScope.CHANNEL_READ_ADS,
              AuthScope.MODERATOR_MANAGE_SHOUTOUTS, AuthScope.MODERATOR_READ_SHOUTOUTS, AuthScope.CHANNEL_READ_PREDICTIONS, AuthScope.CHANNEL_MANAGE_PREDICTIONS,
              AuthScope.CHANNEL_READ_HYPE_TRAIN, AuthScope.CHANNEL_MANAGE_VIPS, AuthScope.CHANNEL_MANAGE_BROADCAST, AuthScope.ANALYTICS_READ_GAMES, AuthScope.MODERATOR_MANAGE_BANNED_USERS,
              AuthScope.MODERATOR_READ_CHATTERS]
## =================================================================================


## =================================================================================
## =================================================================================
###################################### EVENTS ######################################
## =================================================================================
## =================================================================================


## OnReady =========================================================================
async def on_ready (ready_event: EventData):
    try:
        await ready_event.chat.join_room(sv["channel"])
        prompt ("success", "Welcome to Vayl")
        await reload(False)
    except Exception as e:
        logError(tag = "event.on_ready")
## =================================================================================


## OnMessage =======================================================================
async def on_message (msg: ChatMessage):
    try:
        global sv
        name = msg.user.name
        
        ## phrase check ================================================================
        try:
            with open(os.path.join(vdir["configuration"], "phrases.yml"), 'r', encoding = "utf-8") as file:
                data = yaml.safe_load(file)
                for phrase, info in data["phrase"].items():
                    if (info["type"] == "contains" and phrase.lower() in msg.text.lower()) or (info["type"] == "matches" and phrase.lower() == msg.text.lower()):
                        cooldown = sv["phrases"]["cooldown"][phrase.lower()] if phrase.lower() in sv["phrases"]["cooldown"] else 0
                        if time.time() - cooldown >= info["cooldown"]:
                            await runActions(info["actions"], {"user":msg.user.name})
                            sv["phrases"]["cooldown"][phrase.lower()] = time.time()
        except Exception as e:
            logError(tag = "chat.phrasecheck")
        ## =============================================================================
            
        
        ## chat event ==================================================================
        if not msg.text.startswith("!"):
            await addAlert({"type":"chat", "user":name, "message":msg.text}, "0")
        ## =============================================================================
        
        
        ## quotes ======================================================================
        if "!addquote" in msg.text:
            try:
                if msg.reply_parent_msg_body:

                    quote_message = " ".join(msg.reply_parent_msg_body.split("\s"))
                    quote_author = msg.reply_thread_parent_user_login
                    
                    line = '"' + quote_message + '" - ' + quote_author + ", " + datetime.now().strftime("%m/%y")
                    total = 0
                    with open(os.getcwd() + "\\data\\resources\\quotes.yml", 'a+', encoding="utf-8") as file:
                        file.seek(0)
                        total = len(file.readlines())
                        file.seek(0, os.SEEK_END)
                        file.write("\n" + line)
                    await sv["chat"].send_message(sv["channel"], "Quote #" + str(total) + " Added: " + line)
                else:
                    await sv["chat"].send_message(sv["channel"], "!addquote must be used as a reply.")
            except Exception as e:
                logError(tag = "chat.addquote")
        ## =============================================================================
        
        
        ## live check ==================================================================
        if sv["live"] == False:
            async for streams in sv["twitch"].get_streams(user_id = [sv["streamer"].id]):
                sv["live"] = True
        
        if sv["live"] == True:
        
            ## first time chat =============================================================
            if "first-msg" in msg.__dict__["_parsed"]["tags"] and msg.__dict__["_parsed"]["tags"]["first-msg"] == "1":
                await addAlert({"type":"first-time-chat", "user":name, "message":msg.text},"0")
                sv["spoken"].append(name)
            else:
                if name not in sv["spoken"]:
                    sv["spoken"].append(name)
                    await addAlert({"type":"first-session-chat", "user":msg.user.display_name, "message":msg.text},"0")
            ## =============================================================================
            
            ## first session chat ==========================================================
            
            ## =============================================================================
            
            
            
        ## =============================================================================
    except Exception as e:
        logError(tag = "event.on_message")

## =================================================================================


## OnRaid ==========================================================================
async def on_raid (raid: dict):
    try:
        await updateVariable("latest-raid-raider", raid["tags"]["display-name"])
        await updateVariable("latest-raid-amount", raid["tags"]["msg-param-viewerCount"])
        await addAlert({"type":"raid","user":raid["tags"]["display-name"],"viewers":raid["tags"]["msg-param-viewerCount"]}, "0")
    except Exception as e:
        logError(tag = "event.on_raid")
## =================================================================================


## OnAD ============================================================================
async def on_ad (data: ChannelAdBreakBeginEvent):
    try:
        await addAlert({"type":"ad-break"}, "0")
    except Exception as e:
        logError(tag = "event.on_ad")
## =================================================================================


## OnShoutoutGive ==================================================================
async def on_shoutout_give (data: ChannelShoutoutCreateEvent):
    try:
        await updateVariable("latest-shoutout-given", data.event.to_broadcaster_user_name)
        await addAlert({"type":"shoutout-given", "user":data.event.to_broadcaster_user_name, "viewers":data.event.viewer_count}, "0")
    except Exception as e:
        logError(tag = "event.on_shoutout_give")
## =================================================================================


## OnShoutoutReceive ===============================================================
async def on_shoutout_receive (data: ChannelShoutoutReceiveEvent):
    try:
        await updateVariable("latest-shoutout-received", data.event.from_broadcaster_user_name)
        await addAlert({"type":"shoutout-received", "user":data.event.from_broadcaster_user_name, "viewers":data.event.viewer_count}, "0")
    except Exception as e:
        logError(tag = "event.on_shoutout_receieve")
## =================================================================================


## OnPollStart =====================================================================
async def on_poll_start (data: ChannelPollBeginEvent):
    try:
        await updateVariable("latest-poll", data.event.title)
        alert = {"type":"poll-create", "title":data.event.title}
        id = 1
        for choice in data.event.__dict__["choices"]:
            alert["option" + str(id)] = choice.__dict__["title"]
            id += 1
        await addAlert(alert, "0")    
    except Exception as e:
        logError(tag = "event.on_poll_start")
## =================================================================================


## OnPollEnd =======================================================================
async def on_poll_end (data: ChannelPollEndEvent):
    try:
        event = data.event.__dict__
        if event["status"] == "completed":
            alert = {"type":"poll-end", "title":data.event.title}
            id = 1
            for choice in event["choices"]:
                alert["option" + str(id)] = choice.__dict__["title"]
                alert["option" + str(id) + "bits"] = str(choice.__dict__["bits_votes"])
                alert["option" + str(id) + "points"] = str(choice.__dict__["channel_points_votes"])
                alert["option" + str(id) + "votes"] = str(choice.__dict__["votes"])
                id += 1
            await addAlert(alert, "0")   
    except Exception as e:
        logError(tag = "event.on_poll_end")
## =================================================================================


## OnPredictionStart ===============================================================
async def on_prediction_start (data: ChannelPredictionEvent):
    try:
        await updateVariable("latest-prediction", data.event.title)
        alert = {"type":"prediction-created", "title":data.event.title}
        id = 1
        for option in data.event.outcomes:
            alert["option" + str(id)] = option.title
            id += 1
        await addAlert(alert, "0")   
    except Exception as e:
        logError(tag = "event.on_prediction_start")
## =================================================================================


## OnPredictionLock ================================================================
async def on_prediction_lock (data: ChannelPredictionEvent):
    try:
        alert = {"type":"prediction-locked", "title":data.event.title}
        id = 1
        for option in data.event.outcomes:
            alert["option" + str(id)] = option.title
            alert["option" + str(id) + "points"] = option.channel_points
            id += 1
        await addAlert(alert, "0")   
    except Exception as e:
        logError(tag = "event.on_prediction_lock")
## =================================================================================


## OnPredictionEnd =================================================================
async def on_prediction_end (data: ChannelPredictionEndEvent):
    try:
        alert = {"type":"prediction-ended", "title":data.event.title}
        id = 1
        for option in data.event.outcomes:
            alert["option" + str(id)] = option.title
            alert["option" + str(id) + "points"] = option.channel_points
            id += 1
            if option.id == data.event.winning_option_id:
                alert["winner"] = option.title
        await updateVariable("latest-prediction-winner", alert["winner"])
        await addAlert(alert, "0")   
    except Exception as e:
        logError(tag = "event.on_prediction_end")
## =================================================================================


## OnHypeTrain =====================================================================
async def on_hype_train (data: HypeTrainEvent):
    try:
        await addAlert({"type":"hypetrain", "level":data.event.level}, "0")
    except Exception as e:
        logError(tag = "event.on_hype_train")
## =================================================================================


## OnOffline =======================================================================
async def on_offline (data: StreamOfflineEvent):
    try:
        global sv
        sv["live"] = False
        await addAlert({"type":"stream-offline"}, "0")
    except Exception as e:
        logError(tag = "event.on_offline")
## =================================================================================


## OnOnline ========================================================================
async def on_live (data: StreamOnlineEvent):
    try:
        global sv
        sv["live"] = True
        await addAlert({"type":"stream-online"}, "0")
    except Exception as e:
        logError(tag = "event.on_online")
## =================================================================================


## OnFollow ========================================================================
async def on_follow (data: ChannelFollowEvent):
    try:
        await updateVariable("latest-follower", data.event.user_name)
        await addAlert({"type":"follow", "user":data.event.user_name}, "end")
    except Exception as e:
        logError(tag = "event.on_follow")
## =================================================================================

async def on_sub (data: ChannelSubscribeEvent):
    try:
        event = data.event.to_dict()
        event["type"] = "sub"
        event["tier"] = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]
        await addAlert(event, "end")
    except Exception as e:
        pass

async def on_giftsub (data: ChannelSubscriptionGiftEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event["type"] = "giftsub"
        event["tier"] = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]
        await addAlert(event, "end")
    except Exception as e:
        pass

async def on_resub (data: ChannelSubscriptionMessageEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event["type"] = "resub"
        event["message"] = event["message"]["text"]
        event["tier"] = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]
        await addAlert(event, "end")
    except Exception as e:
        pass



'''
## OnSub ===========================================================================
async def on_sub_new (data: ChannelSubscribeEvent):
    try:
        alert = event.data.to_dict(include_none_values = False)
        alert["type"] = "sub"
        alert["tier"] = {"1000":"1", "2000":"2", "3000":"3"}[data.event.tier]
        await addAlert(alert, "end")
    except Exception as e:
        logError(tag = "event.on_sub")


async def on_giftsub (data: ChannelSubscriptionGiftEvent):
    try:
        alert = event.data.to_dict(include_none_values = False)
        alert["type"] = "giftsub"
        await addAlert(alert, "end")
    except:
        logError(tag = "event.on_giftsub")
        
async def on_resub (data: ChannelSubscriptionMessageEvent):
    try:
        alert = event.data.to_dict(include_none_values = False)
        alert["type"] = "resub"
        alert["message"] = event.data.to_dict(include_none_values = False)["message"]["text"]
        alert["tier"] = {"1000":"1", "2000":"2", "3000":"3"}[data.event.tier]
    except:
        logError(tag = "event.on_resub")




async def on_sub (d, data):
    try:
        alert = {}
        alert["tier"] = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}[data["sub_plan"]]
        alert["type"] = "giftsub" if data["is_gift"] else "sub"
        alert["user"] = data["display_name"]
        alert["gifted"] = data["recipient_display_name"] if data["is_gift"] else ""
        alert["sub-message"] = "" if data["is_gift"] else data["sub_message"]["message"]
        alert["total-months"] = "" if data["is_gift"] else data["cumulative_months"]
        
        if data["is_gift"]:
            await updateVariable("latest-giftsub-gifter", data["display_name"])  
            await updateVariable("latest-giftsub-gifted", data["recipient_display_name"])  
        else:
            await updateVariable("latest-subscriber", data["display_name"])  
            alert["streak"] = data["streak_months"] if "streak_months" in data else 1
        
        await addAlert(alert, "end")
    except Exception as e:
        logError(tag = "event.on_sub")
'''

## =================================================================================


## OnWhisper =======================================================================
# async def on_whisper (data: UserWhisperMessageEvent):
#     pass
## =================================================================================


## OnBit ===========================================================================
async def on_bits (d, data):
    try:
        await updateVariable("latest-bits-donator", data["data"]["user_name"])
        await updateVariable("latest-bits-amount", data["data"]["bits_used"])
        message = data["data"]["chat_message"]
        for word in message.split(" "):
            if "Cheer" in word and len(word) > 5:
                message = message.replace(word,"")
        await addAlert({"type":"bits", "user":data["data"]["user_name"], "amount":data["data"]["bits_used"], "message":message}, "end")
    except Exception as e:
        logError(tag = "event.on_bits")
        
        
async def on_bits_new (data: ChannelCheerEvent):
    try:
        alert = event.data.to_dict(include_none_values = False)
        alert["type"] = "bits"
    except Exception as e:
        logError(tag = "event.on_bits")
## =================================================================================


## OnRedeem ========================================================================
async def on_redeem (d, data):
    try:
        redeem = data["data"]["redemption"]
        alert = {"type":"redeem", "userid":redeem["user"]["id"], "user":redeem["user"]["display_name"], "userinput":"", "cost":redeem["reward"]["cost"]}
        if "user_input" in redeem:
            alert["user_input"] = redeem["user_input"]
            
        with open(os.path.join(vdir["configuration"], "redeems.yml"), 'r', encoding = "utf-8") as file:
            redeem_data = yaml.safe_load(file)
            for redeems in redeem_data["redeem"].keys():
                if redeems.lower() in redeem["reward"]["title"].lower():
                    alert["buffer"] = redeem_data["redeem"][redeems]["buffer"]
                    alert["actions"] = redeem_data["redeem"][redeems]["actions"]
                    await addAlert(alert, "0" if redeem_data["redeem"][redeems]["queue"] else "end")
        
        await updateVariable("latest-redeem-user", redeem["user"]["display_name"])
        await updateVariable("latest-redeem-name", redeem["reward"]["title"])
    except Exception as e:
        logError(tag = "event.on_redeem")
        
async def on_redeem_new (data: ChannelPointsCustomRewardRedemptionAddEvent):
    try:
        
        event = data.event
        alert = event.to_dict(include_none_values = False)
        alert["type"] = "redeem"
        alert["redeem"] = alert["reward"]["title"]
        alert["cost"] = str(alert["reward"]["cost"])
        alert["description"] = alert["reward"]["prompt"]
        alert["user"] = alert["user_name"]
        
        # print (alert)
        # print (alert)
        
        with open(os.path.join(vdir["configuration"], "redeems.yml"), 'r', encoding = "utf-8") as file:
            redeem_data = yaml.safe_load(file)
            for r, rd in redeem_data["redeem"].items():
                if r.lower() in alert["redeem"].lower():
                    alert["buffer"] = rd["buffer"]
                    alert["actions"] = rd["actions"]
                    await addAlert(alert, "0" if rd["queue"] else "end")
                    break
    
    except:
        logError(tag = "event.on_redeem")
## =================================================================================


## =================================================================================
## =================================================================================
#################################### COMMANDS ######################################
## =================================================================================
## =================================================================================


## Reload ==========================================================================
async def c_reload (cmd: ChatCommand):
    try:
        if await isStreamer(cmd.user.name):
            await reload(True)
    except Exception as e:
        logError(tag = "command.reload")
## =================================================================================


## Debug ===========================================================================
debug_commands = {
    "sub":                { "defaults":  { "user":"valon", "tier":"1", "months":"12", "message":"" },
                            "potential": ["user", "tier", "months", "message"] },
    "giftsub":            { "defaults":  { "user":"valon", "tier":"1", "gifts":"5"},
                            "potential": ["user", "tier", "gifts"] },
    "hypetrain":          { "defaults":  { "level":"1"},
                            "potential": ["level"] },
    "first-time-chat":    { "defaults":  { "user":"AwesomeUser" },
                            "potential": ["user"] },
    "first-session-chat": { "defaults":  { "user":"AwesomeUser" },
                            "potential": ["user"] },
    "follow":             { "defaults":  { "user":"AwesomeUser" },
                            "potential": ["user"] },
    "raid":               { "defaults":  { "user":"AwesomeUser", "viewers":"1" },
                            "potential": ["user", "viewers"] },
    "shoutout-give":      { "defaults":  { "user":"AwesomeUser", "viewers":"1" },
                            "potential": ["user", "viewers"] },
    "shoutout-receive":   { "defaults":  { "user":"AwesomeUser", "viewers":"1" },
                            "potential": ["user", "viewers"] },
    "bits":               { "defaults":  { "user":"AwesomeUser", "amount":"1", "message":"" },
                            "potential": ["user", "amount", "message"] }
}

argument_prefixes = {
    "u": "user", "user": "user",
    "t": "tier", "tier": "tier",
    "m": "months", "months": "months",
    "g": "gifts", "gifts": "gifts",
    "msg": "message", "message": "message",
    "b": "bits", "bits": "bits",
    "l": "level", "level": "level",
    "v": "viewers", "viewers": "viewers"
}

async def c_debug (cmd: ChatCommand):
    try:
        args = cmd.parameter.split(" ")
        if await isStreamer(cmd.user.name):
        
            if len(args) > 0:
                if args[0] in ["ad-break", "vayl-load", "stream-online", "stream-offline"]:
                    await addAlert({"type":args[0]}, "end")
                if args[0].lower() in debug_commands:
                    
                    command = cmd.text.split("!debug " + args[0])[1]
                    # Fetch the command structure
                    command_structure = debug_commands[args[0].lower()]
                    defaults = command_structure.get("defaults", {})
                    potential_args = command_structure.get("potential", [])

                    # Regex to match arguments
                    pattern = r"(\w+):\"([^\"]+)\"|(\w+):(\S+)"
                    matches = re.findall(pattern, command)

                    # Start with default values
                    parsed_args = defaults.copy()
                    parsed_args["type"] = args[0].lower()

                    # Overwrite defaults with provided arguments
                    for match in matches:
                        key = match[0] or match[2]  # Match prefix (e.g., "u", "tier", etc.)
                        value = match[1] or match[3]  # Match quoted or non-quoted value

                        # Map the prefix to its corresponding argument
                        if key in argument_prefixes:
                            arg_name = argument_prefixes[key]
                            if arg_name in potential_args:
                                parsed_args[arg_name] = value
                    
                    await addAlert(parsed_args, "end")
    
    except Exception as e:
        logError(tag = "command.debug")
## =================================================================================


## Custom ==========================================================================
async def c_custom (cmd: ChatCommand):
    try:
        global sv
        user = cmd.user.name
        arguments = cmd.parameter.split(" ")
        
        if cmd.name.lower() in sv["commands"]:

            
            if user not in sv["commands"][cmd.name.lower()]["user-cooldown"]:
                sv["commands"][cmd.name.lower()]["user-cooldown"][user] = 0
                
            with open(os.path.join(vdir["configuration"], "commands.yml"), 'r', encoding = "utf-8") as file:
                data = yaml.full_load(file)
                data = data["command"][cmd.name.lower()]
                
                if not await isStreamer(user):
                    if "streamer-only" in data and data["streamer-only"] == True:
                        return
                    if "sub-only" in data and data["sub-only"] == True and not await isSubbed(user):
                        return
                    if "mod-only" in data and data["mod-only"] == True and not await isModerator(sv["streamer"], user):
                        return
                    if "vip-only" in data and data["vip-only"] == True and not "vip" in cmd.user.badges:
                        return
                        
            if await isStreamer(user) or (time.time() - sv["commands"][cmd.name.lower()]["user-cooldown"][user] >= data["cooldown"]):
                command = {"user":user, "cmdtext":" ".join(arguments)}
                for i in range (0, 9999):
                    command["arg" + str(i)] = "" if i >= len(arguments) else (arguments[i].replace("@","",1))
                await runActions(data["actions"], command)
                sv["commands"][cmd.name.lower()]["user-cooldown"][user] = time.time()
    except Exception as e:
        logError(tag = "command.custom")
## =================================================================================


## Follow Age ======================================================================
async def c_followage (cmd: ChatCommand):
    try:
        name = cmd.user.name if len(cmd.parameter) == 0 else cmd.parameter
        result = await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id)
        async for follower in result:
            if follower.user_name.lower() == name.lower():
                follow_date = follower.followed_at.replace(tzinfo=pytz.UTC)
                now = datetime.now().replace(tzinfo=pytz.UTC)
                
                years, remainder = divmod((now - follow_date).total_seconds(), 31536000)
                days, remainder = divmod(remainder, 86400)
                hours, remainder = divmod(remainder, 3600)
                minutes, remainder = divmod(remainder, 60)
                
                await sv["chat"].send_message(sv["channel"], name + " has been following for " + str(int(years)) + " Years, " + str(int(days)) + " Days, " + str(int(hours)) + " Hours, " + str(int(minutes)) + " Minutes, " + str(int(remainder)) + " Seconds.")
    except Exception as e:
        logError(tag = "command.followage")
## =================================================================================


## Uptime ==========================================================================
async def c_uptime (cmd: ChatCommand):
    try:
        async for streams in sv["twitch"].get_streams(user_id = sv["streamer"].id):
            uptime = streams.started_at.replace(tzinfo=pytz.UTC)
            now = datetime.now(tz=pytz.UTC)
            days, remainder = divmod((now - uptime).total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, remainder = divmod(remainder, 60)
            await sv["chat"].send_message(sv["channel"], "Uptime: " + str(int(days)) + " Days, " + str(int(hours)) + " Hours, " + str(int(minutes)) + " Minutes, " + str(int(remainder)) + " Seconds.")
    except Exception as e:
        logError(tag = "command.uptime")
## =================================================================================


## Get Game ========================================================================
async def c_getgame (cmd: ChatCommand):
    try:
        infos = await sv["twitch"].get_channel_information(sv["streamer"].id)
        await sv["chat"].send_message(sv["channel"], "Current Game: " + infos[0].game_name)
    except Exception as e:
        logError(tag = "command.game")
## =================================================================================


## Set Game ========================================================================
async def c_setgame (cmd: ChatCommand):
    try:
        if await isStreamer(cmd.user.name) or await isModerator(sv["streamer"].id, cmd.user.name):
            game = {"id":"", "name":""}
            async for games in sv["twitch"].get_games(names = [cmd.parameter]):
                game["id"] = games.id
                game["name"] = games.name
            if game["id"] != "":
                await sv["twitch"].modify_channel_information(sv["streamer"].id, game_id = game["id"])
                await sv["chat"].send_message(sv["channel"], "Game has been set to: " + game["name"])
            else:
                await sv["chat"].send_message(sv["channel"], "Unable to find '" + cmd.parameter + "'")
    except Exception as e:
        logError(tag = "command.setgame")
## =================================================================================


## Set Title =======================================================================
async def c_settitle (cmd: ChatCommand):
    try:
        if (await isStreamer(cmd.user.name)) or await isModerator(sv["streamer"].id, cmd.user.name) and len(cmd.parameter) > 0:
            await sv["twitch"].modify_channel_information(sv["streamer"].id, title = cmd.parameter)
            await sv["chat"].send_message(sv["channel"], "Stream title has been updated.")
    except Exception as e:
        logError(tag = "command.settitle")
## =================================================================================


## Quote ===========================================================================
async def c_quote (cmd: ChatCommand):
    try:
        f = open(os.path.join(vdir["resources"], "quotes.yml"), 'a+', encoding = "utf-8")
        f.seek(0)
        quotes = f.readlines()
        
        if len(quotes) > 0:
            if len(cmd.parameter) == 0:
                # Random
                
                value = random.randint(0, total - 1)
                quote = quotes[value]
                await sv["chat"].send_message(sv["channel"], "Quote #" + str(value + 1) + ": " + quote)
            else:
                value = 1
                try:
                    value = int (cmd.parameter)
                except Exception as e:
                    pass

                if value <= 0:
                    value = 1
                elif value > len(quotes):
                    value = len(quotes)
                    
                quote = quotes[value - 1]
                await sv["chat"].send_message(sv["channel"], "Quote #" + str(value) + ": " + quote)
        else:
            await sv["chat"].send_message(sv["channel"], "No quotes added... yet!")
    except Exception as e:
        logError(tag = "command.quote")
        
        
async def c_quotes (cmd: ChatCommand):
    try:
        f = open(os.path.join(vdir["resources"], "quotes.yml"), 'r', encoding = "utf-8")
        total = len(f.readlines())
        await sv["chat"].send_message(sv["channel"], str(total) + " Available Quotes.")
    except Exception as e:
        logError(tag = "command.quotes")
## =================================================================================


## SFX Toggle ======================================================================
async def c_sfxtoggle (cmd: ChatCommand):
    try:
        if await isStreamer(cmd.user.name) or await isModerator(sv["streamer"].id, cmd.user.name):
            with open(os.path.join(vdir["configuration"], "sfx.yml"), 'r', encoding = "utf-8") as file:
                data = yaml.safe_load(file)
                data["enabled"] = not data["enabled"]
                with open(os.path.join(vdir["configuration"], "sfx.yml"), 'w', encoding = "utf-8") as yaml_file:
                    yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)
                sv["chat"].send_message(sv["channel"], "SFX: " + ("Enabled" if data["enabled"] == "True" else "Diabled"))
    except Exception as e:
        logError(tag = "command.sfxtoggle")
## =================================================================================


## SFX =============================================================================
async def c_sfx (cmd: ChatCommand):
    global sv
    try:
    
        if cmd.name.lower() in sv["sfx"]["sounds"]:
        
            with open(os.path.join(vdir["configuration"], "sfx.yml"), 'r', encoding = "utf-8") as file:
                s_data = yaml.safe_load(file)
                if "enabled" in s_data and not s_data["enabled"]:
                    return

            user = cmd.user.name
            if not await isStreamer(user):
                if sv["sfx"]["sounds"][cmd.name.lower()]["streamer-only"] == True:
                    return
                if sv["sfx"]["sounds"][cmd.name.lower()]["sub-only"] == True and not await isSubbed(user):
                    return
                if sv["sfx"]["sounds"][cmd.name.lower()]["mod-only"] == True and not await isModerator(sv["streamer"], user):
                    return
                if sv["sfx"]["sounds"][cmd.name.lower()]["vip-only"] == True and not "vip" in cmd.user.badges:
                    return
                    
            
            sv["sfx"]["global-usage"][user] = 0 if user not in sv["sfx"]["global-usage"] else sv["sfx"]["global-usage"][user]
            
            t = time.time()
            data = sv["sfx"]["sounds"][cmd.name.lower()]
            
            allowed = await isStreamer(user)
            if t - sv["sfx"]["global-usage"][user] >= sv["sfx"]["global-cooldown"]:
                if user not in data["last-use-user"]:
                    data["last-use-user"][user] = 0
                if t - data["last-use-user"][user] >= data["global-cooldown"]:
                    data["last-use-user"][user] = 0 if user not in data else data[user]
                    if t - data["last-use-user"][user] >= data["user-cooldown"]:
                        allowed = True
                            
            if allowed:
                for type in [".mp3",".wav"]:
                    try:
                        if os.path.exists(os.path.join(vdir["sounds"], data["sound"] + type)):
                            playsound(os.path.join(vdir["sounds"], data["sound"] + type), block = False)
                    except:
                        pass
                #threading.Thread(target=playsound, args=(os.getcwd() + "\\data\\resources\\sounds\\" + data["sound"].replace(".mp3","").replace(".wav",""),), daemon=True).start()
                        
                sv["sfx"]["global-usage"][user] = t
                data["last-use-user"][user] = t
                data["last-use-time"] = t
                        
                            
    except Exception as e:
        logError(tag = "command.sfx")
## =================================================================================


## =================================================================================
## =================================================================================
################################## TIMED ACTIONS ###################################
## =================================================================================
## =================================================================================

## Manage Actions ==================================================================
def timedActions():
    asyncio.run(timedActionsAsync())
## =================================================================================
    

## Manage Actions (async) ==========================================================    
async def timedActionsAsync():
    while True:
        global sv
        for action in sv["actions"]:
            action["counter"] += 1
            if action["counter"] >= action["frequency"]:
                if action["max-iterations"] == -1 or action["iterations"] < action["max-iterations"]:
                    await runActions(action["actions"], {})
                    action["iterations"] += 1
                action["counter"] = 0
        await asyncio.sleep(1)
## =================================================================================





## =================================================================================
## =================================================================================
######################################## OBS #######################################
## =================================================================================
## =================================================================================


## Index OBS =======================================================================
def indexOBS():
    asyncio.run(indexOBSAsync())
## =================================================================================


## Index OBS =======================================================================
async def indexOBSAsync():
    global sv
    new_index = {}
    
    while True:
        scenes = []
        groups = []
        try:
            cl = None
            with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
                data = yaml.safe_load(file)
                cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
                for scene in cl.get_scene_list().__dict__["scenes"]:
                    scenes.append(scene["sceneName"])
                for group in cl.get_group_list().__dict__["groups"]:
                    groups.append(group)
            new_index["scenes"] = scenes
            new_index["groups"] = groups
        except:
            pass
            
        sv["obs"] = new_index
            
        await asyncio.sleep(60)
## =================================================================================


## =================================================================================





## =================================================================================
## =================================================================================
###################################### ALERTS ######################################
## =================================================================================
## =================================================================================


## Add Alert =======================================================================
async def addAlert (alert, position):
    global sv
    
    alert["id"] = str(uuid.uuid4())

    
    if position.isnumeric():
        sv["alerts"].insert(int(position), alert)
    else:
        sv["alerts"].append(alert)
## =================================================================================


## Manage Alerts ===================================================================
def manageAlerts():
    asyncio.run(manageAlertsAsync())
## =================================================================================
    
    
## Manage Alerts (async) ===========================================================



async def manageAlertsAsync():
    global sv
    
    while True:
        buffer = 1
        
        if sv["alerts"] and len(sv["alerts"]) > 0:
            alert = sv["alerts"].popleft()

            if "giftsub" in alert["type"]:
                alert["amount"] = 1
                while sv["alerts"] and sv["alerts"][0]["type"] == "giftsub" and sv["alerts"][0]["user"] == alert["user"]:
                    sv["alerts"].popleft()  # Remove the matching element
                    alert["amount"] += 1
            if "redeem" in alert["type"]:
                actions = alert.get("actions", [])
                buffer = alert.get("buffer", 1)
            else:
                try:
                    with open(os.path.join(os.getcwd(), "configuration", "event", alert['type'] + ".yml"), 'r', encoding="utf-8") as file:
                        data = yaml.safe_load(file)
                        if data.get("enabled", False):
                            actions = data["actions"]
                            buffer = data.get("buffer", 1)
                except FileNotFoundError:
                    print(f"YAML file not found for alert type: {alert['type']}")
                except Exception as e:
                    print(f"Error loading YAML for alert {alert['type']}: {e}")
            
            if alert["type"] != "chat":
                print("Processing alert: " + alert['type'])
            await runActions(actions, alert)
        await asyncio.sleep(buffer)
        
            


## =================================================================================


## =================================================================================
## =================================================================================
#################################### FUNCTIONS #####################################
## =================================================================================
## =================================================================================


## Is Streamer =====================================================================
async def isStreamer (user):
    try:
        return (user.lower() == sv["channel"].lower())
    except Exception as e:
        logError(tag = "vayl.isstreamer")
## =================================================================================


## Is Moderator ====================================================================
async def isModerator (id, user):
    try:
        async for mod in sv["twitch"].get_moderators(sv["streamer"].id):
            if mod.user_name.lower() == user.lower():
                return True
        return False
    except Exception as e:
        logError(tag = "vayl.ismoderator")
## =================================================================================


## Is Subbed =======================================================================
async def isSubbed (user):
    try:
        async for sub in sv["twitch"].get_broadcaster_subscriptions(sv["streamer"].id):
            if user.lower() == sub.user_name.lower():
                return True
        return False
    except Exception as e:
        logError(tag = "vayl.issubbed")
## =================================================================================


## RunActions ======================================================================
async def runActions (actions, variables):

    cl = None
    
    action_requirements = { "obs:scene"      : ["scene"],
                            "obs:show"       : ["source"],
                            "obs:hide"       : ["source"],
                            "obs:toggle"     : ["source"],
                            "obs:label"      : ["source", "text", "color"],
                            "obs:mediafile"  : ["source", "filepath"],
                            "obs:slideshow"  : ["source", "state"],
                            "obs:filter"     : ["source", "filter", "enabled"],
                            "playsound"      : ["sound"],
                            "wait"           : ["time"],
                            "chat"           : ["message"],
                            "text"           : ["name", "modifier", "text"],
                            "counter"        : ["name", "modifier", "amount"],
                            "boolean"        : ["name", "value"],
                            "console"        : ["message"],
                            "list"           : ["name", "modifier", "text"],
                            "conditional"    : ["name"],
                            "tts"            : ["voice", "message", "halt", "limit"],
                            "cmd"            : ["command"],
                            "announce"       : ["message", "color"],
                            "vip"            : ["modifier", "username"],
                            "timeout"        : ["user", "duration", "reason"],
                            "webhook"        : ["name"],
                            "createclip"     : [],
                            "addmarker"      : []}
                            
    
    action_expected = { "obs:scene"      : "'obs:scene ; <scene_name>'",
                        "obs:show"       : "'obs:show ; <source_name>'",
                        "obs:hide"       : "'obs:hide ; <source_name>'",
                        "obs:toggle"     : "'obs:toggle ; <source_name>'",
                        "obs:label"      : "'obs:label ; <source_name> ; <text> ; [color]'",
                        "obs:mediafile"  : "'obs:mediafile ; <source_name> ; <file_path>'",
                        "obs:slideshow"  : "'obs:slideshow ; <source_name> ; <play/pause/stop/restart/next/previous/position>'",
                        "obs:filter"     : "'obs:filter ; <source_name> ; <filter_name> ; <enabled/disabled>'",
                        "playsound"      : "'playsound ; <sound_name>'",
                        "wait"           : "'wait ; <seconds>'",
                        "chat"           : "'chat ; <message>'",
                        "text"           : "'text ; <variable_name> ; <set/append> ; <text>'",
                        "counter"        : "'counter ; <variable_name> ; <set/increase/decrease/multiply/divide> ; <amount>'",
                        "boolean"        : "'boolean ; <variable_name> ; <true/false>'",
                        "list"           : "'list ; <variable_name> ; <clear/add/remove> ; <text>'",
                        "console"        : "'console ; <message>'",
                        "conditional"    : "'conditional ; <conditional_name>'",
                        "tts"            : "'tts ; <voice> ; <message> ; <true/false> ; <character_limit>'",
                        "cmd"            : "'cmd ; <command>'",
                        "announce"       : "'announce ; <message> ; '<blue/green/orange/purple/primary>",
                        "vip"            : "'vip ; <add/remove> ; <username>'",
                        "timeout"        : "'timeout ; <user> ; <duration> ; <reason>'",
                        "webhook"        : "'webhook ; <webhook_name>'",
                        "createclip"     : "'createclip'",
                        "addmarker"      : "'addmarker'"}


    async def processTags (phrase, is_conditional):
        
        was_list = False
        phrase_split = phrase.split(" ")
        for i in range(0, len(phrase_split)):
            try:
                word = phrase_split[i]
            
                for tag, value in variables.items():
                    word = word.replace("[" + tag + "]", str(value))
                    
                if "[nickname:" in word:
                    name = word.split("[nickname:")[1].split("]")[0]
                    with open(os.path.join(vdir["configuration"], "nicknames.yml"), 'r', encoding = "utf-8") as file:
                        data = yaml.safe_load(file)
                        found = False
                        for n,v in data.items():
                            if n.lower() == name.lower():
                                word = word.replace("[nickname:" + name + "]", v)
                                found = True
                                break
                        if not found:
                            word = word.replace("[nickname:" + name + "]", name)
            
                if "[followers]" in word:
                    counter = 0
                    async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                        counter += 0 if follower.user_name.lower() == "vaylbot" else 1
                    word = word.replace("[followers]", str(counter))
                    
            
                if "[rfollower]" in word:
                    followers = []
                    async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                        if follower.user_name.lower() != "vaylbot":
                            followers.append(follower.user_name)
                    word = word.replace("[rfollower]", random.choice(followers))

                if "[subscribers]" in word:
                    counter = 0
                    async for sub in await sv["twitch"].get_broadcaster_subscriptions(sv["streamer"].id):
                        counter += 0 if sub.user_name.lower() == "vaylbot" else 1
                    word = word.replace("[subscribers]", str(counter))

                if "[rsubscriber]" in word:
                    subscribers = []
                    async for sub in await sv["twitch"].get_broadcaster_subscriptions(sv["streamer"].id):
                        if sub.user_name.lower() != "vaylbot":
                            subscribers.append(sub.user_name)
                    word = word.replace("[rsubscriber]", random.choice(subscribers))

                if "{viewers}" in word:
                    async for streams in await sv["twitch"].get_streams(user_id = [sv["streamer"].id]):
                        word = word.replace("[viewers]", str(streams.viewer_count))

                if "[ruser]" in word:
                    chatters = []
                    async for chatter in await sv["twitch"].get_chatters(sv["streamer"].id, sv["streamer"].id):
                        if chatter.user.name.lower() != "vaylbot":
                            chatters.append(chatter.user_name)
                    word = word.replace("[ruser]", random.choice(chatters))
                
                if "[system:dateus]" in word:
                    word = word.replace("[system:dateus]", date.today().strftime("%m/%d/%y"))
                    
                if "[system:dateuk]" in word:
                    word = word.replace("[system:dateuk]", date.today().strftime("%d/%m/%y"))    
                
                if "[system:time]" in word:
                    word = word.replace("[system:time]", datetime.now().strftime("%H:%M:%S"))
                    
                if "[uptime:seconds]" in word:
                    uptime = streams.started_at.replace(tzinfo=pytz.UTC)
                    now = datetime.now(tz=pytz.UTC)
                    word = word.replace("[uptime:seconds]", str(int((now - uptime).total_seconds())))
                
                for type in ["vayl","counter","text","boolean"]:
                    if "[" + type + ":" in word:
                        tag = word.split("[" + type + ":")[1].split("]")[0]
                        with open(os.path.join(vdir["variables"], type, tag + ".txt"), 'r', encoding = "utf-8") as f:
                            word = word.replace("[" + type + ":" + tag + "]", f.read())
                        
                if "[list:" in word:
                    was_list = True
                    tag = word.split("[list:")[1].split("]")[0]
                    with open(os.path.join(vdir["list"], tag + ".txt"), 'r', encoding = "utf-8") as f:
                        information = ", ".join(f.read().splitlines()) if not is_conditional else '["' + '", "'.join(f.read().splitlines()) + '"]'
                        word = word.replace("[list:" + tag + "]", information)
                        
                if "[rlist:" in word:
                    tag = word.split("[rlist:")[1].split("]")[0]
                    with open(os.path.join(vdir["list"], tag + ".txt"), 'r', encoding = "utf-8") as f:
                        word = word.replace("[rlist:" + tag + "]", random.choice(f.read().splitlines()))
                        
                if "[clist:" in word:
                    try:
                        name, text = re.search(r"\[clist:([^:\]]+):([^:\]]+)\]", word).groups()
                        try:
                            with open(os.path.join(vdir["list"], name + ".txt"), 'r', encoding="utf-8") as f:
                                entries = f.read().splitlines()
                            count = sum(1 for entry in entries if entry == text)
                        except FileNotFoundError:
                            count = 0
                        word = re.sub(r"\[clist:[^:\]]+:[^:\]]+\]", str(count), word)
                    except AttributeError:
                        pass
                
                if "[toplist:" in word:
                    try:
                        # Extract name and text from the tag
                        name, text = re.search(r"\[toplist:([^:\]]+):([^:\]]+)\]", word).groups()
                        file_path = os.path.join(vdir["list"], name + ".txt")

                        # Read the list and count occurrences
                        try:
                            with open(file_path, 'r', encoding="utf-8") as f:
                                entries = f.read().splitlines()

                            # Count occurrences and create a leaderboard
                            from collections import Counter
                            counts = Counter(entries)
                            leaderboard = sorted(counts.items(), key=lambda x: (-x[1], x[0]))  # Sort by count, then alphabetically

                            # Find the position of the specified text in the leaderboard
                            position = next((i + 1 for i, (entry, _) in enumerate(leaderboard) if entry == text), 0)

                        except FileNotFoundError:
                            position = 0

                        # Replace the tag with the position
                        word = re.sub(r"\[toplist:[^:\]]+:[^:\]]+\]", str(position), word)
                    except AttributeError:
                        # Handle malformed tags gracefully
                        pass
                        
                if "[rnumber:" in word:
                    min = word.split("[rnumber:")[1].split("-")[0]
                    max = word.split("[rnumber:")[1].split("-")[1].split("]")[0]
                    word = re.sub(r"\[rnumber:([+-]?\d+)-([+-]?\d+)\]", str(random.randint(int(min), int(max))), word)
                        
                if "[xstring:" in word:
                    word = re.sub(r"\[xstring:([^:]+):([+-]?\d+)\]", lambda m: m.group(1) * int(m.group(2)) if int(m.group(2)) >= 0 else "", word )
                
                
                if "[ugame:" in word:
                    name = word.split("[ugame:")[1].split("]")[0]
                    found_game = ""
                    async for users in sv["twitch"].get_users(logins = [name]):
                        infos = await sv["twitch"].get_channel_information(users.id)
                        found_game = infos[0].game_name if infos[0].game_name != "" else "something..."
                    word = word.replace("[ugame:" + name + "]", found_game)
            

            
            except:
                logError (tag = "action.tags")
                
            phrase_split[i] = word
        
        # print (phrase_split)
        return " ".join(phrase_split)
        



    for a in actions:

    
        action = a.split(" ; ")[0]
        arguments = a.split(" ; ")[1:]
        
        if cl is None:
            if action in ["obs:scene","obs:show","obs:hide","obs:toggle","obs:label","obs:image","obs:mediafile","obs:slideshow", "obs:filter"] or "[obs:scene]" in a:
                with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
            
        
        adata = {}
        for i in range(0, len(arguments)):
            adata[action_requirements[action][i]] = arguments[i]

        for key, value in adata.items():
            adata[key] = await processTags(value, False)



        ## ModifySource ============================================================
        def modifySource (source_name, source_action):
            try:
                found = False
                for scene in sv["obs"]["scenes"]:
                    for item in cl.get_scene_item_list(scene).__dict__["scene_items"]:
                        if source_name == item["sourceName"]:
                            id = item['sceneItemId']
                            # id = cl.get_scene_item_id(scene, adata["source"], offset = None).__dict__["scene_item_id"] 
                            if "show" in source_action or "hide" in source_action:
                                cl.set_scene_item_enabled(scene, id, True if "show" in source_action else False)
                            else:
                                enabled = bool(cl.get_scene_item_enabled(scene, id).__dict__["scene_item_enabled"])
                                cl.set_scene_item_enabled(scene, id, not enabled)
                            found = True
                if not found:
                    for group in sv["obs"]["groups"]:
                        for item in cl.get_group_scene_item_list(group).__dict__["scene_items"]:
                            # print (item)
                            if source_name == item["sourceName"]:
                            
                                id = item['sceneItemId']
                                
                                # id = cl.get_scene_item_id(group, adata["source"], offset = None).__dict__["scene_item_id"] 
                                
                                if "show" in source_action or "hide" in source_action:
                                    cl.set_scene_item_enabled(group, id, True if "show" in source_action else False)
                                else:
                                    enabled = bool(cl.get_scene_item_enabled(group, id).__dict__["scene_item_enabled"])
                                    cl.set_scene_item_enabled(group, id, not enabled)
                            found = True
                if not found:
                    prompt ("misc", "Unable to find source: " + adata["source"])
            except Exception as e:
                logError(tag = "obs.modifysource", additional_details = [a, "Expecting: " + action_expected["obs:" + source_action]])
        ## =========================================================================


        ## obs:scene ===============================================================
        if action == "obs:scene":
            try:
                if adata["scene"] in sv["obs"]["scenes"]:
                    cl.set_current_program_scene(adata["scene"])
                else:
                    prompt ("error", "Scene not found: " + adata["scene"])
            except Exception as e:
                logError(tag = "obs.scene", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## obs:show/hide/toggle ====================================================
        if action in ["obs:show","obs:hide","obs:toggle"]:
            modifySource (adata["source"], action.split(":")[1])
        ## =========================================================================
        
        
        ## obs:label ===============================================================
        if action == "obs:label":
            try:
                label = cl.get_input_settings(adata["source"]).__dict__
                data = dict(label["input_settings"])
                if "color" in adata and adata["color"] != "":
                    color_string = str(adata["color"]).replace("0x","")
                    wcs = wrap(color_string, 2)
                    adata["color"] = "0x" + wcs[2] + wcs[1] + wcs[0]
                    data["color"] = int(adata["color"], 0)
                data["text"] = adata["text"]
                cl.set_input_settings(adata["source"], data, True)
            except Exception as e:
                logError(tag = "obs.label", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## obs:image ===============================================================
        if action == "obs:image":
            try:
                image = cl.get_input_settings(adata["source"]).__dict__
                data = dict(image["input_settings"])
                data["file"] = adata["filepath"]
                cl.set_input_settings(adata["source"], data, True)
            except Exception as e:
                logError(tag = "obs.image", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

        
        ## obs:mediafile ===========================================================
        if action == "obs:mediafile":
            try:
                mediafile = cl.get_input_settings(adata["source"]).__dict__
                data = dict(mediafile["input_settings"])
                data["local_file"] = adata["filepath"]
                cl.set_input_settings(adata["source"], data, True)
            except Exception as e:
                logError(tag = "obs.mediafile", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## obs:slideshow ===========================================================
        if action == "obs:slideshow":
            try:
                if str(adata["state"]).isnumeric():
                    cl.set_media_input_cursor(adata["source"], int(adata["state"]))
                else:
                    slideshow_actions = { "play" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY",
                                          "pause" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE",
                                          "stop" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP",
                                          "restart" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART",
                                          "next" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_NEXT",
                                          "previous" : "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PREVIOUS"}
                    cl.trigger_media_input_action(adata["source"], slideshow_actions[adata["state"]])
            except Exception as e:
                logError(tag = "obs.slideshow", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

        
        ## obs:filter ==============================================================
        if action == "obs:filter":
            try:
                cl.set_source_filter_enabled(adata["source"], adata["filter"], (adata["enabled"].lower() == "true"))
            except Exception as e:
                logError(tag = "obs.filter", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## wait ====================================================================
        if action == "wait":
            try:
                await asyncio.sleep(float(adata["time"]))
            except Exception as e:
                logError(tag = "action.wait", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## chat ====================================================================
        if action == "chat":
            try:
                await sv["chat"].send_message(sv["channel"], adata["message"])
            except Exception as e:
                logError(tag = "action.chat", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## text ====================================================================
        if action == "text":
            try:
            
                if not os.path.exists(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt"):
                    with open(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                        pass
            
                text = ""
                try:
                    with open(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as f:
                        text = f.read()
                except:
                    pass
                with open(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(text + str(adata["text"]) if adata["modifier"] == "append" else str(adata["text"]))
            except Exception as e:
                logError(tag = "action.text", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## boolean =================================================================
        if action == "boolean":
            try:
            
                if not os.path.exists(os.getcwd() + "\\data\\variables\\boolean\\" + adata["name"] + ".txt"):
                    with open(os.getcwd() + "\\data\\variables\\boolean\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                        file.write("false")
            
                value = False
                try:
                    with open(os.getcwd() + "\\data\\variables\\boolean\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as f:
                        value = (f.read().lower() == "true")
                except:
                    pass
                value = not value if adata["value"].lower() == "toggle" else (adata["value"].lower() == "true")
                with open(os.getcwd() + "\\data\\variables\\boolean\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as f:
                    f.write(str(value)) 
            except Exception as e:
                logError(tag = "action.boolean", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## counter =================================================================
        if action == "counter":
            try:
            
                if not os.path.exists(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt"):
                    with open(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                        file.write("0")
            
                counter = 0
                try:
                    with open(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as file:
                        counter = float(file.read())
                except:
                    pass
                adata["amount"] = float(adata["amount"])
                modification = {"increase":(counter + adata["amount"]), "decrease":(counter - adata["amount"]), "multiply":(counter * adata["amount"]), "divide":(counter / adata["amount"]) if adata["amount"] != 0 else 0, "set":adata["amount"]}
                counter = modification[adata["modifier"]]
                counter = round(counter) if ".0" in str(round(counter, 1)) else round(counter, 1) 
                with open(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(counter))
            except Exception as e:
                logError(tag = "action.counter", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## list ====================================================================
        if action == "list":
            try:
            
                if not os.path.exists(os.getcwd() + "\\data\\variables\\list\\" + adata["name"] + ".txt"):
                    with open(os.getcwd() + "\\data\\variables\\list\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                        pass
            
                list = []
                with open(os.getcwd() + "\\data\\variables\\list\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as file:
                    list = file.read().splitlines()
                if adata["modifier"] == "add":
                    list.append(adata["text"])
                elif adata["modifier"] == "remove" and adata["text"] in list:
                    list.remove(adata["text"])
                elif adata["modifier"] == "clear":
                    list = []    
                    
                with open(os.getcwd() + "\\data\\variables\\list\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.writelines(f"{line}\n" for line in list if line)
            except Exception as e:
                logError(tag = "action.list", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## announce ================================================================
        if action == "announce":
            try:
                await sv["twitch"].send_chat_announcement(sv["streamer"].id, sv["streamer"].id, adata["message"], adata["color"])
            except Exception as e:
                logError(tag = "action.announce", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

    
        ## vip =====================================================================
        if action == "vip":
            try:
                if adata["modifier"] == "add":
                    await sv["twitch"].add_channel_vip(sv["streamer"].id, adata["username"])
                elif adata["modifier"] == "remove":
                    await sv["twitch"].remove_channel_vip(sv["streamer"].id, adata["username"])
            except Exception as e:
                logError(tag = "action.vip", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        

        ## cmd =====================================================================
        if action == "cmd":
            try:
                subprocess.run(adata["command"], shell = False)
            except Exception as e:
                logError(tag = "action.cmd", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## playsound ===============================================================
        if action == "playsound":
            try:
                found = False
                for type in [".mp3",".wav"]:
                    if os.path.exists(os.getcwd() + "\\data\\resources\\sounds\\" + adata["sound"].replace(".mp3","").replace(".wav","") + type):
                        playsound(os.getcwd() + "\\data\\resources\\sounds\\" + adata["sound"].replace(".mp3","").replace(".wav","") + type, block = False)
                        found = True
                        break
                if not found:
                    prompt ("misc", "Unable to find audio file: " + adata["sound"])
            except Exception as e:
                logError(tag = "action.playsound", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

    
        ## timeout =================================================================
        if action == "timeout":
            try:
                async for u in sv["twitch"].get_users(logins = [adata["user"]]):
                    await sv["twitch"].ban_user(sv["streamer"].id, sv["streamer"].id, u.id, adata["reason"], int(adata["duration"]))
            except Exception as e:
                logError(tag = "action.timeout", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## log =====================================================================
        if action == "console":
            try:
                print(adata["message"])
            except Exception as e:
                logError(tag = "action.console", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

    
        ## webhook =================================================================
        if action == "webhook":
            try:
                with open(os.getcwd() + "\\configuration\\webhook\\" + adata["name"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    
                    webhook = DiscordWebhook(url = data["url"], content = "\n".join(data["message"]), username = "Vayl", avatar_url = "https://i.ibb.co/3rSvnDg/logo2.png")
                    
                    info = await sv["twitch"].get_channel_information(sv["streamer"].id)
                    info = info[0]
                    directory = {"[game]":info.game_name, "[title]":info.title, "[name]":info.broadcaster_name, "[link]":"https://twitch.tv/" + sv["channel"].lower()}
                    
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
                
                    if data["embed"]["fields"]["enabled"] == True:
                        for k,v in data["embed"]["fields"].items():
                            if k != "enabled":
                                for d,r in directory.items():
                                    v["name"] = v["name"].replace(d,r)
                                    v["value"] = v["value"].replace(d,r)
                                embed.add_embed_field (name = v["name"], value = v["value"])
                    
                    webhook.add_embed(embed)
                    response = webhook.execute()

            except Exception as e:
                logError(tag = "action.webhook", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================

        
        ## conditional =============================================================
        if action == "conditional":
            try:
            
                data = {}
                if ":" in adata["name"]:
                    with open(os.getcwd() + "\\configuration\\conditionals\\" + adata["name"].split(":")[0] + ".yml", 'r', encoding = "utf-8") as file:
                        data = yaml.safe_load(file)
                        data = data[adata["name"].split(":")[1]]
                else:
                    with open(os.getcwd() + "\\configuration\\conditionals\\" + adata["name"] + ".yml", 'r', encoding = "utf-8") as file:
                        data = yaml.safe_load(file)
                
                condition = await processTags(data["condition"], True)
                
                result = eval(condition)
                await runActions(data[result], variables)
                            
            except Exception as e:
                logError(tag = "action.conditional", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================


        ## tts =====================================================================
        if action == "tts":
            try:
            
                if len(adata["message"]) <= int(adata["limit"]):

                    for vp, voice in tts_voice.items():
                        for voices in voice:
                            
                            if adata["voice"] == voices.lower():
                                
                                data = None
                                
                                with open(os.getcwd() + "\\configuration\\pronunciation.yml", 'r', encoding = "utf-8") as file:
                                    pdata = yaml.safe_load(file)
                                    for name,pronounce in pdata.items():
                                        adata["message"] = adata["message"].replace(name, pronounce)
                                    
                                if vp == "acapela":
                                    __session__ = requests.session()
                                    __url1__ = 'https://www.acapela-group.com/www/static/website/demoOptionsDef_voicedemo.php'
                                    __url2__ = 'https://h-ir-ssd-1.acapela-group.com/webservices/1-60-00/UrlMaker.json'
                                    __headers__ = { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Referer': 'https://www.acapela-group.com/demos/', 'Origin': 'https://www.acapela-group.com/demos/',}
                                    res = __session__.get(__url1__, headers=__headers__)
                                    json_res = res.text.replace('var vaasOptions = ', '').replace('};', '}')
                                    json_res = json.loads(json_res)
                                    params = { 'cl_login': json_res['login'], 'cl_app': json_res['app'],   'session_start': json_res['session']['start'], 'session_time': json_res['session']['time'], 'session_key': json_res['session']['key'], 'req_voice': voices, 'req_text': adata["message"] }
                                    res = __session__.post(__url2__, params=params, headers=__headers__)
                                    res = __session__.get(res.json()['snd_url'])
                                    data = res.content
                                
                                if vp == "cepstral":
                                    __session__ = requests.session()
                                    __url1__ = 'https://www.cepstral.com/en/demos'
                                    __url2__ = 'https://www.cepstral.com/demos/createAudio.php?'
                                    params = { 'voiceText': adata["message"], 'voice': voices, 'createTime': int(time.time() * 1000), 'rate': 170, 'pitch': 1, 'sfx': 'none' }
                                    __session__.get(__url1__)
                                    res = __session__.get(__url2__, params=params)
                                    mp3_location = 'https://www.cepstral.com' + res.json()['mp3_loc']
                                    res = __session__.get(mp3_location)
                                    data = res.content
                                
                                if vp == "ibmwatson":
                                    __session__ = requests.session()
                                    __url1__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/session'   
                                    __url2__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/store'   
                                    __url3__ = 'https://www.ibm.com/demos/live/tts-demo/api/tts/newSynthesizer'

                                    __headers__ = { 'Origin': 'https://www.ibm.com',  'Referer': 'https://www.ibm.com/demos/live/tts-demo/self-service/home',    'Accept': 'application/json, text/plain, */*',   }
                                    __session__.post(__url1__, headers=__headers__)
                                    id = str(uuid.uuid4())    
                                    jsonPayload = {"ssmlText": f"<prosody pitch=\"0%\" rate=\"-0%\">{adata['voice']}</prosody>", "sessionID": id}   
                                    __session__.post(__url2__, data=jsonPayload, headers=__headers__)
                                    res = __session__.get(__url3__, params={'voice' : voices,'id': id})
                                    data = res.content
                                    
                                if vp == "oddcast":
                                    __url1__ = 'https://cache-a.oddcast.com/tts/genB.php'
                                    voiceParts = voices.split('-')
                                    voiceId, engineId, languageId = voiceParts
                                    params = { 'EID': int(engineId), 'LID': int(languageId), 'VID': int(voiceId), 'TXT':adata["message"], 'EXT':'mp3', 'FNAME':'', 'ACC':15679, 'SceneID':2703396, 'HTTP_ERR':'', 'cache_flag':3}
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
                                
                                if vp == "streamelements":
                                    __url1__ = 'https://api.streamelements.com/kappa/v2/speech?'
                                    params = { 'voice':voices, 'text':adata["message"] }
                                    res = requests.get(__url1__, params)
                                    data = res.content
                                
                                if vp == "streamlabs":
                                    __url1__ = 'https://streamlabs.com/polly/speak'
                                    __headers__ = { 'Referer': 'https://streamlabs.com' }
                                    params = {   'voice':voices, 'text':adata["message"] }
                                    res = requests.post(__url1__, params=params, headers=__headers__)
                                    mp3_url = res.json()['speak_url']
                                    res = requests.get(mp3_url)
                                    data = res.content            
                                    
                                if vp == "voiceforge":
                                    __url1__ = 'https://api.voiceforge.com/swift_engine?'
                                    __headers__ = { 'HTTP_X_API_KEY': '8b3f76a8539', }
                                    params = { 'voice':voices, 'msg':adata["message"], 'email':'null', }
                                    res = requests.get(__url1__, params=params, headers=__headers__)
                                    data = res.content
                                    
                                if data is not None:
                                
                                    file_path = os.path.join(os.getcwd(), "data", "tts", str(uuid.uuid4()) + ".wav")
                                    with open(file_path, "+wb") as file:
                                        file.write(data)
                                    
                                    timeout = 5
                                    start_time = asyncio.get_event_loop().time()
                                    while asyncio.get_event_loop().time() - start_time < timeout:
                                        size_before = os.path.getsize(file_path)
                                        await asyncio.sleep(0.1)
                                        size_after = os.path.getsize(file_path)
                                        if size_before == size_after:
                                            break
                                    else:
                                        raise TimeoutError("File write did not stabilize in time")
                                            
                                    def play_tts(file_path):
                                        try:
                                        
                                            timeout = 5
                                            start_time = time.time()
                                            while time.time() - start_time < timeout:
                                                if os.path.exists(file_path):
                                                    break
                                                time.sleep(0.1)
                                            else:
                                                raise FileNotFoundError(f"File {file_path} did not appear in time.")
                                        
                                            playsound(file_path, block = True)
                                        finally:
                                            if os.path.exists(file_path):
                                                os.remove(file_path)

                                    # Non-daemon thread
                                    thread = threading.Thread(target=play_tts, args=(file_path,))
                                    thread.start()
                                
                                break
                    
                else:
                    await sv["chat"].send_message(sv["channel"], "Unable to play TTS, message length exceeds limit of " + adata["limit"] + " characters. (" + str(len(adata["message"])) + ")")
                    prompt("misc", "Unable to play TTS, message length exceeds limit of " + adata["limit"] + " characters. (" + str(len(adata["message"])) + ")")
            
            except Exception as e:
                logError(tag = "action.tts", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## createclip ==============================================================
        if action == "createclip":
            try:
                clip = await sv["twitch"].create_clip(sv["streamer"].id)
                clips = await sv["twitch"].get_clips(broadcaster_id = sv["streamer"].id, clip_id = clip.id)
                async for c in clips:
                    await updateVariable("latest-vayl-clip", c.url)
            except Exception as e:
                logError(tag = "action.clip", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
        ## addmarker ===============================================================
        if action == "addmarker":
            try:
                marker = await sv["twitch"].create_stream_marker(sv["streamer"].id, "")
            except Exception as e:
                logError(tag = "action.addmarker", additional_details = [a, "Expecting: " + action_expected[action]])
        ## =========================================================================
        
        
## =================================================================================


## PrintLogo =======================================================================
async def printLogo():
    lines = [" ", " ",
             "####       ...       ####",
             " ####     .....     ####", 
             "  ####   ... ...   ####",
             "   ####....   ....####",
             "     #....     ..###",
             "     ...##     ####.",
             "    ...####   ####...",
             "  ....  #### ####  ....",
             " ....     #####     ....",
             "....       ###       ....",
             " "," "]

    for line in lines:
        sys.stdout.write((" " * 20))
        for char in line:   
            sys.stdout.write(char.replace("#", Style.BRIGHT + Fore.RED + "#" + Style.RESET_ALL).replace(".", Style.BRIGHT + Fore.WHITE + "#" + Style.RESET_ALL))
            sys.stdout.flush()
            await asyncio.sleep(0.005)   
        print()

## =================================================================================


## Prompt ==========================================================================
def prompt (type, message):
    try:
        icon = { "success" : Fore.GREEN, "error" : Fore.RED, "misc" : Fore.WHITE, "blank" : Fore.BLACK }
        print (Style.BRIGHT + icon[type] + "• " + Style.RESET_ALL + message)
    except:
        logError(tag = "vayl.prompt")
## =================================================================================


## Reload ==========================================================================
async def reload (chat):
    global sv
    
    ## SFX =========================================================================
    try:
        sv["sfx"] = {}
        sv["sfx"]["sounds"] = {}
        with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)
            
            sv["sfx"]["global-cooldown"] = data["global-cooldown"]
            sv["sfx"]["global-usage"] = {}
            
            for sound in data["sounds"].keys():
            
                sv["chat"].register_command(sound.lower(), c_sfx)
                s = data["sounds"][sound.lower()]
                
                sd = {}
                sd["global-cooldown"] = s["cooldown"]["global"]
                sd["user-cooldown"] = s["cooldown"]["user"]
                sd["sound"] = s["sound"]
                sd["last-use-time"] = 0
                sd["last-use-user"] = {}
                sd["streamer-only"] = str(s["streamer-only"]).lower()
                sd["sub-only"] = str(s["sub-only"]).lower()
                sd["mod-only"] = str(s["mod-only"]).lower()
                sd["vip-only"] = str(s["vip-only"]).lower()
                
                
                sv["sfx"]["sounds"][sound.lower()] = sd
    except:
        logError(tag = "load.sfx")
    ## =============================================================================
       
        
    ## Commands ====================================================================
    try:
        with open(os.getcwd() + "\\configuration\\commands.yml", 'r', encoding = "utf-8") as file:
            data = yaml.full_load(file)
            for command in data["command"].keys():
                sv["chat"].register_command(command.lower(), c_custom)
                sv["commands"][command.lower()] = {"cooldown":data["command"][command.lower()]["cooldown"], "user-cooldown":{}}
        
        cmd = {"setgame":c_setgame, "settitle":c_settitle, "game":c_getgame, "uptime":c_uptime, "togglesfx":c_sfxtoggle, "followage":c_followage, "quote":c_quote, "quotes":c_quotes, "debug":c_debug, "reload":c_reload}
        for key, value in cmd.items():
            sv["chat"].register_command(key, value)
    except:
        logError(tag = "load.commands")
    ## =============================================================================
        
    ## Phrases =====================================================================
    try:
        sv["phrases"] = {"cooldown":{}}
    except:
        logError(tag = "load.phrases")
    ## =============================================================================
        
    ## Timed Actions ===============================================================
    try:
        sv["actions"] = []
        with open(os.getcwd() + "\\configuration\\timed-actions.yml", "r", encoding = "utf-8") as file:
            data = yaml.full_load(file)
            for info in data["actions"].values():
                sv["actions"].append({"counter":0, "frequency":info["frequency"], "iterations":0, "max-iterations":info["max-iterations"], "actions":info["actions"]})
    except:
        logError(tag = "load.timedactions")
    ## =============================================================================
    
    if chat:
        await sv["chat"].send_message(sv["channel"], "Vayl Reloaded")
    
## =================================================================================


## Log Error =======================================================================



def sanitize_path(path, base_path=None):
    if base_path is None:
        base_path = os.getcwd()
    try:
        return os.path.relpath(path, base_path)
    except ValueError:
        return path  # Return the original if it cannot be made relative

def logError(tag = None, additional_details = None):
    # Display error prompt
    prompt("error", "Error Detected")
    base_path = os.getcwd()

    # Load reference for the error cause
    reference = error_reference.get(tag, "Undefined")
    prompt("blank", "Cause: " + reference)

    # Gather error details
    error_traceback = traceback.format_exc()
    sanitized_traceback = "\n".join(
        sanitize_path(line, base_path) for line in error_traceback.splitlines()
    )

    log_details = {
        "User": sv["channel"],
        "Version": __version__,
        "Cause": reference,
        "Error Line": sanitized_traceback.splitlines()[-1] if sanitized_traceback else "N/A",
        "Stack Trace": sanitized_traceback
    }

    # Write error to log file
    timestamp = str(time.time())
    log_file_path = os.path.join(base_path, "data", "logs", f"{timestamp}.txt")
    with open(log_file_path, 'w', encoding="utf-8") as log_file:
        log_file.write(f"User: {log_details['User']}\n")
        log_file.write(f"Version: {log_details['Version']}\n")
        log_file.write(f"Cause: {log_details['Cause']}\n")
        log_file.write(f"Error Line: {log_details['Error Line']}\n")
        
        if additional_details is not None:
            log_file.write("Additional Info:\n")
            for ad_line in additional_details:
                log_file.write("- " + ad_line + "\n")
            log_file.write("\n")
        else:
            log_file.write("Additional Info: None\n\n")
        
        log_file.write("Stack Trace:\n")
        log_file.write(log_details["Stack Trace"])

    # Optionally send error to Discord
    try:
        with open(os.path.join(vdir["configuration"], "configuration.yml"), 'r', encoding="utf-8") as file:
            config = yaml.safe_load(file)
            if config.get("bug-auto-report", False):
                webhook = DiscordWebhook(
                    url="https://discord.com/api/webhooks/1257675918957351013/wiIdAeOQBaXdhzyLrPRhplWz2mBbfZrTbch--c-5wMYDu1YYk2gUexBj6AUMTahnPlZs",
                    username="Bug Report",
                    avatar_url="https://i.ibb.co/ZHwjkms/icon.png"
                )
                with open(log_file_path, 'r', encoding="utf-8") as log_file:
                    webhook.add_file(file=log_file.read(), filename=f"{timestamp}.txt")
                webhook.execute()
    except Exception:
        # Handle exceptions silently to avoid recursive error logging
        pass

## =================================================================================


## Update Variable =================================================================
async def updateVariable (name, value):
    try:
        with open(os.getcwd() + "\\data\\variables\\vayl\\" + name + ".txt", 'w', encoding = "utf-8") as file:
            file.write(str(value))    
    except Exception as e:
        logError(tag = "vayl.updatevariable")
## =================================================================================


## =================================================================================
## =================================================================================
##################################### STARTUP ######################################
## =================================================================================
## =================================================================================


## Run =============================================================================
async def run():

    global sv

    with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
        data = yaml.safe_load(file)
        sv["channel"] = data["connected-account"]
    
    
    prompt ("success", "Launching Vayl (" + __version__ + ")")
    prompt ("success", "Loading Authentication")
    
    sv["twitch"] = await Twitch(sv["id"], sv["secret"])
    auth = UserAuthenticator(sv["twitch"], USER_SCOPE, force_verify = False)
    token, refresh = await auth.authenticate()
    
    await sv["twitch"].set_user_authentication(token, USER_SCOPE, refresh)
    
    await printLogo()
    
    prompt ("success", "Fetching Twitch User")
    
    sv["streamer"] = await first(sv["twitch"].get_users(logins = [sv["channel"]]))
    
    prompt ("success", "Regisering EventSub")
    
    eventsub = EventSubWebsocket(sv["twitch"])
    eventsub.start()
    await eventsub.listen_channel_follow_v2(sv["streamer"].id, sv["streamer"].id, on_follow)
    await eventsub.listen_stream_online(sv["streamer"].id, on_live)
    # await eventsub.listen_stream_offline(sv["streamer"].id, on_offline)
    await eventsub.listen_channel_ad_break_begin(sv["streamer"].id, on_ad)
    await eventsub.listen_channel_poll_begin(sv["streamer"].id, on_poll_start)
    # await eventsub.listen_channel_poll_end(sv["streamer"].id, on_poll_end)
    # await eventsub.listen_channel_prediction_begin(sv["streamer"].id, on_prediction_start)    
    # await eventsub.listen_channel_prediction_lock(sv["streamer"].id, on_prediction_lock)   
    # await eventsub.listen_channel_prediction_end(sv["streamer"].id, on_prediction_end)   
    await eventsub.listen_hype_train_begin(sv["streamer"].id, on_hype_train)   
    # await eventsub.listen_channel_shoutout_create(sv["streamer"].id, sv["streamer"].id, on_shoutout_give)
    # await eventsub.listen_channel_shoutout_receive(sv["streamer"].id, sv["streamer"].id, on_shoutout_receive)
    # await eventsub.listen_user_whisper_message(sv["streamer"].id, on_whisper)
    # await eventsub.listen_channel_cheer(sv["streamer"].id, on_bits)
    # await eventsub.listen_channel_subscribe(sv["streamer"].id, on_sub)
    # await eventsub.listen_channel_subscription_gift(sv["streamer"].id, on_giftsub)
    # await eventsub.listen_channel_subscription_message(sv["streamer"].id, on_resub)
    # await eventsub.listen_channel_points_custom_reward_redemption_add(sv["streamer"].id, on_redeem)
    
    await eventsub.listen_channel_points_custom_reward_redemption_add(sv["streamer"].id, on_redeem_new)
    await eventsub.listen_channel_cheer(sv["streamer"].id, on_bits_new)
    await eventsub.listen_channel_subscribe(sv["streamer"].id, on_sub)
    await eventsub.listen_channel_subscription_gift(sv["streamer"].id, on_giftsub)
    await eventsub.listen_channel_subscription_message(sv["streamer"].id, on_resub)
    
    
    # pubsub = PubSub(sv["twitch"])
    # pubsub.start()
    # redeem_event = await pubsub.listen_channel_points(sv["streamer"].id, on_redeem)
    # sub_event = await pubsub.listen_channel_subscriptions(sv["streamer"].id, on_sub)
    # whisper_event = await pubsub.listen_whispers(sv["streamer"].id, on_whisper)
    # bit_event = await pubsub.listen_bits(sv["streamer"].id, on_bits)
    

    btwitch = await Twitch(sv["id"], sv["secret"])    
    # await btwitch.set_user_authentication("fi7d5m18fm1zmcgfabax16xssvvddc", USER_SCOPE, "qudyvazycvc2ef557n0m4prkg84zbpafgbxkq1u2uxh2fck7jm")
    await btwitch.set_user_authentication("0iq7zso170ystonxazo4l2djh14r1z", USER_SCOPE, "b0yxlcle6le3z3ujfq6fi7kdgifz9229yq6dgscj36n4fd55r8")
    
    prompt ("success", "Connecting to Chat")
    
    sv["chat"] = await Chat(btwitch)
    sv["chat"].register_event(ChatEvent.READY, on_ready)
    sv["chat"].register_event(ChatEvent.MESSAGE, on_message)
    sv["chat"].register_event(ChatEvent.RAID, on_raid)
    sv["chat"].start()
    
    t_obs = threading.Thread(target = indexOBS)
    t_obs.start()
    
    t_alert = threading.Thread(target= manageAlerts)
    t_alert.start()
    
    t_actions = threading.Thread(target = timedActions)
    t_actions.start()

    ## Follower ====================================================================
    follower_data = {"newest":"", "newest-date":"", "oldest":"", "oldest-date":""}
    channel_follower_result = await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id)
    async for follower in channel_follower_result:
        follow_date = follower.followed_at.replace(tzinfo=pytz.UTC)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        followed = now - follow_date
        seconds = followed.days * 24 * 3600 + followed.seconds
     
        if follower_data["newest"] == "":
            follower_data["newest"] = follower.user_name
            follower_data["newest-date"] = seconds
        else:
            if seconds < follower_data["newest-date"]:
                follower_data["newest"] = follower.user_name
                follower_data["newest-date"] = seconds
        
        if follower_data["oldest"] == "":
            follower_data["oldest"] = follower.user_name
            follower_data["oldest-date"] = seconds
        else:
            if seconds > follower_data["oldest-date"]:
                follower_data["oldest"] = follower.user_name
                follower_data["oldest-date"] = seconds
                
    await updateVariable("latest-follower", follower_data["newest"])
    await updateVariable("oldest-follower", follower_data["oldest"])
    ## =============================================================================

    await addAlert({"type":"vayl-load"}, "0")
    
    while True:
        await asyncio.sleep(1)

## =================================================================================


## =================================================================================
## =================================================================================
##################################### ERRORS #######################################
## =================================================================================
## =================================================================================

error_reference = { "chat.moderation" : "Applying ModerationCheck to chat message.",
                    "chat.phrasecheck" : "Applying PhraseCheck to chat message.",
                    "chat.addquote" : "Attempting to add new quote.",
                    "obs.modifysource" : "Attempting to modify OBS source.",
                    "obs.scene" : "Attempting to switch OBS scene.",
                    "obs.label" : "Attempting to modify OBS label.",
                    "obs.image" : "Attempting to modify OBS image.",
                    "obs.mediafile" : "Attempting to modify OBS media file.",
                    "obs.slideshow" : "Attempting to modify OBS slideshow.",
                    "obs.filter" : "Attempting to access OBS source filter.",
                    "action.run" : "Attempting to run actions.",
                    "action.tags" : "Attempting to format action tags.",
                    "action.wait" : "Attempting to run 'wait' action.",
                    "action.chat" : "Attempting to run 'chat' action.",
                    "action.editfile" : "Attempting to run 'editfile' action.",
                    "action.text" : "Attempting to run 'text' action.",
                    "action.boolean" : "Attempting to run 'boolean' action.",
                    "action.oounter" : "Attempting to run 'counter' action.",
                    "action.list" : "Attempting to run 'list' action.",
                    "action.announce" : "Attempting to run 'announce' action.",
                    "action.vip" : "Attempting to run 'vip' action.",
                    "action.cmd" : "Attempting to run 'cmd' action.",
                    "action.playsound" : "Attempting to run 'playsound' action.",
                    "action.timeout" : "Attempting to run 'timeout' action.",
                    "action.console" : "Attempting to run 'console' action.",
                    "action.webhook" : "Attempting to run 'webhook' action.",
                    "action.conditional" : "Attempting to run 'conditional' action.",
                    "action.tts" : "Attempting to run 'tts' action.",
                    "action.clip" : "Attempting to run 'createclip' action",
                    "action.addmarker" : "Attempting to run 'addmarker' action",
                    "action.variables" : "Attempting to format actiion variables.",
                    "vayl.prompt" : "Attempting to print in Vayl console.",
                    "vayl.updatevariable" : "Attempting to update Vayl variable.",
                    "vayl.issubbed" : "Attempting to check if user is subscribed.",
                    "vayl.ismoderator" : "Attempting to check if user is a moderator.",
                    "vayl.isstreamer" : "Attempting to check if user is the streamer.",
                    "load.sfx" : "Attempting to load SFX data.",
                    "load.moderation" : "Attempting to load Moderation data.",
                    "load.commands" : "Attempting to load Custom Commands.",
                    "load.timedactions" : "Attempting to load Timed Actions.",
                    "load.phrases" : "Attempting to load PhraseCheck.",
                    "command.sfx" : "Attempting to run an SFX command.",
                    "command.sfxtoggle" : "Attempting to run '!sfxtoggle' command.",
                    "command.quote" : "Attempting to run '!quote' command.",
                    "command.quotes" : "Attempting to run '!quotes' command.",
                    "command.settitle" : "Attempting to run '!settitle' command.",
                    "command.setgame" : "Attempting to run '!setgame' command.",
                    "command.game" : "Attempting to run '!game' command.",
                    "command.uptime" : "Attempting to run '!uptime' command.",
                    "command.followage" : "Attempting to run '!followage' command.",
                    "command.custom" : "Attempting to run a custom command.",
                    "command.debug" : "Attempting to run '!debug' command.",
                    "command.reload" : "Attempting to run '!reload' command.",
                    "event.on_ready" : "Attempting to handle VaylReady event.",
                    "event.on_message" : "Attempting to handle Message event.",
                    "event.on_raid" : "Attempting to handle Raid event.",
                    "event.on_ad" : "Attempting to handle AD event.",
                    "event.on_shoutout_give" : "Attempting to handle ShoutoutGive event.",
                    "event.on_shoutout_receieve" : "Attempting to handle ShoutoutReceive event.",
                    "event.on_poll_start" : "Attempting to handle PollStart event.",
                    "event.on_poll_end" : "Attempting to handle PollEnd event.",
                    "event.on_prediction_start" : "Attempting to handle PredictionStart event.",
                    "event.on_prediction_lock" : "Attempting to handle PredictionLock event.",
                    "event.on_prediction_end" : "Attempting to handle PredictionEnd event.",
                    "event.on_hype_train" : "Attempting to handle HypeTrain event.",
                    "event.on_offline" : "Attempting to handle StreamOffline event.",
                    "event.on_online" : "Attempting to handle StreamOnline event.",
                    "event.on_follow" : "Attempting to handle Follow event.",
                    "event.on_sub" : "Attempting to handle Sub event.",
                    "event.on_bits" : "Attempting to handle Bit event.",
                    "event.on_redeem" : "Attempting to handle Redeem event.",
                    "stream.viewers" : "Attempting to fetch stream's viewercount.",
                    "debug.invalid" : "Attempting to debug an invalid event."
                    
                }

## =================================================================================

 
 
 
 
 
 
 
 
 
 
init()
asyncio.run(run())
