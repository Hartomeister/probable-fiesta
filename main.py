from aiogram import Bot, Dispatcher, types, executor
import logging
import os
import random
import json
from fuzzywuzzy import fuzz, process
from dbconfig import SQLConfig


datas = [['запорожье', 'ЗП'], ['запорожье', 'запор'], ['запорожье', 'Zaporizja'], ['Zaporizja', 'Zaporoje'], ['киев', 'Київ']]

# Подключение Базы
db = SQLConfig('database.db')

# Получение токена Бота
token = list(db.get_bot_token())[0][0]

# Логирование
logging.basicConfig(level=logging.ERROR)



# go_reg_findis = False  - Ищем девочек 
# go_reg_findis = True  - Ищем мальчиков 


# Инициализируем бота
bot = Bot('5139079205:AAEiHfbGHLi4jWj9Rv5KBFB4SyNLtnlKdCU')
dp = Dispatcher(bot)
print("Бот connected!")

global	i_see_this_person
i_see_this_person = {}
temp = []
i_see_this_persons = {}



class cMarkup:
	def mm(self):
		global markup_mm

		markup_mm = types.ReplyKeyboardMarkup(resize_keyboard=True)
		search = types.KeyboardButton("🚀")
		my_anketa = types.KeyboardButton("📖")
		markup_mm.add(search, my_anketa)

	def anketa(self):
		global markup_anketa

		markup_anketa = types.ReplyKeyboardMarkup(resize_keyboard=True)
		new_ank = types.KeyboardButton("🔄")
		change_img = types.KeyboardButton("🖼")
		change_desk = types.KeyboardButton("🔳")
		change_insta = types.KeyboardButton("🌐")
		home = types.KeyboardButton("⬅️")
		wath_anketas = types.KeyboardButton("🚀")
		markup_anketa.add(new_ank, change_img, change_desk, change_insta, home, wath_anketas)

	def use_anketa(self):
		global markup_anketa_use

		markup_anketa_use = types.ReplyKeyboardMarkup(resize_keyboard=True)
		like = types.KeyboardButton("❤")
		markup_anketa_use.add(like)




marukps = cMarkup()




async def show_ankets(message):
	try:
		global liked_user_id, i_see_this_person
		

		result = list(db.get_sort_users(message.from_user.id, db.get_u_age(message.from_user.id), i_find="girl"))
		choice = random.choice(result)
		city = db.get_u_city(message.from_user.id)
		
		data = i_see_this_person

		if liked_user_id[message.from_user.id] != 0:
			for x in range(len(data[message.from_user.id])):
				#print("data[message.from_user.id][x] = {0}" .format(data[message.from_user.id][x]))
				if choice[1] == data[message.from_user.id][x]:
					print("Skip: {0}" .format(choice[1]))
					return await show_ankets(message)

		succ_chance = fuzz.token_set_ratio(choice[6], city)
		#print("{0} {1} || {2} = {3} / {4} %" .format(choice[4], choice[3], city, choice[6], succ_chance))
		if succ_chance > 75:
			try:
				image = open("./files/images/user_pic/"+str(choice[1])+".jpg", 'rb')

			except FileNotFoundError:
				image = open("./files/images/user_pic/"+str(choice[1])+".png", 'rb')

			liked_user_id[message.from_user.id] = choice[1]
			marukps.use_anketa()
			return await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
				choice[4], choice[3], choice[6], choice[5]), reply_markup=markup_anketa_use)

		elif fuzz.WRatio(choice[6], city) > 80:
			try:
				image = open("./files/images/user_pic/"+str(choice[1])+".jpg", 'rb')

			except FileNotFoundError:
				image = open("./files/images/user_pic/"+str(choice[1])+".png", 'rb')

			return await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
				choice[4], choice[3], choice[6], choice[5]))

		elif succ_chance > 50 and succ_chance < 75:
			for data in datas:
				if fuzz.token_set_ratio(data[1], choice[6]) > 80:
					print("(token_set_ratio) ?? > {0} = {1} | {2} %" .format(data[1], choice[6], fuzz.token_set_ratio(data[1], city)))
					try:
						image = open("./files/images/user_pic/"+str(choice[1])+".jpg", 'rb')

					except FileNotFoundError:
						image = open("./files/images/user_pic/"+str(choice[1])+".png", 'rb')

					return await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
						choice[4], choice[3], choice[6], choice[5]))

				if fuzz.WRatio(data[1], choice[6]) > 80:
					print("(WRatio) ?? > {0} = {1} | {2} %" .format(data[1], choice[6], fuzz.token_set_ratio(data[1], city)))
					try:
						image = open("./files/images/user_pic/"+str(choice[1])+".jpg", 'rb')

					except FileNotFoundError:
						image = open("./files/images/user_pic/"+str(choice[1])+".png", 'rb')

					return await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
						choice[4], choice[3], choice[6], choice[5]))
		
		else:
			await show_ankets(message)


	except Exception as e:
		reset_data(message.from_user.id)
		await show_ankets(message)
		#bot.send_message(message.chat.id, "Прости, но подходящих анкет нет...")

async def send_anketa(message):
	u_id = message.from_user.id
	insta = db.get_u_insta(u_id)
	result = list(db.get_user_data(u_id))
	age = result[0][3]
	name = result[0][4]
	desk = result[0][5]
	city = result[0][6]

	image = open("./files/images/user_pic/"+str(u_id)+".jpg", 'rb')
	marukps.anketa()

	if insta != 'none':
		await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}\n\nInsta: www.instagram.com/{4}/" .format(\
			name, age, city, desk, insta))

	else:
		await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
			name, age, city, desk))



def save_l_data():
	src = "./files/backups/"
	with open(src + 'go_reg_age_tf.txt', 'w') as outfile:
		json.dump(go_reg_age_tf, outfile)
	with open(src + 'go_reg_name_tf.txt', 'w') as outfile:
		json.dump(go_reg_name_tf, outfile)
	with open(src + 'go_reg_sex_tf.txt', 'w') as outfile:
		json.dump(go_reg_sex_tf, outfile)
	with open(src + 'go_reg_city_tf.txt', 'w') as outfile:
		json.dump(go_reg_city_tf, outfile)
	with open(src + 'go_reg_findis_tf.txt', 'w') as outfile:
		json.dump(go_reg_findis_tf, outfile)
	with open(src + 'go_reg_desk_tf.txt', 'w') as outfile:
		json.dump(go_reg_desk_tf, outfile)
	with open(src + 'go_reg_img_tf.txt', 'w') as outfile:
		json.dump(go_reg_img_tf, outfile)
	with open(src + 'go_reg_age.txt', 'w') as outfile:
		json.dump(go_reg_age, outfile)
	with open(src + 'go_reg_name.txt', 'w') as outfile:
		json.dump(go_reg_name, outfile)
	with open(src + 'go_reg_sex.txt', 'w') as outfile:
		json.dump(go_reg_sex, outfile)
	with open(src + 'go_reg_city.txt', 'w') as outfile:
		json.dump(go_reg_city, outfile)
	with open(src + 'go_reg_desk.txt', 'w') as outfile:
		json.dump(go_reg_desk, outfile)
	with open(src + 'go_reg_img.txt', 'w') as outfile:
		json.dump(go_reg_img, outfile)
	with open(src + 'go_reg_findis.txt', 'w') as outfile:
		json.dump(go_reg_findis, outfile)
	with open(src + 'go_reg_imgpath.txt', 'w') as outfile:
		json.dump(go_reg_imgpath, outfile)
	with open(src + 'liked_user_id.txt', 'w') as outfile:
		json.dump(liked_user_id, outfile)
	with open(src + 'update_user_pic.txt', 'w') as outfile:
		json.dump(update_user_pic, outfile)
	with open(src + 'update_user_desk.txt', 'w') as outfile:
		json.dump(update_user_desk, outfile)

	print("[*] Local data was saved!")

def reset_data(uid):
	go_reg_age_tf[uid] = False
	go_reg_name_tf[uid] = False
	go_reg_sex_tf[uid] = False
	go_reg_city_tf[uid] = False
	go_reg_findis_tf[uid] = False
	go_reg_desk_tf[uid] = False
	go_reg_img_tf[uid] = False
	change_insta_tf[uid] = False
	#
	go_reg_age[uid] = False
	go_reg_name[uid] = False
	go_reg_sex[uid] = False
	go_reg_city[uid] = False
	go_reg_desk[uid] = False
	go_reg_img[uid] = False
	go_reg_findis[uid] = False
	go_reg_imgpath[uid] = False
	liked_user_id[uid] = False

	update_user_pic[uid] = False
	update_user_desk[uid] = False


def load_l_data():
	src = "./files/backups/"
	global go_reg_age_tf, go_reg_name_tf, go_reg_sex_tf, go_reg_city_tf, go_reg_findis_tf, go_reg_desk_tf, go_reg_img_tf, change_insta_tf, \
	go_reg_age, go_reg_name, go_reg_sex, go_reg_city, go_reg_desk, go_reg_img, go_reg_findis, go_reg_imgpath, liked_user_id, update_user_pic, \
	update_user_desk
	
	go_reg_age_tf = {}
	go_reg_name_tf = {}
	go_reg_sex_tf = {}
	go_reg_city_tf = {}
	go_reg_findis_tf = {}
	go_reg_desk_tf = {}
	go_reg_img_tf = {}
	change_insta_tf = {}

	#
	go_reg_age = {}
	go_reg_name = {}
	go_reg_sex = {}
	go_reg_city = {}
	go_reg_desk = {}
	go_reg_img = {}
	go_reg_findis = {}
	go_reg_imgpath = {}
	liked_user_id = {}

	update_user_pic = {}
	update_user_desk = {}

	i_see_this_person = {}

	with open(src + 'go_reg_age_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_age_tf = data
	with open(src + 'go_reg_name_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_name_tf = data
	with open(src + 'go_reg_sex_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_sex_tf = data
	with open(src + 'go_reg_city_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_city_tf = data
	with open(src + 'go_reg_findis_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_findis_tf = data
	with open(src + 'go_reg_desk_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_desk_tf = data
	with open(src + 'go_reg_img_tf.txt') as json_file:
		data = json.load(json_file)
		go_reg_img_tf = data
	with open(src + 'go_reg_age.txt') as json_file:
		data = json.load(json_file)
		go_reg_age = data
	with open(src + 'go_reg_name.txt') as json_file:
		data = json.load(json_file)
		go_reg_name = data
	with open(src + 'go_reg_sex.txt') as json_file:
		data = json.load(json_file)
		go_reg_sex = data
	with open(src + 'go_reg_city.txt') as json_file:
		data = json.load(json_file)
		go_reg_city = data
	with open(src + 'go_reg_desk.txt') as json_file:
		data = json.load(json_file)
		go_reg_desk = data
	with open(src + 'go_reg_img.txt') as json_file:
		data = json.load(json_file)
		go_reg_img = data
	with open(src + 'go_reg_findis.txt') as json_file:
		data = json.load(json_file)
		go_reg_findis = data
	with open(src + 'go_reg_imgpath.txt') as json_file:
		data = json.load(json_file)
		go_reg_imgpath = data
	with open(src + 'update_user_pic.txt') as json_file:
		data = json.load(json_file)
		update_user_pic = data
	with open(src + 'liked_user_id.txt') as json_file:
		data = json.load(json_file)
		liked_user_id = data
	with open(src + 'update_user_desk.txt') as json_file:
		data = json.load(json_file)
		update_user_desk = data


	print("[*] Local data has loaded!")

load_l_data()

# Bot Code
@dp.message_handler(commands=['bex'])
async def save_vaiables(message: types.Message):
	save_l_data()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	if(not db.users_exists(message.from_user.id)):
		go_reg = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("📎 Регистрация 📎")
		go_reg.add(item1)

		await message.reply("Привет, {0}!\nПохоже, ты впервые тут. Давай пройдём небольшую регистрацию.\n\nНажми на кнопку чтобы продолжить." .format(message.from_user.first_name), reply_markup=go_reg)
		#db.add_user(message.from_user.id, u_lang, "yes", message.chat.id, message.from_user.first_name)
	else:
		reset_data(message.from_user.id)
		main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
		search = types.KeyboardButton("🚀")
		my_anketa = types.KeyboardButton("📖")
		main_menu.add(search, my_anketa)

		return await message.answer("Главное меню:\n🚀 - Просмотр анкет\n📖 - Посмотреть/изменить свою анкету", reply_markup=main_menu)

@dp.message_handler()
async def messages_handler(message: types.Message):
	global go_reg_age_tf, go_reg_name_tf, go_reg_city_tf, go_reg_desk_tf, go_reg_img_tf, go_reg_findis_tf, go_reg_sex_tf, \
	go_reg_age, go_reg_name, go_reg_city, go_reg_desk, go_reg_findis, go_reg_sex, go_reg_imgpath, \
	change_insta_tf, update_user_pic, update_user_desk


	user_id = message.from_user.id

	if message.text == "📎 Регистрация 📎":
		go_reg_sex_tf[message.from_user.id] = True

		reg_sex = types.ReplyKeyboardMarkup(resize_keyboard=True)
		male = types.KeyboardButton("Я парень")
		female = types.KeyboardButton("Я девушка")
		reg_sex.add(male, female)

		return await message.answer("Вы парень или девушка?", reply_markup=reg_sex)



	if message.text == "Я парень":
		go_reg_sex_tf[message.from_user.id] = False
		go_reg_sex[message.from_user.id] = "male"
		reg_find_is = types.ReplyKeyboardMarkup(resize_keyboard=True)
		male = types.KeyboardButton("Парня")
		female = types.KeyboardButton("Девушку")
		reg_find_is.add(male, female)
		return await message.answer("Кого мы ищем?", reply_markup=reg_find_is)

	if message.text == "Я девушка":
		go_reg_sex_tf[message.from_user.id] = False
		go_reg_sex[message.from_user.id] = "female"
		reg_find_is = types.ReplyKeyboardMarkup(resize_keyboard=True)
		male = types.KeyboardButton("Парня")
		female = types.KeyboardButton("Девушку")
		reg_find_is.add(male, female)
		return await message.answer("Кого мы ищем?", reply_markup=reg_find_is)


	if message.text == "Парня":
		go_reg_age_tf[message.from_user.id] = True
		go_reg_findis[message.from_user.id] = True
		return await message.answer("Отправь мне свой возраст", reply_markup=types.ReplyKeyboardRemove())

	if message.text == "Девушку":
		go_reg_age_tf[message.from_user.id] = True
		go_reg_findis[message.from_user.id] = False
		return await message.answer("Отправь мне свой возраст", reply_markup=types.ReplyKeyboardRemove())

	if message.text == "📍 Пусто 📍":
		go_reg_desk[message.from_user.id] = ""
		go_reg_desk_tf[message.from_user.id] = False
		go_reg_img_tf[message.from_user.id] = True

		return await message.reply("Теперь отправь мне фотку для твоей анкеты.", reply_markup=types.ReplyKeyboardRemove())
	

	if message.text == "👌 Верно":
		go_reg_age_tf[message.from_user.id] = False
		go_reg_name_tf[message.from_user.id] = False
		go_reg_sex_tf[message.from_user.id] = False
		go_reg_city_tf[message.from_user.id] = False
		go_reg_findis_tf[message.from_user.id] = False
		go_reg_desk_tf[message.from_user.id] = False
		go_reg_img_tf[message.from_user.id] = False

		db.add_user(message.from_user.id, message.chat.id, go_reg_age[message.from_user.id], go_reg_name[message.from_user.id], go_reg_desk[message.from_user.id], go_reg_city[message.from_user.id], go_reg_findis[message.from_user.id], sex=go_reg_sex[message.from_user.id])

		
		marukps.mm()
		await message.answer("Регистрация завершена.")
		return await message.answer("Главное меню:\n🚀 - Просмотр анкет\n📖 - Посмотреть/изменить свою анкету", reply_markup=markup_mm)

	if message.text == "😔 Начать с начала":
		go_reg_age_tf = True
		return await message.answer("Отправь мне свой возраст", reply_markup=types.ReplyKeyboardRemove())


	if message.text == "🚀":
		await show_ankets(message)

	if message.text == "⬅️":
		main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
		search = types.KeyboardButton("🚀")
		my_anketa = types.KeyboardButton("📖")
		main_menu.add(search, my_anketa)

		return await message.answer("Главное меню:\n🚀 - Просмотр анкет\n📖 - Посмотреть/изменить свою анкету", reply_markup=main_menu)

	if message.text == "❤":
		global liked_user_id, i_see_this_person
		if liked_user_id[message.from_user.id] != 0:

			db.add_like(liked_user_id[message.from_user.id], message.from_user.id)
			likes = list(db.get_user_likes(user_id=liked_user_id[message.from_user.id]))
			if len(likes) == 1:
				await bot.send_message(db.get_u_chatid(liked_user_id[message.from_user.id]), "Вы понравились {0} пользователю" .format(len(likes)))
			elif len(likes) > 1:
				await bot.send_message(db.get_u_chatid(liked_user_id[message.from_user.id]), "Вы понравились {0} пользователям" .format(len(likes)))
			

			temp.append(int(liked_user_id[message.from_user.id]))
			i_see_this_persons[message.from_user.id] = {}
			i_see_this_person = {fruit : temp for fruit in i_see_this_persons}
			return await show_ankets(message)

	if message.text == "🌐":
		if(db.get_u_insta(user_id) == 'none'):
			change_insta_tf[user_id] = True
			return await message.reply("Отправьте мне ссылку или Ваш ник в Instagram.", reply_markup=types.ReplyKeyboardRemove())
		else:
			db.update_u_insta(user_id)
			await message.reply("Instagram был отвязан от вашей анкеты.")
			await send_anketa(message)
			marukps.anketa()
			return await message.answer("🔄 - Заполнить анкету заново\n🖼 - Изменнить фото анкеты\n🔳 - Изменить описание\n🌐 - Привязка Instagram\n⬅️ - Главное меню\n🚀 - Просмотр анкет", reply_markup=markup_anketa)
		
	if message.text == "🔳":
		update_user_desk[user_id] = True
		return await message.answer("Отправьте мне новое описание для вашей анкеты.", reply_markup=types.ReplyKeyboardRemove())

	if message.text == "🖼":
		update_user_pic[user_id] = True
		return await message.answer("Отправьте мне новое фото.", reply_markup=types.ReplyKeyboardRemove())

	if message.text == "🔄":
		go_reg_sex_tf[message.from_user.id] = True

		reg_sex = types.ReplyKeyboardMarkup(resize_keyboard=True)
		male = types.KeyboardButton("👨 Мужчина")
		female = types.KeyboardButton("👩 Женщина")
		reg_sex.add(male, female)

		return await message.answer("Вы: Мальчик / Девочка ?", reply_markup=reg_sex)

	if message.text == "📖": 
		await send_anketa(message)
		marukps.anketa()
		return await message.answer("🔄 - Заполнить анкету заново\n🖼 - Изменнить фото анкеты\n🔳 - Изменить описание\n🌐 - Привязка Instagram\n⬅️ - Главное меню\n🚀 - Просмотр анкет", reply_markup=markup_anketa)
		"""
		result = list(db.get_user_data(message.from_user.id))
		age = result[0][3]
		name = result[0][4]
		desk = result[0][5]
		city = result[0][6]
		u_id = result[0][1]

		image = open("./files/images/user_pic/"+str(u_id)+".jpg", 'rb')
		

		await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
			name, age, city, desk))
		"""
		
		
	try:
		if go_reg_age_tf[message.from_user.id] == True:
			go_reg_age[message.from_user.id] = int(message.text)
			if go_reg_age[message.from_user.id] < 13: 
				go_reg_age_tf[message.from_user.id] = True
				return await message.reply("Прости, но тебе должно быть больше 13-ти лет..")

			elif go_reg_age[message.from_user.id] > 100:
				go_reg_age_tf[message.from_user.id] = True
				return await message.reply("Прости, но тебе должно быть меньше 100-а лет..")

			go_reg_age_tf[message.from_user.id] = False
			go_reg_name_tf[message.from_user.id] = True

			#print("[id: {0}] age: {1}" .format(message.from_user.id, go_reg_age))			# small debugging
			return await message.reply("Отлично. Теперь, как тебя называть?")

		if go_reg_name_tf[message.from_user.id] == True:
			go_reg_name[message.from_user.id] = message.text
			go_reg_name_tf[message.from_user.id] = False
			go_reg_city_tf[message.from_user.id] = True

			#print("[id: {0}] name: {1}" .format(message.from_user.id, go_reg_name))			# small debugging

			return await message.reply("Отлично. Теперь, в каком городе ты живёшь?")

		if go_reg_city_tf[message.from_user.id] == True:
			go_reg_city[message.from_user.id] = message.text
			go_reg_city_tf[message.from_user.id] = False
			go_reg_desk_tf[message.from_user.id] = True

			#print("[id: {0}] city: {1}" .format(message.from_user.id, go_reg_city))			# small debugging
			reg_desk = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton("📍 Пусто 📍")
			reg_desk.add(item1)

			return await message.reply("Отлично. Теперь, опиши кого ты ищешь,\nсебя, свои качества. \n\nИли, оставь пустым", reply_markup=reg_desk)

		if go_reg_desk_tf[message.from_user.id] == True:
			go_reg_desk[message.from_user.id] = message.text
			go_reg_desk_tf[message.from_user.id] = False
			go_reg_img_tf[message.from_user.id] = True

			#print("[id: {0}] desk: {1}" .format(message.from_user.id, go_reg_desk))			# small debugging
			return await message.reply("Отлично. Теперь, отправь мне фото для твоей анкеты.", reply_markup=types.ReplyKeyboardRemove())

		if change_insta_tf[user_id] == True:
			insta = message.text
			index = insta.find('.com/')  
			if index != -1:
				insta = insta[(index+5):(len(insta)-1)]
			else:
				insta = insta

			db.update_u_insta(user_id, insta)
			change_insta_tf[user_id] = False
			await send_anketa(message)
			marukps.anketa()
			return await message.answer("🔄 - Заполнить анкету заново\n🖼 - Изменнить фото анкеты\n🔳 - Изменить описание\n🌐 - Привязка Instagram\n⬅️ - Главное меню\n🚀 - Просмотр анкет", reply_markup=markup_anketa)
		
		if update_user_desk[user_id] == True:
			db.update_u_desk(user_id, message.text)
			await send_anketa(message)
			marukps.anketa()
			return await message.answer("🔄 - Заполнить анкету заново\n🖼 - Изменнить фото анкеты\n🔳 - Изменить описание\n🌐 - Привязка Instagram\n⬅️ - Главное меню\n🚀 - Просмотр анкет", reply_markup=markup_anketa)
	except KeyError:
		go_reg_age_tf[user_id] = False
		go_reg_name_tf[user_id] = False
		go_reg_sex_tf[user_id] = False
		go_reg_city_tf[user_id] = False
		go_reg_findis_tf[user_id] = False
		go_reg_desk_tf[user_id] = False
		go_reg_img_tf[user_id] = False
		change_insta_tf[user_id] = False
		update_user_desk[user_id] = False

	

@dp.message_handler(content_types=['photo'])
async def handle_sended_files_ph(message):
	global go_reg_img_tf, go_reg_age, go_reg_name, go_reg_city, go_reg_desk, go_reg_imgpath, update_user_pic
	
	try:
		if go_reg_img_tf[message.from_user.id] == True:
			file_info = await bot.get_file(message.photo[-1].file_id)
			src = './files/images/user_pic/'+ str(message.from_user.id) + ".jpg";
			
			await message.photo[-1].download(destination_file =src) 
			go_reg_desk_tf[message.from_user.id] = False
			go_reg_imgpath[message.from_user.id] = file_info.file_path

			await message.answer("Супер.. Так выглдяит твоя анкета. Всё верно?")
			image = open(src, 'rb')

			all_true = types.ReplyKeyboardMarkup(resize_keyboard=True)
			okk = types.KeyboardButton("👌 Верно")
			no_ok = types.KeyboardButton("😔 Начать с начала")
			all_true.add(okk, no_ok)

			return await message.reply_photo(image, "{0}, {1} лет - {2}\n{3}" .format(\
				go_reg_name[message.from_user.id], go_reg_age[message.from_user.id], go_reg_city[message.from_user.id], go_reg_desk[message.from_user.id]), reply_markup=all_true)
		
		if update_user_pic[message.from_user.id] == True:
			file_info = await bot.get_file(message.photo[-1].file_id)
			src = './files/images/user_pic/'+ str(message.from_user.id) + ".jpg";
			
			await message.photo[-1].download(destination_file =src) 
			go_reg_imgpath[message.from_user.id] = file_info.file_path

			await message.answer("Отлично, я обновил фото твоей анкеты.")
			image = open(src, 'rb')
			update_user_pic[message.from_user.id] = False
			await send_anketa(message)
			marukps.anketa()
			return await message.answer("🔄 - Заполнить анкету заново\n🖼 - Изменнить фото анкеты\n🔳 - Изменить описание\n🌐 - Привязка Instagram\n⬅️ - Главное меню\n🚀 - Просмотр анкет", reply_markup=markup_anketa)

	except KeyError:
		go_reg_img_tf[message.from_user.id] = False
		update_user_pic[message.from_user.id] = False

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
	
