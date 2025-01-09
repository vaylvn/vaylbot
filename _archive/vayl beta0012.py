__version__ = "beta0012"

## Imports =========================================================================
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
# from multiprocessing import Pool
# from contextlib import suppress
from playsound3 import playsound
from colorama import Fore, Back, Style, init
from num2words import num2words

from textwrap import wrap
import tldextract
import subprocess
import traceback
import threading
import requests
# import win32gui
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


## Bot Variables ===================================================================
sv = { "id" : "xfc4596ekgo4ewkag6wn01hgs4hfbl", "secret" : "p8wl2zzuk3sgjmbdrlxe9l65xno8wk",
       "version" : "", "twitch" : None, "streamer" : None, "channel" : None, "chat" : None, "live" : False,
       "alerts" : [], "actions" : [], "commands" : {}, "sfx" : {}, "phrases" : {}, "moderation" : {}, "spoken" : [] }
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
        
        ## moderation ==================================================================
        try:
            if name.lower() != "vaylbot":
                
                ## link protection =========================================================
                flagged = []
                if len(sv["moderation"]["link"]["whitelist"]) > 0:
                    for word in msg.text.split(" "):
                        info = tldextract.extract(word)
                        if "http" in word or "www." in word or info.suffix != "":
                            allowed = False
                            for whitelist in sv["moderation"]["link"]["whitelist"]:
                                allowed = (whitelist in word)
                            if not allowed:
                                flagged.append(word)
                else:
                    for word in msg.text.split(" "):
                        for blacklist in sv["moderation"]["link"]["blacklist"]:
                            if blacklist in msg.text:
                                flagged.append(word)
                            
                if len(flagged) > 0:
                    if not await isModerator(sv["streamer"].id, name) and not await isStreamer(name) and name.lower() not in sv["moderation"]["link"]["permitted-users"]:
                        
                        if name not in sv["moderation"]["link"]["warnings"]:
                            sv["moderation"]["link"]["warnings"][name] = 0
                            
                        sv["moderation"]["link"]["warnings"][name] += 1
                        if sv["moderation"]["link"]["warnings"][name] >= int(sv["moderation"]["link"]["warning"]["limit"]):
                            
                            duration = int(sv["moderation"]["link"]["timeout"]["duration"])
                            
                            if len(sv["moderation"]["link"]["timeout"]["message"]) > 0:
                                await sv["chat"].send_message(sv["channel"], sv["moderation"]["link"]["timeout"]["message"].replace("[user]",name).replace("[duration]",str(duration)))
                                await sv["chat"].send_message(sv["channel"], "Warning " + str(sv["moderation"]["link"]["warnings"][name]) + " of " + str(sv["moderation"]["link"]["warning"]["limit"]))
                        
                            async for u in sv["twitch"].get_users(logins = [name]):
                                await sv["twitch"].ban_user(sv["streamer"].id, sv["streamer"].id, u.id, "Vayl Moderation (Link)", duration)
                        
                        else:
                            if len(sv["moderation"]["link"]["warning"]["message"]) > 0:
                                await sv["chat"].send_message(sv["channel"], sv["moderation"]["link"]["warning"]["message"].replace("[user]",name))

                        await sv["twitch"].delete_chat_message(sv["streamer"].id, sv["streamer"].id, msg.id)
                ## =========================================================================
                
                
                ## cap protection ==========================================================
                cap_count = 0
                for letter in msg.text:
                    if letter.isupper():
                        cap_count += 1
                        
                percentage = round(((cap_count / len(msg.text)) * 100))
                if percentage >= sv["moderation"]["cap"]["threshold-percentage"]:
                    if not await isModerator(sv["streamer"].id, name) and not await isStreamer(name) and name.lower() not in sv["moderation"]["link"]["permitted-users"]:
                        
                        if name not in sv["moderation"]["cap"]["warnings"]:
                            sv["moderation"]["cap"]["warnings"][name] = 0
                            
                        sv["moderation"]["cap"]["warnings"][name] += 1
                        if sv["moderation"]["cap"]["warnings"][name] >= int(sv["moderation"]["cap"]["warning"]["limit"]):
                            ## timeout user
                            
                            duration = int(sv["moderation"]["cap"]["timeout"]["duration"])
                            
                            if len(sv["moderation"]["cap"]["timeout"]["msg.text"]) > 0:
                                await sv["chat"].send_message(sv["channel"], sv["moderation"]["cap"]["timeout"]["msg.text"].replace("[user]",name).replace("[duration]",str(duration)))
                                await sv["chat"].send_message(sv["channel"], "Warning " + str(sv["moderation"]["cap"]["warnings"][name]) + " of " + str(sv["moderation"]["cap"]["warning"]["limit"]))
                        
                            async for u in sv["twitch"].get_users(logins = [name]):
                                await sv["twitch"].ban_user(sv["streamer"].id, sv["streamer"].id, u.id, "Vayl Moderation (Cap)", duration)
                        
                        else:
                            if len(sv["moderation"]["cap"]["warning"]["msg.text"]) > 0:
                                await sv["chat"].send_message(sv["channel"], sv["moderation"]["cap"]["warning"]["msg.text"].replace("[user]",name))

                        await sv["twitch"].delete_chat_message(sv["streamer"].id, sv["streamer"].id, msg.id)
                ## =========================================================================
        except Exception as e:
            logError(tag = "chat.moderation")
        ## =========================================================================

        
        ## phrase check ================================================================
        try:
            with open(os.getcwd() + "\\configuration\\phrases.yml", 'r', encoding = "utf-8") as file:
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
        if not sv["live"]:
            async for streams in sv["twitch"].get_streams(user_id = sv["streamer"].id):
                live = True
        else:
        
            ## first session chat ==========================================================
            if name not in sv["spoken"]:
                sv["spoken"].append(name)
                await addAlert({"type":"first-session-chat", "user":name, "message":msg.text},"0")
            ## =============================================================================
            
            ## first time chat =============================================================
            if "first-msg" in msg.__dict__["_parsed"]["tags"] and msg.__dict__["_parsed"]["tags"]["first-msg"] == "1":
                await addAlert({"type":"first-time-chat", "user":name, "message":msg.text},"0")
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
        await addAlert({"type":"raid","user":raid["tags"]["display-name"],"viewercount":raid["tags"]["msg-param-viewerCount"]}, "0")
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
            alert["option" + str(i)] = choice.__dict__["title"]
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
            for choice in data.event["choices"]:
                alert["option" + str(option_id)] = choice.__dict__["title"]
                alert["option" + str(option_id) + "bits"] = str(choice.__dict__["bits_votes"])
                alert["option" + str(option_id) + "points"] = str(choice.__dict__["channel_points_votes"])
                alert["option" + str(option_id) + "votes"] = str(choice.__dict__["votes"])
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
        await addAlert({"type":"hypetrain", "level":data.event.level, "conductor:bits":data.event.top_contributions[0].user_name, "conductor:subs":data.event.top_contributions[1].user_name}, "0")
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


## OnSub ===========================================================================
async def on_sub (d, data):
    try:
        alert = {}
        alert["tier"] = {"Prime":"prime","1000":"1","2000":"2","3000":"3"}[data["sub_plan"]]
        alert["type"] = "giftsub" if data["is_gift"] else "sub"
        alert["user"] = "" if data["is_gift"] else data["display_name"]
        alert["gifter"] = data["display_name"] if data["is_gift"] else ""
        alert["gifted"] = data["recipient_display_name"] if data["is_gift"] else ""
        alert["sub-message"] = "" if data["is_gift"] else data["sub_message"]["message"]
        alert["total-months"] = data["cumulative_months"] if data["is_gift"] else ""
        
        if data["is_gift"]:
            await updateVariable("latest-giftsub-gifter", data["display_name"])  
            await updateVariable("latest-giftsub-gifted", data["recipient_display_name"])  
        else:
            await updateVariable("latest-subscriber", data["display_name"])  
            alert["streak"] = data["streak_months"] if "streak_months" in data else 1
        
        await addAlert(alert, "end")
    except Exception as e:
        logError(tag = "event.on_sub")
## =================================================================================


## OnWhisper =======================================================================
async def on_whisper (d, data):
    pass
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
## =================================================================================


## OnRedeem ========================================================================
async def on_redeem (d, data):
    try:
        redeem = data["data"]["redemption"]
        alert = {"type":"redeem", "userid":redeem["user"]["id"], "user":redeem["user"]["display_name"], "userinput":"", "cost":redeem["reward"]["cost"]}
        if "user_input" in redeem:
            alert["user_input"] = redeem["user_input"]
            
        with open(os.getcwd() + "\\configuration\\redeems.yml", 'r', encoding = "utf-8") as file:
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
async def c_debug (cmd: ChatCommand):
    try:
        args = cmd.parameter.split(" ")
        if await isStreamer(cmd.user.name):
        
            if len(args) == 1:
                if args[0] in ["ad-break", "vayl-load", "stream-online", "stream-offline"]:
                    await addAlert({"type":args[0]}, "end")
            if len(args) == 2:
                if "hypetrain" in args[0] and args[1].isnumeric():
                    await addAlert({"type":"hypetrain","level":int(args[1])}, "end")
                if "first-time-chat" in args[0] and args[1].isalnum():
                    await addAlert({"type":"first-time-chat", "user":args[1]}, "end")
                if "first-session-chat" in args[0] and args[1].isalnum():
                    await addAlert({"type":"first-session-chat", "user":args[1]}, "end")
                if "follow" in args[0] and args[1].isalnum():
                    await addAlert({"type":"follow", "user":args[1]}, "end")
            if len(args) >= 2:
                if "raid" == args[0] and args[1].isalnum():
                    viewers = int(args[2]) if len(args) > 2 and args[2].isnumeric() else 1
                    await addAlert({"type":"raid", "user":args[1], "viewercount":viewers}, "end")
                if "shoutout-give" == args[0] and len(args) == 3 and args[1].isalnum() and args[2].isnumeric():
                    await addAlert({"type":"shoutout-created", "user":args[1], "viewercount":int(args[2])}, "end")
                if "shoutout-receive" == args[0] and len(args) == 3 and args[1].isalnum() and args[2].isnumeric():
                    await addAlert({"type":"shoutout-receive", "user":args[1], "viewercount":int(args[2])},"end")
            if len(args) >= 3:
                if "bits" in args[0] and args[1].isalnum() and args[2].isnumeric():
                    await addAlert({"type":"bits","user":args[1],"amount":int(args[2]),"message":"" if len(args) <= 3 else " ".join(args[3:])}, "end")
                elif "sub" in args[0] and args[1].isalnum() and args[2].isnumeric():
                    
                    tier = args[2].lower if args[2].lower() in ["1","2","3","prime"] else "1"
                    await addAlert({"type":"sub","tier":tier,"user":args[1],"total-months":args[2],"sub-message": "" if len(args) <= 3 else " ".join(args[3:]) }, "end")
            if len(args) == 4:
                if "giftsub" in args[0] and args[1].isalnum() and args[2].isalnum() and args[3].isnumeric():
                    for i in range(0, int(args[3])):
                        await addAlert({"type":"giftsub", "gifter":args[1], "tier":args[2], "gifted":"ExampleUsername"}, "end")
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

            
            if user not in sv["commands"][cmd.name]["user-cooldown"]:
                sv["commands"][cmd.name]["user-cooldown"][user] = 0
                
            with open(os.getcwd() + "\\configuration\\commands.yml", 'r', encoding = "utf-8") as file:
                data = yaml.full_load(file)
                
                if not await isStreamer(user):
                    if "streamer-only" in data and data["streamer-only"] == True:
                        return
                    if "sub-only" in data and data["sub-only"] == True and not await isSubbed(user):
                        return
                    if "mod-only" in data and data["mod-only"] == True and not await isModerator(sv["streamer"], user):
                        return
                    if "vip-only" in data and data["vip-only"] == True and not "vip" in cmd.user.badges:
                        return
                        
            if await isStreamer(user) or (time.time() - sv["commands"][cmd.name]["user-cooldown"][user] >= data["command"][command]["cooldown"]):
                command = {"user":user, "cmdtext":" ".join(arguments)}
                for i in range (0, 9999):
                    command["arg" + str(i)] = "" if i >= len(arguments) else (arguments[i].replace("@","",1))
                await runActions(data["command"][cmd.name]["actions"], command)
                sv["commands"][cmd.name]["user-cooldown"][user] = time.time()
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
        f = open(os.getcwd() + "\\data\\resources\\quotes.yml", 'a+', encoding = "utf-8")
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
        f = open(os.getcwd() + "\\data\\resources\\quotes.yml", 'r', encoding = "utf-8")
        total = len(f.readlines())
        await sv["chat"].send_message(sv["channel"], str(total) + " Available Quotes.")
    except Exception as e:
        logError(tag = "command.quotes")
## =================================================================================


## SFX Toggle ======================================================================
async def c_sfxtoggle (cmd: ChatCommand):
    try:
        if await isStreamer(cmd.user.name) or await isModerator(sv["streamer"].id, cmd.user.name):
            with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
                data = yaml.safe_load(file)
                data["enabled"] = not data["enabled"]
                with open(os.getcwd() + "\\configuration\\sfx.yml", 'w', encoding = "utf-8") as yaml_file:
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
        
            with open(os.getcwd() + "\\configuration\\sfx.yml", 'r', encoding = "utf-8") as file:
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
                        if os.path.exists(os.getcwd() + "\\data\\resources\\sounds\\" + data["sound"] + type):
                            playsound(os.getcwd() + "\\data\\resources\\sounds\\" + data["sound"] + type, block = False)
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
    sv["obs"] = {}
    
    while True:
    
        sv["obs"]["scenes"] = []
        sv["obs"]["groups"] = []
    
        try:
            cl = None
            with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
                data = yaml.safe_load(file)
                cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
                for scene in cl.get_scene_list().__dict__["scenes"]:
                    sv["obs"]["scenes"].append(scene["sceneName"])
                for group in cl.get_group_list().__dict__["groups"]:
                    sv["obs"]["groups"].append(group)
        except:
            pass
    
    
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
        pop_amount = 1
        
        if len(sv["alerts"]) > 0:
            
            alert = sv["alerts"][0]
            actions = []
            
            if "giftsub" in alert["type"]:
                alert["amount"] = 1
                for a in sv["alerts"][1:]:
                    if a["type"] == "giftsub" and a["gifter"] == alert["gifter"]:
                        alert["amount"] += 1
                        pop_amount += 1
            
            if "redeem" in alert["type"]:
                actions = alert["actions"]
                buffer = alert["buffer"]
            else:
                with open(os.getcwd() + "\\configuration\\event\\" + alert["type"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"] == True:
                        actions = data["actions"]
                        buffer = data["buffer"]
                        
                     
                    
            await runActions(actions, alert)
            for i in range(0, pop_amount):
                sv["alerts"].pop(0)
            
            
            continue
            
            ## generic =============================================================
            if alert["type"] in ["vayl-load", "ad-break", "prediction-created", "prediction-locked", "prediction-ended", "poll-created", "poll-ended", "first-time-chat", "stream-online", "stream-offline","chat", "follow"]:
                with open(os.getcwd() + "\\configuration\\event\\" + alert["type"] + ".yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        actions = data["actions"]
            ## =====================================================================
            
            
            ## first session chat ==================================================
            elif "firstsessionchat" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\first-session-chat.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "User sends first message of session":
                                if condition["value"].lower() == alert["user"].lower():
                                    actions = condition["actions"]
                                    break
            ## =====================================================================
            
            
            ## hypetrain ===========================================================
            elif "hypetrain" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\hype-train.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                        
                        complete = False
                        
                        ## specific level ==========================================
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "HypeTrain reaches level ..." and str(condition["value"]) == str(alert["level"]):
                                actions = condition["actions"]
                                complete = True
                                break
                        ## =========================================================
                        
                        
                        ## at least level ==========================================
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
                        ## =========================================================
                        
                        
                        ## any level ===============================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "HypeTrain reaches level ..." and str(condition["value"]) == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
            ## =====================================================================
            
            
            ## shoutout given ======================================================
            elif "shoutout-given" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\shoutout-given.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific user ===========================================
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "Given shoutout to user" and condition["value"].lower() == alert["user"].lower():
                                actions = condition["actions"]
                                complete = True
                                break
                        ## =========================================================
                        
                        
                        ## specifc viewercount =====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains ... viewers" and str(condition["value"]).lower() == str(alert["viewercount"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## at least viewercount ====================================
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
                        ## =========================================================
                        
                        
                        ## any =====================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Given shoutout to user" and str(condition["value"]).lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
            ## =====================================================================
            
            
            ## shoutout received ===================================================
            elif "shoutout-receive" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\shoutout-receieve.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific user ===========================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Received shoutout from user" and condition["value"].lower() == alert["user"].lower():
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                    
                    
                        ## specific viewercount ====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Shoutout contains ... viewers" and str(condition["value"]) == str(alert["viewercount"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                    
                    
                        ## at least viewercount ====================================
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
                        ## =========================================================
                    
                    
                        ## any =====================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Received shoutout from user" and str(condition["value"]).lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
            ## =====================================================================
            
            
            ## sub =================================================================
            elif "sub" == alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\sub.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific user ===========================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User subs" and condition["value"].lower() == alert["user"].lower():
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================    
                            
                            
                        ## specific sub month streak ===============================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... month sub streak" and str(condition["value"]) == str(alert["streak"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================  
                        
                        
                        ## at least sub month streak ===============================
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
                        ## =========================================================  
                                    
                                    
                        ## any sub month streak ====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... month sub streak" and str(condition["value"]) == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================  
                        
                                    
                        ## specific sub month total ================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User on ... total sub months" and str(condition["value"]) == str(alert["total-months"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================  
                                        
                                        
                        ## at least sub month total ================================
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
                        ## =========================================================  
                        
                                    
                        ## specific user ===========================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User subs" and condition["value"].lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================  
            ## =====================================================================
            
            
            ## giftsub =============================================================
            elif "giftsub" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\giftsub.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
            
                        alert["amount"] = 1
                        for a in sv["alerts"][1:]:
                            if a["type"] == "giftsub" and a["gifter"] == alert["gifter"]:
                                alert["amount"] += 1
                        
                        complete = False
                        
                        ## specific user ===========================================
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "User gifts subs" and condition["value"].lower() == alert["gifter"].lower():
                                actions = condition["actions"]
                                complete = True
                                break
                        ## =========================================================
                        
                        
                        ## specific sub amount =====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts ... subs" and str(condition["value"]) == str(amount):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## more than sub amount ====================================
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
                        ## =========================================================
                        
                        
                        ## any user ================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts subs" and condition["value"].lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## giftsub was tier x ======================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts tier ... sub" and str(condition["value"]) == str(alert["tier"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## any =====================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts subs" and condition["value"].lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        new_sv["alerts"] = []
                        for i in range(0, len(sv["alerts"])):
                            if sv["alerts"][i]["type"] == "giftsub":
                                if sv["alerts"][i]["gifter"] != alert["gifter"]:
                                    new_sv["alerts"].append(sv["alerts"][i])
                            else:
                                new_sv["alerts"].append(sv["alerts"][i])
                        sv["alerts"] = new_sv["alerts"]
                        await runActions(actions, alert)
                        continue
            ## =====================================================================
            
            
            ## bits ================================================================
            elif "bits" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\bits.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific user ===========================================
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "User gifts bits" and condition["value"].lower() == alert["user"].lower():
                                actions = condition["actions"]
                                complete = True
                                break
                        ## =========================================================
                        
                        
                        ## specific bit amount =====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts ... bits" and str(condition["value"]) == str(alert["amount"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## more than bit amount ====================================
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
                        ## =========================================================
                        
                        
                        ## any =====================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User gifts bits" and condition["value"].lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
            ## =====================================================================
            
            
            ## raids ===============================================================
            elif "raid" in alert["type"]:
                with open(os.getcwd() + "\\configuration\\event\\raid.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    if "enabled" in data and data["enabled"]:
                    
                        complete = False
                        
                        ## specific user ===========================================
                        for conditional, condition in data["conditionals"].items():
                            if condition["condition"] == "User raids the channel" and condition["value"].lower() == alert["user"].lower():
                                actions = condition["actions"]
                                complete = True
                                break
                        ## =========================================================
                        
                        
                        ## specific viewercount ====================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "Raid contains ... viewers" and str(condition["value"]) == str(alert["viewercount"]):
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
                        
                        ## more than viewercount ===================================
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
                        ## =========================================================
                        
                        
                        ## any =====================================================
                        if not complete:
                            for conditional, condition in data["conditionals"].items():
                                if condition["condition"] == "User raids the channel" and condition["value"].lower() == "any":
                                    actions = condition["actions"]
                                    complete = True
                                    break
                        ## =========================================================
                        
            ## =====================================================================
            
            
            await runActions(actions, alert)
            for i in range(0, pop_amount):
                sv["alerts"].pop(0)
            
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
                            "editfile"       : ["filepath", "modifier", "text"],
                            "text"           : ["name", "modifier", "text"],
                            "counter"        : ["name", "modifier", "amount"],
                            "boolean"        : ["name", "value"],
                            "console"        : ["message"],
                            "list"           : ["name", "modifier", "text"],
                            "conditional"    : ["name"],
                            "tts"            : ["voice", "message", "halt", "limit"],
                            "cmd"            : ["command"],
                            "announce"       : ["message", "color"],
                            "vip"            : ["modifier", "usernmae"],
                            "webhook"        : ["name"],
                            "createclip"     : []}

    for a in actions:
    
        
        action = a.split(" ; ")[0]
        arguments = a.split(" ; ")[1:]
        
        if cl is None:
            if action in ["obs:scene","obs:show","obs:hide","obs:toggle","obs:label","obs:image","obs:mediafile","obs:slideshow", "obs:filter"]:
                with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
                    data = yaml.safe_load(file)
                    cl = obs.ReqClient(host='localhost', port=4455, password = data["obs-password"])
        
        adata = {}
        for i in range(0, len(arguments)):
            adata[action_requirements[action][i]] = arguments[i]
                                
                
        
        # adata = { "obs:scene"      : { "scene":arguments[0] },
        #          "obs:show"       : { "source":arguments[0] },
        #          "obs:hide"       : { "source":arguments[0] },
        #          "obs:toggle"     : { "source":arguments[0] },
        #          "obs:label"      : { "source":arguments[0], "text":arguments[1], "color":arguments[2] },
        #          "obs:mediafile"  : { "source":arguments[0], "filepath":arguments[1] },
        #          "obs:slideshow"  : { "source":arguments[0], "state":arguments[1] },
        #          "playsound"      : { "sound":"" },
        #          "wait"           : { "time":0 },
        #          "chat"           : { "message":"" },
        #          "editfile"       : { "filepath":"", "action":"", "text":"" },
        #          "variable"       : { "name":"", "text":"" },
        #          "counter"        : { "name":"", "modifier":"", "amount":0 },
        #          "boolean"        : { "name":"", "modifier":"", "value":None },
        #          "console"        : { "message":"" },
        #          "list"           : { "name":"", "modifier":"", "text":"" },
        #          "conditional"    : { "name":"" },
        #          "tts"            : { "voice":"", "message":"", "halt":True, "cutoff":99999999 },
        #          "cmd"            : { "command":"" },
        #          "announce"       : { "message":"", "color":"default" },
        #          "vip"            : { "modifier":"", "username":"" },
        #          "webhook"        : { "name":"" }}

        try:
            for key, value in adata.items():
            
                for variable in variables:
                    adata[key] = adata[key].replace("[" + variable + "]", str(variables[variable]))

                for type in ["counter","text","list","boolean"]:
                    if "[" + type + ":" in value:
                        type = type.replace("variable","text")
                        name = adata[key].split("[" + type + ":")[1].split("]")[0]
                        try:
                            with open(os.getcwd() + "\\data\\variables\\" + type + "\\" + name + ".txt", "r", encoding = "utf-8") as f:
                                list = []
                                for line in f.readlines():
                                    list.append(line.rstrip())
                                adata[key] = adata[key].replace("[" + type + ":" + name + "]", ", ".join(list))
                        except Exception as e:
                            pass
                            # print (e)
                
                def randomNumber (match):
                    min_value = int(match.group(1))
                    max_value = int(match.group(2))
                    return str(random.randint(min_value, max_value))
                
                if "[rnumber:" in adata[key]:
                    adata[key] = re.sub(r"\[rnumber:(\d+)-(\d+)\]", randomNumber, adata[key])
                    
                if "[rfollower]" in adata[key]:
                    followers = []
                    async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                        followers.append(follower.user_name)
                    followers.remove("VaylBot")
                    
                    def randomFollower (match):
                        return str(random.choice(followers))
                    
                    adata[key] = re.sub(r"\[rfollower\]", randomFollower, adata[key])

                if "[ruser]" in adata[key]:
                    chatters = []
                    async for chatter in await sv["twitch"].get_chatters(sv["streamer"].id, sv["streamer"].id):
                        chatters.append(chatter.user_name)
                    chatters.remove("VaylBot")
                    
                    def randomUser (match):
                        return str(random.choice(chatters))
                    
                    adata[key] = re.sub(r"\[ruser\]", str(random.choice(chatters)), adata[key])

                def randomList (match):
                    name = match.group(1)
                    with open(os.getcwd() + "\\data\\variables\\list\\" + name + ".txt", 'r', encoding = "utf-8") as f:
                        return str(random.choice(f.read().splitlines()))

                if "[rlist:" in adata[key]:
                    name = adata[key].split("[rlist:")[1].split("]")[0]
                    with open(os.getcwd() + "\\data\\variables\\list\\" + name + ".txt", 'r', encoding = "utf-8") as f:
                        data = f.read().splitlines()
                        adata[key] = re.sub(r"\[rlist:([a-zA-Z0-9_]+)\]", randomList, adata[key])
        
                if "[system:dateus]" in adata[key]:
                    adata[key] = re.sub(r"\[system:dateus\]", date.today().strftime("%m/%d/%y"), adata[key])

                if "[system:dateuk]" in adata[key]:
                    adata[key] = re.sub(r"\[system:dateuk\]", date.today().strftime("%d/%m/%y"), adata[key])
                    
                if "[system:time]" in adata[key]:
                    adata[key] = re.sub(r"\[system:time\]", datetime.now().strftime("%H:%M:%S"), adata[key])
        
                def repeatString (match):
                    text = match.group(1)  # Extract the text part
                    amount = int(match.group(2))  # Extract the amount as an integer
                    return text * amount

                if "[xstring:" in adata[key]:
                    string = adata[key].split(":")[1]
                    amount = adata[key].split(":")[2].split("]")[0]
                    adata[key] = re.sub(r"\[xstring:([^\:]+):(\d+)\]", repeatString, adata[key])

        

   
        except Exception as e:
            logError(tag = "action.variables")


        ## ModifySource ============================================================
        def modifySource (source_name, source_action):
            try:
                found = False
                for scene in sv["obs"]["scenes"]:
                    for item in cl.get_scene_item_list(scene).__dict__["scene_items"]:
                        if source_name == item["sourceName"]:
                            id = cl.get_scene_item_id(scene, adata["source"], offset = None).__dict__["scene_item_id"] 
                            if "show" in source_action or "hide" in source_action:
                                cl.set_scene_item_enabled(scene, id, True if "show" in source_action else False)
                            else:
                                enabled = bool(cl.get_scene_item_enabled(scene, id).__dict__["scene_item_enabled"])
                                cl.set_scene_item_enabled(scene, id, not enabled)
                            found = True
                if not found:
                    for group in sv["obs"]["groups"]:
                        for item in cl.get_group_scene_item_list(group).__dict__["scene_items"]:
                            if source_name in item["sourceName"]:
                                id = cl.get_scene_item_id(group, adata["source"], offset = None).__dict__["scene_item_id"] 
                                if "show" in source_action or "hide" in source_action:
                                    cl.set_scene_item_enabled(group, id, True if "show" in source_action else False)
                                else:
                                    enabled = bool(cl.get_scene_item_enabled(group, id).__dict__["scene_item_enabled"])
                                    cl.set_scene_item_enabled(group, id, not enabled)
                            found = True
                if not found:
                    prompt ("misc", "Unable to find source: " + adata["source"])
            except Exception as e:
                logError(tag = "obs.modifysource")
        ## =========================================================================


        ## obs:scene ===============================================================
        if action == "obs:scene":
            try:
                if adata["scene"] in sv["obs"]["scenes"]:
                    cl.set_current_program_scene(adata["scene"])
                else:
                    prompt ("error", "Scene not found: " + adata["scene"])
            except Exception as e:
                logError(tag = "obs.scene")
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
                logError(tag = "obs.label")
        ## =========================================================================
        
        
        ## obs:image ===============================================================
        if action == "obs:image":
            try:
                image = cl.get_input_settings(adata["source"]).__dict__
                data = dict(image["input_settings"])
                data["file"] = adata["filepath"]
                cl.set_input_settings(adata["source"], data, True)
            except Exception as e:
                logError(tag = "obs.image")
        ## =========================================================================

        
        ## obs:mediafile ===========================================================
        if action == "obs:mediafile":
            try:
                mediafile = cl.get_input_settings(adata["source"]).__dict__
                data = dict(mediafile["input_settings"])
                data["local_file"] = adata["filepath"]
                cl.set_input_settings(adata["source"], data, True)
            except Exception as e:
                logError(tag = "obs.mediafile")
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
                logError(tag = "obs.slideshow")
        ## =========================================================================

        
        ## obs:filter ==============================================================
        if action == "obs:filter":
            try:
                cl.set_source_filter_enabled(adata["source"], adata["filter"], (adata["enabled"].lower() == "true"))
            except Exception as e:
                logError(tag = "obs.filter")
        ## =========================================================================
        
        
        ## wait ====================================================================
        if action == "wait":
            try:
                await asyncio.sleep(float(adata["time"]))
            except Exception as e:
                logError(tag = "action.wait")
        ## =========================================================================


        ## chat ====================================================================
        if action == "chat":
            try:
                await sv["chat"].send_message(sv["channel"], adata["message"])
            except Exception as e:
                logError(tag = "action.chat")
        ## =========================================================================


        ## editfile ================================================================
        if action == "editfile":
            try:
                with open(adata["path"], 'r', encoding = "utf-8") as f:
                    data = f.read()
                    if adata["action"] == "overwrite":
                        try:
                            with open(adata["path"], 'w', encoding = "utf-8") as file:
                                file.write(adata["text"])
                        except Exception as e:
                            with open(adata["path"], 'w', encoding = "utf-8") as file:
                                file.write(data)
                    elif adata["action"] == "append":
                        try:
                            with open(adata["path"], 'a', encoding = "utf-8") as file:
                                file.write(adata["text"])
                        except Exception as e:
                            with open(adata["path"], 'w', encoding = "utf-8") as file:
                                file.write(data)
            except Exception as e:
                logError(tag = "action.editfile")
        ## =========================================================================


        ## text ====================================================================
        if action == "text":
            try:
                text = ""
                try:
                    with open(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as f:
                        text = f.read()
                except:
                    pass
                with open(os.getcwd() + "\\data\\variables\\text\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(text + str(adata["text"]) if adata["modifier"] == "append" else str(adata["text"]))
            except Exception as e:
                logError(tag = "action.text")
        ## =========================================================================
        
        
        ## boolean =================================================================
        if action == "boolean":
            try:
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
                logError(tag = "action.boolean")
        ## =========================================================================
        
        
        ## counter =================================================================
        if action == "counter":
            try:
                counter = 0
                try:
                    with open(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt", 'r', encoding = "utf-8") as file:
                        counter = float(file.read())
                except:
                    pass
                adata["amount"] = float(adata["amount"])
                modification = {"increase":(counter + adata["amount"]), "decrease":(counter - adata["amount"]), "multiply":(counter * adata["amount"]), "divide":(counter / adata["amount"]), "set":adata["amount"]}
                counter = modification[adata["modifier"]]
                counter = round(counter) if ".0" in str(round(counter, 1)) else round(counter, 1) 
                with open(os.getcwd() + "\\data\\variables\\counter\\" + adata["name"] + ".txt", 'w', encoding = "utf-8") as file:
                    file.write(str(counter))
            except Exception as e:
                logError(tag = "action.counter")
        ## =========================================================================


        ## list ====================================================================
        if action == "list":
            try:
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
                logError(tag = "action.list")
        ## =========================================================================


        ## announce ================================================================
        if action == "announce":
            try:
                await sv["twitch"].send_chat_announcement(sv["streamer"].id, sv["streamer"].id, adata["message"], adata["color"])
            except Exception as e:
                logError(tag = "action.announce")
        ## =========================================================================

    
        ## vip =====================================================================
        if action == "vip":
            try:
                if adata["modifier"] == "add":
                    await sv["twitch"].add_channel_vip(sv["streamer"].id, adata["username"])
                elif adata["modifier"] == "remove":
                    await sv["twitch"].remove_channel_vip(sv["streamer"].id, adata["username"])
            except Exception as e:
                logError(tag = "action.vip")
        ## =========================================================================
        

        ## cmd =====================================================================
        if action == "cmd":
            try:
                subprocess.run(adata["command"], shell = False)
            except Exception as e:
                logError(tag = "action.cmd")
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
                logError(tag = "action.playsound")
        ## =========================================================================

    
        ## timeout =================================================================
        if action == "timeout":
            try:
                async for u in sv["twitch"].get_users(logins = [adata["username"]]):
                    await sv["twitch"].ban_user(sv["streamer"].id, sv["streamer"].id, u.id, adata["reason"], int(adata["time"]))
            except Exception as e:
                logError(tag = "action.timeout")
        ## =========================================================================


        ## log =====================================================================
        if action == "console":
            try:
                await sendToConsole(adata["message"])
            except Exception as e:
                logError(tag = "action.console")
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
                logError(tag = "action.webhook")
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
                
                condition = data["condition"]
                
                for tag in variables:
                    condition = condition.replace("[" + tag + "]", str(variables[tag]))
                                          
                if "[rfollower]" in condition:
                    followers = []
                    async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                        followers.append(follower.user_name)
                    followers.remove("VaylBot")
                    
                    def randomFollower (match):
                        return str(random.choice(followers))
                    
                    condition = re.sub(r"\[rfollower\]", randomFollower, condition)

                if "[ruser]" in condition:
                    chatters = []
                    async for chatter in await sv["twitch"].get_chatters(sv["streamer"].id, sv["streamer"].id):
                        chatters.append(chatter.user_name)
                    chatters.remove("VaylBot")
                    
                    def randomUser (match):
                        return str(random.choice(chatters))
                    
                    condition = re.sub(r"\[ruser\]", str(random.choice(chatters)), condition)
                    
                if "[system:dateus]" in condition:
                    condition = re.sub(r"\[system:dateus\]", date.today().strftime("%m/%d/%y"), condition)

                if "[system:dateuk]" in condition:
                    condition = re.sub(r"\[system:dateuk\]", date.today().strftime("%d/%m/%y"), condition)
                    
                if "[system:time]" in condition:
                    condition = re.sub(r"\[system:time\]", datetime.now().strftime("%H:%M:%S"), condition)
                    
                if "[uptime:seconds]" in condition:
                    uptime = streams.started_at.replace(tzinfo=pytz.UTC)
                    now = datetime.now(tz=pytz.UTC)
                    condition = re.sub(r"\[uptime:seconds\]", str(int((now - uptime).total_seconds())), condition)
                
                for word in condition.split(" "):
                    if "[counter:" in word:
                        with open(os.getcwd() + "\\data\\variables\\counter\\" + word.split("[counter:")[1][:-1] + ".txt", "r", encoding = "utf-8") as f:
                            condition = condition.replace("[counter:" + word.split("[counter:")[1][:-1] + "]", f.read())
                    
                    if "[text:" in word:
                        with open(os.getcwd() + "\\data\\variables\\text\\" + word.split("[text:")[1][:-1] + ".txt", "r", encoding = "utf-8") as f:
                            condition = condition.replace("[text:" + word.split("[text:")[1][:-1] + "]", '"' + f.read() + '"')
                        
                    if "[boolean:" in word:
                        with open(os.getcwd() + "\\data\\variables\\boolean\\" + word.split("[boolean:")[1][:-1] + ".txt", "r", encoding = "utf-8") as f:
                            condition = condition.replace("[boolean:" + word.split("[boolean:")[1][:-1] + "]", f.read().capitalize())

                    if "[list:" in word:
                        with open(os.getcwd() + "\\data\\variables\\list\\" + word.split("[list:")[1][:-1] + ".txt", "r", encoding = "utf-8") as f:
                            condition = condition.replace("[list:" + word.split("[list:")[1][:-1] + "]", '["' + '", "'.join(f.read().splitlines()) + '"]')

                    def randomNumber (match):
                        min_value = int(match.group(1))
                        max_value = int(match.group(2))
                        return str(random.randint(min_value, max_value))

                    if "[rnumber:" in word:
                        min = word.split("[rnumber:")[1].split("-")[0]
                        max = word.split("[rnumber:")[1].split("-")[1][:-1]
                        condition = re.sub(r"\[rnumber:(\d+)-(\d+)\]", randomNumber, condition)

                    def randomList (match):
                        name = match.group(1)
                        with open(os.getcwd() + "\\data\\variables\\list\\" + name + ".txt", 'r', encoding = "utf-8") as f:
                            return str(random.choice(f.read().splitlines()))
                            
                    if "[rlist:" in word:
                        name = word.split("[rlist:")[1].split("]")[0]
                        with open(os.getcwd() + "\\data\\variables\\list\\" + name + ".txt", 'r', encoding = "utf-8") as f:
                            data = f.read().splitlines()
                            condition = re.sub(r"\[rlist:([a-zA-Z0-9_]+)\]", randomList, condition)

                    def repeatString (match):
                        text = match.group(1)  # Extract the text part
                        amount = int(match.group(2))  # Extract the amount as an integer
                        return text * amount

                    if "[xstring:" in word:
                        string = word.split(":")[1]
                        amount = word.split(":")[2].split("]")[0]
                        condition = re.sub(r"\[xstring:([^\:]+):(\d+)\]", repeatString, condition)

                # print ("condition: " + condition)
                # print (eval(condition))
                
                result = eval(condition)
                await runActions(data[result], variables)
                            
            except Exception as e:
                logError(tag = "action.conditional")
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
                                
                                    file_path = os.path.join(os.getcwd(),"data","resources","tts.wav")
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
                                            
                                    await asyncio.sleep(1)
                                    playsound(file_path, block = (adata["halt"] == "true"))
                                
                                break
                    
                else:
                    await sv["chat"].send_message(sv["channel"], "Unable to play TTS, message length exceeds limit of " + adata["limit"] + " characters. (" + str(len(adata["message"])) + ")")
                    prompt("misc", "Unable to play TTS, message length exceeds limit of " + adata["limit"] + " characters. (" + str(len(adata["message"])) + ")")
            
            except Exception as e:
                logError(tag = "action.tts")
        ## =========================================================================
        
        
        ## createclip ==============================================================
        if action == "createclip":
            clip = await sv["twitch"].create_clip(sv["streamer"].id)
            clips = await sv["twitch"].get_clips(broadcaster_id = sv["streamer"].id, clip_id = clip.id)
            async for c in clips:
                await updateVariable("latest-vayl-clip", c.url)
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
        
        
        

    '''         
    for line in lines:
        line = (" " * 20) + line.replace("#", Style.BRIGHT + Fore.RED + "#" + Style.RESET_ALL).replace(".", Style.BRIGHT + Fore.WHITE + "#" + Style.RESET_ALL)
        print (line)
    '''
                  

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
        
    ## Moderation ==================================================================
    try:
        if not chat:
            sv["moderation"] = {}
            for option in ["link","cap"]:
                with open(os.getcwd() + "\\configuration\\moderation\\" + option + "-protection.yml", "r", encoding = "utf-8") as file:
                    data = yaml.full_load(file)
                    data["warnings"] = {}
                    sv["moderation"][option] = data
    except:
        logError(tag = "load.moderation")
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
def logError (tag = None):

    prompt ("error", "Error Detected")
    with open(os.getcwd() + "\\data\\logs\\ref.yml", 'r', encoding = "utf-8") as file:
        data = yaml.safe_load(file)
        reference = data["reference"][tag] if tag is not None and tag in data["reference"] else "Undefined"
        prompt ("blank", "Cause: " + reference)
        log = ["User: " + sv["channel"], "Version: " + __version__, "Cause: " + reference]
    
    timestamp = str(time.time())
    with open (os.getcwd() + "\\data\\logs\\" + timestamp + ".txt", 'w') as log_file:
        for line in log:
            log_file.write(line + "\n")
        log_file.write(traceback.format_exc())
    
    try:    
        with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            if "bug-auto-report" in data and data["bug-auto-report"]:
                with open (os.getcwd() + "\\data\\logs\\" + timestamp + ".txt", 'r') as log_file:
                    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/1257675918957351013/wiIdAeOQBaXdhzyLrPRhplWz2mBbfZrTbch--c-5wMYDu1YYk2gUexBj6AUMTahnPlZs", username = "Bug Report", avatar_url = "https://i.ibb.co/ZHwjkms/icon.png")
                    webhook.add_file(file = log_file.read(), filename= timestamp + ".txt")
                    response = webhook.execute()
    except Exception as e:
        pass
## =================================================================================


## Update Variable =================================================================
async def updateVariable (name, value):
    try:
        with open(os.getcwd() + "\\data\\variables\\vayl\\" + name + ".txt", 'w', encoding = "utf-8") as file:
            file.write(value)    
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
    await eventsub.listen_stream_offline(sv["streamer"].id, on_offline)
    await eventsub.listen_channel_ad_break_begin(sv["streamer"].id, on_ad)
    await eventsub.listen_channel_poll_begin(sv["streamer"].id, on_poll_start)
    await eventsub.listen_channel_poll_end(sv["streamer"].id, on_poll_end)
    await eventsub.listen_channel_prediction_begin(sv["streamer"].id, on_prediction_start)    
    await eventsub.listen_channel_prediction_lock(sv["streamer"].id, on_prediction_lock)   
    await eventsub.listen_channel_prediction_end(sv["streamer"].id, on_prediction_end)   
    await eventsub.listen_hype_train_begin(sv["streamer"].id, on_hype_train)   
    await eventsub.listen_channel_shoutout_create(sv["streamer"].id, sv["streamer"].id, on_shoutout_give)
    await eventsub.listen_channel_shoutout_receive(sv["streamer"].id, sv["streamer"].id, on_shoutout_receive)
    
    prompt ("success", "Registering PubSub")
    
    pubsub = PubSub(sv["twitch"])
    pubsub.start()
    redeem_event = await pubsub.listen_channel_points(sv["streamer"].id, on_redeem)
    sub_event = await pubsub.listen_channel_subscriptions(sv["streamer"].id, on_sub)
    whisper_event = await pubsub.listen_whispers(sv["streamer"].id, on_whisper)
    bit_event = await pubsub.listen_bits(sv["streamer"].id, on_bits)
    
    btwitch = await Twitch(sv["id"], sv["secret"])    
    await btwitch.set_user_authentication("fi7d5m18fm1zmcgfabax16xssvvddc", USER_SCOPE, "qudyvazycvc2ef557n0m4prkg84zbpafgbxkq1u2uxh2fck7jm")

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
 
init()
asyncio.run(run())
