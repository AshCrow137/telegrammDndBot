import telebot
import random

bot = telebot.TeleBot('6358163919:AAHO1lf5BJLxQtxLM7mKKwO5ONh_5qMXiI8')


@bot.message_handler(commands=['start'])
def start_message(message):
  id = message.chat.id
  name = message.from_user.first_name
  if not name:
    name = message.from_user.username
    if not name:
      bot.send_message(id, f'Привет, кто бы ты ни был!')
      return
  bot.send_message(id, f'Привет, {name}')


print('bot is on line')
bot.infinity_polling(1)
