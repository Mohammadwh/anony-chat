from aiogram.types import ParseMode, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup
from json import loads
from time import time
class KeyBoards:
	"""
		create object from all keyboards

		"one time create and use any time :)))"

	"""

	def selectGenderMarkup(self):
		markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("من🙎‍♂️پسرم", "من🙍‍♀️دخترم")
		return markup

	def createAgeMarkup(self):
		markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=7)
		for i in range(9,100):
			markup.insert(KeyboardButton(i))
		return markup


	def createCityMarkup(self):
		cities = [i['name'] for i in loads(open("cities.json", 'r').read())]
		markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
		for i in cities:
			markup.insert(KeyboardButton(i))
		return markup

	def createStartMarkup(self):
		markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
		markup.add("🔗 به یه ناشناس وصلم کن!")
		markup.add("🔍 جستجوی کاربران 🔎","📍افراد نزدیک")
		markup.add("💰سکه","👤پروفایل","🤔راهنما")
		markup.add("🚸 معرفی به دوستان (سکه رایگان)")
		return markup

	def createChatMarkup(self,user):
		markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
		markup.add("👀مشاهده پروفایل این مخاطب👤")
		markup.add("غیر فعال سازی چت خصوصی 🔐" if user['search']['secret_chat'] else "فعال سازی چت خصوصی 🔒")
		markup.add("پایان چت")
		return markup

	def createCancelChatMarkup(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("لغو ❌", callback_data='cancel'))
		return markup

	def createFilerAgeMarkup(self,user):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("⚙️ جستجوی همسن : فعال ✅", callback_data='filterAge:off') if user["search"]["filter_age_range"] else InlineKeyboardButton("⚙️ جستجوی همسن : غیرفعال ❌", callback_data='filterAge:on'))
		markup.add(InlineKeyboardButton("لغو ❌", callback_data='cancel'))
		return markup

	def createCandelUpdatePhoto(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("بیخیال ✏️ تغییر عکس", callback_data='cancel_photo'))
		return markup

	def createGpsRequestsKeyboard(self):
		markup = ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add(KeyboardButton("📍 ارسال موقعیت GPS", request_location=True))
		markup.add(KeyboardButton("🔙 بازگشت", request_location=True))
		return markup

	def createCandelAge(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("بیخیال ✏️ تغییر سن", callback_data='cancel_age'))
		return markup

	def createRandomKeyboard(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("🎲جستجوی شانسی🎲", callback_data='random'))
		markup.add(InlineKeyboardButton("🙎‍♂️جستجوی پسر", callback_data='search_boy'),InlineKeyboardButton("🙍‍♀️جستجوی دختر", callback_data='search_girl'))
		markup.add(InlineKeyboardButton("🛰جستجوی اطراف", callback_data='search_gps'))
		return markup

	def createProfileKeyboard(self,user,me=None,is_self=True):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		if is_self:
			if user['location'] != [0,0]:
				markup.add(InlineKeyboardButton("📍مشاهده موقعیت GPS ثبت شده من", callback_data='show_my_location'))
			markup.add(InlineKeyboardButton("🙍‍♀️🙎‍♂️مخاطبین", callback_data='my_contacts'),InlineKeyboardButton("❤️ لایک های من", callback_data='my_likes'))
			markup.add(InlineKeyboardButton("🚫 بلاک شده ها", callback_data='show_blocks'),InlineKeyboardButton("🔕 سایلنت", callback_data='search_gps') if user['silent']['status'] == False else InlineKeyboardButton("🔔 سایلنت", callback_data='search_gps'))
			markup.add(InlineKeyboardButton("📝 ویرایش اطلاعات", callback_data='edit_profile'))
			return markup
		markup.add(InlineKeyboardButton(f"Like ❤️ {len(user['likes'])}", callback_data='random'))
		markup.add(InlineKeyboardButton("📨 پیام دایرکت", callback_data='random'),InlineKeyboardButton("💬 درخواست چت", callback_data='random'))
		markup.add(InlineKeyboardButton("🔒 بلاک کردن کاربر", callback_data='random') if not user['id'] in me['blocked'] else InlineKeyboardButton("🔐 آنبلاک کردن کاربر", callback_data='random'),InlineKeyboardButton("➕ افزودن به مخاطبین", callback_data='random'))
		markup.add(InlineKeyboardButton("🚫 گزارش کاربر", callback_data='random'))
		if user['search']['connected']:
			if user['online_at'] < int(time())-900:
				markup.add(InlineKeyboardButton("🔔 به محض آنلاین شدن اطلاع بده", callback_data='random'))
			else:
				markup.add(InlineKeyboardButton("🔔 به محض اتمام چت اطلاع بده", callback_data='random'))
		return markup

	def createEditProfileKeyboard(self,user):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("✏️ تغییر جنسیت", callback_data='edit_gender'),InlineKeyboardButton("✏️ تغییر نام", callback_data='edit_name'))
		markup.add(InlineKeyboardButton("✏️ تغییر شهر", callback_data='edit_city'),InlineKeyboardButton("✏️ تغییر سن", callback_data='edit_age'))
		markup.add(InlineKeyboardButton("✏️ تغییر استان", callback_data='edit_state'),InlineKeyboardButton("✏️ تغییر عکس", callback_data='edit_photo'))
		if user['location'] != [0, 0]:
			markup.add(InlineKeyboardButton("✏️ تغییر موقعیت GPS", callback_data='edit_gps'))
		else:
			markup.add(InlineKeyboardButton("✏️ ثبت موقعیت GPS", callback_data='edit_gps'))
		return markup

	def createGPSSearchKeyboard(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("فقط 🙍‍♀️ دختر ها", callback_data='show_gps:f:1'),InlineKeyboardButton("فقط پسر🙎‍♂️ پسر ها", callback_data='show_gps:m:1'))
		markup.add(InlineKeyboardButton("همه رو نشون بده", callback_data='show_gps:all:1'))
		return markup

	def createUserSearchKeyboard(self):
		markup = InlineKeyboardMarkup(resize_keyboard=True)
		markup.add(InlineKeyboardButton("👥هم سنی ها", callback_data='random'),InlineKeyboardButton("🎌 هم استانی ها", callback_data='random'))
		markup.add(InlineKeyboardButton("🔍جستجوی پیشرفته🔎", callback_data='random'))
		markup.add(InlineKeyboardButton("🚶‍♂️ بدون چت ها🚶‍♂️", callback_data='random'),InlineKeyboardButton("🙋‍♂️کاربران جدید 🙋‍♀️", callback_data='random'))
		return markup

