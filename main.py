import telebot
import sqlite3
import random
import time
#-----------------------------------------------
# Version 0.2.1
# * Добавь до 100 книг
# * 23/100

bot = telebot.TeleBot('1700158651:AAHDN9aNBOztTUnrpJQEgAQmOeofOt6UIoo')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Начнём подборку книг?', 'Рандомную книгу')
conn = sqlite3.connect('BOOK.db', check_same_thread=False)
cursor = conn.cursor()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Пропустить этот шаг')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('Большие', 'Средние','Маленькие','Пропустить этот шаг')
keyboard4 = telebot.types.ReplyKeyboardMarkup()
keyboard4.row('Роман', 'Фантастика','Триллер','Пропустить этот шаг')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я помогу тебе найти книгу для чтения :D \n---------------------------------------\nVersion 0.2.1\n* Добавлен вывод автора при рандоме и подборки книг\n* Добавлено пару десятков книг\n* Бот вышел из бета версии', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def send_profil(message):
    me = '@Troll_w'
    bot.send_message(message.chat.id, f'Привет, по поводу добавления новой книги обратись к {me}')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Начнём подборку книг?': #Ответ на кнопку 1
        bot.send_message(message.chat.id, 'Напиши имя автора чьё произведение хочешь почитать', reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_autor)
    elif message.text == 'Рандомную книгу': #Ответ на кнопку 1
         for result in (cursor.execute("SELECT Произведение FROM BOOK ORDER BY RANDOM() LIMIT 1;")):
             cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{result[0]}';")
             Art = cursor.fetchone()
             bot.send_message(message.chat.id, 'Советую прочитать тебе ' + result[0] + "\nАвтор - " + Art[0])


@bot.message_handler(content_types=['text'])
def get_autor(message): #Принимаю от пользователя Автора и проверяю не выбрал ли он пропустить этот шаг
    global Author
    if message.text == 'Пропустить этот шаг':
        bot.send_message(message.from_user.id, 'Какой жанр нравится?')
        Author = 'Пропуск'
        bot.register_next_step_handler(message, get_zanr)
    else:
        Author = message.text
        bot.send_message(message.from_user.id, 'Какой жанр нравится?')
        bot.register_next_step_handler(message, get_zanr)


@bot.message_handler(content_types=['text'])
def get_zanr(message): # Индентично что и с Автором
        global Zanr
        if message.text == 'Пропустить этот шаг':
            bot.send_message(message.from_user.id, 'Тебе нравятся большие, средние или маленькие книги?', reply_markup=keyboard3)
            Zanr = 'Пропуск'
            bot.register_next_step_handler(message, get_razmer)
        else:
            Zanr = message.text
            bot.send_message(message.from_user.id, 'Тебе нравятся большие, средние или маленькие книги?', reply_markup=keyboard3)
            bot.register_next_step_handler(message, get_razmer)

@bot.message_handler(content_types=['text'])
def get_razmer(message): # Тоже самое
    global Razmer
    global Books
    if message.text == 'Пропустить этот шаг':
            bot.send_message(message.from_user.id, 'Окей, сейчас подберу для Вас книги :)', reply_markup=keyboard1)
            Razmer = 'Пропуск'
    else:
        Razmer = message.text
        bot.send_message(message.from_user.id, 'Окей, сейчас подберу для Вас книги :)', reply_markup=keyboard1)
    if Author == 'Пропуск' and Zanr == 'Пропуск' and Razmer == 'Пропуск':
        bot.send_message(message.from_user.id, 'Дружище, сам то знаешь что хочешь? ;)')
    elif Author == 'Пропуск' and Zanr == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Размер =='{Razmer}';") # Не забудь где!!!! (Внизу)
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        A = random.choice([Books, Books1])
        B = random.choice([Books, Books1, Books2])
        C = random.choice([Books, Books1, Books2, Books3])
        D = random.choice([Books, Books1, Books2, Books3, Books4])
        E = random.choice([Books, Books1, Books2, Books3, Books4, Books5])

        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{Books}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + Books[0] + '  \nАвтор - ' + Art[0])
        elif not Books2:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{A[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + A[0] + '  \nАвтор - ' + Art[0])
        elif not Books3:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + B[0] + '  \nАвтор - ' + Art[0])
        elif not Books4:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{C[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + C[0] + '  \nАвтор - ' + Art[0])
        elif not Books5:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{D[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + D[0] + '  \nАвтор - ' + Art[0])
        else:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{E[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + E[0] + '  \nАвтор - ' + Art[0])
    elif Author == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        A = random.choice([Books, Books1])
        B = random.choice([Books, Books1, Books2])
        C = random.choice([Books, Books1, Books2, Books3])
        D = random.choice([Books, Books1, Books2, Books3, Books4])
        E = random.choice([Books, Books1, Books2, Books3, Books4, Books5])

        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{Books}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + Books[0] + '  \nАвтор - ' + Art[0])
        elif not Books2:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{A[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + A[0] + '  \nАвтор - ' + Art[0])
        elif not Books3:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + B[0] + '  \nАвтор - ' + Art[0])
        elif not Books4:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{C[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + C[0] + '  \nАвтор - ' + Art[0])
        elif not Books5:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{D[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + D[0] + '  \nАвтор - ' + Art[0])
        else:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{E[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + E[0] + '  \nАвтор - ' + Art[0])
    elif Zanr == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            bot.send_message(message.from_user.id, Books)
        elif not Books2:
            bot.send_message(message.from_user.id, random.choice([Books, Books1]))
        elif not Books3:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2]))
        elif not Books4:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3]))
        elif not Books5:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4]))
        else:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4, Books5]))
    elif Author == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}' AND Размер =='{Razmer}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        A = random.choice([Books, Books1])
        B = random.choice([Books, Books1, Books2])
        C = random.choice([Books, Books1, Books2, Books3])
        D = random.choice([Books, Books1, Books2, Books3, Books4])
        E = random.choice([Books, Books1, Books2, Books3, Books4, Books5])

        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{Books}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + Books[0] + '  \nАвтор - ' + Art[0])
        elif not Books2:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{A[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + A[0] + '  \nАвтор - ' + Art[0])
        elif not Books3:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + B[0] + '  \nАвтор - ' + Art[0])
        elif not Books4:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{C[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + C[0] + '  \nАвтор - ' + Art[0])
        elif not Books5:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{D[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + D[0] + '  \nАвтор - ' + Art[0])
        else:
            cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{E[0]}';")
            Art = cursor.fetchone()
            bot.send_message(message.from_user.id,'Думаю тебе стоит почитать ' + E[0] + '  \nАвтор - ' + Art[0])
    elif Zanr == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Размер =='{Razmer}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            bot.send_message(message.from_user.id, Books)
        elif not Books2:
            bot.send_message(message.from_user.id, random.choice([Books, Books1]))
        elif not Books3:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2]))
        elif not Books4:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3]))
        elif not Books5:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4]))
        else:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4, Books5]))
    elif Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            bot.send_message(message.from_user.id, Books)
        elif not Books2:
            bot.send_message(message.from_user.id, random.choice([Books, Books1]))
        elif not Books3:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2]))
        elif not Books4:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3]))
        elif not Books5:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4]))
        else:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4, Books5]))
    else:
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}' AND Размер =='{Razmer}';")
        Books = cursor.fetchone()
        Books1 = cursor.fetchone()
        Books2 = cursor.fetchone()
        Books3 = cursor.fetchone()
        Books4 = cursor.fetchone()
        Books5 = cursor.fetchone()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        elif not Books1:
            bot.send_message(message.from_user.id, Books)
        elif not Books2:
            bot.send_message(message.from_user.id, random.choice([Books, Books1]))
        elif not Books3:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2]))
        elif not Books4:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3]))
        elif not Books5:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4]))
        else:
            bot.send_message(message.from_user.id, random.choice([Books, Books1, Books2, Books3, Books4, Books5]))

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
