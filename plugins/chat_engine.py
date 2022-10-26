from time import time
from aiogram.types import ParseMode

async def set_searchEngin(msg,chat_type,text,functions,user,bot):
	await msg.message.delete()
	if user['search']['connected']:
		await bot.send_message(msg.message.chat.id,f"⚠️ خطا : هم اکنون شما در حال چت با /user_{user['search']['connected_to']} هستید !\n\n<code>برای استفاده از ربات ابتدا باید مکالمه رو قطع کنی </code>👇",reply_markup=functions.keyBoards.createChatMarkup(user), parse_mode=ParseMode.HTML)
		return
	if user['search']['searching']:
		await bot.send_message(msg.message.chat.id,f"🙄 دارم برات یکیو پیدا میکنم باید یکم صبور باشی\n<code>- میتونی با دکمه پایین 👇گشتنمو لغو کنی</code>",reply_markup=functions.keyBoards.createCancelChatMarkup(), parse_mode=ParseMode.HTML)
		return
	user['search']['searching'] = True
	user['search']['search_gender'] = chat_type
	user['search']['request_at'] = int(time())
	await functions.update_user(msg.from_user.id, {"search": user['search']})
	await bot.send_message(msg.message.chat.id,f"🔎 درحال جستجوی مخاطب ناشناس شما\n- {text}\n\n⏳ حداکثر تا ۲ دقیقه صبر کنید.\n\n",reply_markup=functions.keyBoards.createFilerAgeMarkup(user), parse_mode=ParseMode.HTML)
	return

async def cancel_search(msg,functions,user,bot):
	if user['search']['connected']:
		await bot.send_message(msg.message.chat.id,f"⚠️ خطا : هم اکنون شما در حال چت با /user_{user['search']['connected_to']} هستید !\n\n<code>برای استفاده از ربات ابتدا باید مکالمه رو قطع کنی </code>👇",reply_markup=functions.keyBoards.createChatMarkup(user), parse_mode=ParseMode.HTML)
		return
	user['search']['searching'] = False
	user['search']['search_gender'] = None
	user['search']['request_at'] = None
	await functions.update_user(msg.from_user.id, {"search": user['search']})
	await msg.message.delete()
	await bot.send_message(msg.message.chat.id,"خب ، حالا چه کاری برات انجام بدم؟\n`از منوی پایین👇 انتخاب کن`", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createStartMarkup())
	return

async def run(msg,matches,functions,user,bot):
	pass

async def run_callback(msg,matches,functions,user,bot):

	if matches[0] == "random":
		await set_searchEngin(msg,matches[0],"<code>- 🎲 جستجوی شانسی</code>",functions,user,bot)
		return

	if matches[0] == "search_boy":
		await set_searchEngin(msg, matches[0],"<code>- 🎲 🙎‍♂️جستجوی پسر -</code>", functions, user, bot)
		return
	if matches[0] == "search_girl":
		await set_searchEngin(msg, matches[0],"<code>- 🎲 🙎‍♀️جستجوی دختر -</code>", functions, user, bot)
		return

	if matches[0] == "cancel":
		await cancel_search(msg,functions,user,bot)
		return

	if matches[0] == "filterAge":
		user['search']['filter_age_range'] = not user['search']['filter_age_range']
		await functions.update_user(msg.from_user.id, {"search": user['search']})
		await bot.edit_message_text(chat_id=msg.message.chat.id,message_id=msg.message.message_id,text=msg.message.text,reply_markup=functions.keyBoards.createFilerAgeMarkup(user), parse_mode=ParseMode.HTML)
		return

plugin = {
	"name": "pv",
	"desc": "manage pv bot",
	"run": run,
	"run_callback": run_callback,
	"chat_type": "private",
	"step": 1,

	"on_chat":False,
	"patterns_message": [
	],
	"patterns_callback": [
		"random",
		"search_boy",
		"search_girl",
		"search_gps",
		"cancel",
		"(filterAge):(.*)",
	]
}