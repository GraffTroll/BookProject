import flask
import telebot
from telebot import types
import os

server = flask.Flask(__name__)
bot = telebot.TeleBot('1700158651:AAHDN9aNBOztTUnrpJQEgAQmOeofOt6UIoo')

@server.route('/' + '1700158651:AAHDN9aNBOztTUnrpJQEgAQmOeofOt6UIoo', methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
         flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format('menbots', '1700158651:AAHDN9aNBOztTUnrpJQEgAQmOeofOt6UIoo'))
    return "Hello from Heroku!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
