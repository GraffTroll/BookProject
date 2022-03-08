import telebot
import sqlite3
import random
import time
#-----------------------------------------------
# Version 0.2.1
# * Добавь до 100 книг
# * 55/100

bot = telebot.TeleBot('1700158651:AAHDN9aNBOztTUnrpJQEgAQmOeofOt6UIoo')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Начнём подборку книг?', 'Случайную книгу', 'Вернуться назад')
conn_B = sqlite3.connect('BOOK.db', check_same_thread=False)
cursor_B = conn_B.cursor()
conn_S = sqlite3.connect('SCHOOL.db', check_same_thread=False)
cursor_S = conn_S.cursor()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Пропустить этот шаг')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('Большие', 'Средние', 'Маленькие', 'Пропустить\nэтот\nшаг')
keyboard_start = telebot.types.ReplyKeyboardMarkup()
keyboard_start.row('Школьная программа', 'Внеклассное чтение')
keyboard_klass = telebot.types.ReplyKeyboardMarkup()
keyboard_klass.row('11', '10', '9', 'Вернуться назад')
A = []
B = []
N = []


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я помогу тебе найти книгу для чтения :D \n---------------------------------------\nVersion 1.1.5\n* Добавлен вывод автора при рандоме и подборки книг\n* Добавлено пару десятков книг\n* Авторов стоит указывать с именем и фамилией', reply_markup=keyboard_start)

@bot.message_handler(commands=['help'])
def send_profil(message):
    me = '@Troll_w'
    bot.send_message(message.chat.id, f'Привет, по поводу ошибки или добавления новой книги обратись к {me}')

@bot.message_handler(content_types=['text'])
def start_text(message):
    if message.text == 'Внеклассное чтение':
        bot.send_message(message.chat.id, '---', reply_markup=keyboard1) #Как так, текст придумать
        #bot.delete_message(message.chat.id, message.id)
        bot.register_next_step_handler(message, send_text)
    elif message.text == 'Школьная программа':
        bot.send_message(message.chat.id, 'Выбери какой тебе нужен класс', reply_markup=keyboard_klass)
        bot.register_next_step_handler(message, get_klass)

@bot.message_handler(func=lambda c:True, content_types=['text'])
def get_klass(message):
    if message.text == 'Вернуться назад':
        bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
        bot.register_next_step_handler(message, start_text)
    klass = message.text
    cursor_S.execute(f"SELECT Автор FROM SCHOOL WHERE Класс == {klass};")
    A = cursor_S.fetchall()
    cursor_S.execute(f"SELECT Название FROM SCHOOL WHERE Класс == {klass};")
    B = cursor_S.fetchall()
    cursor_S.execute(f"SELECT Номер FROM SCHOOL WHERE Класс == {klass};")
    N = cursor_S.fetchall()
    for i in range(len(A)):
        bot.send_message(message.chat.id, str(N[i])[1:-1][:-1] + ')' + str(A[i])[1:-1][1:-1][:-1] + ' - \'' + str(B[i])[1:-1][:-1] + '\'')
    bot.send_message(message.chat.id, 'Для выбора книги введите цифру')
    bot.register_next_step_handler(message, continion_1)

@bot.message_handler(content_types=['text'])
def continion_1(message):
    if message.text == 'Вернуться назад':
        bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
        bot.register_next_step_handler(message, start_text)
    bot.register_next_step_handler(message, continion_2)

@bot.message_handler(content_types=['text'])
def continion_2(message):
    num = int(message.text)
    cursor_S.execute(f"SELECT Название FROM SCHOOL WHERE Номер == {num};")
    fails = cursor_S.fetchone()
    with open(f'SchoolBook\{fails[0]}.pdf', 'rb') as f1:
        bot.send_document(message.chat.id, f1)
    bot.send_message(message.chat.id, 'Приятного чтения :D', reply_markup=keyboard_start)
    bot.delete_message(message.chat.id, message.message_id) # !!!!!!!
    bot.register_next_step_handler(message, start_text)
######################################################Добавить инлайн кнопки для каждой книги

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Начнём подборку книг?':
        bot.send_message(message.chat.id, 'Напиши имя автора чьё произведение хочешь почитать', reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_autor)
    elif message.text == 'Случайную книгу':
        cursor_B.execute("SELECT Произведение FROM BOOK ORDER BY RANDOM() LIMIT 1;")
        Books = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{Books[0]}';")
        Art = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{Books[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.chat.id, 'Советую прочитать тебе \"' + Books[0] + "\"\nАвтор - " + Art[0] + '\n' + K[0])
        bot.register_next_step_handler(message, send_text)
    elif message.text == 'Вернуться назад':
        bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
        bot.register_next_step_handler(message, start_text)

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
def get_zanr(message):
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
    bot.register_next_step_handler(message, Itogi)

@bot.message_handler(content_types=['text'])
def Itogi(message):
    if Author == 'Пропуск' and Zanr == 'Пропуск' and Razmer == 'Пропуск':
        bot.send_message(message.from_user.id, 'Дружище, сам то знаешь что хочешь?\n---------------------------------------\nВоспользуйся кнопкой \"Случайную книгу\"')
        bot.register_next_step_handler(message, start_text)
######################################################################################################################
    elif Author == 'Пропуск' and Zanr == 'Пропуск':
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Размер =='{Razmer}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

    elif Author == 'Пропуск' and Razmer == 'Пропуск':
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Жанр == '{Zanr}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

    elif Zanr == 'Пропуск' and Razmer == 'Пропуск':
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

    elif Zanr == 'Пропуск':
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Размер =='{Razmer}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

    elif Razmer == 'Пропуск':
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

    else:
        cursor_B.execute(f"SELECT Произведение FROM BOOK WHERE Автор == '{Author}' AND Жанр == '{Zanr}' AND Размер =='{Razmer}';")
        Books = cursor_B.fetchall()
        if not Books:
            bot.send_message(message.from_user.id, "Прости друг, но кажется моя база данных не может найти книгу, она не такая большая как ты думаешь :(")
            bot.send_message(message.from_user.id, "Но ты можешь попросить добавить их (Команда /help) :D")
        B = Books[random.randint(0, len(Books) - 1)]
        cursor_B.execute(f"SELECT Автор FROM BOOK WHERE Произведение =='{B[0]}';")
        A = cursor_B.fetchone()
        cursor_B.execute(f"SELECT Книга FROM BOOK WHERE Произведение =='{B[0]}';")
        K = cursor_B.fetchone()
        bot.send_message(message.from_user.id, 'Советую тебе прочитать книгу \"' + B[0] + '\"\nАвтор - ' + A[0] + '\n' + K[0])
        if message.text == 'Вернуться назад':
            bot.send_message(message.chat.id, 'Возвращаем', reply_markup=keyboard_start)
            bot.register_next_step_handler(message, start_text)
        else:
            bot.register_next_step_handler(message, send_text)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
