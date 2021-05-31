# -*- coding: utf-8 -*-
import os
import vk_api
import time
import json
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
import re

import sys
import urllib
import datetime
import re
import traceback
__update__ = "03.04.2021"

# osk = ["текст","текст"] и так далее в случае если мозг ебет


files = ["Database.json", "Admins.json", "Accounts.txt"]

def CheckFiles():
    for file_ in files:
        if not os.path.isfile(file_):
            fileNew = open(file_,"w")
            if file_ == "Accounts.txt":
                print("Введите данные аккаунтов по одномy. Логин и пароль через пробел. Как закончаться аккаунты введите пустую строку")
                data = input("\n")
                while data:
                    fileNew.write(data)
                    data = input("\n")
            elif file_ == "Admins.json":
                admin_id = input("Введите ваше айди для управления ботнетом \n")
                data = {admin_id:str(time.time()+86400*365*10)}
                fileNew.write(str(json.dumps(data)))
            else:
                fileNew.write("{}")
            fileNew.close()
            print(f"Файл <{file_}> создан")

    _ = list()

    for file_ in files:
        with open(file_) as f:
            _.append(f.readlines())

    variables.database, variables.admins, accounts = _
    variables.admins = json.loads("".join(variables.admins))
    variables.database = json.loads("".join(variables.database))


class variables:
    database = None
    admins = None
    raid_bots = None
    insult = None
    botAdminId = None
    attach = None
    bot_ids = []
    hate = False
    blitz = False
    stopBotnet = False
    bots = 0
    floodComm = ("!помощь", "!staff", "/help", "!пинг", "!онлайн", "!позвать модераторов", "!бан @id12345", "!кик @id12345", "!мут @id12345", "гиф порно")

ava = [
    "https://sun9-1.userapi.com/impg/9S7zocv-joV-bykF5mQIjJLJfxRzH0cEKjWH6g/uwPrQV3-OeA.jpg?size=947x1080&quality=96&sign=99228f299366c2e945e89229c054692a&c_uniq_tag=48Q10Sbi37YjexwMJTGw6J5lN7oKWttmY-3z0ZeYppk&type=album%27",
    "https://sun9-52.userapi.com/impf/c850120/v850120279/19d550/jz1f3OmJjUo.jpg?size=453x604&quality=96&sign=184399f3e2a969aa5b1afc6c4e7c6b15&c_uniq_tag=gDKAampR4HRnjZfAyNdUb7Sr3-egAu26XmSH-czPGVc&type=album%27",
    "https://sun9-4.userapi.com/impg/WupZ-gWxY3w96IjCB26sr4waOiQKQrefttsVWw/_uQ3Nx6FgrE.jpg?size=570x583&quality=96&sign=c93167224188482081be11a5f4886e68&c_uniq_tag=k41ggrqwSCYWKVWmSKlEs6FB7W7p4gsQuvmReNFdjhA&type=album%27",
    "https://sun9-49.userapi.com/impg/c857336/v857336685/146ef8/AKpm66QZX60.jpg?size=576x850&quality=96&sign=c868a2900490b4dcbea6e966e98cc5b5&c_uniq_tag=Gysdhr4OXOC6suAghl6fl6xboMCoKjotL_19hZNh9ds&type=album%27",
    "https://sun9-2.userapi.com/impg/-lbV4MoDt1KoXKYAWJXe3f8o8kpUSfmFPIFjHQ/vy09Tx-zcL8.jpg?size=1017x786&quality=96&sign=43a541687675bcdcce6dca10293fad0e&c_uniq_tag=FQsJp6Sps2uL69Gx2KhFr660ho5V8xjVkMdjKIKUZAk&type=album%27",
    "https://sun1-47.userapi.com/impg/c858228/v858228871/166b48/clx8kHGd92Y.jpg?size=736x909&quality=96&sign=c05418486000c1acd011478a1622394b&c_uniq_tag=gmKcpjNlmLxYNvYtrcb6cLpZ6gxc4Ddukd91FcHo6TM&type=album%27",
    "https://sun9-17.userapi.com/impg/c858332/v858332656/163b22/Rlpk-044p8w.jpg?size=600x600&quality=96&sign=d24c03f7d0e85c70ab021e604fdbf8d2&c_uniq_tag=eUIAgGFBS4w_Y_-KGWisDrpRe01KzT7gSYREAo-Dbcw&type=album%27",
    "https://sun9-62.userapi.com/impg/c853420/v853420644/195c3f/FixoOEX4wk0.jpg?size=1280x1138&quality=96&sign=ee842ea46e5d3f68a364d1d76078d9f9&c_uniq_tag=oJvslRAMGrKn6EavCFeStnqZDom01j2CrODGeREN6Io&type=album%27",
    "https://sun9-3.userapi.com/impg/c857416/v857416475/1279a2/H5lUek1-Iio.jpg?size=1000x600&quality=96&sign=3e1e34aa5dd5d54ece294e6ff10bae29&c_uniq_tag=ILLG4UiT4-DZL7J4PSKKPNRWka8TMmZTUR81LqJxBRI&type=album%27",
    "https://sun9-73.userapi.com/impf/c850428/v850428383/19bfd1/s_YNf6D4w6U.jpg?size=512x512&quality=96&sign=3747bbc26683f44bbe5939cc78b2fc27&c_uniq_tag=JLKzautaoOUN65-7_XcdzH7EG-65zTkEw9eEG9dSZgE&type=album%27",
    "https://sun9-11.userapi.com/impf/c858424/v858424312/1275e/Ke8W6Aef0E8.jpg?size=864x1080&quality=96&sign=b2465138acb25d4ee7d544f7004c4806&c_uniq_tag=HO8iL5kSnnoPYL5xcQhlHXAqChxB2xxWJGn68bXRhD4&type=album%27",
    "https://sun9-39.userapi.com/impf/c856016/v856016482/7404c/OWrZ-aKMDdQ.jpg?size=720x720&quality=96&sign=b0da0d0d0247216f2525c62aecdc9f26&c_uniq_tag=q3oMtken__GChJWaUYMkgGhp7Nz7W2c67vV13rOo678&type=album%27",
    "https://sun9-38.userapi.com/impf/c849328/v849328657/1c1b3a/WwBXwrV-xXk.jpg?size=720x720&quality=96&sign=6a5d84a128073ec5aa61400f570e3201&c_uniq_tag=R5K4FZ1dj9ud4beq_38BlxHtBTceLTWC8azU27Jc2cg&type=album%27",
    "https://sun9-13.userapi.com/impf/c852136/v852136507/b45d0/XIpSafYo9Ig.jpg?size=280x280&quality=96&sign=54422144a664d5e29b4f2415dee49284&c_uniq_tag=u-hDRo0IzTIqxYTju1rYy-vdbxLVP0kebILsRuLLBpQ&type=album%27"

    ]

def dd(d):
    days = ['день', 'дня', 'дней']
    if d % 10 == 1 and d % 100 != 11:
        p = 0
    elif 2 <= d % 10 <= 4 and (d % 100 < 10 or d % 100 >= 20):
        p = 1
    else:
        p = 2
    return str(d) + ' ' + days[p]

def vk_reg(user_id):
    link = rf'https://vk.com/foaf.php?id={user_id}'
    try:
        date = str(urllib.request.urlopen(link).read())
        match = re.search(r'\d{4}-\d\d-\d\d',date)[0]
        z = match.replace('-',',')
        a,b,d = int(z.split(",")[0]),int(z.split(",")[1]),int(z.split(",")[2])
        a = datetime.datetime.now() - datetime.datetime(a,b,d)
        match1 = re.search(r'\d\d:\d\d:\d\d',date)[0]
        months = {1:"Января",2:"Февраля",3:"Марта",4:"Апреля",5:"Мая",6:"Июня",7:"Июля",8:"Августа",9:"Сентября",10:"Октября",11:"Ноября",12:"Декабря"}
        match = f'{match.split("-")[2]} {months[int(match.split("-")[1])]} {match.split("-")[0] + " г."}'
        reg = f"{match} [{dd(a.days)}]"
    except:
        reg = vk_reg(user_id+1)
    return reg

class Helper:

    def parting(spisok,part_len):

        """Разбивает список на равные части нужной длины"""

        parts = len(spisok)//part_len+1

        return [spisok[part_len*k:part_len*(k+1)] for k in range(parts)]

    def takeToken(login, password):

        """Берёт токены из базы, если их нет, то получает через запросы"""

        data = Helper.checkAccount(login)
        if data:
            kate = data["kate"]
            user_id = data["user_id"]
            expired = data["expired"]
        else:
            try:
                f = requests.get(f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}")
                kate = f.json()["access_token"]
                user_id = f.json()["user_id"]
                expired = time.time()+86000
            except KeyError:
                print(f.json())
                if "redirect_uri" in f.json().keys():
                    if f.json()["redirect_uri"].startswith("https://m.vk.com/login?act=blocked"):
                        raise Exception(f"Account is blocked")
                raise Exception(f"Не могу взять токен у {login} {password}: \n {f.json()}")
            except Exception as error:
                raise Exception(f"Не могу взять токен у {login} {password}: \n {error}")
        variables.bot_ids.append(user_id)

        return kate, user_id, expired

    def checkAccount(login):

        """Проверяет, есть ли аккаунт в базе токенов"""

        with open("Database.json", "r") as f:
            database = f.readlines()
            database = json.loads("".join(database))
        for i in database:
            if login == database[i]["login"]:
                return {
                    "kate":variables.database[i]["kate"],
                    "user_id":variables.database[i]["id"],
                    "expired": variables.database[i]["expired"]
                }
        return False

    def checkExpiredTokens():

        """Проверяет базу на истёкшие токены. Пока не нужна,
        скорее всего удалю позже"""

        _ = list()
        for i in variables.database.keys():
            if variables.database[i]["expired"] < time.time():
                _.append([variables.database[i]["login"], variables.database[i]["password"]])
        return _

if variables.database:
    variables.botAdminId = variables.database["0"]["id"]
    for i in variables.database:
        variables.bot_ids.append(variables.database[i]["id"])

class Antikick:
    def __init__(self, kate, number):
        self.number = number
        self.id = variables.database[str(self.number)]['id']
        self.kate = kate

        self.event = None

    def testAntikick(self, **kwargs):

        """функция антикика эксекьютом. Направлена для противодействия кику
        @cm(Чат-менеджера), который кикает так же эксекьютом. Обычный антикик не успевает реагировать.
        Поэтому запускается цикл с эксекьютом для приглашения всех ботов сразу, не дожидаясь евентов от
        кика, что должно значительно повысить скорость антикика"""

        time.sleep(1) #Небольшая задержка, чтобы боты успели найти цель
        if not variables.database[self.number]['target']:
            return "Цель не задана! Укажите цель командой /target"
        code = f"var ch_id = {variables.database[self.number]['target']};\n"
        for i in variables.bot_ids:
            code += "API.messages.addChatUser({chat_id:ch_id,user_id:%s});\n" % i
        print(f"Антикик запущен: \n {code}")
        errors = []
        for i in range(50):
            try:
                self.vk.execute(code=code)
                time.sleep(0.34) # Небольшая задержка, т.к у ВК ограничение на 3 запроса в секунду.
            except Exception as err:
                print(f"[Bot #{self.number}]: ошибка в антикике эксекьютом: \n {err}")

        return "Антикик успешно отработал!"

    def antikickStart(self):

        """ Запуск сессии с токеном от кейта для антикика """
        self.session = vk_api.VkApi(token=self.kate)
        self.vk = self.session.get_api()
        longpoll = VkLongPoll(self.session)

        for self.event in longpoll.listen():
            if variables.stopBotnet:
                print(f"[Воин #{self.number}]: antikick stop!")
                exit()
            if self.event.type == VkEventType.CHAT_UPDATE:
                if self.event.type_id == 8:
                    if self.event.info["user_id"] > 0:
                        try:
                            self.vk.messages.addChatUser(
                                chat_id= self.event.chat_id,
                                user_id = self.event.info["user_id"]
                            )
                            print(f"[Воин #{self.number}]: add {self.event.info['user_id']}")
                        except vk_api.exceptions.ApiError as v:
                            print(f"[Воин #{self.number}]: no add {self.event.info['user_id']} \n Error: {v}")

            elif self.event.from_user:
                try:
                    if self.vk.messages.getById(message_ids = self.event.message_id)["items"][0]["from_id"] != self.id:
                        self.vk.messages.send(
                            forward_messages = self.event.message_id,
                            user_id = variables.adminId,
                            random_id = 0
                        )
                except IndexError:
                    print(x)
                    self.vk.messages.send(
                        forward_messages = self.event.message_id,
                        user_id = variables.adminId,
                        random_id = 0
                    )

            elif self.event.from_chat:
                try:
                    message = self.event.message.lower()
                except AttributeError:
                    pass
                else:
                    if (self.event.user_id == variables.adminId or str(self.event.user_id) in variables.admins.keys()) and message:

                        if message.startswith("/antikick"): #Команда одна, поэтому пока так
                            self.testAntikick()

    def starts(self):

        """Создаём рекурсию для антикика"""

        try:
            self.antikickStart()
        except vk_api.exceptions.Captcha as err:
            print(f"[Bot #{self.number}]: у меня капча")
            self.starts()
        except ConnectionResetError:
            self.starts()
        except requests.exceptions.ConnectionError:
            self.starts()
        except requests.exceptions.ReadTimeout:
            self.starts()
        except vk_api.exceptions.ApiError as err:
            if not "invalid" in str(err): # Если неверный логин/токен, то бот отрубается
                self.starts()
        except Exception as err:
            print(f"Антикик [Bot #{self.number}]: \n {err}")
            self.starts()
        finally:
            time.sleep(2)

class Botnet:
    def __init__(self, login, password, kate, expired, number):
        AntikickThread(kate,number).start()
        self.kate = kate

        self.password = password
        self.login = login
        self.number = str(number)
        self.id = variables.database[str(self.number)]['id']
        self.expired =  expired
        self.event = None
        variables.bot_ids.append(self.id)


    def getObjId(self):

        """Возвращает ID пользователя по ссылке на его страницу"""
        try:
            if "https://vk.com/" in self.event.message:
                pattern = re.compile(r"https://vk.com/")
                screen_name = pattern.sub("",self.event.message.split()[1])
                response =  self.vk.utils.resolveScreenName(screen_name=screen_name)
                user_id = response["object_id"]
                if response["type"] == "group":
                    user_id = -response["object_id"]
                else:
                    user_id = response["object_id"]

            elif re.search("[0-9]{1,}",self.event.message):
                user_id = int(re.search("[0-9]{1,}",self.event.message)[0])   # ]
                if re.search(r"\[club",self.event.message):
                    user_id *= -1
            else:
                response = self.vk.messages.getById(message_ids = self.event.message_id)
                if "reply_message" in response["items"][0].keys():
                    user_id = response["items"][0]["reply_message"]["from_id"]
                elif response["items"][0]["fwd_messages"]:
                    user_id = response["items"][0]["fwd_messages"][0]["from_id"]
            return user_id
        except:
            raise Exception("Нужно переслать сообщение")

    def users_get(self,screen_name,fields = 'online,name'):
        x = self.vk.users.get(
            user_ids = screen_name,
            fields = fields
        )
        return x

    def bots_info(self,**kwargs):
        """чекает ботов на присутствие в чате"""
        if self.id == variables.botAdminId:
            response = self.vk.messages.getChat(chat_id = self.event.chat_id)
            users = response["users"]
            bots_info = []
            number = 0
            qq = self.vk.users.get(user_ids=variables.bot_ids)
            for i in qq:
                if i["id"] in users:
                    in_chat = "(в чате)"
                else:
                    in_chat = "(нет в чате)"
                registration = vk_reg(i["id"])
                bots_info.append(f'#{number} @id{i["id"]}({i["first_name"]}) {in_chat} рега: {registration}')
                number += 1
            message = f"Информация о ботах ({len(bots_info)}):\n"+"\n".join(bots_info)
            return message

    def likes(self,**kwargs):
        """Ставит отметку << Мне нравится. >> на фото/пост/видео"""
        message = self.event.message
        response = self.vk.messages.getById(message_ids = self.event.message_id)
        if "reply_message" in response["items"][0].keys():
            user_id = response["items"][0]["reply_message"]["from_id"]
        elif response["items"][0]["fwd_messages"]:
            user_id = response["items"][0]["fwd_messages"][0]["from_id"]
        else:
            user_id = self.event.user_id
        try:
            message.find('https://vk.com')
            obj = re.findall("wall|photo|video|\d+",message)
            type,owner_id,item_id = obj[0].replace("wall","post"),obj[1],obj[2]
        except:
            response = self.users_get(
                screen_name = user_id,
                fields = 'photo_id',
            )
            photo_id = response[0]["photo_id"]
            item_id = int(photo_id[photo_id.find("_")+1:])
            type,owner_id = "photo",user_id
        try:
            likes = self.vk.likes.add(
                type = type,
                owner_id = owner_id,
                item_id = item_id
            )["likes"]
            message = f"Лайкнул, кол-во лайков: {likes} ❤ "
        except Exception as v:
            message = f"{v}"
        return message

    def sendMessage(self, message):

        """Отправляет сообщение в диалог/беседу"""

        response = self.vk.messages.send(
            peer_id = self.event.peer_id,
            message = message,
            random_id = 0,
            disable_mentions = 1
        )
        return response

    def crack(self, **kwargs):

        """Флудит командами некоторых чат-менеджеров.  Параметры:
        [iris] - команды Ириса
        [cm] - команды Чат-менеджера
        [ab] - команды AdminBot
        [kai] - команды Кая

        По умолчанию общие, наиболее употребительные, команды"""

        if "iris" in self.event.message:
            comms = ["ирис помощь", "!staff", "!позвать модераторов", "кто я", "!онлайн", "кто не вип", "!топ"
            "стата", "гиф порно", "адвокат!!!", "награды", "заметки", "биржа клава", "биржа график", "беседы",
            "карта помощь", "карта", "правила", "темы", "купить 10", "мешок", "кто дуэль", f"брак @id{self.id}"]

        elif "cm" in self.event.message:
            comms = ["!помощь", "!staff", "!роль", "!моястата", "!онлайн", "!статистика",
            "!оффлайн", "!рейтинг", "!моичаты", "!неупоминать", "!неоповещать", "!сообщатьбаны", "!сообщатьразбаны", "!сообщатьпреды",
            "!сообщатьпревенты", "!сообщатьсобытия", "!вчат", "!правила", "!togglegroup", "!привязат"]

        elif "ab"in self.event.message:
            comms = ["/help", "онлайн", "/info @id{self.id}", "ножки", "дошик 5 минут", "/chat",
            "/правила", "/приветствие", "/ник Огай гей", f"уебать @id{self.id}", f"брак @id{self.id}", "мафстарт"]

        elif "kai" in self.event.message:
            comms = ["кай топ", "кай погода москва", "кай выбери вилкой в глаз или в жопу раз", "кай помощь", "кай мне значок ✅",
            "кай кто дятел", "/приветствие", "кай чат", f"кай созвать всех", f"кай мне ник кай какашка", "кай праздники",
            "кай браки", "кай онлайн", "кай топ бесед", "кай беседы", "кай оффлайн", "кай актив", "кай имена"]

        else:
            comms = variables.floodComm
        for i in range(4):
            self.vk.messages.send(
                message = random.choice(comms),
                chat_id = variables.database[self.number]["target"],
                random_id = 0
            )

    def blitzMode(self, **kwargs):

        """При включеном блице боты автоматически флудят при инвайте в беседу"""

        if self.id == variables.botAdminId:
            variables.blitz ^= True
            return f"Блицкриг: {variables.blitz}"

    def hateMode(self, **kwargs):

        """Боты начинают материть всех фразами из базы осков"""

        if self.id == variables.botAdminId:
            variables.hate ^= True
            return f"Хейтмод – {variables.hate}"

    def push(self,**kwargs):

        """Пропушивает всех юзеров в беседе. Заваливает уведомления"""

        users = self.vk.messages.getChat(chat_id = variables.database[self.number]["target"])["users"]
        users = Helper.parting([f"@id{i}(а)" for i in users if i > 0],25)
        for i in users:
            self.vk.messages.send(
                message = "@еvеrуоnе "+ " ".join(i)+f"\n\n Созыв пидоров... ",
                chat_id = variables.database[self.number]["target"],
                random_id = 0
            )
            time.sleep(2)
        print(f"Bot #{self.number} пропушал всех")

    def addDesant(self,**kwargs):
        variables.desant = self.event.message.split("\n")[1].split(",")
        self.sendMessage("Боты к закидке:\n"+",".join(variables.desant))

    def showAdmins(self,**kwargs):

        """Показывает админки. Удаляет из списка истёкшие админки и заблокированные профили"""
        if self.id == variables.botAdminId:
            message = "\n🎩 Админы: \n"
            response = self.vk.users.get(user_ids = ",".join(variables.admins.keys()))
            expired, *banned, copyAdmins = [[],list(variables.admins.values())]
            for i in response:
                if "deactivated" in i.keys():
                    banned.append(f'@id{i["id"]}({i["first_name"]} {i["last_name"]})')
                    variables.admins.pop(str(i["id"]))
                else:
                    date = copyAdmins[response.index(i)]
                    if date < time.time():
                        expired.append(f'@id{i["id"]}({i["first_name"]} {i["last_name"]})')
                        variables.admins.pop(str(i["id"]))
                    else:
                        date = time.strftime('%H:%M %d %B %Y', time.gmtime(date + 18000))
                        message += f'@id{i["id"]}({i["first_name"]} {i["last_name"]}) – {date}\n'
            if banned:
                message += "\n 🐩 Заблокированные профили удалены: \n" + ", ".join(banned)
            if expired:
                message += "\n ⏱ Истёкшие админки: \n" + ", ".join(expired)
            with open("Admins.json","w") as f:
                f.write(json.dumps(variables.admins))
            return message

    def setAdminBot(self, **kwargs):

        """Выдаёт делает главным другого бота"""
        bot_id = self.getObjId()
        assert bot_id in variables.bot_ids, "Это не бот"
        variables.botAdminId = bot_id
        if self.id == variables.botAdminId:
            return "Теперь я главный бот ✅"

    def addAdmin(self, **kwargs):

        """Добавить админа. Необходимо переслать сообщение или указать на него ссылку.
        Срок на который нужно выдать админку указывается в днях с новой строки"""

        if self.id == variables.botAdminId:
            response = self.vk.messages.getById(message_ids = self.event.message_id)
            if "reply_message" in response["items"][0].keys():
                user_id = response["items"][0]["reply_message"]["from_id"]
            elif response["items"][0]["fwd_messages"]:
                user_id = response["items"][0]["fwd_messages"][0]["from_id"]
            else:
                try:
                    user_id = self.getObjId()
                except:
                    user_id = self.event.user_id
                assert user_id > 0, "Это группа дятел"
            assert user_id > 0, "Это группа дятел"
            try:
                date = time.time() + int(self.event.message.split("\n")[1])*86400
            except Exception as v:
                date = time.time() + 7*86400
            variables.admins.update({(str(user_id)):date})
            with open("Admins.json","w") as f:
                f.write(json.dumps(variables.admins))
            return f"@id{user_id}(Админ) добавлен✅\nСрок окончания админки: {time.strftime('%d-%m-%y %H:%M:%S', time.gmtime(date+14400))}"

    def report(self,**kwargs):
        """Репортим юзера"""

        user_id = self.getObjId()
        assert user_id > 0, "Это группа дятел"
        try:
            self.vk.users.report(
                user_id = user_id,
                type = "spam"
            )
            return f"@id{user_id} жалоба отправлена"
        except vk_api.exceptions.ApiError as v:
            return f"{v}"

    def flood(self, **kwargs):

        """Флудит сообщениями. Можно указать свой текст с новой строки.
        Текст по умолчанию стоит в настройках. Его также можно изменить"""

        for i in range(8):
            message_id = self.vk.messages.send(
                message = "\n❤😋⛔🔥💨🖤🌚🆘💙💚💜💝🔥💨🖤⛔💞💝😜😄😉🙂😐🤔❤💋😍😘☺😻😈👿💩🙊🙉😾😿🙀😺👺👹🆘🔞"*4,
                chat_id = variables.database[self.number]["target"],
                random_id = 0
            )
            time.sleep(1.5)
            self.vk.messages.edit(
                attachment = variables.repost,
                message_id = message_id,
                message = "༒۞☬L͍ᵉ͍ᵍ͍ⁱ͍ᵒ͍ⁿ͍ R͍ᵃ͍ⁱ͍ᵈ͍☬͍۞༒"+"\n❤😋⛔🔥💨🖤🌚🆘💙💚💜💝🔥💨🖤⛔💞💝😜😄😉🙂😐🤔❤💋😍😘☺😻😈👿💩🙊🙉😾😿🙀😺👺👹🆘🔞"*500,
                peer_id = 2000000000+variables.database[self.number]["target"],
            )
        print(f"[Bot #{self.number}]: успешно профлудил редачем!")

    def spamToUser(self, **kwargs):

        """Спамит в личку пользователю. Необходимо указать ссылку на него.
        Текст либо по умолчанию, либо укажите свой с новой строки"""

        user_id = self.getObjId()
        for i in range(18):
            self.vk.messages.send(
                peer_id = user_id,
                message = kwargs["defaultText"],
                attachment = variables.repost,
                random_id = 0
            )
            time.sleep(1.5)
        return f"[Bot #{self.number}]:Пользователь @id{user_id} заспамлен!"

    def spamToComments(self, **kwargs):

        """Спамит на стенку. Необходимо указать ссылку на нужный пост.
        Текст либо по умолчанию, либо укажите свой с новой строки"""

        try:
            response = re.findall(r"-\d+|\d+", self.event.message)
            owner_id = response[0]
            post_id = response[1]
        except IndexError:
            raise Exception("❗ Укажите ссылку на пост")
        else:
            for i in range(4):
                self.vk.wall.createComment(
                    owner_id = owner_id,
                    post_id = post_id,
                    message = kwargs["defaultText"]
                )
            print(f"[Bot #{self.number}]: Оставил комментарии. \n Цель: wall{owner_id}_{post_id} \n Текст: {kwargs['defaultText']}")

    def addBotsToFriend(self, **kwargs):

        """Добавить всех ботов в друзья к друг другу"""

        errors = []
        for i in set(variables.bot_ids):
            try:
                if i != self.id: self.vk.friends.add(user_id = i)
            except Exception as err:
                errors.append(f"@id{i}: {err}")
            time.sleep(3)
        if errors:
            return F"Не удалось добавить некоторых ботов:\n\n" + "\n".join(errors)
        return f"Successfully ✅ "

    def test(self, **kwargs):

        """Проверяет пинг ботов"""
        variables.bots = 0
        ping = time.time() - self.event.timestamp
        self.vk.messages.setActivity(peer_id = self.event.peer_id,type = "typing")
        variables.bots += 1
        time.sleep(2.5)
        if self.id == variables.botAdminId:
            return f"*Botnet Ready!*\n[ping {round(ping,3)}с]\nNumber #{self.number}\nЗапущено {format(str(variables.bots))} / {len(set(variables.bot_ids))} "


    def sendText(self, **kwargs):

        """Отправляет флудит заданным текстом"""

        self.vk.messages.send(
            chat_id = variables.database[self.number]["target"],
            message = kwargs["defaultText"],
            attachment = variables.repost,
            random_id = 0
        )
        print(f"[Bot #{self.number}]: успешно отправил сообщение в цель")


    def joinToChat(self, **kwargs):

        """Зайти в чат по ссылке. Поддерживает параметры:
        /t - зайти в беседу с интервалом в 3 сек
        /d - при заходе закинуть ботов, а точнее всех друзей бота, это могут \
        быть другие боты, а можно закинуть 200-300 рандомных человек с друзей
        /f - флудить командами при заходе
        /r - закинуть групповых ботов"""

        response = self.vk.messages.getById(message_ids = self.event.message_id)
        inviteLink = re.search(r"https://vk.me/join/[^']{1,}", str(response))
        if not inviteLink:
            raise ValueError("Ссылка на чат не найдена")
        self.vk.messages.getChatPreview(link=inviteLink[0])
        code = "var chat_id = API.messages.joinChatByInviteLink({link:'%s'}).chat_id; \n" % inviteLink[0]
        if "/f" in self.event.message:
            code += "var msg_id = API.messages.send({chat_id:chat_id,message:'%s',random_id:0});\n"*4
            code = code % tuple(random.choice(variables.floodComm) for i in range(4))
        try:
            self.vk.messages.getChat(chat_ids = ",".join([str(i) for i in range(3000)]))
        except vk_api.exceptions.ApiError as Error:
            variables.database[self.number]["target"] = int(str(Error).split("incorrect")[1])
        if "/t" in self.event.message:
            time.sleep(int(self.number)*3)
        self.vk.execute(code=code)
        if "/d" in self.event.message:
            self.addUsers()

    def setAvatar(self, **kwargs):

        """Устанавливает аватарку ботам прикрепленного фото"""

        response = self.vk.messages.getById(
            message_ids = self.event.message_id,
            extended = 1
        )
        try:
            link = response["items"][0]["attachments"][0]["photo"]["sizes"][-1]["url"]
        except:
            link = random.choice(ava)
        p = requests.get(link)
        out = open("photo.jpg", "wb")
        out.write(p.content)
        out.close()
        a = self.vk.photos.getOwnerPhotoUploadServer(
            owner_id = self.id
        )
        b = requests.post(a['upload_url'], files={'photo': open('photo.jpg', 'rb')}).json()
        self.vk.photos.saveOwnerPhoto(
            photo= b['photo'],
            server= b['server'],
            hash= b['hash']
        )
        return "Аватарка обновлена ✅"

    def setTarget(self, **kwargs):

        """Задать цель для атаки. Большинство команд работает по цели.
        Для задания цели необходимо указать название или часть названия нужного чата"""

        if self.event.message == "/target":
            variables.database[self.number]["target"] = self.event.chat_id
            self.sendMessage(f"[Bot #{self.number}]: Цель – эта беседа")
        else:
            title =self.event.message[self.event.message.find("target")+7:]
            found = False
            response = self.vk.messages.getConversations(count = 200)
            for i in response["items"]:

                try:
                    if title.lower() in i["conversation"]["chat_settings"]["title"].lower():
                        found = True
                        state =i["conversation"]["chat_settings"]["state"]
                        variables.database[self.number]["target"] = i["conversation"]["peer"]["local_id"]
                        self.sendMessage(f"[Bot #{self.number}]: цель – {i['conversation']['chat_settings']['title']} \n State: {state}")
                        break
                except KeyError as e:
                    pass

            if not found:
                self.sendMessage(f"[Bot #{self.number}]: Не нашёл чата с названием {title}")

    def setChatPhoto(self, **kwargs):

        """Обновляет обложку беседы. По умолчанию на феникса, можно прикрепить свою к сообщению"""

        response = self.vk.messages.getById(message_ids =self.event.message_id,extended = 1)
        try:
            link = response["items"][0]["attachments"][0]["photo"]["sizes"][-1]["url"]
        except:
            link = "https://sun9-44.userapi.com/x_yacO4iYQ_M-hE3oDAjLl-I6ZbUXMfSdy1vYA/sG5K9TY4LNw.jpg"
        finally:
            p = requests.get(link)
            out = open("photo.jpg", "wb")
            out.write(p.content)
            out.close()
            a = self.vk.photos.getChatUploadServer(chat_id = variables.database[self.number]["target"])
            b = requests.post(a['upload_url'], files={'photo': open('photo.jpg', 'rb')}).json()
            for i in range(4):
                self.vk.messages.setChatPhoto(file=b["response"])
            print(f"[Bot #{self.number}]: Успешно сменил обложку беседы!")

    def setChatTitle(self, **kwargs):

        """Меняет название чата. Указывать новое название с новой строки"""

        for i in range(10):
            self.vk.messages.editChat(
                chat_id = variables.database[self.number]["target"],
                title = kwargs["defaultText"]
            )
        print(f"[Bot #{self.number}]: Успешно сменил название беседы!")

    def setPinMessage(self, **kwargs):

        """Закрепляет/открепляет сообщение. Его можно задать с новой строки"""

        x = self.vk.messages.send(
            chat_id = variables.database[self.number]["target"],
            message = kwargs["defaultText"],
            random_id = 0
        )
        for i in range(20):
            self.vk.messages.pin(peer_id = 2e9 + variables.database[self.number]["target"],message_id = x)
            self.vk.messages.unpin(peer_id = 2e9 + variables.database[self.number]["target"])
        print(f"[Bot #{self.number}]: Успешно проспамил закрепом/открепом сообщений!")

    def clear(self, **kwargs):

        """Удалить свои сообщения в беседе"""

        response = self.vk.messages.getHistory(peer_id = self.event.peer_id,count = 200)
        delete_msg = ""
        for i in response["items"]:
            if i["from_id"] == self.id and "action" not in i.keys():
                delete_msg += f"{i['id']},"
        try:
            self.vk.messages.delete(
                message_ids = delete_msg,
                delete_for_all = 1
            )
        except vk_api.exceptions.ApiError as v:
            pass
        print(f"[Bot #{self.number}]: Удалил свои сообщения")

    def joinGroup(self, **kwargs):

        """Вступить в группу. Указывать цифрами нужное айди"""

        group_id = self.event.message.split()[1]
        self.vk.groups.join(group_id = group_id)
        print(f"[Bot #{self.number}]: вступил в @club{group_id}")

    def leaveGroup(self, **kwargs):

        """Выйти с группы. Указывать цифрами нужное айди"""

        group_id = self.event.message.split()[1]
        self.vk.groups.leave(group_id = group_id)
        print(f"[Bot #{self.number}]: отписался от @club{group_id}")

    def leaveChat(self, **kwargs):

        """Ливнуть с беседы.
        /leave - ливнуть с этой беседы
        /leave target - ливнуть с таргета"""

        if self.event.message == "/leave target":
            chat_id = variables.database[self.number]["target"]
        else:
            chat_id = self.event.chat_id
        self.vk.messages.removeChatUser(
            member_id = self.id,
            chat_id = chat_id
        )
        print(f"[Bot #{self.number}]: вышел с чата")

    def addFriend(self, **kwargs):

        """Добавляет в друзья по айдишнику. По умолчанию добавит
        вызвавшего данную команду"""
        try:
            user_id = self.getObjId()
        except:
            user_id = self.event.user_id

        assert user_id > 0, "Это группа дятел"

        self.vk.friends.add(user_id = user_id)
        return f"Добавил @id{user_id} ✅"

    def execute(self, **kwargs):

        """Выполнить код в vk.execute"""

        code = self.event.message[8:]
        try:
            message = self.vk.execute(code=code)
        except Exception as err:
            message = f"{err}"
        return message

    def evalExpression(self, **kwargs):

        """Выполнить строку кода в eval. Возвращает результат выражения"""

        assert self.event.user_id == int(variables.adminId), "Команда недоступна"
        try:
            message = str(eval(self.event.message[5:]))
        except Exception as err:
            message = f"{err}"
        return message

    def execExpression(self, **kwargs):

        """Выполнить код в exec. Возвращает None"""

        assert self.event.user_id == int(variables.adminId), "Команда недоступна"
        try:
            message = str(exec(self.event.message[6:]))
        except Exception as err:
            message = f"{err}"
        return message

    def edit(self,**kwargs):

        """Флудить редактированием сообщения"""

        for i in range(4):
            message_id = self.vk.messages.send(
                message = random.choice(variables.floodComm),
                chat_id = variables.database[self.number]["target"],
                random_id = 0
            )
            time.sleep(1)
            self.vk.messages.edit(
                message = kwargs["defaultText"],
                attachment = variables.repost,
                message_id = message_id,
                peer_id = 2e9 + variables.database[self.number]["target"]
            )
        print(f"[Bot #{self.number}]: успешно профлудил редачем!")

    def deleteDog(self, **kwargs):

        """Удаляет заблокированные группы, если указать параметр /u, то
        удалит заблокированные аккаунты ботов"""

        if self.id == variables.botAdminId:
            if "/u" in self.event.message:
                banned, invalid = [], []
                with open("Accounts.txt", "r") as f:
                    accounts = f.readlines()
                for i in accounts:
                    login = i.split()[0]
                    password = i.split()[1]
                    response = requests.get(f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}").json()

                    if "username_or_password_is_incorrect" in str(response):
                        invalid.append(login)
                        for q in variables.database.copy():
                            if variables.database[q]["login"] == login:
                                variables.database.pop(q)

                    elif "login?act=blocked" in str(response):
                        banned.append(login)
                        for q in variables.database.copy():
                            if variables.database[q]["login"] == login:
                                variables.database.pop(q)
                    time.sleep(3)
                with open("Accounts.txt", "w") as f:
                    for i in accounts:
                        if i.split()[0] not in [*invalid, *banned]:
                            f.write(i)
                with open("Database.json","w") as f:
                    f.write(json.dumps(variables.database))

                message = ""
                if banned:
                    message += "Заблокированные логины: \n" + "\n".join(banned)
                if invalid:
                    message += "\n\n Логины с неверными паролями: \n" + "\n".join(invalid)
                if not any([banned, invalid]):
                    message += "Заблокированных аккаунтов и аккаунтов с неверными паролями не обнаружено"
            else:
                banned, *lived = [[]]
                response = self.vk.groups.getById(group_ids = ",".join(variables.raid_bots))
                for i in response:
                    if "deactivated" in i.keys():
                        variables.raid_bots.remove(str(i["id"]))
                        banned.append(f"@club{i['id']}({i['name']})")
                    else:
                        lived.append(f"@club{i['id']}({i['name']})")
                with open(r"RaidBots.txt", "w") as f:
                    f.write("\n".join(variables.raid_bots)+"\n")
                if banned:
                    message = "Рейд-боты обновлены. Заблокированные боты: \n" + "\n".join(banned) + "\n\n Действующие: \n" + "\n".join(lived)
                else:
                    message = "Заблокированных ботов не обнаружено 😎"+"\n\nДействующие:\n" + "\n".join(lived)
            return message

    def addUsers(self,**kwargs):

        """Добавляет всех пользователей с друзей в таргетированную беседу"""

        qq = self.vk.friends.get()["items"]
        qq2 = Helper.parting(qq,25)
        for i in qq2:
            code = f"var \nch_id = {variables.database[self.number]['target']};\n"
            for q in i:
                code += "API.messages.addChatUser({user_id:"+str(q)+",chat_id:ch_id});\n"
            self.vk.execute(code=code)

    def comeback(self, **kwargs):

        """Инвайтит всех ботов в таргетированную беседу"""
        if not variables.database[self.number]['target']:
            return "Цель отсутствут! Задайте цель /target название беседы"
        qq2 = Helper.parting(variables.bot_ids,24)
        for i in qq2:
            code = f"var \nch_id = {variables.database[self.number]['target']};\n"
            for q in i:
                code += "API.messages.addChatUser({user_id:"+str(q)+",chat_id:ch_id});\n"
            self.vk.execute(code=code)
        try:
            self.vk.messages.addChatUser(user_id = int(random.choice(variables.bot_ids)), chat_id = variables.database[self.number]['target'])
        except Exception as error:
            message = f"{error}"
        return message

    def leave_return_flood(self, **kwargs):

        """Флудит входами/выходами из беседы"""

        code = """
            var chat_id = %s, user_id = %s;
            while(true){
                API.messages.addChatUser({chat_id:chat_id,user_id:user_id});
                API.messages.removeChatUser({chat_id:chat_id,user_id:user_id});
            }
        """ % tuple([variables.database[self.number]['target'], self.id])
        self.vk.execute(code = code)
        return "Профлудил входом/выходом ✅"

    def savePhoto(self, **kwargs):

        """Загружает фотографии со стенки себе в сохры"""

        owner_id = self.getObjId()
        response = self.vk.wall.get(owner_id = owner_id, count = 100)
        count = 0
        for i in response["items"]:
            try:
                if i["attachments"][0]["type"] == "photo":
                    owner_photo = i["attachments"][0]["photo"]["owner_id"]
                    photo_id = i["attachments"][0]["photo"]["id"]
                    self.vk.photos.copy(owner_id = owner_photo, photo_id = photo_id)
                    time.sleep(2)
            except KeyError as e:
                print(e)
            except vk_api.exceptions.ApiError as err:
                return f"Загрузил {count} фоток. \n {err}"
            else:
                count += 1
        return f"Все {count} фоток успешно загружены в сохры ✅"

    def clearSavePhotos(self, **kwargs):

        """Удаляет все фотографии в сохранёнках"""

        response = self.vk.photos.get(owner_id = self.id, album_id = "saved", count = 100)
        count = 0
        for i in response["items"]:
            self.vk.photos.delete(owner_id = self.id, photo_id = i["id"])
            count += 1
        return f"Удалил {count} фото из сохр ✅"

    def floodSavedPhotos(self, **kwargs):
        """Флудит фотками из альбома своих сохранёнок"""

        response = self.vk.photos.get(owner_id = self.id, album_id = "saved", count = 100)
        attachments = []
        for i in response["items"]:
            attachments.append(f"photo{i['owner_id']}_{i['id']}")
        assert bool(attachments) is True, "Альбом сохранёнок пуст! Загрузите сохры командой /save"
        for i in range(4):
            self.vk.messages.send(
                chat_id = variables.database[self.number]["target"],
                attachment = random.choice(attachments),
                random_id = 0
            )
        print(f"[Bot #{self.number}]: сообщения с фото-флудом успешно отправлены!")

    def exit_(self, **kwargs):

        """Оффнуть ботнет"""

        self.sendMessage("Ботнет деактивирован!")
        variables.stopBotnet = True

    def botnetStart(self):
        """ Запуск сессии с токеном от кейта """
        print(f"{self.number}:")
        self.session = vk_api.VkApi(token=self.kate)
        self.vk = self.session.get_api()
        longpoll = VkLongPoll(self.session)

        commands = {"/flood":self.flood, "/leave":self.leaveChat, "/groupleave":self.leaveGroup, "/groupjoin":self.joinGroup,
              "/clear":self.clear, "/pin":self.setPinMessage, "/title":self.setChatTitle, "/photo":self.setChatPhoto, "/botfriend":self.addBotsToFriend,
              "/target":self.setTarget, "/join":self.joinToChat, "/text":self.sendText, "/comment":self.spamToComments, "/execute":self.execute,
              "/test":self.test, "/spam":self.spamToUser,"/exit":self.exit_, "/eval":self.evalExpression, "/edit":self.edit, "/avatar":self.setAvatar,
              "/friend":self.addFriend, "/admin":self.addAdmin, "/admins":self.showAdmins,
              "/push":self.push,"/exec":self.execExpression,"/dog":self.deleteDog,
              "/desant":self.addDesant, "/hate":self.hateMode, "/blitz":self.blitzMode, "/crack":self.crack,
              "/boom":self.leave_return_flood, "/save":self.savePhoto, "/clearalbum":self.clearSavePhotos, "/attach":self.floodSavedPhotos,
              "/admbot":self.setAdminBot, "/comeback":self.comeback, "/report":self.report,"/likes":self.likes,"/botsinfo":self.bots_info}

        try:
            self.vk.friends.add(user_id = variables.adminId)
            chat_id = self.vk.messages.joinChatByInviteLink(link=variables.adminChatLink)["chat_id"]
            self.vk.messages.send(chat_id=chat_id,message=f"Bot #{self.number} прибыл!",random_id=0)
            self.vk.account.setPrivacy(key = 'closed_profile', value = "true")
        except Exception as v:
            print(v)

        for self.event in longpoll.listen():
            if variables.stopBotnet:
                print(f"[Bot #{self.number}]: основной поток остановлен!")
                exit()
            if self.event.type == VkEventType.CHAT_UPDATE:
                if self.event.type_id == 6:
                    if self.event.info["user_id"] == self.id and variables.blitz:
                        try:
                            for i in range(4):
                                message_id = self.vk.messages.send(
                                    message = random.choice(variables.floodComm),
                                    chat_id = self.event.chat_id,
                                    random_id = 0
                                )
                                time.sleep(1)
                                self.vk.messages.edit(
                                    attachment = variables.repost,
                                    message_id = message_id,
                                    message = "༒۞☬L͍ᵉ͍ᵍ͍ⁱ͍ᵒ͍ⁿ͍ R͍ᵃ͍ⁱ͍ᵈ͍☬͍۞༒"+"\n❤😋⛔🔥💨🖤🌚🆘💙💚💜💝🔥💨🖤⛔💞💝😜😄😉🙂😐🤔❤💋😍😘☺😻😈👿💩🙊🙉😾😿🙀😺👺👹🆘🔞"*500,
                                    peer_id = 2000000000+self.event.chat_id
                                )
                            print(f"[Bot #{self.number}]: успешно профлудил редачем!")
                        except Exception as error:
                            message = f"{error}"

            elif self.event.from_user:
                try:
                    message = self.event.message.lower()
                except AttributeError:
                    pass
                else:
                    if message.startswith("/reg"):
                        try:
                            response = self.vk.messages.getById(message_ids = self.event.message_id)
                            inviteLink = re.search(r"https://vk.me/join/[^']{1,}", str(response))

                            if inviteLink:
                                variables.adminChatLink = inviteLink[0]

                            with open("Accounts.txt", "r") as f:
                                accounts = f.readlines()
                                login = self.event.message.split()[1]
                                password = self.event.message.split()[2]
                                assert f"{login} {password}\n" not in accounts, "Вы уже есть в базе"
                                BotnetThread(login, password, len(accounts)).start()

                            with open("Accounts.txt", "a") as f:
                                f.write(f"{login} {password}\n")
                            message = f"Аккаунт успешно добавлен!"
                        except Exception as error:
                            message = f"{error}"
                        finally:
                            self.vk.messages.send(
                                user_id = self.event.user_id,
                                message = message,
                                random_id = 0
                            )
                    if message.startswith("/hatetext"):
                        try:
                            with open("hate.txt", "r") as f:
                                hate = f.readlines()
                                TEXT = self.event.message[10:]
                            with open("hate.txt", "a") as f:
                                f.write(f"{TEXT}\n")
                            message = f"триггер добавлен"
                        except Exception as error:
                            message = f"{error}"
                        finally:
                            self.vk.messages.send(
                                user_id = self.event.user_id,
                                message = message,
                                random_id = 0
                            )

            elif self.event.from_chat:
                try:
                    message = self.event.message.lower()
                    if "\n" in self.event.message:
                        defaultText = self.event.message.split("\n")[1]
                    else:
                        defaultText = variables.defaultText
                except AttributeError:
                    pass
                else:
                    if not variables.botAdminId:
                        variables.botAdminId = random.choice(variables.bot_ids)

                    if "vto.pe" in self.event.text.lower() or "vkbot.ru" in self.event.text.lower() and self.id not in variables.bot_ids:
                        self.vk.messages.delete(message_ids=self.event.message_id,spam = 1)
                        print(f"Пометил лоха [id{self.event.user_id}] как спам")

                    if (self.event.user_id in (variables.adminId, *variables.bot_ids) or str(self.event.user_id) in variables.admins.keys()):

                        if self.event.user_id not in variables.bot_ids:
                            if float(variables.admins[str(self.event.user_id)]) < time.time():
                                variables.admins.pop(str(self.event.user_id))
                                with open("Admins.json","w") as f:
                                    f.write(json.dumps(variables.admins))
                                self.sendMessage("❗ Ваша админка истекла")

                        if message.split()[0] in commands.keys():
                            if "#" not in self.event.message or f"{self.number}" in self.event.message.split("#")[-1].split(","):
                                try:
                                    if message.endswith("?help") and self.id == variables.botAdminId:
                                        message = commands[message.split()[0]].__doc__
                                    elif not message.endswith("?help"):
                                        message = commands[message.split()[0]](defaultText=defaultText)
                                    else:
                                        message = False
                                except  Exception as error:
                                    if str(error) == "[100] One of the parameters specified was missing or invalid: chat_id is undefined":
                                        self.sendMessage(f"[Bot #{self.number}]: Ошибка в команде {message.split()[0]}. Скорее всего вы не указали цель")
                                    else:
                                        self.sendMessage(f"[Bot #{self.number}]: Ошибка в команде {message.split()[0]}: \n{error}")
                                else:
                                    if message: self.sendMessage(message.replace("  ",""))

                        elif message == "/help" and self.id == variables.botAdminId:
                            comms = []
                            for i in commands.keys():
                                comms.append(f"📌 {i}: {commands[i].__doc__}")
                            message = f"Команды ботнета v{__update__}:\n" + "\n".join(comms)
                            self.sendMessage(message)

                    elif not any([variables.hate == False,
                                self.id == self.event.user_id, len(self.event.text) == 0, self.event.user_id < 0]):
                        self.vk.messages.setActivity(peer_id = self.event.peer_id, type="typing")
                        time.sleep(random.randint(2,4))
                        self.vk.messages.send(message=random.choice(osk),reply_to=self.event.message_id,chat_id=self.event.chat_id,random_id=0)

    def starts(self):

        try:
            self.botnetStart()
        except Exception as err:
            if "invalid" in str(err):
                print(f"Bot id{self.id} отлетел \n {err}")
            else:
                print(f"Bot #{self.number}: \n {err}")
                time.sleep(2)
                self.starts()

class BotnetThread(Thread):

    def __init__(self, login, password, number):

        """Инициализация потока"""

        Thread.__init__(self)
        self.number = number
        self.login = login
        self.password = password
        self.kate, self.user_id, self.expired = Helper.takeToken(login, password)
        variables.database.update({str(self.number):{"kate":self.kate, "id":
            self.user_id, "expired":self.expired, "target":None, "desant":True, "login":self.login, "password":self.password}})

    def run(self):

        """Запуск потока"""

        print(F"Bot #{self.number} основной поток запущен")
        Botnet(self.login, self.password, self.kate, self.expired, self.number).starts()

class AntikickThread(Thread):

    def __init__(self, kate, number):

        """Инициализация потока"""
        Thread.__init__(self, daemon = True)
        self.kate = kate
        self.number = number

    def run(self):

        """Запуск потока"""
        print(F"Воин #{self.number} антикик запущен")
        Antikick(self.kate,self.number).starts()