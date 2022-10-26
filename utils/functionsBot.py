import string
import random
import sys

from .db import redis_db,mongo_db
from aiogram.types import InputFile
import os
from time import time
from json import loads
from .keyboards import KeyBoards
plugins = []
adminList = []
def loadPlugins():
    global plugins
    for plugin in os.listdir('./plugins'):
        values = {}
        plugin_dir = f'./plugins/{plugin}'
        with open(plugin_dir, encoding="utf-8") as f:
            code = compile(f.read(), plugin_dir, 'exec')
            exec(code, values)
            f.close()
        plugin = values['plugin']
        plugins.append(plugin)

loadPlugins()

class functions:

    def __init__(self):
        self.config = loads(open('config.json','r').read())

        self.keyBoards = KeyBoards()
        self.infoBot = None

    def setInfoBot(self,data):
        self.infoBot = data

    def getToken(self,index=0) -> str:
        if index > len(self.config['tokens'])-1:
            print("token index out of range !")
            sys.exit()
        self.bot_id = self.config['tokens'][index].split(':')[0]
        return self.config['tokens'][index]

    async def update_user(self,user_id=None,telegram_id=None,row=None) -> None:
        mongo_db.userlist['list'].update_one({"id": user_id},{"$set": row}) if user_id else mongo_db.userlist['list'].update_one({"user_id": telegram_id},{"$set": row})

    async def create_user(self,user_id) -> dict:
        ID = await self.generate_user_id()
        mongo_db.userlist['list'].insert_one({
            "id": ID,
            "name": None,
            "step": 0,
            "profile": None,
            "city": None,
            "silent": {
                "status": False,
                "disable_at": None
            },
            "invited_by": 0,
            "invited": 0,
            "online_at": 0,
            "age": 0,
            "user_id": user_id,
            "coin": 0,
            "gender": None,
            "blocked": [],
            "contacts": [],
            "likes": [],
            "location": [0, 0],
            "action": "set_gender",
            "search": {
                "searching": False,
                "search_gender": None,
                "search_type": None,
                "connected": False,
                "connected_to": None,
                "request_at": None,
                "secret_chat": False,
                "filter_age_range": False,
            },
            "bot_id": self.bot_id
        })
        return mongo_db.userlist['list'].find_one({"id": ID})
    async def load_user(self,user_id=None,telegram_id=None,self_get=False):
        #x = mongo_db.userlist['list'].delete_one({"id": user_id} if user_id else {"user_id": telegram_id})
        #print(x.deleted_count, " documents deleted.")
        user = mongo_db.userlist['list'].find_one({"id": user_id} if user_id else {"user_id": telegram_id})
        if user:
            if self_get:
                await self.update_last_online(user_id=user_id,telegram_id=telegram_id)
        else:
             return await self.create_user(telegram_id)
        return user

    async def is_admin(self,user_id):
        status = False
        if user_id in adminList:
            status = True
        return status

    async def update_last_online(self,user_id=None,telegram_id=None):
        await self.update_user(user_id=user_id,row={"online_at": int(time())}) if user_id else await self.update_user(telegram_id=telegram_id,row={"online_at": int(time())})

    async def get_profile(self,user):
        if user['bot_id'] == self.bot_id and len(user["profile"]) > 20:
            return False, user['profile']
        return True, InputFile(open(f'profiles/{user["profile"]}','rb'))

    async def get_content_type(self,msg):
        if msg.forward_from_chat:
            await msg.answer("forwarded")
            msg_type = '[%forwarded%]'
        elif msg.text:
            msg_type = msg.text
        elif msg.photo:
            msg_type = '[%photo%]'
        elif msg.sticker:
            msg_type = '[%sticker%]'
        elif msg.document and (msg.document.mime_type != "audio/mpeg" and msg.document.mime_type != "video/mp4" and msg.document.mime_type != 'image/gif'):
            msg_type = '[%document%]'
        elif msg.document and msg.audio:
            msg_type = '[%music%]'
        elif msg.document and msg.document.mime_type == "video/mp4":
            msg_type = '[%gif%]'
        elif msg.voice:
            msg_type = '[%voice%]'
        elif msg.contact:
            msg_type = '[%contact%]'
        elif msg.video_note:
            msg_type = '[%video_note%]'
        elif msg.video:
            msg_type = '[%video%]'
        elif msg.location:
            msg_type = '[%location%]'
        elif msg.game:
            msg_type = '[%game%]'
        else:
            msg_type = '[%unknow%]'
        return msg_type

    async def generate_user_id(self) -> str:
        characters = string.ascii_letters + string.digits
        while True:
            ID = ''.join(random.choice(characters) for i in range(6))
            if mongo_db.userlist['list'].count_documents({"id": ID}) == 0:
                break
        return ID

    async def check_is_chating(self,user_id) -> bool:
        pass

    async def check_join_to_channel(self,user_id)-> bool:
        pass

    async def check_exists_to_userList(self,user_id) -> bool:
        mongo_db.userlist['list'].delete_one({"user_id": user_id})
        if mongo_db.userlist['list'].count_documents({"user_id": user_id}) == 0:
            return False
        else:
            return True

    def convertHoumanTime(self,unixtime,is_chat=False) -> str:
        time_ = int(time() - unixtime)
        print(time_)
        if time_ > 360:
            if time_ < 0 :
                time_ = -time_
            day = time_//86400
            if day >= 0:
                if day < 31:
                    text =  f"⏳ {day} روز قبل "
                else:
                    text = "مدت ها قبل...👻 "
            if day == 0:
                hour = (time_ //3600)
                if hour != 0:
                    text = f"{hour} ساعت قبل⏳ "
                else:
                    min = (time_ //60)
                    if min >= 0:
                        text = f"⏳ {min} دقیقه قبل آنلاین بوده"
                if min == 0 and hour == 0 and day == 0:
                    text = "چند لحظه پیش ..."
        else:
            text = "هم اکنون 👀 آنلایـــن"
        if is_chat:
            text += " (🗣 درحال‌چت)"
        return text

    def get_gender(self,gender) -> str:
        if gender == "m":
            return "پسر 🙎‍♂️"
        return "دختر 🙍‍♀️"

    def openPhoto(self,file) -> bytes:
        return InputFile(open(f'profiles/{file}','rb'))