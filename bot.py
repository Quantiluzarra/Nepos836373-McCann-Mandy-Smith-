import telebot
from telebot import types
import logging
import os
import requests
from bs4 import BeautifulSoup
import wikipedia
from googletrans import Translator

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
TOKEN = "5706304063:AAHZslRmiWykmYaFG84E19GcO8i2x5oYjvU"

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Команды бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я супербот. Чем могу помочь?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я могу помочь с:\n"
                         "1. Переводом текста\n"
                         "2. Поиском информации в Википедии\n"
                         "3. Получением случайной цитаты\n"
                         "4. Конвертацией валют\n"
                         "5. И многим другим!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Перевод текста
    if message.text.startswith("/translate"):
        translator = Translator()
        text = message.text[10:]
        result = translator.translate(text, dest="ru")
        bot.reply_to(message, f"Перевод: {result.text}")

    # Поиск информации в Википедии
    elif message.text.startswith("/wiki"):
        query = message.text[6:]
        try:
            result = wikipedia.summary(query, sentences=2)
            bot.reply_to(message, f"Результат поиска: {result}")
        except wikipedia.exceptions.DisambiguationError as e:
            bot.reply_to(message, f"Ошибка: {e}")

    # Получение случайной цитаты
    elif message.text.startswith("/quote"):
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        quote = data["content"]
        author = data["author"]
        bot.reply_to(message, f"Цитата: {quote} - {author}")

    # Конвертация валют
    elif message.text.startswith("/convert"):
        amount, from_currency, to_currency = message.text[8:].split()
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()
        rate = data["rates"][to_currency]
        result = float(amount) * rate
        bot.reply_to(message, f"Конвертация: {amount} {from_currency} = {result} {to_currency}")

    # Обработка неизвестных команд
    else:
        bot.reply_to(message, "Извините, я не понял ваш запрос. Попробуйте /help для списка команд.")

# Запуск бота
bot.polling(none_stop=True)
