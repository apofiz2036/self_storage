import os
from dotenv import load_dotenv
from celery import shared_task
from django.utils import timezone
from .models import Order
from telegram import Bot

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = Bot(token=TELEGRAM_TOKEN)

@shared_task
def send_order_reminder():
    today = timezone.now()
    orders = Order.objects.filter(reminder_2=today)

    for order in orders:
        message = f"Здравствуйте, {order.user.username}! Напоминаем, что срок хранения вашего заказа заканчивается через 14 дней."
        bot.send_message(chat_id=order.user.telegram_id, text=message)