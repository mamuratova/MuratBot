import telebot
from decouple import config
bot = telebot.TeleBot(config('Token'))
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random


inline_keyboard = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton('Да', callback_data='yes')
btn2 = InlineKeyboardButton('Нет', callback_data='no')
inline_keyboard.add(btn1, btn2)


@bot.message_handler(commands=['start'])
def starting(message):
    chat_id = message.chat.id
    user = message.from_user.first_name
    bot.send_message(chat_id, f'Hi, {user}')
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBOklgiOlR-KFj2lEU9nMlPSGJ2zKIOQACpAADr8ZRGgTuYv70faXbHwQ')
    bot.send_message(chat_id, "Хочешь поиграть:", reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda c: True)
def func(c):
    chat_id = c.message.chat.id
    if c.data == 'no':
        bot.send_message(chat_id, 'Хорошо, до встречи!!!')
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBOm5giSkFwcu1wHWrxte7Qsx_BmiI_gACCAMAAm2wQgMvOYPVPlZS6R8E')
    if c.data == 'yes':
        global rnum
        rnum = random.randrange(1, 100)
        global attempt
        attempt = 0
        bot.send_message(chat_id, 'Угадай число которое я загадал! От 1 до 100!!!')


@bot.message_handler(content_types=['text'])
def game(message):
    chat_id = message.chat.id
    text = message.text
    try:
        global attempt
        if 6 != attempt and attempt < 6:
            attempt += 1
            if int(text) == rnum:
                bot.send_message(message.chat.id, 'Поздравляю! Ты угадал!')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBOolgiULKH1_eCj2f4RVZBbIh0T3OQAACIgMAAm2wQgO8x8PfoXC1eB8E')
                bot.send_message(chat_id, f'Ты использовал {attempt} попыток!')
                bot.send_message(chat_id, 'Хочешь сыграть еще раз?', reply_markup=inline_keyboard)
            elif int(text) != rnum:
                if int(text) > rnum:
                    bot.send_message(chat_id, 'Загаданное число меньше чем ты думаешь!')
                    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBOoxgiUi0VGil2euTtCfFyAj53WHvyAACEwMAAm2wQgMrGNM75XhwfB8E')
                    bot.send_message(chat_id, f'Ты использовал {attempt} попыток!')
                elif int(text) < rnum:
                    bot.send_message(chat_id, 'Загаданное число больше чем ты думаешь!')
                    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBOqRgiUkaG3a0vlf-7pFqcoci90pdjAACDAMAAm2wQgNUfsxB8ZeE-x8E')
                    bot.send_message(chat_id, f'Ты использовал {attempt} попыток!')
        else:
            bot.send_message(chat_id, 'Ты проиграл!!!')
            bot.send_message(chat_id, f'Ты использовал {attempt} попыток!')
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBOrlgiUutzNC-SOvJirp0Xzij_E4zhAACzgwAApmBUUu-SEJ4AYw9hR8E')
            bot.send_message(chat_id, 'Хочешь сыграть еще раз?', reply_markup=inline_keyboard)
    except Exception as e:
        bot.send_message(chat_id, f'Я не знаю что делать!{e}')


bot.polling(none_stop=True)