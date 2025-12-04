## Imports =========================================================================
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from discord_webhook import DiscordWebhook, DiscordEmbed
# from twitchAPI.object.eventsub import ChannelFollowEvent, StreamOnlineEvent, StreamOfflineEvent, ChannelPollBeginEvent, ChannelPollEndEvent, ChannelPredictionEvent, ChannelPredictionEndEvent, HypeTrainEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, ChannelAdBreakBeginEvent, ChannelSubscribeEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelCheerEvent, ChannelPointsCustomRewardRedemptionAddEvent, ChannelPointsCustomRewardRedemptionUpdateEvent
from twitchAPI.object.eventsub import ChannelFollowEvent, StreamOnlineEvent, StreamOfflineEvent, ChannelPollBeginEvent, ChannelPollEndEvent, ChannelPredictionEvent, ChannelPredictionEndEvent, HypeTrainEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, ChannelAdBreakBeginEvent, ChannelSubscribeEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelCheerEvent, ChannelPointsCustomRewardRedemptionAddEvent, ChannelPointsCustomRewardRedemptionUpdateEvent, ChannelVIPAddEvent, ChannelVIPRemoveEvent, CharityCampaignStartEvent, CharityDonationEvent, CharityCampaignProgressEvent, CharityCampaignStopEvent, GoalEvent, ChannelBanEvent, ChannelUnbanEvent, ChannelRaidEvent

from twitchAPI.eventsub.websocket import EventSubWebsocket
from datetime import datetime, timedelta, date, timezone
from dateutil.relativedelta import relativedelta

from collections import OrderedDict
from twitchAPI.helper import first
from playsound3 import playsound


from num2words import num2words
from collections import deque

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markup import render

console = Console()
logs = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]


import difflib
import socket

from textwrap import wrap
import tldextract
import subprocess
import traceback
import threading

import requests
import asyncio
import random
import yaml
import time
import json
import uuid
import pytz
import math
import sys
import os
import re

from pyt2s.services import stream_elements
from pyt2s.services import streamlabs
from pyt2s.services import oddcast

import obsws_python as obs

import tkinter as tk
import customtkinter as ctk



CONSOLE_UI_ENABLED = False

## =================================================================================


## TTS =============================================================================
tts_voicepack = {"oddcast":oddcast, "streamelements":stream_elements, "streamlabs":streamlabs }
tts_voice = { "oddcast"         : ["4-3-1", "6-2-1", "5-4-1", "4-2-1", "5-3-1", "2-7-1", "1-7-1", "7-4-1", "5-2-1", "12-4-1", "8-4-1", "9-2-1", "10-2-1", "4-7-1", "4-4-1", "10-4-1", "3-7-1", "13-4-1", "5-7-1", "6-7-1", "9-4-1", "11-2-1", "7-2-1", "6-3-1", "8-3-1", "7-7-1", "3-1-1", "1-1-1", "2-2-1", "7-3-1", "2-4-1", "3-3-1", "1-3-1", "2-1-1", "2-3-1", "4-1-1", "11-4-1", "8-2-1", "1-2-1", "3-4-1", "8-7-1", "1-7-27", "2-7-27", "2-2-27", "1-4-27", "1-2-27", "1-4-22", "3-2-5", "2-2-5", "1-2-5", "1-4-5", "3-3-10", "5-3-10", "4-3-10", "1-2-10", "2-2-10", "4-4-10", "4-7-10", "6-3-10", "7-3-10", "1-4-10", "3-7-10", "2-7-10", "1-7-10", "2-4-10", "8-3-10", "1-7-18", "1-4-18", "1-7-19", "2-7-19", "1-2-19", "1-4-19", "2-2-19", "2-4-11", "2-7-11", "1-7-11", "2-2-11", "1-2-11", "4-4-11", "1-4-11", "1-2-31", "2-7-32", "1-7-32", "2-2-23", "1-4-23", "1-2-23", "1-7-23", "2-1-4", "2-7-4", "1-7-4", "2-2-4", "4-2-4", "3-2-4", "1-1-4", "4-3-4", "3-3-4", "3-4-4", "5-4-4", "4-4-4", "5-2-4", "1-3-4", "1-4-4", "4-7-4", "2-4-4", "2-3-4", "3-7-4", "6-2-4", "3-1-4", "1-2-15", "3-4-3", "2-7-3", "1-7-3", "3-2-3", "1-1-3", "1-3-3", "2-1-3", "2-2-3", "1-4-3", "2-3-3", "2-4-3", "1-2-8", "1-4-8", "1-7-8", "2-7-8", "3-2-8", "2-7-24", "1-4-24", "1-7-24", "1-4-29", "1-7-29", "2-7-28", "1-4-28", "1-7-28", "2-7-7", "1-7-7", "1-3-7", "10-2-7", "9-2-7", "5-2-7", "6-2-7", "8-2-7", "1-2-7", "1-4-7", "7-2-7", "2-3-7", "2-2-7", "2-4-7", "3-2-7", "6-3-12", "5-3-12", "1-7-12", "2-7-12", "1-4-12", "3-3-12", "7-3-12", "4-3-12", "2-3-12", "8-3-12", "7-3-13", "4-3-13", "8-3-13", "10-3-13", "5-3-13", "2-3-13", "1-4-13", "6-3-13", "1-3-13", "9-3-13", "1-7-20", "2-2-20", "2-7-20", "2-4-20", "1-2-20", "1-4-14", "1-7-14", "2-2-14", "2-7-14", "1-2-14", "2-7-6", "3-4-6", "3-7-6", "4-7-6", "1-7-6", "1-3-6", "2-3-6", "2-4-6", "1-2-30", "1-4-30", "2-2-21", "2-4-21", "1-2-21", "1-7-37", "3-4-37", "1-2-2", "6-2-2", "2-2-2", "9-2-2", "4-3-2", "5-3-2", "1-4-2", "3-4-2", "7-2-2", "8-2-2", "10-2-2", "4-2-2", "3-2-2", "2-1-2", "5-2-2", "2-3-2", "3-3-2", "5-4-2", "4-4-2", "1-1-2", "1-3-2", "1-4-9", "1-2-9", "1-7-9", "2-7-9", "3-4-9", "2-2-9", "1-4-26", "1-3-26", "2-3-26", "1-4-16", "2-7-16", "1-2-16", "3-2-16", "1-7-16", "2-2-16", "1-7-40"],
              "streamelements"  : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Mia", "Miguel", "Penelope", "Astrid", "Filiz", "Gwyneth", "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E", "en-US-Wavenet-F", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D", "en-AU-Standard-C", "en-AU-Standard-D", "en-IN-Wavenet-A", "en-IN-Wavenet-B", "en-IN-Wavenet-C", "af-ZA-Standard-A", "ar-XA-Wavenet-A", "ar-XA-Wavenet-B", "ar-XA-Wavenet-C", "bg-bg-Standard-A", "cmn-CN-Wavenet-A", "cmn-CN-Wavenet-B", "cmn-CN-Wavenet-C", "cmn-CN-Wavenet-D", "cs-CZ-Wavenet-A", "da-DK-Wavenet-A", "nl-NL-Standard-A", "nl-NL-Wavenet-A", "nl-NL-Wavenet-B", "nl-NL-Wavenet-C", "nl-NL-Wavenet-D", "nl-NL-Wavenet-E", "fil-PH-Wavenet-A", "fi-FI-Wavenet-A", "fr-FR-Standard-C", "fr-FR-Standard-D", "fr-FR-Wavenet-A", "fr-FR-Wavenet-B", "fr-FR-Wavenet-C", "fr-FR-Wavenet-D", "fr-CA-Standard-A", "fr-CA-Standard-B", "fr-CA-Standard-C", "fr-CA-Standard-D", "de-DE-Standard-A", "de-DE-Standard-B", "de-DE-Wavenet-A", "de-DE-Wavenet-B", "de-DE-Wavenet-C", "de-DE-Wavenet-D", "el-GR-Wavenet-A", "hi-IN-Wavenet-A", "hi-IN-Wavenet-B", "hi-IN-Wavenet-C", "hu-HU-Wavenet-A", "is-is-Standard-A", "id-ID-Wavenet-A", "id-ID-Wavenet-B", "id-ID-Wavenet-C", "it-IT-Standard-A", "it-IT-Wavenet-A", "it-IT-Wavenet-B", "it-IT-Wavenet-C", "it-IT-Wavenet-D", "ja-JP-Standard-A", "ja-JP-Wavenet-A", "ja-JP-Wavenet-B", "ja-JP-Wavenet-C", "ja-JP-Wavenet-D", "ko-KR-Standard-A", "ko-KR-Wavenet-A", "lv-lv-Standard-A", "nb-no-Wavenet-E", "nb-no-Wavenet-A", "nb-no-Wavenet-B", "nb-no-Wavenet-C", "nb-no-Wavenet-D", "pl-PL-Wavenet-A", "pl-PL-Wavenet-B", "pl-PL-Wavenet-C", "pl-PL-Wavenet-D", "pt-PT-Wavenet-A", "pt-PT-Wavenet-B", "pt-PT-Wavenet-C", "pt-PT-Wavenet-D", "pt-BR-Standard-A", "ru-RU-Wavenet-A", "ru-RU-Wavenet-B", "ru-RU-Wavenet-C", "ru-RU-Wavenet-D", "sr-rs-Standard-A", "sk-SK-Wavenet-A", "es-ES-Standard-A", "sv-SE-Standard-A", "tr-TR-Standard-A", "tr-TR-Wavenet-A", "tr-TR-Wavenet-B", "tr-TR-Wavenet-C", "tr-TR-Wavenet-D", "tr-TR-Wavenet-E", "uk-UA-Wavenet-A", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "Linda", "Heather", "Sean", "Hoda", "Naayf", "Ivan", "Herena", "Tracy", "Danny", "Huihui", "Yaoyao", "Kangkang", "HanHan", "Zhiwei", "Matej", "Jakub", "Guillaume", "Michael", "Karsten", "Stefanos", "Szabolcs", "Andika", "Heidi", "Kalpana", "Hemant", "Rizwan", "Filip", "Lado", "Valluvar", "Pattara", "An"],
              "streamlabs"      : ["Brian", "Amy", "Emma", "Geraint", "Russell", "Nicole", "Joey", "Justin", "Matthew", "Ivy", "Joanna", "Kendra", "Kimberly", "Salli", "Raveena", "Zeina", "Zhiyu", "Mads", "Naja", "Ruben", "Lotte", "Mathieu", "Celine", "Lea", "Chantal", "Hans", "Marlene", "Vicki", "Aditi", "Karl", "Dora", "Carla", "Bianca", "Giorgio", "Takumi", "Mizuki", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", "Ricardo", "Camila", "Vitoria", "Cristiano", "Ines", "Carmen", "Maxim", "Tatyana", "Enrique", "Conchita", "Lucia", "Mia", "Miguel", "Lupe", "Penelope", "Astrid", "Filiz", "Gwyneth"]}
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

# id = xfc4596ekgo4ewkag6wn01hgs4hfbl
# secret = p8wl2zzuk3sgjmbdrlxe9l65xno8wk


configuration = {
    "events": {},
    "redeems": {},
    "commands": {},
    "actions": {},
    "phrases": {},
    "sfx": {},
}

system_variables = {
    "twitch": {
        "client": None,
        "chat": None,
        "streamer": None,
        "channel": None,
        "live": False,
    },
    "obs": {},
    "alerts": deque(),
    "cooldowns": {
        "sfx":       {"user": {}, "global": {}, "universal": {}},
        "commands":  {"user": {}, "global": {}, "universal": {}},
        "phrases":   {"user": {}, "global": {}, "universal": {}},
    },
    "quotes": [],
    "spoken": set(),
}









## Bot Variables ===================================================================
sv = { "id" : "xfc4596ekgo4ewkag6wn01hgs4hfbl", "secret" : "kvrz8tfupqfc14u2pn539oh1lyko6p",
       "version" : "", "twitch" : None, "streamer" : None, "channel" : None, "chat" : None, "live" : False,
       "alerts" : deque(), "actions" : [], "commands" : {}, "sfx" : {}, "phrases" : {}, "spoken" : [] }
## =================================================================================


## UserScope =======================================================================
USER_SCOPE = list(AuthScope)         
## =================================================================================







def is_on_cooldown(category: str, user: str, name: str):
    """
    Check if a user or command/phrase/sfx is on cooldown.
    Returns (bool, reason, remaining_time)
    """
    now = time.time()
    c = system_variables["cooldowns"].get(category, {})

    # Universal (user-wide lockout)
    universal_expiry = c.get("universal", {}).get(user, 0)
    if universal_expiry > now:
        return True, "universal", round(universal_expiry - now, 1)

    # Global (shared lockout)
    global_expiry = c.get("global", {}).get(name, 0)
    if global_expiry > now:
        return True, "global", round(global_expiry - now, 1)

    # User-specific (per-item)
    user_expiry = c.get("user", {}).get(user, {}).get(name, 0)
    if user_expiry > now:
        return True, "user", round(user_expiry - now, 1)

    return False, None, 0


def set_cooldown(category, user, name):
    now = time.time()
    c = system_variables["cooldowns"].setdefault(category, {"user": {}, "global": {}, "universal": {}})
    user_cd, global_cd, universal_cd = get_cooldowns(category, name)

    if user_cd:
        c["user"].setdefault(user, {})[name] = now + user_cd
    if global_cd:
        c["global"][name] = now + global_cd
    if universal_cd:
        c["universal"][user] = now + universal_cd



def get_cooldowns(category: str, name: str):
    """
    Retrieve cooldown values for a specific category (commands, phrases, sfx).
    Automatically handles per-entry and top-level 'universal-cooldown' values.
    Returns (user_cd, global_cd, universal_cd)
    """
    cfg = configuration.get(category, {})
    # Normalize plural key to match YAML section
    subkey = {"commands": "command", "phrases": "phrase", "sfx": "sound"}.get(category, category)
    section = cfg.get(subkey, {})

    # Grab universal cooldown at file top
    universal_cd = cfg.get("universal-cooldown", 0)

    # Grab entry-specific cooldowns (if present)
    entry_cd = section.get(name, {}).get("cooldown", {})
    user_cd = entry_cd.get("user", 0)
    global_cd = entry_cd.get("global", 0)

    return user_cd, global_cd, universal_cd









## =================================================================================
## =================================================================================
###################################### EVENTS ######################################
## =================================================================================
## =================================================================================




## OnMessage =======================================================================
async def on_message (msg: ChatMessage):
    try:
        global sv
        name = msg.user.name
        
        '''
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
        '''
        
        '''
        ## chat event ==================================================================
        if not msg.text.startswith("!"):
            await addAlert({"type":"chat", "user":name, "message":msg.text})
        ## =============================================================================
        '''
        
        ## quotes ======================================================================
        if "!addquote" in msg.text:
            try:
                # Must be a reply or we can’t grab the original message
                if not msg.reply_parent_msg_body:
                    await sv["chat"].send_message(sv["channel"], "!addquote must be used as a reply.")
                    return

                # Extract original message + author
                quote_message = msg.reply_parent_msg_body.strip()
                quote_author = msg.reply_thread_parent_user_login or "Unknown"
                timestamp = datetime.now().strftime("%m/%y")

                line = f'"{quote_message}" - {quote_author}, {timestamp}'

                # --- Store in-memory ---
                system_variables["quotes"].append(line)

                # --- Persist to file ---
                quotes_path = os.path.join(os.getcwd(), "data", "variables", "list", "quotes.txt")
                os.makedirs(os.path.dirname(quotes_path), exist_ok=True)
                with open(quotes_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(configuration["quotes"]))

                # --- Feedback to chat ---
                quote_num = len(system_variables["quotes"])
                await sv["chat"].send_message(
                    sv["channel"], f"Quote #{quote_num} added: {line}"
                )

            except Exception as e:
                pass
        ## =============================================================================
        
        
        ## live check ==================================================================
        if system_variables["twitch"]["live"] == False:
            async for streams in system_variables["twitch"]["client"].get_streams(user_id = [system_variables["twitch"]["streamer"].id]):
                system_variables["twitch"]["live"] = True
        
        if system_variables["twitch"]["live"] == True:
        
            ## first time chat =============================================================
            if "first-msg" in msg.__dict__["_parsed"]["tags"] and msg.__dict__["_parsed"]["tags"]["first-msg"] == "1":
                await addAlert({"type":"first-time-chat", "user":name, "message":msg.text})
                system_variables["spoken"].append(name)
            else:
                if name not in system_variables["spoken"]:
                    system_variables["spoken"].append(name)
                    await addAlert({"type":"first-session-chat", "user":msg.user.display_name, "message":msg.text})
            ## =============================================================================
            
            ## first session chat ==========================================================
            
            ## =============================================================================
            
            
            
        ## =============================================================================
    except Exception as e:
        logError(tag = "event.on_message")

## =================================================================================




        

## =================================================================================








## Event - VaylReady =============================================================
async def on_ready (event: EventData):
    try:
        await event.chat.join_room(system_variables["twitch"]["channel"])
        prompt ("success", "Welcome to Vayl")
        
        
        await reload(False)
    except Exception as e:
        pass
        



        

## Event - AddVIP ================================================================
async def on_vip_add(data: ChannelVIPAddEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "vip-add"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - RemoveVIP =============================================================
async def on_vip_remove(data: ChannelVIPRemoveEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "vip-remove"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - CharityBegin ==========================================================
async def on_charity_begin(data: CharityCampaignStartEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "charity-begin"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - CharityDonate =========================================================
async def on_charity_donate(data: CharityDonationEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "charity-donate"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - CharityProgress =======================================================
async def on_charity_progress(data: CharityCampaignProgressEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "charity-progress"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - CharityStop ===========================================================
async def on_charity_end(data: CharityCampaignStopEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "charity-end"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - GoalBegin =============================================================
async def on_goal_begin(data: GoalEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "goal-begin"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - GoalProgress ==========================================================
async def on_goal_progress(data: GoalEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "goal-progress"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - GoalEnd ===============================================================
async def on_goal_end(data: GoalEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "goal-end"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Ban ===================================================================
async def on_ban(data: ChannelBanEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "ban-add"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Unban =================================================================
async def on_unban(data: ChannelUnbanEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "ban-remove"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass
        
        
        

## Event - Redeem ================================================================
async def on_redeem(data: ChannelPointsCustomRewardRedemptionAddEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type": "redeem"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - RedeemUpdate ==========================================================
async def on_redeem_update (data: ChannelPointsCustomRewardRedemptionUpdateEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"redeem-update"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Bits ==================================================================
async def on_bits (data: ChannelCheerEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"cheer"})
        
        full_msg = event.get("message", "")
        clean_msg = " ".join(word for word in full_msg.split() if not (word.lower().startswith("cheer") and word[5:].isdigit()))

        event["fullmessage"] = full_msg
        event["message"] = clean_msg
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Raid ==================================================================
async def on_raid (data: ChannelRaidEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"raid"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - AD ====================================================================
async def on_ad (data: ChannelAdBreakBeginEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"ad-break"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - ShoutoutReceive =======================================================
async def on_shoutout_receive (data: ChannelShoutoutReceiveEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"shoutout-receive"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - ShoutoutCreate ========================================================
async def on_shoutout_create (data: ChannelShoutoutCreateEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"shoutout-create"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - PollStar ==============================================================
async def on_poll_begin (data: ChannelPollBeginEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"poll-begin"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - PollEnd ===============================================================
async def on_poll_end (data: ChannelPollEndEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        if event["status"] == "completed":
            event.update({"type":"poll-end"})
            await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - PredictionStart =======================================================
async def on_prediction (data: ChannelPredictionEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"prediction-start"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - PredictionEnd =========================================================
async def on_prediction_end (data: ChannelPredictionEndEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"prediction-end"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - HypeTrain =============================================================
async def on_hype_train (data: HypeTrainEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"hype-train"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - StreamOnline ==========================================================
async def on_online (data: StreamOnlineEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"stream-online"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - StreamOffline =========================================================
async def on_offline (data: StreamOfflineEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"stream-offline"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Follow ================================================================
async def on_follow (data: ChannelFollowEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"follow"})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Sub ===================================================================
async def on_sub (data: ChannelSubscribeEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"sub","tier":{"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - GiftSub ===============================================================
async def on_giftsub (data: ChannelSubscriptionGiftEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"sub-gift","tier":{"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]})
        await addAlert(flattenData(event))
    except Exception as e:
        pass

## Event - Resub =================================================================
async def on_resub (data: ChannelSubscriptionMessageEvent):
    try:
        event = data.event.to_dict(include_none_values=True)
        event.update({"type":"sub-resub","tier":{"Prime":"prime","1000":"1","2000":"2","3000":"3"}[event["tier"]]})
        await addAlert(flattenData(event))
    except Exception as e:
        pass





def flattenData(data, prefix="", add_numeric_ids=False):

    key_replacements = {
        "user_name": "username",  # consistency
        "from_broadcaster_user_name": "from_username",
        "to_broadcaster_user_name": "to_username",
        "from_broadcaster_user_id": "from_userid",
        "to_broadcaster_user_id": "to_userid",
        "from_broadcaster_user_login": "from_userlogin",
        "to_broadcaster_user_login": "to_userlogin"
    }

    def transform_key(key):
        new_key = key_replacements.get(key, key)
        return new_key.replace("_", "-")  # Use "-" for variable names

    flattened = {}

    if isinstance(data, dict):
        for key, value in data.items():
            transformed_key = transform_key(key)
            full_key = f"{prefix}.{transformed_key}" if prefix else transformed_key
            flattened.update(flattenData(value, full_key, add_numeric_ids))
    elif isinstance(data, list):
        for index, item in enumerate(data, start=1):
            item_key = f"{prefix}.{index}" if prefix else str(index)
            flattened.update(flattenData(item, item_key, add_numeric_ids))
    else:
        flattened[prefix] = "" if data is None else str(data)

    return flattened





## =================================================================================



## =================================================================================
## =================================================================================
#################################### COMMANDS ######################################
## =================================================================================
## =================================================================================



## =================================================================================





## Command !currency ===============================================================

async def getUserCurrencyData(username: str):
    try:
        async for user in system_variables["twitch"]["client"].get_users(logins=[username]):
            return {"login": user.login, "display": user.display_name}
    except Exception:
        pass
    return None


async def getBalance(user: str) -> float | None:
    data = await getUserData(user)
    if not data:
        return None  # user not found

    userid = data["id"]
    username = data["display"]

    base_dir = os.path.join(os.getcwd(), "data", "currency", "users")
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{userid}.yml")

    if not os.path.exists(filepath):
        default_balance = 0.0
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.safe_dump({
                "login": username,
                "balance": default_balance,
            }, f)
        return default_balance

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return float(data.get("balance", 0.0))
    except Exception:
        return 0.0

    
async def setBalance(user: str, amount: float) -> bool:
    data = await getUserData(user)
    if not data:
        return False  # invalid user

    userid = data["id"]
    username = data["display"]

    base_dir = os.path.join(os.getcwd(), "data", "currency", "users")
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{userid}.yml")

    entry = {
        "login": username,
        "balance": round(float(amount), 2),
    }

    tmp = filepath + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            yaml.safe_dump(entry, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, filepath)
        return True
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        return False



## Command - !debug ================================================================
EVENT_CLASSES = {
    "ad-break": ChannelAdBreakBeginEvent,
    "ban-add": ChannelBanEvent,
    "ban-remove": ChannelUnbanEvent,
    "bits": ChannelCheerEvent,
    "charity-begin": CharityCampaignStartEvent,
    "charity-donate": CharityDonationEvent,
    "charity-progress": CharityCampaignProgressEvent,
    "charity-end": CharityCampaignStopEvent,
    "chat": None,
    "first-time-chat": None,
    "first-session-chat": None,
    "follow": ChannelFollowEvent,
    "goal-begin": GoalEvent,
    "goal-progress": GoalEvent,
    "goal-end": GoalEvent,
    "hype-train": HypeTrainEvent,
    "poll-created": ChannelPollBeginEvent,
    "poll-begin": ChannelPollBeginEvent,
    "poll-end": ChannelPollEndEvent,
    "prediction-begin": ChannelPredictionEvent,
    "prediction-end": ChannelPredictionEndEvent,
    "raid": ChannelRaidEvent,
    "redeem": ChannelPointsCustomRewardRedemptionAddEvent,
    "redeem-update": ChannelPointsCustomRewardRedemptionUpdateEvent,
    "shoutout-create": ChannelShoutoutCreateEvent,
    "shoutout-receive": ChannelShoutoutReceiveEvent,
    "stream-online": StreamOnlineEvent,
    "stream-offline": StreamOfflineEvent,
    "sub": ChannelSubscribeEvent,
    "sub-gift": ChannelSubscriptionGiftEvent,
    "sub-resub": ChannelSubscriptionMessageEvent,
    "vayl-load": None,
    "vip-add": ChannelVIPAddEvent,
    "vip-remove": ChannelVIPRemoveEvent,
}

async def c_debug(cmd: ChatCommand):
    try:
    
        if not await hasPermission(cmd.user, ["streamer"]):
            return

        parts = cmd.parameter.split(maxsplit=1)
        if not parts:
            await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], "Usage: !debug <event> [fields...]")
            return

        event_name = parts[0].lower()
        overrides = parts[1] if len(parts) > 1 else ""

        event_cls = EVENT_CLASSES.get(event_name)
        if not event_cls:
            await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], f"Unsupported event: {event_name}")
            return

        # --- Step 1: Build the default event dictionary ---
        base_event = {}
        for key, hint in getattr(event_cls, "__annotations__", {}).items():
            tname = str(hint)
            if "str" in tname:
                base_event[key] = f"default_{key}"
            elif "int" in tname:
                base_event[key] = 1
            elif "bool" in tname:
                base_event[key] = False
            elif "datetime" in tname:
                base_event[key] = datetime.utcnow().isoformat()
            else:
                base_event[key] = ""

        # --- Step 2: Flatten for Vayl’s format ---
        flat_event = flattenData(base_event)
        flat_event["type"] = event_name

        # --- Step 3: Apply any overrides provided by the user ---
        # Accepts key:value or key:"value with spaces"
        for match in re.findall(r'(\S+):"([^"]+)"|(\S+):(\S+)', overrides):
            key = (match[0] or match[2]).replace("_", "-").lower()
            value = match[1] or match[3]
            if key in flat_event:
                flat_event[key] = value
            else:
                # add anyway for flexibility, even if not present
                flat_event[key] = value

        # --- Step 4: Dispatch event ---
        await addAlert(flat_event)
        await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], f"Debug event '{event_name}' dispatched.")

    except Exception as e:
        logError(tag="command.debug", additional_details=[str(e)])

## Command - !indexobs =============================================================
async def c_indexobs (cmd: ChatCommand):
    try:
        if await hasPermission(cmd.user, ["streamer"]):
            await indexOBSAsync()
    except Exception as e:
        pass

## Command - !reload ===============================================================
async def c_reload (cmd: ChatCommand):
    try:
        if await hasPermission(cmd.user, ["streamer"]):
            await reload(True)
    except Exception as e:
        pass

## Command - !custom ===============================================================
async def c_custom(cmd: ChatCommand):
    try:
    
        print (cmd.name)
    
        user = cmd.user.name.lower()
        cmd_name = cmd.name.lower()
        args = cmd.parameter.split() if cmd.parameter else []

        base_cmd = None
        commands = configuration.get("commands", {}).get("command", {})
        for name, info in commands.items():
            aliases = [a.lower() for a in info.get("alias", [])]
            if cmd_name == name.lower() or cmd_name in aliases:
                base_cmd = name.lower()
                cfg = info
                break
        if not base_cmd:
            return

        if not await hasPermission(user, cfg.get("permission", "all")):
            return

        if not await isStreamer(user) and is_on_cooldown("commands", user, base_cmd):
            return

        vars = {"user": user, "cmdtext": " ".join(args), "args": cmd.parameter or ""}
        for i, arg in enumerate(args[:100]):
            vars[f"arg{i}"] = arg.replace("@", "", 1)

        asyncio.create_task(runActions(cfg.get("actions", []), vars))

        set_cooldown("commands", user, base_cmd)

    except Exception as e:
        logError(tag="command.custom", additional_details=[str(e)])

## Command - !uptime ===============================================================
async def c_uptime(cmd: ChatCommand):
    try:
        async for stream in system_variables["twitch"]["client"].get_streams(user_id=[system_variables["twitch"]["streamer"].id]):
            start = stream.started_at.replace(tzinfo=timezone.utc)
            diff = relativedelta(datetime.now(timezone.utc), start)

            parts = []
            if diff.days:
                parts.append(f"{diff.days}d")
            if diff.hours:
                parts.append(f"{diff.hours}h")
            if diff.minutes:
                parts.append(f"{diff.minutes}m")
            if diff.seconds:
                parts.append(f"{diff.seconds}s")

            time_str = " ".join(parts) if parts else "just started"

            msg = f"Uptime: {time_str}"
            await system_variables["twitch"]["chat"].send_message(
                system_variables["twitch"]["channel"], msg
            )
            return

        await system_variables["twitch"]["chat"].send_message(
            system_variables["twitch"]["channel"], "The stream is currently offline."
        )

    except Exception as e:
        pass

## Command - !followage ============================================================
async def c_followage(cmd: ChatCommand):
    try:
        user = cmd.parameter.strip() if cmd.parameter else cmd.user.name
        result = await system_variables["twitch"]["client"].get_channel_followers(broadcaster_id=system_variables["twitch"]["streamer"].id)

        async for follower in result:
            if follower.user_name.lower() == user.lower():
                follow_date = follower.followed_at.replace(tzinfo=timezone.utc)
                diff = relativedelta(datetime.now(timezone.utc), follow_date)

                parts = []
                if diff.years:
                    parts.append(f"{diff.years}y")
                if diff.months:
                    parts.append(f"{diff.months}m")
                if diff.days:
                    parts.append(f"{diff.days}d")
                if diff.hours:
                    parts.append(f"{diff.hours}h")
                if diff.minutes:
                    parts.append(f"{diff.minutes}m")

                time_str = " ".join(parts) if parts else "just now"
                msg = f"{user} has been following for {time_str}."
                await system_variables["twitch"]["chat"].send_message(
                    system_variables["twitch"]["channel"], msg
                )
                return

        await system_variables["twitch"]["chat"].send_message(
            system_variables["twitch"]["channel"], f"{user} is not following."
        )

    except Exception as e:
        pass

## Command - !getgame ==============================================================
async def c_getgame (cmd: ChatCommand):
    try:
        infos = await system_variables["twitch"]["client"].get_channel_information(system_variables["twitch"]["streamer"].id)
        await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], "Current Game: " + infos[0].game_name)
    except Exception as e:
        pass

## Command - !setgame ==============================================================
async def c_setgame (cmd: ChatCommand):
    try:
        if not (await isStreamer(cmd.user.name) or await isModerator(cmd.user.name)):
            return
        async for game in system_variables["twitch"]["client"].get_games(names=[cmd.parameter]):
            await system_variables["twitch"]["client"].modify_channel_information(system_variables["twitch"]["streamer"].id, game_id=game.id)
            await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], f"Game has been set to: {game.name}")
            return  # success, stop after first match
        await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], f"Unable to find '{cmd.parameter}'")
    except Exception as e:
        pass

## Command - !title ================================================================
async def c_settitle (cmd: ChatCommand):
    try:
        if (await isStreamer(cmd.user.name) or await isModerator(cmd.user.name)):
            await system_variables["twitch"]["client"].modify_channel_information(system_variables["twitch"]["streamer"].id, title = cmd.parameter)
            await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], f"{cmd.user.name} has updated the stream title.")
    except Exception as e:
        pass

## Command - !quote ================================================================
async def c_quotes (cmd: ChatCommand):
    try:
        quotes = system_variables.get("quotes", [])
        chat = system_variables["twitch"]["chat"]
        channel = system_variables["twitch"]["channel"]

        if not quotes:
            await chat.send_message(channel, "No quotes... yet!")
            return
        try:
            index = int(cmd.parameter) - 1 if cmd.parameter else None
        except ValueError:
            index = None

        if index is not None and 0 <= index < len(quotes):
            await chat.send_message(channel, f"Quote #{index + 1}: {quotes[index]}")
        elif index is not None:
            await chat.send_message(channel, f"Invalid quote number. Try 1–{len(quotes)}.")
        else:
            random_index = random.randint(0, len(quotes) - 1)
            quote = quotes[random_index]
            await chat.send_message(channel, f"Quote #{random_index + 1} > {quote}")

    except Exception as e:
        pass

## Command - !quotes ===============================================================
async def c_quote (cmd: ChatCommand):
    try:
        quotes = system_variables.get("quotes", [])
        await chat.send_message(channel, f"{len(quotes)} Avaiable quotes.")
    except Exception as e:
        pass

## Command - !sfx ==================================================================
async def c_sfx (cmd: ChatCommand):
    try:
        user = cmd.user.name.lower()
        sfx_name = cmd.name.lower()

        sfx_cfg = configuration.get("sfx", {}).get("sound", {}).get(sfx_name)
        if not sfx_cfg or not sfx_cfg.get("enabled", True):
            return
        if not await has_permission(user, cmd.user.badges, sfx_cfg.get("permission", "all")):
            return
        if not await isStreamer(user) and is_on_cooldown("sfx", user, sfx_name):
            return

        for ext in [".mp3", ".wav"]:
            sound_path = os.path.join(vdir["sounds"], sfx_cfg["sound"] + ext)
            if os.path.exists(sound_path):
                threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
                break

        set_cooldown("sfx", user, sfx_name)

    except Exception as e:
        logError(tag="command.sfx", additional_details=[str(e)])





## =================================================================================
## =================================================================================
################################## TIMED ACTIONS ###################################
## =================================================================================
## =================================================================================



async def timedActionsAsync():
    try:
        while True:
            if "timed-actions" in system_variables:
                for action in system_variables["timed-actions"]:
                    action["counter"] += 1
                    if action["counter"] >= action["frequency"]:
                        if action["max-iterations"] == -1 or action["iterations"] < action["max-iterations"]:
                            asyncio.create_task(runActions(action["actions"], {}))
                            action["iterations"] += 1
                        action["counter"] = 0
                await asyncio.sleep(1)
    except Exception as e:
        logError(tag="timedActionsAsync", additional_details=[str(e)])




## =================================================================================





## =================================================================================
## =================================================================================
######################################## OBS #######################################
## =================================================================================
## =================================================================================


## Index OBS =======================================================================
def indexOBS():
    asyncio.run(indexOBSAsync())

async def indexOBSAsync():
    global system_variables
    global configuration

    while True:
        config = configuration.get("obs", {})
        new_index = {}

        try:
            # Try to obtain an active OBS client via the new utility function
            cl = get_obs_client()

            if cl is None:
                # OBS not running or connection failed — skip this cycle silently
                await asyncio.sleep(config.get("index-frequency", 60))
                continue

            # --- Scene & group indexing ---
            try:
                for scene in cl.get_scene_list().__dict__.get("scenes", []):
                    scene_name = scene["sceneName"]
                    items = cl.get_scene_item_list(scene_name).__dict__.get("scene_items", [])
                    new_index[scene_name] = [i["sourceName"] for i in items]

                for group in cl.get_group_list().__dict__.get("groups", []):
                    items = cl.get_group_scene_item_list(group).__dict__.get("scene_items", [])
                    new_index[group] = [i["sourceName"] for i in items]

            except Exception as e:
                # Handle any mid-connection or parsing error
                logError(tag="obs.index", additional_details=[f"Indexing failed: {e}"])

        except Exception as e:
            # Fallback catch-all for unexpected issues
            logError(tag="obs.index", additional_details=[str(e)])

        # --- Update global state and wait for next pass ---
        system_variables["obs"] = new_index
        await asyncio.sleep(config.get("index-frequency", 60))
        

        



## =================================================================================
## =================================================================================
###################################### ALERTS ######################################
## =================================================================================
## =================================================================================


## Add Alert =======================================================================
async def addAlert(alert: dict):

    global configuration
    alert["id"] = str(uuid.uuid4())
    event_type = alert.get("type")

    # Determine configuration section (normal event or redeem)
    if event_type == "redeem":
        # Match redeem by title
        for name, rd in configuration.get("redeems", {}).items():
            if name.lower() in alert.get("reward.title", "").lower():
                config = rd
                break
        else:
            return  # no match found
    else:
        config = configuration.get("events", {}).get(event_type, {})

    # Skip if disabled
    if not config.get("enabled", False):
        return

    priority = config.get("priority", "back")

    # Instant = independent async task
    if priority == "instant":
        print ("Running Alert Actions: " + alert["type"])
        asyncio.create_task(runActions(config.get("actions", []), alert))
        return

    # Normal queued alerts
    if priority == "front":
        print ("Adding Alert to Queue FRONT: " + alert["type"])
        system_variables["alerts"].appendleft(alert)
    else:
        print ("Adding Alert to Queue: " + alert["type"])
        system_variables["alerts"].append(alert)




## Manage Alerts (async) ===========================================================
async def manageAlertsAsync():
    try:
        while True:
        
            
            if not system_variables["alerts"]:
                await asyncio.sleep(0.25)
                continue

            alert = system_variables["alerts"].popleft()
            actions = []

            # --- Handle Gift Subs (group all matching user events) ---
            if alert["type"] == "giftsub":
                alert["amount"] = 1
                user = alert.get("user", "").lower()

                # Collect all matching giftsub alerts by same user
                remaining = deque()
                while system_variables["alerts"]:
                    next_alert = system_variables["alerts"].popleft()
                    if (
                        next_alert.get("type") == "giftsub"
                        and next_alert.get("user", "").lower() == user
                    ):
                        alert["amount"] += 1
                    else:
                        remaining.append(next_alert)

                # restore all unrelated alerts back to the queue
                system_variables["alerts"] = remaining

            # --- Determine configuration source ---
            if "redeem" in alert["type"]:
                actions = alert.get("actions", [])
            else:
            
            
                event_cfg = configuration.get("events", {}).get(alert["type"], {})
                if not event_cfg.get("enabled", False):
                    continue

                actions = event_cfg.get("actions", [])
                if event_cfg.get("announce", False):
                    prompt("misc", f"Processing alert: {alert['type']}")

            # --- Execute alert actions (sequential, blocking next) ---
            if actions:
                await runActions(actions, alert)

    except Exception as e:
        print (e)
    
        logError(tag="manageAlertsAsync", additional_details=[str(e)])

        
            


## =================================================================================


## =================================================================================
## =================================================================================
#################################### FUNCTIONS #####################################
## =================================================================================
## =================================================================================


async def hasPermission(user, required) -> bool:
    """
    Check if a user has permission based on roles or explicit usernames.
    'user' should be a ChatUser object with `.name` and `.badges` attributes.
    'required' can be a string or list.
    """
    username = user.name.lower()
    badges = [b.lower() for b in getattr(user, "badges", []) or []]

    try:
        streamer_name = system_variables["twitch"]["channel"].lower()
        client = system_variables["twitch"]["client"]
        streamer_id = system_variables["twitch"]["streamer"].id
    except KeyError:
        return False

    # Normalize permission input
    if isinstance(required, str):
        perms = [p.strip().lower() for p in required.split(",")]
    elif isinstance(required, list):
        perms = [str(p).strip().lower() for p in required]
    else:
        perms = []

    # Default: all users allowed
    if not perms or "all" in perms:
        return True

    # Streamer always allowed
    if username == streamer_name:
        return True

    # Preload lists as needed
    mod_list, sub_list = set(), set()
    if any(r in perms for r in ("mod", "moderator")):
        mod_list = {m.user_name.lower() async for m in client.get_moderators(streamer_id)}
    if any(r in perms for r in ("sub", "subscriber")):
        sub_list = {s.user_name.lower() async for s in client.get_broadcaster_subscriptions(streamer_id)}

    # Check roles
    if username in mod_list:
        return True
    if "vip" in perms and "vip" in badges:
        return True
    if username in sub_list:
        return True

    # Explicit user whitelisting
    if username in perms:
        return True

    return False



'''
async def has_permission(user: str, badges: list[str], required: str | list[str]) -> bool:
    user = user.lower()
    if await isStreamer(user):
        return True

    if isinstance(required, str):
        perms = [p.strip().lower() for p in required.split(",")]
    else:
        perms = [p.strip().lower() for p in required]

    if not perms or "all" in perms:
        return True

    if "mod" in perms and await isModerator(system_variables["twitch"]["streamer"], user):
        return True
    if "vip" in perms and "vip" in badges:
        return True
    if "sub" in perms and await isSubbed(user):
        return True

    return False

## isStreamer ======================================================================
async def isStreamer(user: str) -> bool:
    try:
        return user.lower() == system_variables["twitch"]["channel"].lower()
    except Exception as e:
        return False

## isModerator =====================================================================
async def isModerator(user: str) -> bool:
    try:
        return any(mod.user_name.lower() == user.lower()
            async for mod in system_variables["twitch"]["client"].get_moderators(
                system_variables["twitch"]["streamer"].id
            )
        )
    except Exception as e:
        return False

## isSubbed ========================================================================
async def isSubbed(user: str) -> bool:
    try:
        return any(sub.user_name.lower() == user.lower()
            async for sub in system_variables["twitch"]["client"].get_broadcaster_subscriptions(
                system_variables["twitch"]["streamer"].id
            )
        )
    except Exception as e:
        return False
'''






def safeEval(expr: str, variables: dict = None):
    safe_env = {
        # Core literals (case-insensitive)
        "True": True, "False": False, "None": None,
        "true": True, "false": False, "none": None,

        # Common math and number helpers
        "abs": abs,
        "min": min,
        "max": max,
        "round": round,
        "int": int,
        "float": float,
        "pow": pow,

        # Math constants and functions
        "pi": math.pi,
        "e": math.e,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "ceil": math.ceil,
        "floor": math.floor,

        # Optional aliases for readability
        "and_": lambda a, b: a and b,
        "or_": lambda a, b: a or b,
        "not_": lambda a: not a,
    }

    if variables:
        safe_env.update(variables)

    try:
        return eval(expr, {"__builtins__": None}, safe_env)
    except Exception:
        return None


## ModifySource ============================================================
async def modifySource(cl, source_name: str, action: str):
    global system_variables

    try:
        found = False

        for container, sources in system_variables["obs"].items():
            if source_name not in sources:
                continue

            found = True
            item = cl.get_scene_item_id(container, source_name)
            item_id = item.scene_item_id

            if action == "show":
                cl.set_scene_item_enabled(container, item_id, True)
            elif action == "hide":
                cl.set_scene_item_enabled(container, item_id, False)
            elif action == "toggle":
                current_state = cl.get_scene_item_enabled(container, item_id)
                enabled = bool(current_state.__dict__["scene_item_enabled"])
                cl.set_scene_item_enabled(container, item_id, not enabled)
            else:
                prompt("error", f"Unknown modifySource action: {action}")
                return

            break  # stop after first match (sources should be unique)

        if not found:
            prompt("error", f"Unable to find source: {source_name}")

    except Exception as e:
        logError(tag=f"obs.{action}", additional_details=[str(e)])
## =========================================================================


def resolve_list_path(name: str) -> str:
    base = os.path.join(os.getcwd(), "data", "variables", "list")
    path = os.path.join(base, f"{name}.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
    
    

def get_obs_client(timeout=0.5):
    """Safely return an active OBS WebSocket client if OBS is running, else None."""
    try:
    
        global configuration
        
        obs_data = configuration.get("config",{}).get("obs",{})
        host = obs_data.get("hostname", "localhost")
        port = obs_data.get("port", 4455)
        password = obs_data.get("password", "password")

        # Check if OBS is running before connecting
        with socket.create_connection((host, port), timeout=timeout):
            return obs.ReqClient(host=host, port=port, password=password)
    except OSError:
        # OBS not reachable
        return None
    except Exception as e:
        # Catch config / connection issues
        # print(f"[OBS] Connection failed: {e}")
        return None


## RunActions ======================================================================
async def runActions (actions, variables):

    global state
    
    cl = None
    
    action_frame = {
        "obs:scene": {
            "args": {
                "s": {"name": "scene", "required": True}
            },
            "example": "obs:scene | s:scene"
        },
        "obs:show": {
            "args": {
                "s": {"name": "source", "required": True}
            },
            "example": "obs:show | s:source"
        },
        "obs:hide": {
            "args": {
                "s": {"name": "source", "required": True}
            },
            "example": "obs:hide | s:source"
        },
        "obs:toggle": {
            "args": {
                "s": {"name": "source", "required": True}
            },
            "example": "obs:toggle | s:source"
        },
        "obs:image": {
            "args": {
                "s": {"name": "source", "required": True},
                "f": {"name": "filepath", "required": True}
            },
            "example": "obs:image | s:source | f:filepath"
        },
        "obs:audio": {
            "args": {
                "s":  {"name": "source", "required": True},
                "p":  {"name": "percent", "required": True},
                "st": {"name": "steps", "required": False},
                "d":  {"name": "duration", "required": False}
            },
            "example": "obs:audio | s:source | p:percent | [st:steps] | [d:duration]"
        },
        "obs:label": {
            "args": {
                "s":  {"name": "source", "required": True},
                "t":  {"name": "text", "required": True},
                "c":  {"name": "color", "required": False},
                "sz": {"name": "size", "required": False},
                "a":  {"name": "alignment", "required": False},
                "o":  {"name": "opacity", "required": False},
                "f":  {"name": "font", "required": False}
            },
            "example": "obs:label | s:source | t:text | [c:hex] | [sz:size] | [f:font]"
        },
        "obs:mediafile": {
            "args": {
                "s": {"name": "source", "required": True},
                "p": {"name": "filepath", "required": True}
            },
            "example": "obs:mediafile | s:source | p:filepath"
        },
        "obs:media": {
            "args": {
                "s": {"name": "source", "required": True},
                "st": {"name": "state", "required": True}
            },
            "example": "obs:media | s:source | st:play/pause/stop/seek"
        },
        "obs:filteron": {
            "args": {
                "s": {"name": "source", "required": True},
                "f": {"name": "filter", "required": True}
            },
            "example": "obs:filteron | s:source | f:filter"
        },
        "obs:filteroff": {
            "args": {
                "s": {"name": "source", "required": True},
                "f": {"name": "filter", "required": True}
            },
            "example": "obs:filteroff | s:source | f:filter"
        },
        "playsound": {
            "args": {
                "s": {"name": "sound", "required": True}
            },
            "example": "playsound | s:sound"
        },
        "wait": {
            "args": {
                "t": {"name": "time", "required": True}
            },
            "example": "wait | t:seconds"
        },
        "notify": {
            "args": {
                "t": {"name": "text", "required": True}
            },
            "example": "notify | t:text"
        },
        "syscmd": {
            "args": {
                "c": {"name": "command", "required": True}
            },
            "example": "syscmd | c:command"
        },
        "conditional": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "conditional | n:name"
        },
        "actionpack": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "actionpack | n:name"
        },
        "text": {
            "args": {
                "n": {"name": "name", "required": True},
                "t": {"name": "text", "required": True}
            },
            "example": 'text | n:name | t:"text"'
        },
        "number": {
            "args": {
                "n": {"name": "name", "required": True},
                "v": {"name": "value", "required": True}
            },
            "example": "number | n:name | v:value"
        },
        "list:append": {
            "args": {
                "n": {"name": "name", "required": True},
                "t": {"name": "text", "required": True}
            },
            "example": "list:append | n:name | t:text"
        },
        "list:prepend": {
            "args": {
                "n": {"name": "name", "required": True},
                "t": {"name": "text", "required": True}
            },
            "example": "list:prepend | n:name | t:text"
        },
        "list:remove": {
            "args": {
                "n": {"name": "name", "required": True},
                "t": {"name": "text", "required": True}
            },
            "example": "list:remove | n:name | t:text"
        },
        "list:removeall": {
            "args": {
                "n": {"name": "name", "required": True},
                "t": {"name": "text", "required": True}
            },
            "example": "list:removeall | n:name | t:text"
        },
        "list:shuffle": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "list:clear | n:name"
        },
        "list:az": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "list:az | n:name"
        },
        "list:za": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "list:za | n:name"
        },
        "list:clear": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "list:clear | n:name"
        },
        "boolean": {
            "args": {
                "n": {"name": "name", "required": True},
                "v": {"name": "value", "required": True},
            },
            "example": "boolean | n:name | v:value/expression"
        },
        "variable": {
            "args": {
                "n": {"name": "name", "required": True},
                "v": {"name": "value", "required": True}
            },
            "example": "variable | n:name | v:value/expression"
        },
        "chat:message": {
            "args": {
                "m": {"name": "message", "required": True}
            },
            "example": "chat:message | m:message"
        },
        "chat:announce": {
            "args": {
                "m": {"name": "message", "required": True},
                "c": {"name": "color", "required": False}
            },
            "example": "chat:announce | m:message | [c:color]"
        },
        "tts": {
            "args": {
                "v": {"name": "voice", "required": True},
                "m": {"name": "message", "required": True},
                "h": {"name": "halt", "required": True},
                "l": {"name": "limit", "required": True}
            },
            "example": "tts | v:voice | m:message | h:true/false | l:limit"
        },
        "chat:addvip": {
            "args": {
                "u": {"name": "user", "required": True}
            },
            "example": "chat:addvip | u:user"
        },
        "chat:removevip": {
            "args": {
                "u": {"name": "user", "required": True}
            },
            "example": "chat:removevip | u:user"
        },
        "stream:timeout": {
            "args": {
                "u": {"name": "user", "required": True},
                "t": {"name": "time", "required": True},
                "r": {"name": "reason", "required": True}
            },
            "example": "timeout | u:user | t:seconds | r:reason"
        },
        "webhook": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "webhook | n:name"
        },
        "redeem:create": {
            "args": {},
            "example": "redeem:create"
        },
        "stream:clip": {
            "args": {},
            "example": "stream:clip"
        },
        "stream:marker": {
            "args": {},
            "example": "stream:marker"
        },
        "stream:raid": {
            "args": {
                "u": {"name": "user", "required": True}
            },
            "example": "stream:raid | u:user"
        },
        "redeem:enable": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "redeem:enable | n:name"
        },
        "redeem:disable": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "redeem:disable | n:name"
        },
        "redeem:toggle": {
            "args": {
                "n": {"name": "name", "required": True}
            },
            "example": "redeem:toggle | n:name"
        }
    }
        
    async def parse_action(line: str):
        line = line.strip()
        if not line or line.startswith("#"):
            return None  # ignore blanks / comments

        # Split using | or ; separators
        parts = [p.strip() for p in (line.split("|") if "|" in line else line.split(";"))]
        action = parts[0].lower()

        # --- validate action
        if action not in action_frame:
            matches = difflib.get_close_matches(action, action_frame.keys(), n=1, cutoff=0.6)
            suggestion = f" Did you mean '{matches[0]}'?" if matches else ""
            prompt("error", f"Unknown action '{action}'.{suggestion}")
            return None

        # --- pull argument definitions (may be empty)
        defs = action_frame[action].get("args", {})
        adata = {k: None for k in defs}

        # --- if no args defined but args given → warn (optional)
        if not defs and len(parts) > 1:
            prompt("warn", f"Action '{action}' does not take arguments — extras ignored.")
            return action, adata

        # --- parse arguments
        for arg in parts[1:]:
            if ":" not in arg:
                prompt("error", f"Malformed argument '{arg}' in '{action}'. Expected prefix:value")
                return None

            prefix, value = arg.split(":", 1)
            prefix = prefix.strip().lower()
            value = value.strip()

            if prefix not in defs:
                prompt("error", f"Unknown prefix '{prefix}' in '{action}'")
                return None

            # Allow tag parsing in argument values
            if "[" in value and "]" in value:
                adata[prefix] = await processTags(value, False)
            else:
                adata[prefix] = value

        # --- check required args (only if args exist)
        if defs:
            missing = [p for p, meta in defs.items() if meta.get("required") and not adata[p]]
            if missing:
                names = ", ".join(defs[m]["name"] for m in missing)
                prompt(
                    "error",
                    f"Missing required arguments for '{action}': {names}\nExpected: {action_frame[action]['example']}"
                )
                return None

        return action, adata


    ############################################################################################

    async def processTags(phrase: str, is_conditional: bool):
        async def resolve_once(word: str) -> str:
        
            for tag, value in variables.items():
                word = word.replace(f"[{tag}]", str(value))

            if "[nickname:" in word:
                name = word.split("[nickname:")[1].split("]")[0]
                path = os.path.join(vdir["configuration"], "nicknames.yml")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    nickname = next((v for n, v in data.items() if n.lower() == name.lower()), name)
                    word = word.replace(f"[nickname:{name}]", nickname)
                except Exception:
                    # Fallback: leave original name
                    word = word.replace(f"[nickname:{name}]", name)

            if "[viewers]" in word:
                try:
                    async for stream in await sv["twitch"].get_streams(user_id=[sv["streamer"].id]):
                        count = getattr(stream, "viewer_count", 0)
                        break
                    else:
                        count = 0  # no active stream returned
                    word = word.replace("[viewers]", str(count))
                except Exception:
                    word = word.replace("[viewers]", "0")

            if "[uptime" in word:
                try:
                    async for stream in await sv["twitch"].get_streams(user_id=[sv["streamer"].id]):
                        started_at = stream.started_at.replace(tzinfo=pytz.UTC)
                        now = datetime.now(tz=pytz.UTC)
                        elapsed = now - started_at
                        total_seconds = int(elapsed.total_seconds())

                        # Time breakdown
                        days, remainder = divmod(total_seconds, 86400)
                        hours, remainder = divmod(remainder, 3600)
                        minutes, seconds = divmod(remainder, 60)

                        match = re.search(r"\[uptime(?::([^\]]+))?\]", word)
                        mode = match.group(1) if match else None

                        if not mode:
                            result = f"{hours}h {minutes}m {seconds}s"
                        elif mode == "seconds":
                            result = str(total_seconds)
                        elif mode == "minutes":
                            result = str(total_seconds // 60)
                        elif mode == "hours":
                            result = str(total_seconds // 3600)
                        elif mode == "days":
                            result = str(total_seconds // 86400)
                        elif mode == "full":
                            result = f"{days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds"
                        elif mode == "clean":
                            units = [("Days", days), ("Hours", hours), ("Minutes", minutes), ("Seconds", seconds)]
                            start_index = next((i for i, (_, v) in enumerate(units) if v > 0), len(units) - 1)
                            relevant = units[start_index:]
                            result = ", ".join(f"{v} {n}" for n, v in relevant)
                        elif any(p in mode for p in ["{H}", "{M}", "{S}", "{D}", "{TOTAL_S}", "{TOTAL_M}", "{TOTAL_H}", "{HH}", "{MM}", "{SS}"]):
                            HH, MM, SS = str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)
                            result = (
                                mode.replace("{D}", str(days))
                                    .replace("{H}", str(hours))
                                    .replace("{M}", str(minutes))
                                    .replace("{S}", str(seconds))
                                    .replace("{HH}", HH)
                                    .replace("{MM}", MM)
                                    .replace("{SS}", SS)
                                    .replace("{TOTAL_S}", str(total_seconds))
                                    .replace("{TOTAL_M}", str(total_seconds // 60))
                                    .replace("{TOTAL_H}", str(total_seconds // 3600))
                            )
                        else:
                            result = "Invalid format"

                        word = re.sub(r"\[uptime(?::[^\]]+)?\]", result, word)
                        break
                    else:
                        word = re.sub(r"\[uptime(?::[^\]]+)?\]", "Offline", word)
                except Exception:
                    word = re.sub(r"\[uptime(?::[^\]]+)?\]", "Offline", word)

            if "[followers]" in word:
                count = 0
                async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                    count += 0 if follower.user_name.lower() == "vaylbot" else 1
                word = word.replace("[followers]", str(count))

            if "[rfollower" in word:
                try:
                    followers = []
                    async for follower in await sv["twitch"].get_channel_followers(broadcaster_id=sv["streamer"].id):
                        if follower.user_name.lower() != "vaylbot":
                            followers.append(follower.user_name)

                    if followers:
                        match = re.search(r"\[rfollower:(\d+)\]", word)
                        if match:
                            count = int(match.group(1))
                            sample = random.sample(followers, min(count, len(followers)))
                            word = word.replace(match.group(0), ", ".join(sample))
                        elif "[rfollower]" in word:
                            word = word.replace("[rfollower]", random.choice(followers))
                    else:
                        word = re.sub(r"\[rfollower(?::\d+)?\]", "", word)
                except Exception:
                    word = re.sub(r"\[rfollower(?::\d+)?\]", "", word)

            if "[obs:scene]" in word:
                if cl in None:
                    cl = get_obs_client()
                    if cl is not None:
                        scene = cl.get_current_program_scene().__dict__["current_program_scene_name"]
                        word = word.replace("[obs:scene]", scene)

            if "[obs:muted:" in word:
                if cl is None:
                    cl = get_obs_client()
                    if cl is not None:
                        try:
                            # Handle multiple [obs:muted:<source>] occurrences in a single word
                            matches = re.findall(r"\[obs:muted:([^\]]+)\]", word)
                            for source_name in matches:
                                try:
                                    muted = cl.get_input_mute(source_name).inputMuted
                                    word = word.replace(f"[obs:muted:{source_name}]", str(muted).lower())
                                except Exception:
                                    # Source not found, default to false
                                    word = word.replace(f"[obs:muted:{source_name}]", "false")
                        except Exception:
                            pass
                    else:
                        # No OBS client available, default to false
                        word = re.sub(r"\[obs:muted:[^\]]+\]", "false", word)

            if "[subscribers]" in word:
                count = 0
                async for sub in await sv["twitch"].get_broadcaster_subscriptions(sv["streamer"].id):
                    count += 0 if sub.user_name.lower() == "vaylbot" else 1
                word = word.replace("[subscribers]", str(count))

            if "[rsubscriber" in word:
                try:
                    subs = []
                    async for sub in await sv["twitch"].get_broadcaster_subscriptions(sv["streamer"].id):
                        if sub.user_name.lower() != "vaylbot":
                            subs.append(sub.user_name)

                    if subs:
                        # Check for [rsubscriber:x]
                        match = re.search(r"\[rsubscriber:(\d+)\]", word)
                        if match:
                            count = int(match.group(1))
                            sample = random.sample(subs, min(count, len(subs)))
                            word = word.replace(match.group(0), ", ".join(sample))
                        elif "[rsubscriber]" in word:
                            # Single random subscriber (legacy form)
                            word = word.replace("[rsubscriber]", random.choice(subs))
                    else:
                        # No subs found
                        word = re.sub(r"\[rsubscriber(?::\d+)?\]", "", word)
                except Exception:
                    word = re.sub(r"\[rsubscriber(?::\d+)?\]", "", word)

            if "[table:" in word:
                try:
                    # Match e.g. [table:events/deaths:v:player1]
                    for match in re.finditer(r"\[table:([A-Za-z0-9_\-\/\\]+):(e|v):([^\]]+)\]", word):
                        table_name, mode, index_raw = match.groups()

                        # Normalize slashes and build full path
                        normalized_name = table_name.strip("/\\")
                        path = os.path.join(os.getcwd(), "data", "variables", "table", f"{normalized_name}.yml")

                        # Ensure directories exist if the user namespaced the path
                        os.makedirs(os.path.dirname(path), exist_ok=True)

                        # Load YAML safely
                        data = {}
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as file:
                                data = yaml.safe_load(file) or {}
                        else:
                            # Auto-create missing table file if not present
                            with open(path, "w", encoding="utf-8") as f:
                                yaml.safe_dump({}, f)

                        replacement = ""
                        if isinstance(data, dict) and data:
                            try:
                                # If index is numeric → sort by value (desc) and get Nth item
                                index = int(index_raw)

                                def sort_key(item):
                                    val = item[1]
                                    try:
                                        return float(val)
                                    except (ValueError, TypeError):
                                        return str(val)

                                sorted_items = sorted(data.items(), key=sort_key, reverse=True)
                                idx = index - 1 if index > 0 else index
                                key, value = sorted_items[idx] if abs(index) <= len(sorted_items) else ("", "")
                                replacement = str(key if mode == "e" else value)

                            except ValueError:
                                # Non-numeric index → treat as direct key lookup
                                key_name = str(index_raw)
                                replacement = str(data.get(key_name, "")) if mode == "v" else key_name

                        # Replace this specific tag instance only
                        word = word.replace(match.group(0), replacement)

                except Exception:
                    # Silently strip malformed tags to avoid breaking the console
                    word = re.sub(r"\[table:[A-Za-z0-9_\-\/\\]+:(e|v):[^\]]+\]", "", word)

            word = word.replace("[system:dateus]", date.today().strftime("%m/%d/%y"))
            word = word.replace("[system:dateuk]", date.today().strftime("%d/%m/%y"))
            word = word.replace("[system:time]", datetime.now().strftime("%H:%M:%S"))

            word = re.sub(
                r"\[rnumber:([+-]?\d+)-([+-]?\d+)\]",
                lambda m: str(random.randint(int(m.group(1)), int(m.group(2)))),
                word,
            )

            word = re.sub(
                r"\[xstring:([^:]+):([+-]?\d+)\]",
                lambda m: m.group(1) * int(m.group(2)) if int(m.group(2)) >= 0 else "",
                word,
            )
            
            if any(tag in word for tag in ("[image:", "[sound:", "[video:")):
                base = os.path.join(vdir["resources"])

                filetypes = {
                    "image": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
                    "sound": [".mp3", ".wav", ".ogg"],
                    "video": [".mp4", ".mov", ".mkv", ".webm"]
                }

                def resolve(tag_type: str, relpath: str):
                    folder = os.path.join(base, f"{tag_type}s")
                    # normalize and strip leading slashes/backslashes
                    relpath = relpath.strip("/\\")
                    search_path = os.path.join(folder, relpath)

                    # Direct file match
                    if os.path.isfile(search_path):
                        return search_path

                    # Try common extensions
                    for ext in filetypes.get(tag_type, []):
                        candidate = search_path + ext
                        if os.path.isfile(candidate):
                            return candidate

                    return ""  # graceful fallback

                # Iterate tag types
                for tag_type in ("image", "sound", "video"):
                    pattern = f"[{tag_type}:"
                    if pattern in word:
                        name = word.split(pattern)[1].split("]")[0]
                        word = word.replace(f"[{tag_type}:{name}]", resolve(tag_type, name))

            for vtype in ["integer", "text", "list", "boolean"]:
                tag_pattern = f"[{vtype}:"
                if tag_pattern in word:
                    relpath = word.split(tag_pattern)[1].split("]")[0].strip("/\\")
                    base = os.path.join(vdir["variables"], vtype)
                    filepath = os.path.join(base, relpath + ".txt")

                    try:
                        if os.path.exists(filepath):
                            with open(filepath, "r", encoding="utf-8") as f:
                                content = f.read().strip()
                            word = word.replace(f"[{vtype}:{relpath}]", content)
                        else:
                            # Auto-create missing file (default values)
                            os.makedirs(os.path.dirname(filepath), exist_ok=True)
                            default = "0" if vtype == "integer" else ""
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(default)
                            word = word.replace(f"[{vtype}:{relpath}]", default)
                    except Exception:
                        word = word.replace(f"[{vtype}:{relpath}]", "")

            if "[list:" in word:
                try:
                    # Extract list name
                    tag = word.split("[list:")[1].split("]")[0]
                    path = os.path.join(vdir["list"], f"{tag}.txt")

                    # Read list entries safely
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            entries = [line.strip() for line in f if line.strip()]
                    else:
                        entries = []

                    # Format output depending on context
                    if is_conditional:
                        # Conditional mode → usable inside Python-style logic
                        # e.g. ['"a"', '"b"'] → ["a", "b"]
                        formatted = "[" + ", ".join(f'"{entry}"' for entry in entries) + "]"
                    else:
                        # Regular usage → human-readable inline list
                        formatted = ", ".join(entries)

                    # Replace the tag with formatted text
                    word = word.replace(f"[list:{tag}]", formatted)

                except Exception:
                    # Gracefully remove unresolved tag on error
                    word = re.sub(r"\[list:[^\]]+\]", "", word)
            
            if "[rlist:" in word:
                try:
                    # Find all matches (supports multiple per message)
                    for match in re.finditer(r"\[rlist:([^:\]]+)(?::(\d+))?\]", word):
                        name, count = match.groups()
                        count = int(count) if count else 1  # default to 1
                        path = os.path.join(vdir["list"], f"{name}.txt")

                        entries = []
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                entries = [line.strip() for line in f if line.strip()]

                        if entries:
                            sample = random.sample(entries, min(count, len(entries)))
                            replacement = ", ".join(sample)
                        else:
                            replacement = ""

                        word = word.replace(match.group(0), replacement)
                except Exception:
                    word = re.sub(r"\[rlist:[^:\]]+(?::\d+)?\]", "", word)

            if "[clist:" in word:
                try:
                    match = re.search(r"\[clist:([^:\]]+):([^:\]]+)\]", word)
                    if match:
                        name, text = match.groups()
                        path = os.path.join(vdir["list"], f"{name}.txt")

                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                entries = [line.strip() for line in f if line.strip()]
                            count = entries.count(text)
                        else:
                            count = 0

                        word = word.replace(match.group(0), str(count))
                except Exception:
                    word = re.sub(r"\[clist:[^:\]]+:[^:\]]+\]", "0", word)

            if "[toplist:" in word:
                try:
                    match = re.search(r"\[toplist:([^:\]]+)\]", word)
                    if match:
                        name = match.group(1)
                        path = os.path.join(vdir["list"], f"{name}.txt")

                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                entries = [line.strip() for line in f if line.strip()]

                            if entries:
                                from collections import Counter
                                counts = Counter(entries)
                                # Sort by count (descending), then alphabetically
                                leaderboard = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
                                top_entry = leaderboard[0][0] if leaderboard else ""
                                word = word.replace(match.group(0), top_entry)
                            else:
                                word = word.replace(match.group(0), "")
                        else:
                            word = word.replace(match.group(0), "")
                except Exception:
                    word = re.sub(r"\[toplist:[^:\]]+\]", "", word)

            if "[ruser" in word:
                try:
                    users = []
                    async for chatter in await sv["twitch"].get_chatters(sv["streamer"].id, sv["streamer"].id):
                        if chatter.user.name.lower() != "vaylbot":
                            users.append(chatter.user_name)

                    if users:
                        match = re.search(r"\[ruser:(\d+)\]", word)
                        if match:
                            count = int(match.group(1))
                            sample = random.sample(users, min(count, len(users)))
                            word = word.replace(match.group(0), ", ".join(sample))
                        elif "[ruser]" in word:
                            word = word.replace("[ruser]", random.choice(users))
                    else:
                        word = re.sub(r"\[ruser(?::\d+)?\]", "", word)
                except Exception:
                    word = re.sub(r"\[ruser(?::\d+)?\]", "", word)

            if "[ugame:" in word:
                name = word.split("[ugame:")[1].split("]")[0]
                found_game = ""
                async for users in sv["twitch"].get_users(logins=[name]):
                    infos = await sv["twitch"].get_channel_information(users.id)
                    found_game = infos[0].game_name or "something..."
                word = word.replace(f"[ugame:{name}]", found_game)

            return word

        pattern = re.compile(r"\[[^\[\]]+\]")  # Regex: match any [ ... ] without nested brackets
        last = None

        while last != phrase and pattern.search(phrase):
            last = phrase
            words = phrase.split(" ")   # Handle each word separately
            resolved = []

            for w in words:
                try:
                    # Resolve one layer of tags for each word
                    resolved.append(await resolve_once(w))
                except Exception:
                    # Never crash — log error and keep original text
                    logError(tag="action.tags")
                    resolved.append(w)

            phrase = " ".join(resolved)

        return phrase

    
    
    for a in actions:
    
        a = a.strip()
        if not a or a.startswith("#"):
            continue
    
        if "|" in a:
            parts = [x.strip() for x in a.split("|")]
        else:
            parts = [x.strip() for x in a.split(";")]
            
        parsed = await parse_action(a)
        if not parsed:
            continue 
        action, adata = parsed
            
        if cl is None and "obs:" in action:
            cl = get_obs_client()

            if cl is None:
                prompt("misc", f"Skipping '{source_name}', no active OBS connection.")
                continue
            
        ## obs:scene =====================================================================
        if action == "obs:scene":
            scene = adata["s"]
            if scene not in obs_index["scenes"]:
                return prompt("error", f"Scene not found: {scene}")
            await cl.set_current_program_scene(scene)
                 
        ## obs:show/hide/toggle ==========================================================
        if action in ["obs:show", "obs:hide", "obs:toggle"]:
            await modifySource(cl, adata["s"], action.split(":")[1])
                    
        ## obs:image =====================================================================
        if action == "obs:image":
            try:
                image = cl.get_input_settings(adata["s"]).__dict__
                data = dict(image["input_settings"])
                data["file"] = adata["p"]
                cl.set_input_settings(adata["s"], data, True)
            except Exception as e:
                logError(tag="obs.image", additional_details=[a, f"OBS Image Error: {e}"])
                
        ## obs:label =====================================================================
        if action == "obs:label":
            try:
                src = adata["s"]

                # Fetch existing input data
                label = cl.get_input_settings(src).__dict__
                data = dict(label["input_settings"])

                # Ensure font structure exists if font or size is being modified
                if adata["f"] or adata["sz"] is not None:
                    data.setdefault("font", {
                        "face": adata["f"] or "Arial",
                        "size": int(adata["sz"] or 24),
                        "style": "Regular",
                        "flags": 0
                    })

                # Text
                if adata["t"]:
                    data["text"] = adata["t"]

                # Color (convert RGB → BGR integer)
                if adata["c"]:
                    hexstr = adata["c"].replace("0x", "").replace("#", "").zfill(6)[-6:]
                    hex_bgr = "0x" + hexstr[4:6] + hexstr[2:4] + hexstr[0:2]
                    data["color"] = int(hex_bgr, 16)

                # Font face & size
                if adata["f"]:
                    data["font"]["face"] = adata["f"]

                if adata["sz"] is not None:
                    data["font"]["size"] = int(adata["sz"])

                # Alignment
                if adata["a"]:
                    data["align"] = {
                        "left": "left",
                        "center": "center",
                        "right": "right"
                    }.get(adata["a"].lower(), "left")

                # Opacity (clamped to 0–100)
                if adata["o"] is not None:
                    try:
                        data["opacity"] = max(0, min(int(adata["o"]), 100))
                    except ValueError:
                        data["opacity"] = 100

                # Apply settings
                cl.set_input_settings(src, data, True)

            except Exception as e:
                logError(
                    tag="obs.label",
                    additional_details=[a, f"OBS Label Error: {e}"]
                )
            
        ## obs:audio =====================================================================
        if action == "obs:audio":
            try:
                source = adata["s"]
                percent = str(adata.get("p", "100")).strip()
                steps = int(adata.get("st", 1))
                duration = float(adata.get("du", 1))
                delay = duration / max(steps, 1)

                # get current multiplier
                current = (await cl.get_input_volume(source)).get("inputVolumeMul", 1.0)
                current_percent = current * 100

                # determine target %
                if percent.startswith(("+", "-")):
                    target_percent = max(0.0, min(current_percent + float(percent), 200.0))
                else:
                    target_percent = max(0.0, min(float(percent), 200.0))

                # convert to multiplier
                target = target_percent / 100.0
                diff = (target - current) / steps

                # gradual fade
                for i in range(1, steps + 1):
                    cl.set_input_volume(source, vol_mul=current + diff * i)
                    await asyncio.sleep(delay)

            except Exception as e:
                print(f"OBS:Audio Error: {e}")
            
        ## obs:mediafile =================================================================
        if action == "obs:mediafile":
            try:
                source = adata["s"]
                path = adata["p"]
                media = cl.get_input_settings(source).__dict__
                data = dict(media["input_settings"])

                data["local_file"] = path
                cl.set_input_settings(source, data, True)

            except Exception as e:
                logError(tag="obs.mediafile", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])


        ## obs:media =====================================================================
        if action == "obs:media":
            try:
                source = adata["s"]
                state = adata["st"]

                if str(state).isnumeric():
                    cl.set_media_input_cursor(source, int(state))
                else:
                    actions = {
                        "play": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY",
                        "pause": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE",
                        "stop": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP",
                        "restart": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART",
                        "next": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_NEXT",
                        "previous": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PREVIOUS"
                    }

                    key = state.lower()
                    if key not in actions:
                        return prompt("error", f"Invalid media action: {state}")
                    cl.trigger_media_input_action(source, actions[key])

            except Exception as e:
                logError(tag="obs.media", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])

        ## obs:filteron ==================================================================
        if action == "obs:filteron":
            try:
                cl.set_source_filter_enabled(adata["s"], adata["f"], True)
            except Exception as e:
                logError(tag="obs.filteron", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])

        ## obs:filteroff =================================================================
        if action == "obs:filteroff":
            try:
                cl.set_source_filter_enabled(adata["s"], adata["f"], False)
            except Exception as e:
                logError(tag="obs.filteroff", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])

        
        ## playsound =====================================================================
        if action == "playsound":
            try:
                path = adata["s"]
                found = False

                # Case 1: Direct path exists (absolute or relative)
                if os.path.exists(path):
                    playsound(path, block=False)
                    found = True

                # Case 2: Use fallback to resources/sounds directory
                else:
                    base = os.path.join(os.getcwd(), "data", "resources", "sounds")
                    name = path.replace(".mp3", "").replace(".wav", "")
                    for ext in (".mp3", ".wav"):
                        candidate = os.path.join(base, name + ext)
                        if os.path.exists(candidate):
                            playsound(candidate, block=False)
                            found = True
                            break

                if not found:
                    prompt("misc", f"Unable to find audio file: {path}")

            except Exception as e:
                logError(tag="action.playsound", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])
                
        ## wait ==========================================================================
        if action == "wait":
            try:
                duration = float(adata["t"])
                await asyncio.sleep(duration)
            except Exception as e:
                logError(tag="action.wait", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])
            
        ## text:set ======================================================================
        if action == "text:set":
            try:
                name = adata["n"]
                text = str(adata["t"])
                path = os.path.join(os.getcwd(), "data", "variables", "text", f"{name}.txt")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
            except Exception as e:
                logError(tag="action.textset", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])

        ## text:append ==================================================================
        if action == "text:append":
            try:
                name = adata["n"]
                text = str(adata["t"])
                path = os.path.join(os.getcwd(), "data", "variables", "text", f"{name}.txt")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "a", encoding="utf-8") as f:
                    f.write(text)
            except Exception as e:
                logError(tag="action.textappend", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])

        ## text:prepend ===================================================================
        if action == "text:prepend":
            try:
                name = adata["n"]
                text = str(adata["t"])
                path = os.path.join(os.getcwd(), "data", "variables", "text", f"{name}.txt")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                old = ""
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        old = f.read()
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text + old)
            except Exception as e:
                logError(tag="action.textprepend", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])
       
        ## text ====================================================================
        if action == "text":
            try:
                name = adata["n"]
                expr = adata["t"]
                result = safeEval(expr)
                if result is None:
                    result = expr  # fallback, shouldn't happen often
                path = os.path.join(os.getcwd(), "data", "variables", "text", f"{name}.txt")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(result))
            except Exception as e:
                logError(tag="action.text", additional_details=[a, f"Expecting: {action_frame[action]['example']}"])
        
        ## number =======================================================================
        if action == "number":
            try:
                name = adata["n"]
                expr = adata["v"]

                result = safeEval(expr)

                try:
                    result = float(result)
                    if result.is_integer():
                        result = int(result)
                except (ValueError, TypeError):
                    result = 0

                base = os.path.join(os.getcwd(), "data", "variables", "number")
                os.makedirs(base, exist_ok=True)
                path = os.path.join(base, f"{name}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(result))

            except Exception as e:
                logError(tag="action.number", additional_details=[a, "Expecting: " + action_definitions[action]["example"]])
            
        ## list:append ===================================================================
        if action == "list:append":
            try:
                path = resolve_list_path(adata["n"])
                text = str(adata["t"])
                with open(path, "a", encoding="utf-8") as f:
                    f.write(text + "\n")
            except Exception as e:
                logError(tag="list.append", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
            
        ## list:prepend ==================================================================
        if action == "list:prepend":
            try:
                path = resolve_list_path(adata["n"])
                text = str(adata["t"])
                lines = []
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text + "\n")
                    f.writelines(lines)
            except Exception as e:
                logError(tag="list.prepend", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## list:remove ===================================================================
        if action == "list:remove":
            try:
                path = resolve_list_path(adata["n"])
                text = str(adata["t"])
                if not os.path.exists(path):
                    return
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if text + "\n" in lines:
                    lines.remove(text + "\n")
                else:
                    # remove without newline fallback
                    lines = [l for l in lines if l.strip() != text.strip()]
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as e:
                logError(tag="list.remove", additional_details=[a, "Expecting: " + action_frame[action]["example"]])

        ## list:removeall ================================================================
        if action == "list:removeall":
            try:
                path = resolve_list_path(adata["n"])
                text = str(adata["t"])
                if not os.path.exists(path):
                    return
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                lines = [l for l in lines if l.strip() != text.strip()]
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as e:
                logError(tag="list.removeall", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
            
        ## list:clear ====================================================================
        if action == "list:clear":
            try:
                path = resolve_list_path(adata["n"])
                open(path, "w", encoding="utf-8").close()
            except Exception as e:
                logError(tag="list.clear", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## list:shuffle ==================================================================
        if action == "list:shuffle":
            try:
                path = resolve_list_path(adata["n"])
                if not os.path.exists(path):
                    return prompt("misc", f"List not found: {adata['n']}")

                with open(path, "r", encoding="utf-8") as f:
                    lines = [line for line in f if line.strip()]

                if not lines:
                    return  # nothing to shuffle

                random.shuffle(lines)

                with open(path, "w", encoding="utf-8") as f:
                    f.writelines([l if l.endswith("\n") else l + "\n" for l in lines])

            except Exception as e:
                logError(tag="list.shuffle", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## list:az =======================================================================
        if action == "list:az":
            try:
                path = resolve_list_path(adata["n"])
                if not os.path.exists(path):
                    return prompt("misc", f"List not found: {adata['n']}")

                with open(path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                if not lines:
                    return

                lines.sort(key=lambda x: x.lower())

                with open(path, "w", encoding="utf-8") as f:
                    f.writelines([l + "\n" for l in lines])

            except Exception as e:
                logError(tag="list.az", additional_details=[a, "Expecting: " + action_frame[action]["example"]])

        ## list:za =======================================================================
        if action == "list:za":
            try:
                path = resolve_list_path(adata["n"])
                if not os.path.exists(path):
                    return prompt("misc", f"List not found: {adata['n']}")

                with open(path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                if not lines:
                    return

                lines.sort(key=lambda x: x.lower(), reverse=True)

                with open(path, "w", encoding="utf-8") as f:
                    f.writelines([l + "\n" for l in lines])

            except Exception as e:
                logError(tag="list.za", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
               
        ## boolean =======================================================================
        if action == "boolean":
            try:
                name = adata["n"]
                expr = adata["v"]

                result = safeEval(expr)
                if isinstance(result, str):
                    result = result.strip().lower() in ["true", "1", "yes", "on"]

                result = bool(result)

                base = os.path.join(os.getcwd(), "data", "variables", "boolean")
                os.makedirs(base, exist_ok=True)
                path = os.path.join(base, f"{name}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("true" if result else "false")

            except Exception as e:
                logError(tag="action.boolean", additional_details=[a, "Expecting: " + action_definitions[action]["example"]])                           
            
        ## variable ======================================================================
        if action == "variable":
            try:
                name = adata["n"]
                expr = adata["v"]
                result = safeEval(expr)
                variables[name] = result
            except Exception as e:
                logError(tag="action.variable", additional_details=[a, f"Failed to set variable '{name}'"])
            
        ## actionpack ====================================================================
        if action == "actionpack":
            try:
                name = adata["n"]
                pack_path = os.path.join(os.getcwd(), "configuration", "actionpacks", f"{name}.yml")

                if not os.path.exists(pack_path):
                    return prompt("error", f"ActionPack not found: {name}")

                with open(pack_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}

                # Load actions array (ignore if missing)
                actions_in_pack = data.get("actions", [])
                if not actions_in_pack:
                    return prompt("misc", f"ActionPack '{name}' is empty")

                await runActions(actions_in_pack, variables)

            except Exception as e:
                logError(tag="actionpack", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## notify ========================================================================
        if action == "notify":
            try:
                message = str(adata["t"])
                prompt("misc", message)
            except Exception as e:
                logError(tag="notify", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
            
        ## conditional ===================================================================
        if action == "conditional":
            try:
                name = adata["n"]
                base, _, key = name.partition(":")
                cond_path = os.path.join(os.getcwd(), "configuration", "conditionals", f"{base}.yml")

                if not os.path.exists(cond_path):
                    return prompt("error", f"Conditional file not found: {base}")

                with open(cond_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}

                section = data.get(key, data)
                condition = await processTags(section["condition"], True)
                result = eval(condition, {}, variables)
                await runActions(section.get(result, []), variables)

            except Exception as e:
                logError(tag="conditional", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                
        
        ## tts ===========================================================================
        if action == "tts":
            try:
                msg = adata["m"]
                voice = adata["v"]
                halt = adata["h"].lower() == "true"
                limit = int(adata["l"])

                if len(msg) > limit:
                    text = f"TTS message too long ({len(msg)}/{limit})."
                    await sv["chat"].send_message(sv["channel"], text)
                    return prompt("misc", text)

                # pronunciation substitution
                with open(os.path.join(os.getcwd(), "configuration", "pronunciation.yml"), "r", encoding="utf-8") as f:
                    pdata = yaml.safe_load(f) or {}
                for name, pronounce in pdata.items():
                    msg = msg.replace(name, pronounce)

                data = None
                for vp, voices in tts_voice.items():
                    if voice.lower() not in [v.lower() for v in voices]:
                        continue

                    # provider handlers
                    if vp == "oddcast":
                        vid, eid, lid = voice.split("-")
                        url = "https://cache-a.oddcast.com/tts/genB.php"
                        params = {
                            "EID": int(eid), "LID": int(lid), "VID": int(vid),
                            "TXT": msg, "EXT": "mp3", "ACC": 15679, "SceneID": 2703396,
                            "cache_flag": 3
                        }
                        data = requests.get(url, params=params).content

                    elif vp == "streamelements":
                        url = "https://api.streamelements.com/kappa/v2/speech"
                        data = requests.get(url, params={"voice": voice, "text": msg}).content

                    elif vp == "streamlabs":
                        url = "https://streamlabs.com/polly/speak"
                        res = requests.post(url, params={"voice": voice, "text": msg}, headers={"Referer": "https://streamlabs.com"})
                        mp3_url = res.json()["speak_url"]
                        data = requests.get(mp3_url).content

                    break

                if not data:
                    return prompt("error", f"TTS voice not found: {voice}")

                file_path = os.path.join(os.getcwd(), "data", "tts", f"{uuid.uuid4()}.wav")
                with open(file_path, "wb") as f:
                    f.write(data)

                # play in thread
                def play_tts(fp):
                    try:
                        playsound(fp, block=True)
                    finally:
                        if os.path.exists(fp):
                            os.remove(fp)

                threading.Thread(target=play_tts, args=(file_path,), daemon=False).start()

            except Exception as e:
                logError(tag="tts", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## syscmd ========================================================================
        if action == "syscmd":
            try:
                subprocess.run(adata["c"], shell=False)
            except Exception as e:
                logError(tag="syscmd", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## chat:announce =================================================================
        if action == "chat:announce":
            try:
                message = adata["m"]
                color = adata.get("c", "primary")
                await system_variables["twitch"]["client2"].send_chat_announcement(
                    system_variables["twitch"]["streamer"].id, system_variables["twitch"]["streamer"].id, message, color
                )
            except Exception as e:
                logError(tag="chat.announce", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## chat:message ==================================================================
        if action == "chat:message":
            try:
                msg = await processTags(adata["m"], False)
                await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], msg)
            except Exception as e:
                logError(tag="chat.message", additional_details=[a, "Expecting: " + action_frame[action]["example"]])

        ## chat:addvip ===================================================================
        if action == "chat:addvip":
            try:
                user = adata["u"]
                async for u in sv["twitch"].get_users(logins=[user]):
                    await sv["twitch"].add_channel_vip(sv["streamer"].id, u.id)
                prompt("misc", f"VIP added: {user}")
            except Exception as e:
                logError(tag="vip.add", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## chat:removevip ================================================================
        if action == "chat:removevip":
            try:
                user = adata["u"]
                async for u in sv["twitch"].get_users(logins=[user]):
                    await sv["twitch"].remove_channel_vip(sv["streamer"].id, u.id)
                prompt("misc", f"VIP removed: {user}")
            except Exception as e:
                logError(tag="vip.remove", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## timeout =======================================================================
        if action in ["timeout", "stream:timeout"]:
            try:
                user = adata["u"]
                duration = int(adata["t"])
                reason = adata.get("r", "Timed out by bot")

                async for u in sv["twitch"].get_users(logins=[user]):
                    await sv["twitch"].ban_user(
                        sv["streamer"].id, sv["streamer"].id, u.id, reason, duration
                    )
                prompt("misc", f"User timed out: {user} ({duration}s)")
            except Exception as e:
                logError(tag="stream.timeout", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## webhook =======================================================================
        if action == "webhook":
            try:
                name = adata["n"]
                path = os.path.join(os.getcwd(), "configuration", "webhook", f"{name}.yml")

                if not os.path.exists(path):
                    return prompt("error", f"Webhook not found: {name}")

                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}

                # Main message body
                webhook = DiscordWebhook(
                    url=data["url"],
                    content="\n".join(data.get("message", [])),
                    username="Vayl",
                    avatar_url="https://i.ibb.co/DPSRDwGK/discord.png"
                )

                # Twitch info substitution
                info = (await sv["twitch"].get_channel_information(sv["streamer"].id))[0]
                directory = {
                    "[game]": info.game_name,
                    "[title]": info.title,
                    "[name]": info.broadcaster_name,
                    "[link]": f"https://twitch.tv/{sv['channel'].lower()}",
                }

                embed = DiscordEmbed(
                    title=data["embed"]["title"],
                    description="\n".join(data["embed"]["description"]),
                    color="C14844",
                )
                embed.set_image(url=data["embed"]["image-url"])
                embed.set_thumbnail(url=data["embed"]["thumbnail-url"])
                embed.set_author(
                    name=data["embed"]["title"], icon_url="https://i.ibb.co/mHgBcY2/icon.png"
                )

                if data["embed"]["fields"]["enabled"]:
                    for k, v in data["embed"]["fields"].items():
                        if k == "enabled":
                            continue
                        for d, r in directory.items():
                            v["name"] = v["name"].replace(d, r)
                            v["value"] = v["value"].replace(d, r)
                        embed.add_embed_field(name=v["name"], value=v["value"])

                webhook.add_embed(embed)
                webhook.execute()

            except Exception as e:
                logError(tag="webhook", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## stream:clip ===================================================================
        if action == "stream:clip":
            try:
                clip = await sv["twitch"].create_clip(sv["streamer"].id)
                clips = await sv["twitch"].get_clips(broadcaster_id=sv["streamer"].id, clip_id=clip.id)
                async for c in clips:
                    await updateVariable("latest-vayl-clip", c.url)
                prompt("misc", "Clip created successfully")
            except Exception as e:
                logError(tag="stream.clip", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## stream:marker =================================================================
        if action == "stream:marker":
            try:
                await sv["twitch"].create_stream_marker(sv["streamer"].id, "")
                prompt("misc", "Stream marker added")
            except Exception as e:
                logError(tag="stream.marker", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## stream:raid ===================================================================
        if action == "stream:raid":
            try:
                target = adata["u"]
                async for u in sv["twitch"].get_users(logins=[target]):
                    await sv["twitch"].start_raid(sv["streamer"].id, u.id)
                prompt("misc", f"Raiding {target}...")
            except Exception as e:
                logError(tag="stream.raid", additional_details=[a, "Expecting: " + action_frame[action]["example"]])
                    
        ## redeem:create =================================================================
        if action == "redeem:create":
            try:
                # Simple placeholder redeem to establish bot ownership
                # Real customization handled manually afterward by streamer
                redeem_name = "[vayl_redeem]"
                cost = 1

                # Create a basic channel point reward if it doesn't already exist
                existing = [r async for r in sv["twitch"].get_custom_reward(sv["streamer"].id)]
                if not any(r.title.lower() == redeem_name.lower() for r in existing):
                    await sv["twitch"].create_custom_reward(
                        sv["streamer"].id,
                        title=redeem_name,
                        cost=cost,
                        is_enabled=True,
                        prompt="(auto-created by Vayl)"
                    )
                    prompt("success", f"Created redeem '{redeem_name}' with cost {cost}")
                else:
                    prompt("misc", f"Redeem '{redeem_name}' already exists")

            except Exception as e:
                logError(tag="redeem.create", additional_details=[a, str(e)])
                    
        ## redeem:enable =================================================================
        if action == "redeem:enable":
            try:
                redeem_name = adata.get("n") or adata.get("name")
                if not redeem_name:
                    return prompt("error", "Missing redeem name for redeem:enable")

                async for r in sv["twitch"].get_custom_reward(sv["streamer"].id):
                    if r.title.lower() == redeem_name.lower():
                        await sv["twitch"].update_custom_reward(
                            sv["streamer"].id, r.id, is_enabled=True
                        )
                        prompt("success", f"Enabled redeem '{redeem_name}'")
                        break
                else:
                    prompt("error", f"Redeem '{redeem_name}' not found")

            except Exception as e:
                logError(tag="redeem.enable", additional_details=[a, str(e)])
                    
        ## stream:disable ================================================================
        if action == "redeem:disable":
            try:
                redeem_name = adata.get("n") or adata.get("name")
                if not redeem_name:
                    return prompt("error", "Missing redeem name for redeem:disable")

                async for r in sv["twitch"].get_custom_reward(sv["streamer"].id):
                    if r.title.lower() == redeem_name.lower():
                        await sv["twitch"].update_custom_reward(
                            sv["streamer"].id, r.id, is_enabled=False
                        )
                        prompt("success", f"Disabled redeem '{redeem_name}'")
                        break
                else:
                    prompt("error", f"Redeem '{redeem_name}' not found")

            except Exception as e:
                logError(tag="redeem.disable", additional_details=[a, str(e)])
                    
        ## redeem:toggle =================================================================
        if action == "redeem:toggle":
            try:
                redeem_name = adata.get("n") or adata.get("name")
                if not redeem_name:
                    return prompt("error", "Missing redeem name for redeem:toggle")

                async for r in sv["twitch"].get_custom_reward(sv["streamer"].id):
                    if r.title.lower() == redeem_name.lower():
                        new_state = not r.is_enabled
                        await sv["twitch"].update_custom_reward(
                            sv["streamer"].id, r.id, is_enabled=new_state
                        )
                        state_text = "enabled" if new_state else "disabled"
                        prompt("success", f"Toggled redeem '{redeem_name}' ({state_text})")
                        break
                else:
                    prompt("error", f"Redeem '{redeem_name}' not found")

            except Exception as e:
                logError(tag="redeem.toggle", additional_details=[a, str(e)])



        
## =================================================================================


async def reload (chat):

    global configuration, system_variables, state

    try:
        base = os.path.join(os.getcwd(), "configuration")

        # Reload core configuration groups
        configuration["config"] = yaml.safe_load(open(os.path.join(base, "configuration.yml"), "r", encoding="utf-8"))
        configuration["sfx"] = yaml.safe_load(open(os.path.join(base, "sfx.yml"), "r", encoding="utf-8"))
        configuration["commands"] = yaml.safe_load(open(os.path.join(base, "commands.yml"), "r", encoding="utf-8"))
        configuration["phrases"] = yaml.safe_load(open(os.path.join(base, "phrases.yml"), "r", encoding="utf-8"))
        configuration["redeems"] = yaml.safe_load(open(os.path.join(base, "event", "redeem.yml"), "r", encoding="utf-8"))
        configuration["timed-actions"] = yaml.safe_load(open(os.path.join(base, "timed-actions.yml"), "r", encoding="utf-8"))
        configuration["currency"] = yaml.safe_load(open(os.path.join(base, "currency.yml"), "r", encoding="utf-8"))

        quotes_path = os.path.join(os.getcwd(), "data", "variables", "list", "quotes.txt")
        system_variables["quotes"] = (
            [line.strip() for line in open(quotes_path, "r", encoding="utf-8") if line.strip()]
            if os.path.exists(quotes_path) else []
        )

        events_dir = os.path.join(base, "event")
        configuration["events"] = {}

        # Loop through all .yml or .yaml files in the folder
        for file in os.listdir(events_dir):
            
            if not file.lower().endswith((".yml", ".yaml")):
                continue

            if file.lower() != "redeem.yml":
                name = os.path.splitext(file)[0]  # e.g. "raid" from "raid.yml"
                path = os.path.join(events_dir, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        # prompt("success", f"Registered Event: {name}")
                        configuration["events"][name] = yaml.safe_load(f) or {}
                except Exception as e:
                    prompt("error", f"Failed to load event config: {file}")
                    configuration["events"][name] = {}
                

        # Reset runtime state
        system_variables["alerts"].clear()
        system_variables["cooldowns"] = {"user": {}, "global": {}, "universal": {}}
        
        if chat:
            system_variables["spoken"].clear()

        # Register commands from commands.yml
        for command, info in configuration["commands"].get("command", {}).items():
            aliases = info.get("alias", "").replace(" ","").split(",")
            for alias in aliases:
                if alias:
                    system_variables["twitch"]["chat"].register_command(alias.lower(), c_custom)
            system_variables["twitch"]["chat"].register_command(command.lower(), c_custom)

        # Register core system commands
        base_cmds = {
            "setgame": c_setgame,
            "settitle": c_settitle,
            "game": c_getgame,
            "uptime": c_uptime,
            "followage": c_followage,
            "quote": c_quote,
            "quotes": c_quotes,
            "debug": c_debug,
            "reload": c_reload,
            "indexobs": c_indexobs,
        }
        for name, func in base_cmds.items():
            system_variables["twitch"]["chat"].register_command(name, func)

        # Initialize timed actions runtime data
        system_variables["timed-actions"] = []
        for name, info in configuration["timed-actions"].get("actions", {}).items():
            system_variables["timed-actions"].append({
                "name": name,
                "counter": 0,
                "frequency": info.get("frequency", 0),
                "iterations": 0,
                "max-iterations": info.get("max-iterations", 0),
                "actions": info.get("actions", [])
            })

        if chat:
            await system_variables["twitch"]["chat"].send_message(system_variables["twitch"]["channel"], "Vayl Reloaded")
        else:
            await addAlert({"type":"vayl-load"})

        # print ("Loaded Configuration:")
        # print (configuration["events"])

    except Exception as e:
        print (e)







## Log Error =======================================================================



def sanitize_path(path, base_path=None):
    if base_path is None:
        base_path = os.getcwd()
    try:
        return os.path.relpath(path, base_path)
    except ValueError:
        return path  # Return the original if it cannot be made relative

def logError(tag=None, additional_details=None):
    """Handles error logging, file creation, and optional auto-reporting."""
    prompt("error", "Error Detected")
    base_path = os.getcwd()

    # Load reference for the error cause
    reference = error_reference.get(tag, "Undefined")
    prompt("blank", f"Cause: {reference}")

    # Gather error details
    error_traceback = traceback.format_exc()
    sanitized_traceback = "\n".join(
        sanitize_path(line, base_path) for line in error_traceback.splitlines()
    )

    log_details = {
        "User": sv.get("channel", "Unknown"),
        "Version": __version__,
        "Cause": reference,
        "Error Line": sanitized_traceback.splitlines()[-1] if sanitized_traceback else "N/A",
        "Stack Trace": sanitized_traceback
    }

    # Ensure error directory exists
    error_dir = os.path.join(base_path, "data", "logs", "errors")
    os.makedirs(error_dir, exist_ok=True)

    # Write error to log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(error_dir, f"{timestamp}.txt")

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"User: {log_details['User']}\n")
        log_file.write(f"Version: {log_details['Version']}\n")
        log_file.write(f"Cause: {log_details['Cause']}\n")
        log_file.write(f"Error Line: {log_details['Error Line']}\n\n")

        if additional_details:
            log_file.write("Additional Info:\n")
            for ad_line in additional_details:
                log_file.write(f"- {ad_line}\n")
            log_file.write("\n")
        else:
            log_file.write("Additional Info: None\n\n")

        log_file.write("Stack Trace:\n")
        log_file.write(log_details["Stack Trace"])


        


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
    
    global state
    
    
    

    
    
    

    with open(os.getcwd() + "\\configuration\\configuration.yml", 'r', encoding = "utf-8") as file:
        data = yaml.safe_load(file)
        system_variables["twitch"]["channel"] = data["connected-account"]
    
    
    
    system_variables["twitch"]["client"] = await Twitch(sv["id"], sv["secret"])    
    
    path = os.path.join(os.getcwd(), "configuration", "credentials.yml")
    if not os.path.exists(path):
        prompt("error", "Missing credentials.yml")
        await asyncio.sleep(999999)
    else:
        
        with open(os.getcwd() + "\\configuration\\credentials.yml", 'r', encoding = "utf-8") as file:
            
            data = yaml.safe_load(file)
            
            user_access = data.get("credentials",{}).get("user",{}).get("access","none")
            user_refresh = data.get("credentials",{}).get("user",{}).get("refresh","none")
            if user_access == "none":
            
                prompt("misc", "Missing UserAuth, prompting...")

                auth = UserAuthenticator(sv["twitch"], USER_SCOPE, force_verify = True)
                user_access, user_refresh = await auth.authenticate()
                await system_variables["twitch"]["client"].set_user_authentication(user_access, USER_SCOPE, user_refresh)

                data["credentials"]["user"]["access"] = user_access
                data["credentials"]["user"]["refresh"] = user_refresh
                
                prompt("success", "Authorized User")
                

                await asyncio.sleep(1)
                
            else:
                await system_variables["twitch"]["client"].set_user_authentication(user_access, USER_SCOPE, user_refresh)
                prompt("success", "Assigning UserAuth from credentials")
                
            
            
            bot_access = data.get("credentials",{}).get("bot",{}).get("access","none")
            bot_refresh = data.get("credentials",{}).get("bot",{}).get("refresh","none")
            
            
            system_variables["twitch"]["client2"] = await Twitch(sv["id"], sv["secret"])  
            if bot_access == "none":
                
                prompt("misc", "Missing BotAuth, prompting...")
                await asyncio.sleep(1)

                

                response = auth_bot_prompt("Missing Credentials", "Missing Bot Credentials, do you want to add?")
                
                if response == "yes":
                    
                    import pyperclip
                    
                    auth = UserAuthenticator(sv["btwitch"], USER_SCOPE, force_verify = True)
                    pyperclip.copy(auth.return_auth_url())
                    prompt("misc", " ")
                    prompt("misc", "BotAuth URL Copied")
                    prompt("misc", "1. Login to your Bot account")
                    prompt("misc", "2. Paste URL into your browser")
                    prompt("misc", "3. Authorize when prompted")
                    prompt("misc", " ")
                    
                    bot_access, bot_refresh = await auth.authenticate(use_browser = False)
                    await system_variables["twitch"]["client2"].set_user_authentication(bot_access, USER_SCOPE, bot_refresh)
                    
                    data["credentials"]["bot"]["access"] = bot_access
                    data["credentials"]["bot"]["refresh"] = bot_refresh
                    prompt("success", "Bot authentication completed!")

                elif response == "no":
                    await system_variables["twitch"]["client2"].set_user_authentication(user_access, USER_SCOPE, user_refresh)
                    data["credentials"]["bot"]["access"] = user_access
                    data["credentials"]["bot"]["refresh"] = user_refresh
                    prompt("success", "Assigning UserAuth to Bot")

                save_credentials(data)
                
            else:
                await system_variables["twitch"]["client2"].set_user_authentication(bot_access, USER_SCOPE, bot_refresh)
                prompt("success", "Assigning BotAuth from credentials")
    






    await asyncio.sleep(1)
    
    prompt ("success", "Fetching Twitch User")
    
    system_variables["twitch"]["streamer"] = await first(system_variables["twitch"]["client"].get_users(logins = [system_variables["twitch"]["channel"]]))
    
    prompt ("success", "Regisering EventSub")
    
    eventsub = EventSubWebsocket(system_variables["twitch"]["client"])
    eventsub.start()
    
    handlers = [
        eventsub.listen_stream_online(system_variables["twitch"]["streamer"].id, on_online),
        eventsub.listen_stream_offline(system_variables["twitch"]["streamer"].id, on_offline),
        eventsub.listen_channel_ad_break_begin(system_variables["twitch"]["streamer"].id, on_ad),
        eventsub.listen_channel_poll_begin(system_variables["twitch"]["streamer"].id, on_poll_begin),
        eventsub.listen_channel_poll_end(system_variables["twitch"]["streamer"].id, on_poll_end),
        eventsub.listen_channel_prediction_begin(system_variables["twitch"]["streamer"].id, on_prediction),
        eventsub.listen_channel_prediction_end(system_variables["twitch"]["streamer"].id, on_prediction_end),
        eventsub.listen_hype_train_begin(system_variables["twitch"]["streamer"].id, on_hype_train),
        eventsub.listen_channel_shoutout_create(system_variables["twitch"]["streamer"].id, system_variables["twitch"]["streamer"].id, on_shoutout_create),
        eventsub.listen_channel_points_custom_reward_redemption_add(system_variables["twitch"]["streamer"].id, on_redeem),
        eventsub.listen_channel_points_custom_reward_redemption_update(system_variables["twitch"]["streamer"].id, on_redeem_update),
        eventsub.listen_channel_cheer(system_variables["twitch"]["streamer"].id, on_bits),
        eventsub.listen_channel_subscribe(system_variables["twitch"]["streamer"].id, on_sub),
        eventsub.listen_channel_subscription_gift(system_variables["twitch"]["streamer"].id, on_giftsub),
        eventsub.listen_channel_subscription_message(system_variables["twitch"]["streamer"].id, on_resub),
        eventsub.listen_channel_follow_v2(system_variables["twitch"]["streamer"].id, system_variables["twitch"]["streamer"].id, on_follow),
        eventsub.listen_channel_raid(on_raid, system_variables["twitch"]["streamer"].id),
        eventsub.listen_goal_begin(system_variables["twitch"]["streamer"].id, on_goal_begin),
        eventsub.listen_goal_progress(system_variables["twitch"]["streamer"].id, on_goal_progress),
        eventsub.listen_goal_end(system_variables["twitch"]["streamer"].id, on_goal_end),
        eventsub.listen_channel_ban(system_variables["twitch"]["streamer"].id, on_ban),
        eventsub.listen_channel_unban(system_variables["twitch"]["streamer"].id, on_unban),
    
        eventsub.listen_channel_charity_campaign_donate(system_variables["twitch"]["streamer"].id, on_charity_donate),
        eventsub.listen_channel_charity_campaign_progress(system_variables["twitch"]["streamer"].id, on_charity_progress),
        eventsub.listen_channel_charity_campaign_start(system_variables["twitch"]["streamer"].id, on_charity_begin),
        eventsub.listen_channel_charity_campaign_stop(system_variables["twitch"]["streamer"].id, on_charity_end),
        
        eventsub.listen_channel_vip_add(system_variables["twitch"]["streamer"].id, on_vip_add),
        eventsub.listen_channel_vip_remove(system_variables["twitch"]["streamer"].id, on_vip_remove),
    
    ]
    await asyncio.gather(*handlers)
        

    prompt ("success", "Connecting to Chat")
    
    system_variables["twitch"]["chat"] = await Chat(system_variables["twitch"]["client2"])
    system_variables["twitch"]["chat"].register_event(ChatEvent.READY, on_ready)
    system_variables["twitch"]["chat"].register_event(ChatEvent.MESSAGE, on_message)
    system_variables["twitch"]["chat"].start()

    t_obs = threading.Thread(target = indexOBS)
    t_obs.start()
        
    asyncio.create_task(timedActionsAsync())
    asyncio.create_task(manageAlertsAsync())
    

    while True:
        await asyncio.sleep(1)





    pass
    
    
    

    
    btwitch = await Twitch(sv["id"], sv["secret"])    
    # await btwitch.set_user_authentication("fi7d5m18fm1zmcgfabax16xssvvddc", USER_SCOPE, "qudyvazycvc2ef557n0m4prkg84zbpafgbxkq1u2uxh2fck7jm")
    await btwitch.set_user_authentication("lhx0q9xhwt8z94kaeofh8py1uzzjb5", USER_SCOPE, "knwm50obq6mx13x53e3rc5gswazsgdxjzdv92c7qm58cvo0mg2")
    sv["btwitch"] = btwitch
    sv["btwitch_user"] = await first(sv["btwitch"].get_users(logins = ["vaylbot"]))
    
    
    
    
    
    
    

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

    
    

    
    

## =================================================================================


















## Customtkinter








class YesNoDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, message: str):
        super().__init__(master)
        
        
        self.title(title)
        self.geometry("340x120")
        self.resizable(False, False)
        self.grab_set()  # Modal
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    

        # Text
        label = ctk.CTkLabel(self, text=message, wraplength=280, justify="center")
        label.pack(padx=20, pady=(25, 15))

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))

        yes_btn = ctk.CTkButton(btn_frame, text="Yes", width=80, command=self.on_yes, fg_color="#FF4D4D", hover_color="#444444", text_color="white")
        yes_btn.pack(side="left", padx=5)

        no_btn = ctk.CTkButton(btn_frame, text="No", width=80, command=self.on_no, fg_color="#FF4D4D", hover_color="#444444", text_color="white")
        no_btn.pack(side="left", padx=5)

    def on_yes(self):
        self.result = "yes"
        self.destroy()

    def on_no(self):
        self.result = "no"
        self.destroy()

    def on_close(self):
        self.result = "no"
        self.destroy()



def auth_bot_prompt(title: str, message: str):
    import tkinter

    root = ctk.CTk()
    set_vayl_icons(root)
    root.update_idletasks()
    root.withdraw()  # hide base window

    dialog = YesNoDialog(root, title, message)
    dialog.update_idletasks()

    root.wait_window(dialog)
    root.destroy()
    # 🧹 Force Tk/Tcl to fully shut down so it doesn't block asyncio/aiohttp
    try:
        if tkinter._default_root is not None:
            tkinter._default_root.quit()
    except Exception:
        pass
    tkinter._default_root = None

    return dialog.result






# Bot Auth

def save_credentials(data, path=None):
    """Safely save updated credentials.yml."""
    if path is None:
        path = os.path.join(os.getcwd(), "configuration", "credentials.yml")

    # Ensure folder exists (in case user deleted 'configuration')
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                default_flow_style=False,
                sort_keys=False,   # keep your _version and structure order
                allow_unicode=True
            )
        prompt("success", "Saved Credentials")
    except Exception as e:
        prompt("error", "Failed to save credentials")
        





def get_resource_path(relative_path: str) -> str:
    """Return path that works in both script and frozen exe."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running as a bundled exe
        base_path = sys._MEIPASS
    else:
        # Running as a normal .py script
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def set_vayl_icons(window):
    try:
        icon16 = tk.PhotoImage(file=get_resource_path("_vresources/vayl16.png"))
        icon32 = tk.PhotoImage(file=get_resource_path("_vresources/vayl32.png"))
        window.iconphoto(True, icon16, icon32)
    except Exception as e:
        print(f"Could not set icon: {e}")

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
                    "action.slideshow" : "Attempting to run 'slideshow' action.",
                    "action.media" : "Attempting to run 'media' action.",
                    "action.timeout" : "Attempting to run 'timeout' action.",
                    "action.console" : "Attempting to run 'console' action.",
                    "action.webhook" : "Attempting to run 'webhook' action.",
                    "action.conditional" : "Attempting to run 'conditional' action.",
                    "action.table" : "Attempting to run 'table' action.",
                    "action.tts" : "Attempting to run 'tts' action.",
                    "action.clip" : "Attempting to run 'createclip' action",
                    "action.addmarker" : "Attempting to run 'addmarker' action",
                    "action.actionpack" : "Attempting to run 'actionpack' action",
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

 

 
 
 
def get_version():
    try:
        version_path = os.path.join(os.getcwd(), "configuration", "version.txt")
        with open(version_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        prompt ("error", "Missing version.txt")
        return "missing version.txt"
        
        
   
def set_console_size(cols=80, lines=20):
    """Force smaller console dimensions on Windows only."""
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("Vayl")
            os.system(f"mode con: cols={cols} lines={lines}")
        except Exception:
            pass
       

# --- Build header ---
def build_header():
    header_text = Text.assemble(
        ("Vayl", "bold red"),
        ("  |  ", "bright_black"),
        (f"Version {__version__}", "white")
    )
    return Panel(header_text, border_style="red", expand=True)


# --- Build log area ---
def build_log_panel():

    global logs
    # ✅ NEW: keep only the most recent N lines so old ones scroll off naturally
    MAX_VISIBLE = 18
    table = Table(show_header=False, box=None, expand=True)
    for line in logs[-MAX_VISIBLE:]:
        table.add_row(Text.from_markup(line))
    return Panel(table, border_style="bright_black", expand=True)


# --- Background display updater ---
async def console_ui():
    if not CONSOLE_UI_ENABLED:
        return  # no fancy UI, let prompt() handle prints

    with Live(console=console, refresh_per_second=8, screen=False) as live:
        while True:
            header = build_header()
            log_panel = build_log_panel()
            live.update(Panel(log_panel.renderable, title="Vayl (" + __version__ + ")", border_style="white"))

            await asyncio.sleep(0.25)

# --- Prompt function ---
def prompt(kind: str, message: str):
    icons = {
        "success": ("[+]", "green"),
        "error":   ("[!]", "red"),
        "warn":    ("[~]", "yellow"),
        "info":    ("[>]", "cyan"),
        "misc":    ("[·]", "white"),
        "blank":   ("   ", "bright_black"),
    }
    sym, color = icons.get(kind, icons["misc"])
    timestamp = datetime.now().strftime("%H:%M:%S")

    # proper Rich markup
    line = f"[dim][{timestamp}][/dim] [{color}]{sym}[/] {message}"
    plain = Text.from_markup(line).plain

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(plain + "\n")
    except Exception:
        pass
    
    logs.append(line)

    # extra visibility when UI disabled
    if not globals().get("CONSOLE_UI_ENABLED", True):
        print(line)  # prints raw Rich markup nicely




version_path = get_resource_path("_vresources/version.txt")
with open(version_path, "r", encoding="utf-8") as f:
    __version__ = f.read().strip()


LOG_DIR = os.path.join(os.getcwd(), "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt"))
 
ERROR_DIR = os.path.join(LOG_DIR, "errors")
os.makedirs(ERROR_DIR, exist_ok=True)
 
async def main():
    # run both concurrently
    await asyncio.gather(
        console_ui(),  # live console refresh
        run(),         # your Twitch logic
    )


if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    set_console_size()
    asyncio.run(main())
 
 

