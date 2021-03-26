import telebot
import sqlite3
#-----------------------------------------------
# Version 0.0.9
# * Добавь до 100 книг
# * 14/100

bot = telebot.TeleBot('1731058683:AAHnZD2BSKEcK_zduD600eXCy77xNCyum_k')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Начнём подборку книг?', 'Рандомную книгу')
conn = sqlite3.connect('BOOK.db', check_same_thread=False)
cursor = conn.cursor()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Пропустить этот шаг')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('Большие', 'Средние','Маленькие','Пропустить этот шаг')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я помогу тебе найти книгу для чтения :D \n---------------------------------------\nVersion 0.0.9 BETA', reply_markup=keyboard1)

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
         for gg in (cursor.execute("SELECT Произведение FROM BOOK ORDER BY RANDOM() LIMIT 1;")):
             bot.send_message(message.chat.id, f'Советую прочитать тебе {gg}')


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
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    elif Author == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    elif Zanr == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}';")
        Books = cursor.fetchall()
        if not Books: #Если БД ничего не дала то выводит этот текст
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    elif Author == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}' AND Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    elif Zanr == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    elif Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        else:
            bot.send_message(message.from_user.id, Books)
    else:
         cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}' AND Размер =='{Razmer}';")
         Books = cursor.fetchall()
         if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
         else:
            bot.send_message(message.from_user.id, Books)


bot.polling(none_stop=True)
