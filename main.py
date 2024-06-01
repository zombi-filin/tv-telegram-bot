# -*- coding: utf-8 -*-
import os
import re
import telebot
import urllib.request


#
channel_url_list = [
    'https://tv.yandex.ru/channel/pervyy-16', # Первый
]

#
bot_token = os.environ.get('bot_token')
telegram_bot = telebot.TeleBot(bot_token)

#
def get_channel_program():
    out_text = ''
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in channel_url_list:
        #
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        #
        if len(out_text)>0: out_text = out_text + '\n'
        #
        regx = r'<h1 class=\"channel-header__text\">(.*)</h1>'
        title = re.findall(regx, html)
        out_text = out_text + f'{title[0]}\n'
        #
        regx = r'<time class=\"channel-schedule__time\">(.*?)<'
        channel_schedule_time = re.findall(regx, html)
        #
        regx = r'<span class=\"channel-schedule__text\">(.*?)<'
        channel_schedule_text = re.findall(regx, html)

        pass
    return out_text

# 
@telegram_bot.message_handler(commands=['start'])
def command(message):
    telegram_bot.send_message(
        chat_id=message.chat.id,
        text=get_channel_program()
    )

#
telegram_bot.polling(none_stop=True)