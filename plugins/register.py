from json import loads
from aiogram.types import ParseMode,ReplyKeyboardRemove
import re


async def run(msg,matches,functions,user,bot):

	if matches[0] == "/start":
		await msg.reply(f"سلام {msg.from_user.first_name} عزیز ✋\n\nبه 《{functions.config['bot_name']}🤖》 خوش اومدی ، توی این ربات می تونی افراد #نزدیک ات رو پیدا کنی و باهاشون آشنا شی و یا به یه نفر بصورت #ناشناس وصل شی و باهاش #چت کنی ❗️\n\n- استفاده از این ربات رایگانه و اطلاعات تلگرام شما مثل اسم،عکس پروفایل یا موقعیت *GPS* کاملا محرمانه هست😎\n\n`برای شروع جنسیتت رو انتخاب کن`👇",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.selectGenderMarkup())
		return

	if user['action'] == 'set_gender':
		if msg.text in ["من🙎‍♂️پسرم", "من🙍‍♀️دخترم"]:
			await functions.update_user(msg.from_user.id,{"gender": "f" if msg.text == "من🙍‍♀️دخترم" else "m", "action": "set_name","profile": "default_girl.jpg" if msg.text == "من🙍‍♀️دخترم" else "default_boy.jpg"})
			await msg.reply("خب حالا اسمتو بهم بگو فقط فارسی بگو چون اینگلیسیم خوب نی ☺️",reply_markup=ReplyKeyboardRemove())
			return
		else:
			await msg.reply("🙄لطفا جنسیتت رو از پنل زیر👇انتخاب کن", parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.selectGenderMarkup())
			return

	elif user['action'] == 'set_name':
		if not re.findall(r'[a-z][a-z][a-z]+', msg.text):
			await functions.update_user(msg.from_user.id, {"action": "set_age", "name": msg.text})
			await msg.reply("خب حالا باید سنتو بهم بگی ☺️\n\n• سنت رو از لیست پایین 👇انتخاب کن یا خودت تایپ کن",reply_markup=functions.keyBoards.createAgeMarkup())
			return
		else:
			await msg.reply("🙄 گفتم که اینگلیسیم خوب نیست لطفا فارسی بگو بهم")
			return
	elif user['action'] == 'set_age':
		if msg.text.isdigit():
			if int(msg.text) >= 9 and int(msg.text) < 100:
				await functions.update_user(msg.from_user.id, {"action": "set_city", "age": msg.text})
				await msg.reply("خب حالا فقط کافیه استانت رو انتخاب کنی تا وارد ربات شیم\n\n• استانت رو از لیست پایین 👇انتخاب کن",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createCityMarkup())
				return
			else:
				await msg.reply("🙄لطفا سنتو از رنج مشخص شده 9 تا 99 سال از پنل زیر👇 انتخاب کن یا برام تایپش کن",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createAgeMarkup())
				return
		else:
			await msg.reply("🙄لطفا سنتو رو از پنل زیر👇انتخاب کن یا به صورت عدد برام تایپش کن",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createAgeMarkup())
			return
	elif user['action'] == 'set_city':
		if msg.text in [i['name'] for i in loads(open("cities.json", 'r').read())]:
			await functions.update_user(msg.from_user.id, {"city": msg.text, "action": None, "coin": 10,"step":1})
			await msg.reply("✅اطلاعات شما ثبت شد.\n\nبه جمع ما خوش اومدی 😉\nبرای کار با ربات از دکمه ای زیر👇 استفاده کن\n\n🤗به مناسبت ورودت 10 تا سکه رایگان دریافت کردی به جمع ما خوش اومدی!",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
			return
		else:
			await msg.reply("🙄لطفا استانت رو از پنل زیر👇انتخاب کن", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createCityMarkup())
			return
plugin = {
	"name": "pv",
	"desc": "manage pv bot",
	"run": run,
	"chat_type": "private",
	"step": 0,

	"patterns_message": [
		"^/start$",
		"(.*)"
	],
	"patterns_callback": [
		"random",
		"search_boy",
		"search_girl",
		"search_gps",
	]
}