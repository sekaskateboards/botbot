import telebot
from telebot import types
from  telebot.apihelper import ApiTelegramException
from config import TOKEN, PROVIDER_TOKEN, TOKEN_QIWI, PHONE, TEXT, ADMIN, CHAT_ID
from telebot.types import LabeledPrice, ShippingOption
from pypayment import *
from datetime import timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random


bot = telebot.TeleBot(TOKEN)

#payment part
QiwiPayment.authorize(TOKEN_QIWI,                             
                      theme_code="test",
                      expiration_duration=timedelta(hours=1),
                      payment_type=QiwiPaymentType.ALL)
Payment = QiwiPayment(amount=3000)
payment_lite = QiwiPayment(amount=1000)
payment_full = QiwiPayment(amount=7500)
gc = gspread.service_account(filename='TEST.json')
sh = gc.open("TEST")
worksheet = sh.get_worksheet(0)
CHECK = 0 # used when a user leaves a feedback
WHAT = 0  # Used when a user chooses payment method


@bot.message_handler(commands=['admin'])
def admin_start(message):
    global worksheet
    """Admin panel. Check ID and gives access"""
    global ADMIN
    if str(message.chat.id) == ADMIN:
        bot.send_message(message.chat.id, 'Следующее твоё сообщение отправится всем юзерам')
        bot.register_next_step_handler(message, all_user)
def all_user(message):
    global worksheet
    """Mailing for all users"""
    for user in worksheet.col_values(5):
        try:
            bot.copy_message(user, message.chat.id, message.message_id)
        except Exception:
            pass


@bot.message_handler(commands=['start'])
def main_keyboard(message):
    global worksheet
    """Subscription check and main keyboard"""
    if bot.get_chat_member(CHAT_ID,message.chat.id).status in ['member','creator','administrator']:
            print(11111)
    else:
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Я подписан')
        mark.add(btn)
        bot.send_message(message.chat.id, 'Для начала - подпишись\nhttps://t.me/BiahezaRussian', reply_markup=mark)
        return 0
    data = worksheet.col_values(5)        # column with users ID
    if str(message.chat.id) not in data:
        for i in range(1, 10 ** 10):
            if type(worksheet.cell(i, 5).value) != str:
                worksheet.update('E' + str(i), message.chat.id)
                break
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    course = types.InlineKeyboardButton('📚Курс')
    helper = types.KeyboardButton('⚙️Техническая поддержка')
    feedback = types.KeyboardButton('📣Отзывы')
    info = types.KeyboardButton('❓О курсе')
    markup.add(course, helper)
    markup.add(info, feedback)
    bot.send_message(message.chat.id,
                     '👋Приветствую',
                     reply_markup=markup)
    return markup


@bot.message_handler(content_types='text')
def message_reply(message):
    global CHECK
    global WHAT
    global worksheet
    if CHECK == 1:
        for i in range(1, 10 ** 10):
            if type(worksheet.cell(i, 2).value) != str:
                worksheet.update('B' + str(i), message.text)
                break
        CHECK = 0
    if 'ADMINSAY:' in message.text:
        for user in worksheet.col_values(5):
            try:
                bot.send_message(user, message.text[9:])
            except Exception:
                pass
    if bot.get_chat_member(CHAT_ID,message.chat.id).status in ['member','creator','administrator']:
            print(11111)
    else:
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Я подписан')
        mark.add(btn)
        bot.send_message(message.chat.id, 'Для начала - подпишись\nhttps://t.me/BiahezaRussian', reply_markup=mark)
        return 0
    if message.text == 'Я подписан':
        main_keyboard(message)
    if message.text == '📚Курс':
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton('🗣️Консультация')
        b2 = types.KeyboardButton('✨Курс')
        b3 = types.KeyboardButton('🛍️Полный курс')
        b4 = types.KeyboardButton('👀Назад')
        mark.add(b1,b2,b3,b4)
        bot.send_message(message.chat.id, '🚀<b>Если вас заинтересовал наш прайс-лист:\n🗣️Консультация: 1000₽</b> <s>1500₽</s>\n✨<b>Курс: 3000₽</b> <s>4500₽</s>\n🛍️<b>Полный курс, консультация: 7500₽</b> <s>10000₽</s>', reply_markup=mark, parse_mode='HTML')
    if message.text == '🤑Оплатил':
        if Payment.status == PaymentStatus.PAID or str(message.chat.id) in worksheet.col_values(1) and WHAT==1:
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Урок №1', url='https://www.youtube.com/watch?v=WDPpliSF0GM')
            b2 = types.InlineKeyboardButton(text='Урок №2', url='https://www.youtube.com/watch?v=qa-yMuGjOp4')
            b3 = types.InlineKeyboardButton(text='Урок №3', url='https://www.youtube.com/watch?v=k6tIOmMrwJ8')
            b4 = types.InlineKeyboardButton(text='Урок №4', url='https://www.youtube.com/watch?v=d2hIALhrLBM')
            b5 = types.InlineKeyboardButton(text='Урок №5', url='https://www.youtube.com/watch?v=m6AhC0Jl2E8')   
            b6 = types.InlineKeyboardButton(text='Урок №6', url='https://www.youtube.com/watch?v=gmhMnV5DdZk')
            mark.add(b1,b2,b3,b4,b5,b6)
            bot.send_message(message.chat.id, 'А вот и курс!', reply_markup=mark)
            #bot.send_message(message.chat.id, 'Что-то ещё?', reply_markup=main_keyboard(message))
            for i in range(1, 10 ** 10):
                if type(worksheet.cell(i, 1).value) != str:
                    worksheet.update('A' + str(i), message.chat.id)
                    break
        elif payment_lite.status == PaymentStatus.PAID or str(message.chat.id) in worksheet.col_values(3) and WHAT==3:
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Свзяь', url='https://t.me/MRXPROGER')
            mark.add(b1)
            bot.send_message(message.chat.id, 'Консультация оплачена! Для её прохождения - свяжитесь со мной, переслав данное сообщение', reply_markup=mark)
            for i in range(1, 10 ** 10):
                if type(worksheet.cell(i, 3).value) != str:
                    worksheet.update('C' + str(i), message.chat.id)
                    break
        elif payment_full.status == PaymentStatus.PAID or str(message.chat.id) in worksheet.col_values(4) and WHAT==4:
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Урок №1', url='https://www.youtube.com/watch?v=WDPpliSF0GM')
            b2 = types.InlineKeyboardButton(text='Урок №2', url='https://www.youtube.com/watch?v=qa-yMuGjOp4')
            b3 = types.InlineKeyboardButton(text='Урок №3', url='https://www.youtube.com/watch?v=k6tIOmMrwJ8')
            b4 = types.InlineKeyboardButton(text='Урок №4', url='https://www.youtube.com/watch?v=d2hIALhrLBM')
            b5 = types.InlineKeyboardButton(text='Урок №5', url='https://www.youtube.com/watch?v=m6AhC0Jl2E8')   
            b6 = types.InlineKeyboardButton(text='Урок №6', url='https://www.youtube.com/watch?v=gmhMnV5DdZk')
            mark.add(b1,b2,b3,b4,b5,b6)
            bot.send_message(message.chat.id, 'А вот и курс!', reply_markup=mark)
            mark1 = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Свзяь', url='https://t.me/MRXPROGER')
            mark.add(b1)
            bot.send_message(message.chat.id, 'Вы приобрели полный курс + консультация! Свяжитесь со мной, переслав данное сообщение', reply_markup=mark1)
            #bot.send_message(message.chat.id, 'Что-то ещё?', reply_markup=main_keyboard(message))
            for i in range(1, 10 ** 10):
                if type(worksheet.cell(i, 4).value) != str:
                    worksheet.update('D' + str(i), message.chat.id)
                    break
        else:
            bot.send_message(message.chat.id, 'Нет подтверждения транзакции. Попробуйте через минуту')
    if message.text == '👀Назад':
        main_keyboard(message)
    if message.text == '⚙️Техническая поддержка':
        mark = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Поддержка', url='https://t.me/helphelphelper_bot')
        mark.add(btn)
        bot.send_message(message.chat.id, 'По всем вопросам пишите сюда', reply_markup=mark)
    if message.text == '❓О курсе':
        bot.send_message(message.chat.id, TEXT, parse_mode='Markdown')
    if message.text == '📣Отзывы':
        markup_feedback = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_new_feedback = types.KeyboardButton('👌Оставить отзыв')
        btn_random_feedback = types.KeyboardButton('🎲Рандомный отзыв')
        btn_back = types.KeyboardButton('👀Назад')
        markup_feedback.add(btn_new_feedback, btn_random_feedback)
        markup_feedback.add(btn_back)
        bot.send_message(message.chat.id, 'Выберите интересующий Вас пункт', reply_markup=markup_feedback)
    if message.text == '👌Оставить отзыв':
        if str(message.chat.id) in worksheet.col_values(1):
            bot.send_message(message.chat.id, 'Напишите свой отзыв о наших курсах')
            CHECK = 1
            return 0
        else:
            bot.send_message(message.chat.id, 'Вы не можете оставить отзыв - Вы ещё не покупали курс')
    if message.text == '🎲Рандомный отзыв':
        data = worksheet.col_values(2)
        bot.send_message(message.chat.id, data[random.randint(1, len(data) - 1)])
    if message.text == '✨Курс':
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='💴 Оплата', url=Payment.url)
        markup_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('🤑Оплатил')
        btn_back = types.KeyboardButton('👀Назад')
        btn_yeban = types.KeyboardButton('💳Оплатить другим способом')
        markup_check.add(btn_yes,btn_yeban)
        markup_check.add(btn_back)
        markup.add(btn_my_site)
        WHAT = 1
        if str(message.chat.id) in worksheet.col_values(1):
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Урок №1', url='https://www.youtube.com/watch?v=WDPpliSF0GM')
            b2 = types.InlineKeyboardButton(text='Урок №2', url='https://www.youtube.com/watch?v=qa-yMuGjOp4')
            b3 = types.InlineKeyboardButton(text='Урок №3', url='https://www.youtube.com/watch?v=k6tIOmMrwJ8')
            b4 = types.InlineKeyboardButton(text='Урок №4', url='https://www.youtube.com/watch?v=d2hIALhrLBM')
            b5 = types.InlineKeyboardButton(text='Урок №5', url='https://www.youtube.com/watch?v=m6AhC0Jl2E8')   
            b6 = types.InlineKeyboardButton(text='Урок №6', url='https://www.youtube.com/watch?v=gmhMnV5DdZk')
            mark.add(b1,b2,b3,b4,b5,b6)
            bot.send_message(message.chat.id, 'А вот и курс!', reply_markup=mark)
        else:
            bot.send_message(message.chat.id, "Для того, чтобы получить доступ к курсам - произведите оплату",
                                reply_markup=markup)
            bot.send_message(message.chat.id, "После успешной оплаты - нажмите на кнопку 'Оплатил'",
                                reply_markup=markup_check)
    if message.text == '🗣️Консультация':
        WHAT = 3
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='💴 Оплата', url=payment_lite.url)
        markup_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('🤑Оплатил')
        btn_back = types.KeyboardButton('👀Назад')
        btn_yeban = types.KeyboardButton('💳Оплатить другим способом')
        markup_check.add(btn_yes, btn_yeban)
        markup_check.add(btn_back)
        markup.add(btn_my_site)
        if str(message.chat.id) in worksheet.col_values(3):
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Свзяь', url='https://t.me/MRXPROGER')
            mark.add(b1)
            bot.send_message(message.chat.id, 'Консультация оплачена! Для её прохождения - свяжитесь со мной, переслав данное сообщение', reply_markup=mark)
        else:
            bot.send_message(message.chat.id, "Для того, чтобы получить доступ к курсам - произведите оплату",
                                reply_markup=markup)
            bot.send_message(message.chat.id, "После успешной оплаты - нажмите на кнопку 'Оплатил'",
                                reply_markup=markup_check)
    if message.text == '🛍️Полный курс':
        WHAT = 4
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='💴 Оплата', url=payment_full.url)
        markup_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('🤑Оплатил')
        btn_back = types.KeyboardButton('👀Назад')
        btn_yeban = types.KeyboardButton('💳Оплатить другим способом')
        markup_check.add(btn_yes,btn_yeban)
        markup_check.add(btn_back)
        markup.add(btn_my_site)
        if str(message.chat.id) in worksheet.col_values(4):
            mark = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Урок №1', url='https://www.youtube.com/watch?v=WDPpliSF0GM')
            b2 = types.InlineKeyboardButton(text='Урок №2', url='https://www.youtube.com/watch?v=qa-yMuGjOp4')
            b3 = types.InlineKeyboardButton(text='Урок №3', url='https://www.youtube.com/watch?v=k6tIOmMrwJ8')
            b4 = types.InlineKeyboardButton(text='Урок №4', url='https://www.youtube.com/watch?v=d2hIALhrLBM')
            b5 = types.InlineKeyboardButton(text='Урок №5', url='https://www.youtube.com/watch?v=m6AhC0Jl2E8')   
            b6 = types.InlineKeyboardButton(text='Урок №6', url='https://www.youtube.com/watch?v=gmhMnV5DdZk')
            mark.add(b1,b2,b3,b4,b5,b6)
            bot.send_message(message.chat.id, 'А вот и курс!', reply_markup=mark)
            mark1 = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text='Свзяь', url='https://t.me/MRXPROGER')
            mark.add(b1)
            bot.send_message(message.chat.id, 'Вы приобрели полный курс + консультация! Свяжитесь со мной, переслав данное сообщение', reply_markup=mark1)
        else:
            bot.send_message(message.chat.id, "Для того, чтобы получить доступ к курсам - произведите оплату",
                                reply_markup=markup)
            bot.send_message(message.chat.id, "После успешной оплаты - нажмите на кнопку 'Оплатил'",
                                reply_markup=markup_check)
    if message.text == '💳Оплатить другим способом':
        bot.send_message(message.chat.id, 'Свяжитесь со мной по поводу оплаты\nhttps://t.me/MRXPROGER')

bot.infinity_polling()


