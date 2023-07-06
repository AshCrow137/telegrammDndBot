import telebot
from telebot import types
import random
import os
import background
import get_token
token = get_token.getToken()
bot = telebot.TeleBot(token)

dice_list = [2, 4, 6, 8, 10, 12, 20, 100]
user_dict = {}
def create_number_keyboard():
  keyboard = []
  column = []
  for i in range(1,11):
    button = types.InlineKeyboardButton(str(i),callback_data=f'number={i}')
    column.append(button)
    if len(column) % 3 == 0 and len(column) != 0: 
      keyboard.append(column)

      column = []
  column.append(types.InlineKeyboardButton('Свое число',callback_data='custom_number'))
  keyboard.append(column)
  print('number keyboard created')
  markup = types.InlineKeyboardMarkup(keyboard)
  return markup
def create_number_datalist():
    result = []
    for i in range(1,11):
      result.append(f'number={i}')
    return result  
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
    if len(column) % 4 == 0 and len(column) != 0:  #делаем по 3 кнопки в ряд
      keyboard.append(column)

      column = []

  keyboard.append(column)
  print('dice keyboard created')
  markup = types.InlineKeyboardMarkup(keyboard)
  return markup
def roll_dices(number: int,roll_range: int):
  results = []
  for num in range(1,number+1):
    random_number = random.randint(1, roll_range)
    results.append(random_number)
  return results  

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
  global user_dict #TODO Remove
  if not call:
    return
  # if call.data in dice_datalist:
  #   random_number = random.randint(1, dice_dict[call.data])
  #   text = f' {random_number}'
  #   bot.send_message(call.message.chat.id, text)
  chat_id = call.message.chat.id
  if call.data in dice_datalist:
    user_dict[str(call.message.from_user.id)] = dice_dict[call.data]
    bot.send_message(chat_id,'Выбран куб d{}\nВыберите количество кубов'.format(dice_dict[call.data]),reply_markup=number_markup)
  elif call.data in number_datalist:
    
    dices =roll_dices(number_dict[call.data],user_dict[str(call.message.from_user.id)])
    summ = sum(dices)
    text = f'Результат:\n{dices} = {summ}'
    bot.send_message(chat_id,text)



dice_markup = create_dice_keyboard()
dice_datalist = create_dice_datalist()
dice_dict = dict(zip(dice_datalist, dice_list))
number_markup = create_number_keyboard()
number_datalist = create_number_datalist()
number_dict = dict(zip(number_datalist,list(range(1,11))))
background.keep_alive()
print('bot is on line')

bot.infinity_polling(1)
