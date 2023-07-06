import telebot
from telebot import types
import random
import os
import background
import get_token
token = get_token.getToken()
bot = telebot.TeleBot(token)

dice_list = [2, 4, 6, 8, 10, 12, 20, 100]


def create_dice_datalist():
  result = []
  for dice in dice_list:
    result.append(f'dice_type={dice}')
  return result


def create_dice_keyboard():
  keyboard = []
  column = []
  for dice in dice_list:
    button = types.InlineKeyboardButton(str(dice),
                                        callback_data=f'dice_type={dice}')
    column.append(button)
    if len(column) % 3 == 0 and len(column) != 0:  #делаем по 3 кнопки в ряд
      keyboard.append(column)

      column = []

  keyboard.append(column)
  print('dice keyboard created')
  markup = types.InlineKeyboardMarkup(keyboard)
  return markup


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


@bot.message_handler(commands=['r'])
def create_dice_message(message):
  bot.send_message(message.chat.id,
                   text='Выберите куб',
                   reply_markup=dice_markup)


@bot.callback_query_handler(func=lambda call: True)
def catch_data(call):
  if not call:
    return
  if call.data in dice_datalist:
    random_number = random.randint(1, dice_dict[call.data])
    text = f' {random_number}'
    bot.send_message(call.message.chat.id, text)


dice_markup = create_dice_keyboard()
dice_datalist = create_dice_datalist()
dice_dict = dict(zip(dice_datalist, dice_list))
background.keep_alive()
print('bot is on line')
bot.infinity_polling(1)
