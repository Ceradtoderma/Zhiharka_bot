import telebot
import requests
import os
from random import shuffle

#  Переменные
token = os.environ["TELEGRAM_TOKEN"]
api_weather_key = 'fc3837d82e69a8bea3f8c2a0f1e68643'
bot = telebot.TeleBot(token)
weather_api = 'https://api.openweathermap.org/data/2.5/onecall'
weather_coord = 'http://api.openweathermap.org/data/2.5/weather'
mill_api = 'https://engine.lifeis.porn/api/millionaire.php'
accent_api = 'https://stepik.akentev.com/api/stress'
password = '123'
remove_key = telebot.types.ReplyKeyboardRemove()

data = {"state": {"param": {}, "298325596": "choice liter"},
        'password': {}}
#  Состояния
MAIN = 'Главное меню'
WEATHER_CITY = 'Меню погоды'
WEATHER_DAY = 'Погода, выбор дня'
MILLIONER_MAIN = 'Меню миллионера'
MILLIONER_GAME = 'Игра миллионер'
MILLIONER_ANSWER = 'Ожидание правильного ответа'
ANIMALS_PASS = 'Авторизация животных'
ANIMALS_VIEW = 'Показывем фото животных'

ACCENTS = 'Меню ударений'
ACCENTS_CHOISE = 'Выбор буквы'


#  функции

def view_photo(file, user_id):
    photo = open(file, 'rb')
    bot.send_chat_action(user_id, 'upload_photo')
    bot.send_photo(user_id, photo)
    bot.send_message(user_id, 'Еще фоток?')
    bot.send_message(user_id, 'Ты всегда можешь написать "/start", чтобы вернутся в начало')


@bot.message_handler(commands=['stop', 'start'])
def command(message):
    user_id = str(message.from_user.id)
    data['param'] = {}
    if message.text == '/stop':
        data['state'][user_id] = MAIN
        bot.send_message(user_id, 'Начнем сначала')
    if message.text == '/start':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add('Погода', 'Зверушки', 'Викторина', 'Ударения')
        bot.send_message(user_id,
                         'Привет! Начнем? Я умею показывать погоду и фотки зверушек которые '
                         'живут у Андрея. Еще есть две игры - "Викторина" и "Ударения"',
                         reply_markup=keyboard)
        data['state'][user_id] = MAIN


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = data['state'].get(user_id, MAIN)
    if state == MAIN:
        main_handler(message)
    elif state == WEATHER_CITY:
        weather_city_handler(message)
    elif state == WEATHER_DAY:
        weather_day_handler(message)
    elif state == MILLIONER_MAIN:
        millioner_main_handler(message)
    elif state == MILLIONER_GAME:
        millioner_game_handler(message)
    elif state == MILLIONER_ANSWER:
        millioner_answer_handler(message)
    elif state == ANIMALS_VIEW:
        animals_view_handler(message)
    elif state == ANIMALS_PASS:
        animals_pass_handler(message)
    elif state == ACCENTS:
        accent_handler(message)
    elif state == ACCENTS_CHOISE:
        accent_choise(message)


def main_handler(message):
    user_id = str(message.from_user.id)
    if message.text == 'Погода':
        bot.send_message(user_id, 'Отлично! Посмотрим погоду 😇\nНапиши название интересующего города:',
                         reply_markup=remove_key)
        data['state'][user_id] = WEATHER_CITY

    elif message.text == 'Викторина':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add('1', '2', '3')

        bot.send_message(user_id,
                         'Давай сыграем в "Викторину"\n'
                         'выбери сложность: от 1 до 3',
                         reply_markup=keyboard)
        data['state'][user_id] = MILLIONER_MAIN

    elif message.text == 'Ударения':
        data['param'][user_id] = {}
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add('Случайная')
        bot.send_message(user_id, 'Расставление правильных ударений ')
        bot.send_message(user_id, 'Отправь мне букву или напиши "Случайная"', reply_markup=keyboard)
        data['state'][user_id] = ACCENTS_CHOISE

    elif message.text == 'Зверушки':
        bot.send_message(user_id, 'Посмотрим на моих зверушек) ')
        if data['password'].get(user_id, 0) == password:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add('Рэй', 'Бэсси', 'Рикки')
            bot.send_message(user_id, 'Я тебя знаю)', reply_markup=keyboard)
            bot.send_message(user_id, 'Ты всегда можешь написать "/start", чтобы вернутся в начало')
            data['state'][user_id] = ANIMALS_VIEW
            animals_view_handler(message)
        else:
            bot.send_message(user_id, 'Это очень личное, надо бы ввести пароль')
            data['state'][user_id] = ANIMALS_PASS


def animals_pass_handler(message):
    user_id = str(message.from_user.id)
    data['password'][user_id] = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add('Рэй', 'Бэсси', 'Рикки')
    if data['password'][user_id] == password:
        # animals_view_handler(message)
        bot.send_message(user_id, 'Верно! Выбирай:', reply_markup=keyboard)
        bot.send_message(user_id, 'Ты всегда можешь написать "/start", чтобы вернутся в начало')
        data['state'][user_id] = ANIMALS_VIEW
    else:
        bot.send_message(user_id, 'Пароль не верный, попробуй ещё')


def animals_view_handler(message):
    user_id = str(message.from_user.id)
    if message.text == 'Рэй':
        view_photo('Rey.jpg', user_id)
    if message.text == 'Рикки':
        view_photo('Rik.jpg', user_id)
    if message.text == 'Бэсси':
        view_photo('Bes.jpg', user_id)


def accent_choise(message):
    user_id = str(message.from_user.id)
    data['right_answer'] = {}
    data['question'] = {}
    if len(message.text) == 1:
        data['param'][user_id]['first_letter'] = message.text
        response = requests.get(accent_api, params=data['param'][user_id]).json()
        data['question'][user_id] = response['word'].lower()
        data['right_answer'][user_id] = response['word']
    else:
        response = requests.get(accent_api).json()
        data['question'][user_id] = response['word'].lower()
        data['right_answer'][user_id] = response['word']
    bot.send_message(user_id, 'Выдели заглавной буквой правильное ударение в слове:\n'
                              '"{}"'.format(data['question'][user_id]))
    data['state'][user_id] = ACCENTS


def accent_handler(message):
    user_id = str(message.from_user.id)
    if data['right_answer'][user_id] in message.text:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add('Случайная')
        bot.reply_to(message, 'Верно!')
        bot.send_message(user_id, 'Отправь мне букву или выбери "Случайная", для возврата '
                                  'в начало нажми "/start"', reply_markup=keyboard)
        data['state'][user_id] = ACCENTS_CHOISE
    else:
        bot.reply_to(message, 'Неправильно!')


def weather_city_handler(message):
    user_id = str(message.from_user.id)
    data['param'][user_id] = {
        'appid': api_weather_key,
        'exclude': 'current, hourly',
        'lang': 'ru',
        'lat': '',
        'lon': '',
        'units': 'metric'
    }
    param_city = {
        'q': message.text,
        'appid': api_weather_key
    }
    data['city'] = {}
    data['city'][user_id] = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('Сегодня', 'Завтра', 'Послезавтра')
    response = requests.get(weather_coord, params=param_city).json()
    try:
        data['param'][user_id]['lat'] = response['coord']['lat']
        data['param'][user_id]['lon'] = response['coord']['lon']
        bot.send_message(user_id, 'На когда смотрим погоду?', reply_markup=keyboard)
        data['state'][user_id] = WEATHER_DAY
    except KeyError:
        bot.send_message(user_id, 'Я не знаю такого города. Подумай лучше')


def weather_day_handler(message):
    user_id = str(message.from_user.id)
    if message.text == 'Сегодня':
        day = 0
    elif message.text == 'Завтра':
        day = 1
    elif message.text == 'Послезавтра':
        day = 2
    try:
        response = requests.get(weather_api, params=data['param'][user_id]).json()
        temp_morn = response['daily'][day]['temp']['morn']
        temp_day = response['daily'][day]['temp']['day']
        temp_eve = response['daily'][day]['temp']['eve']
        temp_night = response['daily'][day]['temp']['night']
        feels_like_morn = response['daily'][day]['feels_like']['morn']
        feels_like_day = response['daily'][day]['feels_like']['day']
        feels_like_eve = response['daily'][day]['feels_like']['eve']
        feels_like_night = response['daily'][day]['feels_like']['night']
        clouds = response['daily'][day]['clouds']
        description = response['daily'][day]['weather'][0]['description']

        bot.send_message(user_id, '{} в городе {} - {}\nУтром: {} ℃\nДнем: {} ℃\n'
                                  'Вечером: {} ℃\nНочью: {} ℃\nОщущается как:\nУтром: {} ℃\nДнем: {} ℃\n'
                                  'Вечером: {} ℃\nНочью: {} ℃\nОблачность {} %\n'.format(message.text,
                                                                                         data['city'][user_id],
                                                                                         description, temp_morn,
                                                                                         temp_day, temp_eve, temp_night,
                                                                                         feels_like_morn,
                                                                                         feels_like_day,
                                                                                         feels_like_eve,
                                                                                         feels_like_night,
                                                                                         clouds))
        bot.send_message(user_id, 'Мы можем посмотреть погоду на другой день. Чтобы вернутся в начало напиши /start')
    except UnboundLocalError:
        bot.send_message(user_id, 'Тебе нужно написать: "Сегодня", "Завтра" или "Послезавтра"\n'
                                  'Чтобы вернутся в начало напиши /start')


def millioner_main_handler(message):
    user_id = str(message.from_user.id)
    count_mil = {'count': 1}
    data['param'][user_id] = count_mil
    param_diff = {'qType': message.text}
    data['param'][user_id].update(param_diff)
    data['state'][user_id] = MILLIONER_GAME
    millioner_game_handler(message)


def millioner_game_handler(message):
    user_id = str(message.from_user.id)
    data['right_answer'] = {}
    data['question'] = {}
    data['answers'] = {}
    response = requests.get(mill_api, params=data['param'][user_id]).json()
    data['right_answer'][user_id] = response['data'][0]['answers'][0]
    data['question'][user_id] = response['data'][0]['question']
    data['answers'][user_id] = response['data'][0]['answers']
    shuffle(data['answers'][user_id])
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(*data['answers'][user_id])
    bot.send_message(user_id, data['question'][user_id], reply_markup=keyboard)
    data['state'][user_id] = MILLIONER_ANSWER
    print('Правильный ответ для {} - {}'.format(message.from_user.first_name, data['right_answer'][user_id]))


def millioner_answer_handler(message):
    user_id = str(message.from_user.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('1', '2', '3')

    if data['right_answer'][user_id].lower() in message.text.lower():
        bot.reply_to(message, 'Правильно!')
        data['state'][user_id] = MILLIONER_MAIN
        bot.send_message(user_id, 'Выбери сложность или нажми "/start"',
                         reply_markup=keyboard)
    else:
        bot.reply_to(message, 'Неправильно, попробуй еще!')


bot.polling()
