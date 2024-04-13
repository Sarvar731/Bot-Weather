import telebot  # Импортируем модуль telebot из библиотеки pyTelegramBotAPI.
from pyowm import OWM  # Импортируем модуль OWM (Open Weather Map) из библиотеки pyowm.


def get_location(lat, lon):  # Определяем функцию для получения URL карты погоды для определенной широты и долготы.
    url = f"https://yandex.uz/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_lightning=1"  # Форматируем URL с предоставленными широтой и долготой.
    return url  # Возвращаем URL.


def weather(city: str):  # Определяем функцию для получения погоды в определенном городе.
    owm = OWM('81bf711240c88ed94fcdabb8f0d86001')  # Создаем экземпляр класса OWM, используя ваш API-ключ.
    mgr = owm.weather_manager()  # Получаем менеджер погоды.
    observation = mgr.weather_at_place(city)  # Получаем наблюдение за погодой в указанном городе.
    weather = observation.weather  # Получаем данные о погоде из наблюдения.
    location = get_location(observation.location.lat,
                            observation.location.lon)  # Получаем URL карты погоды для местоположения наблюдения.
    temperature = weather.temperature("celsius")  # Получаем температуру в градусах Цельсия.
    return temperature, location  # Возвращаем температуру и URL карты погоды.


bot = telebot.TeleBot(
    '6632279379:AAGG6VMmum6XEBmwa_0dyXxq4b6_WWLBS8w')  # Создаем экземпляр класса TeleBot, используя ваш API-ключ.


@bot.message_handler(content_types=['text'])  # Определяем обработчик сообщений для текстовых сообщений.
def get_text_messages(message):  # Определяем функцию для обработки текстовых сообщений.
    if message.text == '/weather':  # Если текст сообщения равен '/weather'...
        bot.send_message(message.from_user.id,
                         "Введите название Города 🏙️")  # ...просим пользователя ввести название города.
        bot.register_next_step_handler(message,
                                       get_weather)  # Регистрируем обработчик следующего шага, который вызовет функцию get_weather.
    else:  # Если текст сообщения не равен '/weather'...
        bot.send_message(message.from_user.id, 'Напишите ☔ /weather')  # ...просим пользователя написать '/weather'.


def get_weather(message):  # Определяем функцию для получения погоды.
    city = message.text  # Получаем текст сообщения, который является названием города.
    try:  # Пытаемся...
        w = weather(city)  # ...получить погоду для города.
        bot.send_message(message.from_user.id, f'В {city} сейчас {round(w[0]["temp"])} градуса,'
                                               f'чувствуеться как {round(w[0]["feels_like"])} градуса')  # ...отправить сообщение с текущей температурой и ощущаемой температурой.
        bot.send_message(message.from_user.id, w[1])  # ...отправить сообщение с URL карты погоды.
        bot.send_message(message.from_user.id,
                         "Введите название города")  # ...просим пользователя ввести название другого города.
        bot.register_next_step_handler(message,
                                       get_weather)  # Регистрируем обработчик следующего шага, который снова вызовет функцию get_weather.
    except Exception:  # Если произошла ошибка...
        bot.send_message(message.from_user.id,
                         'ПРОИЗОШЛА ОШИБКА...ТАКОГО ГОРОДА  ИЛИ СТРАНЫ НЕТУ В БАЗЕ, ПАПРОБУЙТЕ ЕЩЁ РАЗ')  # ...сообщаем об этом пользователю.
        bot.send_message(message.from_user.id,
                         "ВВедите название города")  # ...просим пользователя ввести название города снова.
        bot.register_next_step_handler(message,
                                       get_weather)  # Регистрируем обработчик следующего шага, который снова вызовет функцию get_weather.


bot.polling(none_stop=True)  # Запускаем бота.
