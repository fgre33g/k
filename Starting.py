# -*- coding: utf-8 -*-
import vk_api
from math import ceil
import time
import json
import traceback
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
import re

import sys
from Botnet import *

variables.adminId = "66105035"
variables.adminChatLink = "https://vk.me/join/rsk/eWpm3zhXRP7ZyU9oephure0mRj6KVVg=" #при старте боты зайдут в нужною конфу откуда ты будешь управлять ботами
variables.repost = "wall-202171360_9" #сюда attacment для репоста смайлами
variables.defaultText = "хуй"*200
 
CheckFiles()

with open("Accounts.txt") as f:
    accounts = f.readlines()

def create_threads():

    global i

    for i in accounts:
        try:
            number = accounts.index(i)
            login = i.split()[0]
            password = i.split()[1]
            print(f"Беру токен у {login} {password}")
            BotnetThread(login, password, accounts.index(i)).start()
            time.sleep(4)
        except Exception as error:            
            print(error)
            time.sleep(4)

    with open("Database.json", "w") as f:
        f.write(json.dumps(variables.database))
if __name__ == "__main__":
    create_threads()