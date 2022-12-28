import telebot
from telebot import types

bot = telebot.TeleBot('5890998907:AAFcYWWrkjMWInilEDqiHzuW_XSecaMIDkY')


@bot.message_handler(commands=["start"])
def help(m, res=False):
   global help_user_id
   help_user_id = m.from_user.id
   markup = types.InlineKeyboardMarkup()
   button1 = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
   markup.add(button1)
   msg = bot.send_message(m.chat.id, 'Задайте вопрос боту.', reply_markup=markup)
   bot.register_next_step_handler(msg, helpBot)

# Функция, отправляющая вопрос от пользователя в чат поддержки
def helpBot(m):
     bot.forward_message(-1001826305476, m.chat.id, m.message_id)

# Получение сообщений от юзера,
@bot.message_handler(content_types=["text"])
def handle_text(m):
   global help_user_id
   # здесь если чат id равен id чата поддержки, то отправить сообщение пользователю который задал вопрос
   if int(m.chat.id) == int(-1001826305476):
      bot.send_message(help_user_id, m.text)

bot.infinity_polling()