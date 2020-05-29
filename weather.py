import requests
import telebot
import os
token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)
# Переменные
api_url = 'https://stepik.akentev.com/api/weather'
param = {
    'city': 'Ростов-на-Дону',
    'forecast': 0
}
state = {}

# Состояния

MAIN = 'main'
DAY = 'day'
WEATHER = 'weather'


@bot.message_handler(func=lambda message: state.get(message.from_user.id, MAIN) == MAIN)
def main_handler(message):
    print(message.from_user.id)
    bot.send_message(message.from_user.id, 'Выбери город: ')
    state[message.from_user.id] = DAY


@bot.message_handler(func=lambda message: state.get(message.from_user.id, MAIN) == DAY)
def day_handler(message):
    param['city'] = message.text
    bot.send_message(message.from_user.id, 'Когда? (Сегодня, Завтра, Послезавтра): ')
    state[message.from_user.id] = WEATHER


@bot.message_handler(func=lambda message: state.get(message.from_user.id, MAIN) == WEATHER)
def day_handler(message):
    if message.text.lower() == 'сегодня':
        param['forecast'] = 0
        response = requests.get(api_url).json()
        bot.send_message(message.from_user.id,
                         'Сегодня в {}: {} градусов. В целом {}'.format(param['city'], response['temp'],
                                                                        response['description']))
    if message.text.lower() == 'завтра':
        param['forecast'] = 1
        response = requests.get(api_url).json()
        bot.send_message(message.from_user.id,
                         'Завтра в {}: {} градусов. В целом {}'.format(param['city'], response['temp'],
                                                                        response['description']))
    if message.text.lower() == 'послезавтра':
        param['forecast'] = 2
        response = requests.get(api_url).json()
        bot.send_message(message.from_user.id,
                         'Послезавтра в {}: {} градусов. В целом {}'.format(param['city'], response['temp'],
                                                                        response['description']))

bot.polling()
