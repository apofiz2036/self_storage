import os
from dotenv import load_dotenv
import django
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()

from storage.models import Warehouse, Clients, Order

NAME, PHONE, EMAIL = range(3)

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = """В наше время, когда пространство в квартирах становится все более ограниченным, многие люди сталкиваются с проблемой хранения сезонных вещей. Склад для хранения может стать отличным решением для тех, кто хочет освободить место в доме, не избавляясь от своих вещей.

Вот несколько примеров, как аренда склада может пригодиться:

1. Сезонная одежда: У каждого из нас есть зимняя и летняя одежда, которую мы не носим круглый год. Вместо того чтобы загромождать шкафы, вы можете арендовать небольшой контейнер и хранить в нем одежду, незадачливо упакованную в вакуумные пакеты.

2. Спортивное оборудование: Летом вы можете активно заниматься водными видами спорта, а зимой — катанием на лыжах. Где хранить весла, доски или лыжи, когда они не используются? Склад поможет освободить место в квартире, а вы будете уверены, что ваше оборудование надежно защищено.

3. Предметы декора и мебель: Смена интерьеров стала популярной среди людей. Часто мы хотим заменить мебель или обновить дизайн, но не хотим избавляться от старых вещей. Хранение лишних предметов на складе даст вам возможность экспериментировать с оформлением, не отказываясь от любимых вещей.

4. Бытовая техника и электроника: Если вы планируете переезд или хотите обновить технику, но не хотите выбрасывать старый телевизор или холодильник, аренда склада поможет вам временно сохранить эти предметы, пока вы не решите, что с ними делать.

5. Документы и архивы: Для владельцев бизнеса, особенно малых, аренда склада может служить идеальным местом для хранения архивных документов, которые не нужны каждый день, но должны храниться по юридическим причинам.

6. Проекты и хобби: Если вы увлекаетесь рукоделием или занимаетесь каким-то проектом, вы, вероятно, сталкивались с недостатком места для ваших материалов и инструментов. Аренда склада позволит вам организовать пространство для творчества.

Таким образом, аренда склада становится удобным и практичным решением для хранения сезонных вещей, освобождая пространство в вашем доме и давая возможность сосредоточиться на том, что действительно важно. Николай, как предприниматель, предоставляет такой уникальный сервис, который может помочь множеству людей находить решение их проблем с пространством.

"""
    keyboard = [[InlineKeyboardButton("Узнать больше", callback_data='consent_personal_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def consent_personal_data(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    text = "Для дальнейшей работы необходимо ознакомится с согласием на обработку персональных данных"
    keyboard = [[InlineKeyboardButton("Ознакомится с согласием на обработку персональных данных", callback_data='send_consents')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)


def send_consents(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    file_path = 'files/consents.pdf'
    context.bot.send_document(chat_id=query.message.chat.id, document=open(file_path, 'rb'), caption="Вот ваше соглашение на обработку персональных данных.")

    keyboard = [[InlineKeyboardButton("Перейти в главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Теперь вы можете начинать работу'
    context.bot.send_message(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [[InlineKeyboardButton("Правила хранения", callback_data='rules')],
                [InlineKeyboardButton("Сделать заказ", callback_data='make_order')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Это главное меню'
    context.bot.send_message(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)


def rules(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [[InlineKeyboardButton("Перейти в главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """Разрешенные вещи:
- Одежда и обувь
- Книги и документы
- Мебель и предметы интерьера
- Спортивный инвентарь
- Инструменты и строительные материалы
- Жидкости (при условии, что они упакованы в герметичные контейнеры и не представляют опасности)

Запрещенные вещи:
- Животные и растения
- Опасные вещества (кислоты, яды и т.д.)
- Огнестрельное оружие и боеприпасы
- Наркотики
- Легковоспламеняющиеся материалы
- Ценные предметы (драгоценности, деньги) без предварительного уведомления
"""
    context.bot.send_message(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)


def make_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    warehouses = Warehouse.objects.all()
    addresses = [warehouse.address for warehouse in warehouses]

    if addresses:
        address_list = '\n'.join(addresses)
        text = (f"Вот адреса наших складов:\n{address_list}\n\n"
                "Мы предлагаем бесплатные обмерки и доставку на склад.\n"
                "Выберите способ доставки, чтобы продолжить:")
    else:
        text = "К сожалению, нет доступных складов."

    keyboard = [
        [InlineKeyboardButton("Бесплатная доставка", callback_data='check_client')],
        [InlineKeyboardButton("Самостоятельная доставка доставка", callback_data='self_delivery')],
        [InlineKeyboardButton("Перейти в главное меню", callback_data='main_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)


def check_client(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    telegram_id = query.from_user.id
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    if client is None:
        text = 'Сначала давайте зарегестрируем вас в нашей системе'
        context.bot.send_message(chat_id=query.message.chat.id, text=text)
        start_name_input(update, context)
    else:
        text = 'Вы уже зарегистрированы, это хорошо)'
        context.bot.send_message(chat_id=query.message.chat.id, text=text)
        address_input(update, context)


def start_name_input(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    text = 'Пожалуйста введите ваше ФИО'
    context.bot.send_message(chat_id=chat_id, text=text)

    return NAME


def name_input(update: Update, context: CallbackContext):
    user_name = update.message.text
    chat_id = update.message.chat.id

    context.user_data['tg_id'] = str(update.message.from_user.id)
    context.user_data['name'] = user_name

    context.bot.send_message(chat_id=chat_id, text='Пожалуйста, введите ваш номер телефона.')
    return PHONE


def phone_input(update: Update, context: CallbackContext):
    user_phone = update.message.text
    chat_id = update.message.chat.id

    context.user_data['phone'] = user_phone
    context.bot.send_message(chat_id=chat_id, text='Пожалуйста, введите ваш email')

    return EMAIL


def email_input(update: Update, context: CallbackContext):
    user_email = update.message.text

    context.user_data['email'] = user_email
    check_personal_data(update, context)


def check_personal_data(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    user_name = context.user_data['name']
    user_phone = context.user_data['phone']
    user_email = context.user_data['email']

    text = (
        f"Проверьте введенные данные:\n"
        f"ФИО: {user_name}\n"
        f"Телефон: {user_phone}\n"
        f"Email: {user_email}\n"
        "Все верно?"
    )

    keyboard = [
        [InlineKeyboardButton("Всё верно", callback_data='save_personal_data')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def save_personal_data(update: Update, context: CallbackContext):
    user_name = context.user_data.get('name')
    user_phone = context.user_data.get('phone')
    user_telegram_id = context.user_data.get('tg_id')
    user_email = context.user_data.get('email')

    if not all([user_name, user_phone, user_telegram_id]):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пожалуйста, предоставьте все обязательные данные: имя или телефон')
        return main_menu(update, context)    

    client = Clients(
        name=user_name,
        phone_number=user_phone,
        telegram_id=user_telegram_id,
        email=user_email
    )

    client.save()
    return create_order(update, context)


def address_input(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    keyboard = [[InlineKeyboardButton("Главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Тут будет что-то по регистрации заказа'
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_name_input, pattern='free_delivery')],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name_input)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone_input)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email_input)],
        },
                fallbacks=[CallbackQueryHandler(main_menu, pattern='main_menu')]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(consent_personal_data, pattern='consent_personal_data'))
    dp.add_handler(CallbackQueryHandler(send_consents, pattern='send_consents'))
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main_menu'))
    dp.add_handler(CallbackQueryHandler(rules, pattern='rules'))
    dp.add_handler(CallbackQueryHandler(make_order, pattern='make_order'))
    dp.add_handler(CallbackQueryHandler(check_client, pattern='check_client'))
    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(save_personal_data, pattern='save_personal_data'))
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='self_delivery'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
