import telebot
from config import TOKEN, currency
from extensions import APIException, CurrencyConverter
 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите комманду в формате:\n\
<Имя валюты> <имя валюты, в которой надо узнать цену первой валюты> <Количество первой валюты> \
\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)
 
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = [i.lower() for i in message.text.split()]
        if len(values) != 3:
            raise APIException('Неверное количество параметров')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base:.2f}'
        bot.send_message(message.chat.id, text)

   

bot.polling(none_stop=True)