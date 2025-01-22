import os
from dotenv import load_dotenv
import django
import requests
from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()

from storage.models import OrderStatus, Warehouse, Clients, Orders


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = """Как аренда склада может решить ваши проблемы с хранением

В наше время, когда пространство в квартирах становится все более ограниченным, многие люди сталкиваются с проблемой хранения сезонных вещей. Склад для хранения может стать отличным решением для тех, кто хочет освободить место в доме, не избавляясь от своих вещей.

Вот несколько примеров, как аренда склада может пригодиться:

1. Сезонная одежда: У каждого из нас есть зимняя и летняя одежда, которую мы не носим круглый год. Вместо того чтобы загромождать шкафы, вы можете арендовать небольшой контейнер и хранить в нем одежду, незадачливо упакованную в вакуумные пакеты.

2. Спортивное оборудование: Летом вы можете активно заниматься водными видами спорта, а зимой — катанием на лыжах. Где хранить весла, доски или лыжи, когда они не используются? Склад поможет освободить место в квартире, а вы будете уверены, что ваше оборудование надежно защищено.

3. Предметы декора и мебель: Смена интерьеров стала популярной среди людей. Часто мы хотим заменить мебель или обновить дизайн, но не хотим избавляться от старых вещей. Хранение лишних предметов на складе даст вам возможность экспериментировать с оформлением, не отказываясь от любимых вещей.

4. Бытовая техника и электроника: Если вы планируете переезд или хотите обновить технику, но не хотите выбрасывать старый телевизор или холодильник, аренда склада поможет вам временно сохранить эти предметы, пока вы не решите, что с ними делать.

5. Документы и архивы: Для владельцев бизнеса, особенно малых, аренда склада может служить идеальным местом для хранения архивных документов, которые не нужны каждый день, но должны храниться по юридическим причинам.

6. Проекты и хобби: Если вы увлекаетесь рукоделием или занимаетесь каким-то проектом, вы, вероятно, сталкивались с недостатком места для ваших материалов и инструментов. Аренда склада позволит вам организовать пространство для творчества.

Таким образом, аренда склада становится удобным и практичным решением для хранения сезонных вещей, освобождая пространство в вашем доме и давая возможность сосредоточиться на том, что действительно важно. Николай, как предприниматель, предоставляет такой уникальный сервис, который может помочь множеству людей находить решение их проблем с пространством.
"""
    keyboard = [[InlineKeyboardButton("Узнать больше", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text, reply_markup=reply_markup)


def count_clicks(update: Update, context: CallbackContext):
    if update.effective_user.id == OWNER_ID:
        VK_API_KEY = os.environ['VK_API_KEY']
        LINK = os.environ['ADVERTSING_LINK']
        key_link = urlparse(LINK).path.split('/')[-1]
        url = 'https://api.vk.ru/method/utils.getLinkStats'
        params = {
            'key': key_link,
            'access_token': VK_API_KEY,
            'interval': 'forever',
            'v': '5.199'
        }
        response = requests.get(url, params)
        response.raise_for_status()
        number_of_clicks = response.json()['response']['stats'][0]['views']
        return f'По вашей ссылке перешли {number_of_clicks} раз'
    else:
        return 'У вас нет доступа к этой функции.'


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    OWNER_ID = os.environ['OWNER_ID']
    
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clicks", count_clicks))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
