import telebot
from telebot import types
import requests


bot = telebot.TeleBot('6022568831:AAEqnB3J8_EEJDrTx6K75Al3PRss4BYH1qM')


@bot.message_handler(commands=['Hello'])
def hello(message):
    mess = f'Hello, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # start = types.KeyboardButton('Start')
    website = types.KeyboardButton('Website')
    markup.add(website)
    bot.send_message(message.chat.id, 'Help', reply_markup=markup)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет! Я бот по финансам. Я могу помочь тебе узнать текущий курс валют. Для этого введи тикеры двух валют через пробел.')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Website":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Visit website', url="https://t.me/n0mercy_01"))
        bot.send_message(message.chat.id, 'Go to website', parse_mode='html', reply_markup=markup)
    else:
        # Разбиваем полученную строку на две валюты
        from_currency, to_currency = message.text.split()
        # Получаем данные о курсе валют
        exchange_rate = get_exchange_rate(from_currency.upper(), to_currency.upper())
        # Отправляем ответ пользователю
        bot.send_message(message.chat.id,
                         f'Текущий курс {from_currency.upper()} к {to_currency.upper()}: {exchange_rate}')


# Функция для получения данных о курсах валют с сайта Alpha Vantage
def get_exchange_rate(from_currency, to_currency):
    api_key = 'ваш API ключ'
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}'
    response = requests.get(url).json()
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return exchange_rate


# Запускаем бота
bot.polling(none_stop=True)
