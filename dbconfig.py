import sqlite3

class SQLConfig:

    def __init__(self, database):
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            print("The bot is connected to к {0} | Successfully" .format(database))

        except Exception as e:
            prinr(e)


    def users_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))


    def get_bot_token(self):
        with self.connection:
            result = self.cursor.execute('SELECT `bot_TOKEN` FROM `bot_settings`').fetchall()
            return result

    def add_user(self, user_id, chat_id=0, age=17, name="love", desk=" ", city="Zaporizha", find=False, user_pic="", sex="male"):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `chat_id`, `user_age`, `user_name`, `user_desk`, `user_city`, `find_boys`, `user_pic_id`, `user_sex`) VALUES\
                (?, ?, ?, ?, ?, ?, ?, ?, ?)", (\
                user_id, chat_id, age, name, desk, city, bool(find), user_pic, sex))

    def get_user_likes(self, user_id):
        with self.connection: 
            result = self.cursor.execute('SELECT `liker_uid` FROM `likes` WHERE `liked_uid` = ?', (user_id,))
            return result



    def get_user_data(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,))
            return result

    def get_u_insta(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `user_insta` FROM `users` WHERE `user_id` = ?', (user_id,))
            return list(result)[0][0]

    def update_u_insta(self, user_id, insta='none'):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `user_insta` = ? WHERE `user_id` = ?", (insta, user_id))

    def update_u_desk(self, user_id, desk=''):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `user_desk` = ? WHERE `user_id` = ?", (desk, user_id))

    def get_u_city(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `user_city` FROM `users` WHERE `user_id` = ?', (user_id,))
            return list(result)[0][0]

    def get_u_age(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `user_age` FROM `users` WHERE `user_id` = ?', (user_id,))
            return list(result)[0][0]

    def get_u_desk(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `user_desk` FROM `users` WHERE `user_id` = ?', (user_id,))
            return list(result)[0][0]

    def get_u_ifind(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `find_boys` FROM `users` WHERE `user_id` = ?', (user_id,))
            if list(result)[0][0] == 0:
                return "girl"
            else:
                return "boy"


    def get_u_chatid(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `chat_id` FROM `users` WHERE `user_id` = ?', (user_id,))
            return list(result)[0][0]



    def add_like(self, liked_id, liker_id):
        with self.connection: 
            return self.cursor.execute("INSERT INTO `likes` (`liked_uid`, `liker_uid`) VALUES(?, ?)", (liked_id, liker_id))


    def get_sort_users(self, user_id, age="17", city="", i_find="girl"):
        with self.connection:
            if i_find == "girl":
                result = self.cursor.execute('SELECT * FROM `users` WHERE `user_age` >= ? and `user_age` <= ? and `user_id` != ? and `user_sex` = "female" and `find_boys` = "1"', (int(age)-1, int(age)+1, user_id) ) 
            else:
                result = self.cursor.execute('SELECT * FROM `users` WHERE `user_age` >= ? and `user_age` <= ? and `user_id` != ? and `user_sex` = "male" and `find_boys` = "0"', (int(age)-1, int(age)+1, user_id) ) 
            return result
"""
    def get_subscriptions(self, status=1):
        with self.connection:
            return self.cursor.execute("SELECT `chat_id` FROM `users` WHERE `subscribe` = ?", (status,)).fetchall()

   

    def add_users(self, user_id, lang, repmes="yes", chatid=0, firt_name='snaze -_-'):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `lang`, `rep_mes`, `chat_id`, `first_name`) VALUES(?, ?, ?, ?, ?)", (user_id, lang, repmes, chatid, firt_name))

    def get_first_name(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `first_name` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return result

    def get_version(self):
        with self.connection:
            result = self.cursor.execute('SELECT `version` FROM `SETTINGS`').fetchall()
            return result

    def updatelang(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `lang` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        self.connection.close()

    def get_chat_ids(self):
        with self.connection:
            result = self.cursor.execute('SELECT `chat_id` FROM `users`').fetchall()
            return result

    def get_bot_token(self):
        with self.connection:
            result = self.cursor.execute('SELECT `TOKEN` FROM `SETTINGS`').fetchall()
            return result

    def save_config(self, token):
        with self.connection:
            return self.cursor.execute("UPDATE `SETTINGS` SET `TOKEN` = ? WHERE `id` = `1`", (token))

    def getlang(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `lang` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            text = str(result)
            index = text.find("('")
            return (text[3:5])
            #return list(result)[0]

"""
