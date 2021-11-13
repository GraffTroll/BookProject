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
keyboard1.row('Начнём подборку книг?', 'Случайную книгу')
conn = sqlite3.connect('BOOK.db', check_same_thread=False)
cursor = conn.cursor()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Пропустить этот шаг')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('Большие', 'Средние', 'Маленькие', 'Пропустить этот шаг')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я помогу тебе найти книгу для чтения :D \n---------------------------------------\nVersion 1.1.5\n* Добавлен вывод автора при рандоме и подборки книг\n* Добавлено пару десятков книг\n* Авторов стоит указывать с именем и фамилией', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def send_profil(message):
    me = '@Troll_w'
    bot.send_message(message.chat.id, f'Привет, по поводу ошибки или добавления новой книги обратись к {me}')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Начнём подборку книг?':
        bot.send_message(message.chat.id, 'Напиши имя автора чьё произведение хочешь почитать', reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_autor)
    elif message.text == 'Случайную книгу':
        cursor.execute("SELECT Произведение FROM BOOK ORDER BY RANDOM() LIMIT 1;")
        Books = cursor.fetchone()
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{Books[0]}';")
        Art = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{Books[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.chat.id, 'Советую прочитать тебе \"' + Books[0] + "\"\nАвтор - " + Art[0] + '\n' + K[0])


@bot.message_handler(content_types=['text'])
def get_autor(message):
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
def get_razmer(message):
    global Razmer
    global Books
    if message.text == 'Пропустить этот шаг':
            bot.send_message(message.from_user.id, 'Окей, сейчас подберу для Вас книги :)', reply_markup=keyboard1)
            Razmer = 'Пропуск'
    else:
        Razmer = message.text
        bot.send_message(message.from_user.id, 'Окей, сейчас подберу для Вас книги :)', reply_markup=keyboard1)

    if Author == 'Пропуск' and Zanr == 'Пропуск' and Razmer == 'Пропуск':
        bot.send_message(message.from_user.id, 'Дружище, сам то знаешь что хочешь?\n---------------------------------------\nВоспользуйся кнопкой \"Случайную книгу\"')
######################################################################################################################
    elif Author == 'Пропуск' and Zanr == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

    elif Author == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

    elif Zanr == 'Пропуск' and Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

    elif Zanr == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

    elif Razmer == 'Пропуск':
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

    else:
        cursor.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}' AND Размер =='{Razmer}';")
        Books = cursor.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor.fetchone()
        cursor.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
