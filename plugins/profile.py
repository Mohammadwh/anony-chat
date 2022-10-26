from aiogram.types import ParseMode
import re

async def run(msg,matches,functions,user,bot):

	if user['action'] == 'set_name':
		if not re.findall(r'[a-z][a-z][a-z]+', msg.text):
			await functions.update_user(msg.from_user.id, {"action": None, "step": 1,"name": msg.text})
			await msg.reply("✏️ تغییر نام با موفقیت انجام شد ✅",reply_markup=functions.keyBoards.createStartMarkup())
			return
		else:
			await msg.reply("🙄 من اینگلیسیم خوب نیست فارسی بفرست برام")
			return

	elif user['action'] == 'set_age':
		if msg.text.isdigit():
			if int(msg.text) >= 9 and int(msg.text) < 100:
				await functions.update_user(msg.from_user.id, {"action": None, "age": msg.text, "step": 1})
				await msg.reply("✏️ تغییر سن  با موفقیت انجام شد ✅\n\nخب ، حالا چه کاری برات انجام بدم؟",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
			else:
				await msg.reply("🙄لطفا سنتو از رنج مشخص شده 9 تا 99 سال بفرست.",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createCandelAge())
		else:
			await msg.reply("⚠️ خط : ورودی باید بصورت اعداد انگلیسی باشد.",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createCandelAge())
		return

	elif user['action'] == 'set_photo':
		if matches[0] == '[%photo%]':
			await functions.update_user(msg.from_user.id, {"action": None, "step": 1, "profile": msg.photo[len(msg.photo) - 1].file_id})
			await bot.download_file_by_id(file_id=msg.photo[len(msg.photo) - 1].file_id,destination=f"profiles/{msg.from_user.id}.jpg")
			await msg.reply("✏️ تغییر نام با موفقیت انجام شد ✅", reply_markup=functions.keyBoards.createStartMarkup())
		else:
			await msg.reply("⚠️ خطا: ورودی باید بصورت عکس باشد.", reply_markup=functions.keyBoards.createCandelUpdatePhoto())
		return
	elif user['action'] == 'set_gps':
		if matches[0] == '[%location%]':
			await functions.update_user(msg.from_user.id,{"action": None, "step": 1, "location": [msg.location.latitude,msg.location.longitude]})
			await msg.reply("✏️ موقیعت GPS شما ثبت گردید ✅", reply_markup=functions.keyBoards.createStartMarkup())
		elif msg.text == "🔙 بازگشت":
			await functions.update_user(msg.from_user.id, {"action": None, "step": 1})
			await msg.reply("خب ، حالا چه کاری برات انجام بدم؟",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
		return

async def run_callback(msg,matches,functions,user,bot):

	if matches[0] == "cancel_photo":
		await functions.update_user(msg.from_user.id, {"action": None, "step": 1})
		await bot.send_message(msg.message.chat.id, "خب ، حالا چه کاری برات انجام بدم؟\n`از منوی پایین👇 انتخاب کن`",parse_mode=ParseMode.MARKDOWN, reply_markup=functions.keyBoards.createStartMarkup())
		return



plugin = {
	"name": "pv",
	"desc": "manage pv bot",
	"run": run,
	"run_callback": None,
	"chat_type": "private",
	"step": 3,
	"on_chat":False,
	"patterns_message": [
		"(.*)",
		"[%photo%]",
		"[%location%]",
	],
	"patterns_callback": []
}