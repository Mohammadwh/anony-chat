from aiogram.types import ParseMode
from aiogram.types.user import User
from utils.db import mongo_db
import geopy.distance

async def create_line_user(location,data,index,functions):
	km = int(geopy.distance.geodesic(location, data['location']).km)
	return f"‏{index}. {'🙍‍♀️' if data['gender'] == 'f' else '🙎‍♂️'} {data['name']} /user_{data['id']}\n{data['age']} - {data['city']}  (🏁 {km}km)\n{functions.convertHoumanTime(data['online_at'],data['search']['connected'])}\n\n"

async def create_users_list(msg,gender,functions,user,bot,page):
	filters = {'location': {"$ne" : [0,0]},"id":{"$ne":user['id']}}
	index = 0
	if page != 1:
		index = page*10
	if gender != "all":
		filters["gender"] = gender
	text = "🛰 لیست افراد نزدیک به شما.\n"
	location = (user['location'][0], user['location'][1])
	for i in mongo_db.userlist['list'].find(filters).sort("online_at").skip(index):
		index += 1
		line = await create_line_user(user['location'],i,index,functions)
		text += line
	await bot.edit_message_text(chat_id=msg.message.chat.id,message_id=msg.message.message_id,text=text,parse_mode=ParseMode.HTML)



async def run(msg,matches,functions,user,bot):

	if matches[0] == '/start':
		await functions.check_exists_to_userList(msg.from_user.id)
		await msg.reply("خب ، حالا چه کاری برات انجام بدم؟\n`از منوی پایین👇 انتخاب کن`", parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
		return

	if matches[0] == '/user_':
		get_user = await functions.load_user(matches[1])
		if get_user:
			profile_status, profile = await functions.get_profile(get_user)
			await bot.send_photo(msg.from_user.id, photo=profile, reply_markup=functions.keyBoards.createProfileKeyboard(get_user, me=user,is_self=True if get_user['user_id'] == msg.from_user.id else False),caption=f"• نام: {get_user['name']}\n• جنسیت: {functions.get_gender(get_user['gender'])} \n• استان: {get_user['city']}\n• سن: {get_user['age']}\n\n♥️ لایک ها : {len(get_user['likes'])}\n\n{functions.convertHoumanTime(get_user['online_at'],get_user['search']['connected'])}\n\n‏🆔 آیدی : /user_{get_user['id']}\n‏")
		else:
			await msg.reply("⚠️ خطا : چنین کاربری وجود ندارد")
		return

	if matches[0] == "🔗 به یه ناشناس وصلم کن!":
		await msg.reply("به کی وصلت کنم؟ `انتخاب کن👇`", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createRandomKeyboard())
		return

	if matches[0] == "👤پروفایل":
		profile_status, profile = await functions.get_profile(user)
		response = await bot.send_photo(msg.from_user.id, photo=profile, reply_markup=functions.keyBoards.createProfileKeyboard(user),caption=f"• نام: {user['name']}\n• جنسیت: {functions.get_gender(user['gender'])} \n• استان: {user['city']}\n• سن: {user['age']}\n\n♥️ لایک ها : {len(user['likes'])}\n\n{functions.convertHoumanTime(user['online_at'],user['search']['connected'])}\n\n‏🆔 آیدی : /user_{user['id']}\n‏")
		if profile_status:
			await functions.update_user(msg.from_user.id, {"profile": response.photo[len(response.photo) - 1].file_id})
		return

	if matches[0] == "📍افراد نزدیک":
		if user['location'] == [0,0]:
			await msg.reply("- برای استفاده از این قابلیت اول باید موقعیت خودتو با استفاده از پنل پروفایل ثبت کنی 🙃🙄", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createStartMarkup())
		else:
			await msg.reply("🛰 چه کسایی رو نشونت بدم؟ `انتخاب کن`👇", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createGPSSearchKeyboard())
		return

	if matches[0] == "🔍 جستجوی کاربران 🔎":
		await msg.reply("🛰 چه کسایی رو نشونت بدم؟ `انتخاب کن`👇", parse_mode=ParseMode.MARKDOWN,reply_markup=functions.keyBoards.createUserSearchKeyboard())
		return

	if matches[0] == "💰سکه":
		await msg.reply(f"💰سکه فعلی شما : {user['coin']}\nـــــــــــــــــــــــــــــــ\n❓روش های بدست آوردن سکه چیست؟\n\n1️⃣ معرفی دوستان (رایگان) :\n\nبرای افزایش سکه به صورت رایگان بنر لینک⚡️ مخصوص خودت (/link) رو برای دوستات  بفرست و 20 سکه دریافت کن\n\n- برای اطلاعات بیشتر راهنمای سکه رو بخون (/help_credit)\n\n2️⃣خرید سکه بصورت آنلاین :\n\n<code>برای خرید سکه یکی از تعرفه های زیر را انتخاب نمایید</code>👇", parse_mode=ParseMode.HTML)
		return

	if matches[0] == "🚸 معرفی به دوستان (سکه رایگان)":
		if not isinstance(functions.infoBot,User):
			functions.infoBot = await functions.infoBot
		await bot.send_photo(msg.chat.id,photo=functions.openPhoto("bot-banner.jpg"),caption=f"《{functions.config['bot_name']}》 هستم،بامن میتونی\n\n📡 افراد #نزدیک ، #هم‌سنی ، #هم‌استانی خودتو پیداکنی و باهاشون #ناشناس چت کنی و آشنا شی😍\n\nپس منتظر چی هستی؟🤔 بدووو بیا که منتظرتم!🏃‍♂️\n\nهمین الان روی لینک بزن  👇\nt.me/{functions.infoBot.username}?start={user['id']}\n\n✅ #رایگان و #واقعی 😎")
		return

async def run_callback(msg,matches,functions,user,bot):

	if matches[0] == "show_gps":
		await create_users_list(msg, matches[1], functions, user, bot, int(matches[2]))
		return

	if matches[0] == "edit_profile":
		await bot.edit_message_caption(chat_id=msg.message.chat.id,message_id=msg.message.message_id,caption=msg.message.caption,reply_markup=functions.keyBoards.createEditProfileKeyboard(user), parse_mode=ParseMode.HTML)
		return

	if matches[0] == "edit_gender":
		if user['gender'] == "f":
			await functions.update_user(msg.message.chat.id, {"gender": "m","profile": "default_boy.jpg"})
			await bot.answer_callback_query(msg.id,"جنسیت فعلی شما: 🙎‍♂️پسر")
			user['gender'] = "m"
		else:
			await functions.update_user(msg.message.chat.id, {"gender": "f","profile": "default_girl.jpg"})
			await bot.answer_callback_query(msg.id, "جنسیت فعلی شما: 🙍‍♀️دختر")
			user['gender'] = "f"
		await bot.edit_message_caption(chat_id=msg.message.chat.id, message_id=msg.message.message_id, caption=f"• نام: {user['name']}\n• جنسیت: {functions.get_gender(user['gender'])} \n• استان: {user['city']}\n• سن: {user['age']}\n\n♥️ لایک ها : {len(user['likes'])}\n\n{functions.convertHoumanTime(user['online_at'],user['search']['connected'])}\n\n‏🆔 آیدی : /user_{user['id']}\n‏", reply_markup=functions.keyBoards.createEditProfileKeyboard(user), parse_mode=ParseMode.HTML)
		return

	if matches[0] == "edit_name":
		await functions.update_user(msg.message.chat.id, {"step": 3, "action": "set_name"})
		await msg.message.delete()
		await bot.send_message(msg.message.chat.id, "❓ لطفا نام خود را به صورت متن ارسال کنید.",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
		return

	if matches[0] == "edit_age":
		await functions.update_user(msg.message.chat.id, {"step": 3, "action": "set_age"})
		await msg.message.delete()
		await bot.send_message(msg.message.chat.id, "❓لطفا عدد سن خود را ارسال کنید \nمثلا : 20",parse_mode=ParseMode.MARKDOWN)
		return

	if matches[0] == "edit_gps":
		await functions.update_user(msg.message.chat.id, {"step": 3, "action": "set_gps"})
		await msg.message.delete()
		await bot.send_message(msg.message.chat.id, "\n\n✅ کسی قادر به دیدن موقعیت مکانی شما در ربات نخواهد بود و فقط برای تخمین فاصله و یافتن افراد نزدیک کاربرد خواهد داشت❓ لطفا با استفاده از دکمه زیر 👇 موقعیت خود را ارسال کنید.",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createGpsRequestsKeyboard())
		return

	if matches[0] == "edit_photo":
		await functions.update_user(msg.message.chat.id, {"step": 3, "action": "set_photo"})
		await msg.message.delete()
		await bot.send_message(msg.message.chat.id, "❓ لطفا عکس خود را ارسال کنید.",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
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
		"^/start$",
		"^(/user_)(.*)",
		"🔗 به یه ناشناس وصلم کن!",
		"👤پروفایل",
		"📍افراد نزدیک",
		"🔍 جستجوی کاربران 🔎",
		"💰سکه",
		"🚸 معرفی به دوستان \(سکه رایگان\)",
	],
	"patterns_callback": [
		"(show_gps):(.*):(\d+)",
		"edit_profile",
		"edit_gender",
		"edit_name",
		"edit_state",
		"edit_age",
		"edit_city",
		"edit_gps",
		"edit_photo",
	]
}